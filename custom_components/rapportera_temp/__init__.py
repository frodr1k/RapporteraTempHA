"""Report Temperature to Temperatur.nu integration."""
import logging
from datetime import datetime, timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval
import aiohttp

_LOGGER = logging.getLogger(__name__)

DOMAIN = "rapportera_temp"
PLATFORMS = [Platform.SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Report Temperature from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Initialize status tracking
    hass.data[DOMAIN][entry.entry_id] = {
        "config": entry.data,
        "last_update_status": "pending",
        "last_update_message": "Waiting for first report",
        "last_update_time": None,
        "last_temperature": None,
    }

    # Schedule temperature reporting
    async def report_temperature(now):
        """Report temperature to Temperatur.nu."""
        sensor_entity_id = entry.data["sensor_entity_id"]
        hash_code = entry.data["hash_code"]
        
        state = hass.states.get(sensor_entity_id)
        if state is None:
            msg = f"Sensor {sensor_entity_id} not found"
            _LOGGER.warning(msg)
            hass.data[DOMAIN][entry.entry_id]["last_update_status"] = "failed"
            hass.data[DOMAIN][entry.entry_id]["last_update_message"] = msg
            hass.data[DOMAIN][entry.entry_id]["last_update_time"] = datetime.now()
            return
        
        # Check if state is unavailable or unknown
        if state.state in ["unavailable", "unknown", "none", None]:
            msg = f"Sensor {sensor_entity_id} is {state.state}"
            _LOGGER.warning(msg)
            hass.data[DOMAIN][entry.entry_id]["last_update_status"] = "failed"
            hass.data[DOMAIN][entry.entry_id]["last_update_message"] = msg
            hass.data[DOMAIN][entry.entry_id]["last_update_time"] = datetime.now()
            return
        
        try:
            temperature = float(state.state)
            # Round to 1 decimal place
            temperature = round(temperature, 1)
        except (ValueError, TypeError) as err:
            msg = f"Invalid temperature value from sensor {sensor_entity_id}: {state.state}"
            _LOGGER.warning("%s (error: %s)", msg, err)
            hass.data[DOMAIN][entry.entry_id]["last_update_status"] = "failed"
            hass.data[DOMAIN][entry.entry_id]["last_update_message"] = msg
            hass.data[DOMAIN][entry.entry_id]["last_update_time"] = datetime.now()
            return
        
        # Format temperature with dot as decimal separator (US format)
        # Using :.1f ensures one decimal place with dot separator
        temp_formatted = f"{temperature:.1f}"
        url = f"http://www.temperatur.nu/rapportera.php?hash={hash_code}&t={temp_formatted}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    response_text = await response.text()
                    
                    if response.status == 200:
                        msg = f"Successfully reported {temp_formatted}°C. Server response: {response_text}"
                        _LOGGER.info(msg)
                        _LOGGER.debug("URL used: %s", url)
                        hass.data[DOMAIN][entry.entry_id]["last_update_status"] = "success"
                        hass.data[DOMAIN][entry.entry_id]["last_update_message"] = response_text
                        hass.data[DOMAIN][entry.entry_id]["last_temperature"] = temperature
                    else:
                        msg = f"Failed with HTTP {response.status}. Response: {response_text}. URL: {url}"
                        _LOGGER.error(msg)
                        hass.data[DOMAIN][entry.entry_id]["last_update_status"] = "failed"
                        hass.data[DOMAIN][entry.entry_id]["last_update_message"] = msg
                    
                    hass.data[DOMAIN][entry.entry_id]["last_update_time"] = datetime.now()
                    
        except Exception as err:
            msg = f"Error reporting temperature: {err}. URL: {url}"
            _LOGGER.error(msg)
            hass.data[DOMAIN][entry.entry_id]["last_update_status"] = "failed"
            hass.data[DOMAIN][entry.entry_id]["last_update_message"] = msg
            hass.data[DOMAIN][entry.entry_id]["last_update_time"] = datetime.now()

    # Get interval from config (default 5 minutes)
    interval_minutes = entry.data.get("interval", 5)
    interval = timedelta(minutes=interval_minutes)
    
    # Schedule the reporting
    entry.async_on_unload(
        async_track_time_interval(hass, report_temperature, interval)
    )
    
    # Don't report immediately on startup - wait for first interval
    # This gives sensors time to become available
    _LOGGER.info("Report Temperature configured for sensor %s with %d minute interval", 
                 entry.data["sensor_entity_id"], interval_minutes)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
