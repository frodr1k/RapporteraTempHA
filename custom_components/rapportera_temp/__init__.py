"""Report Temperature to Temperatur.nu integration."""
import logging
from datetime import datetime, timedelta
import statistics

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval
import aiohttp

from .const import AGGREGATION_MIN, AGGREGATION_MEAN

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
        "last_reported_temperature": None,
        "sensor_temperatures": {},
    }

    # Schedule temperature reporting
    async def report_temperature(now):
        """Report temperature to Temperatur.nu."""
        # Support both old (single) and new (multiple) sensor format
        sensor_ids = entry.data.get("sensor_entity_ids", [entry.data.get("sensor_entity_id")])
        if not isinstance(sensor_ids, list):
            sensor_ids = [sensor_ids]
        
        hash_code = entry.data.get("hash_code")
        if not hash_code:
            _LOGGER.error("No hash_code found in configuration")
            return
        
        aggregation_method = entry.data.get("aggregation_method", AGGREGATION_MIN)
        
        # Collect temperatures from all sensors
        temperatures = []
        sensor_temps = {}
        
        for sensor_id in sensor_ids:
            if not sensor_id:
                continue
                
            state = hass.states.get(sensor_id)
            if state is None:
                _LOGGER.warning("Sensor %s not found", sensor_id)
                continue
            
            # Check if state is unavailable or unknown
            if state.state in ["unavailable", "unknown", "none", None]:
                _LOGGER.warning("Sensor %s is %s", sensor_id, state.state)
                continue
            
            try:
                temperature = float(state.state)
                temperatures.append(temperature)
                sensor_temps[sensor_id] = round(temperature, 1)
            except (ValueError, TypeError) as err:
                _LOGGER.warning("Invalid temperature value from sensor %s: %s (error: %s)", 
                              sensor_id, state.state, err)
                continue
        
        # Update sensor temperatures in data
        hass.data[DOMAIN][entry.entry_id]["sensor_temperatures"] = sensor_temps
        
        if not temperatures:
            msg = "No valid temperature readings from any sensor"
            _LOGGER.warning(msg)
            hass.data[DOMAIN][entry.entry_id]["last_update_status"] = "failed"
            hass.data[DOMAIN][entry.entry_id]["last_update_message"] = msg
            hass.data[DOMAIN][entry.entry_id]["last_update_time"] = datetime.now()
            return
        
        # Calculate aggregated temperature
        if aggregation_method == AGGREGATION_MEAN:
            aggregated_temp = statistics.mean(temperatures)
        else:  # AGGREGATION_MIN (default)
            aggregated_temp = min(temperatures)
        
        # Round to 1 decimal place
        aggregated_temp = round(aggregated_temp, 1)
        
        # Store the calculated temperature (before reporting)
        hass.data[DOMAIN][entry.entry_id]["last_temperature"] = aggregated_temp
        
        # Format temperature with dot as decimal separator (US format)
        temp_formatted = f"{aggregated_temp:.1f}"
        url = f"http://www.temperatur.nu/rapportera.php?hash={hash_code}&t={temp_formatted}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    response_text = await response.text()
                    
                    if response.status == 200:
                        msg = f"Successfully reported {temp_formatted}°C ({aggregation_method} of {len(temperatures)} sensor(s)). Server response: {response_text}"
                        _LOGGER.info(msg)
                        _LOGGER.debug("URL used: %s", url)
                        hass.data[DOMAIN][entry.entry_id]["last_update_status"] = "success"
                        hass.data[DOMAIN][entry.entry_id]["last_update_message"] = response_text
                        hass.data[DOMAIN][entry.entry_id]["last_reported_temperature"] = aggregated_temp
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
    sensor_count = len(entry.data.get("sensor_entity_ids", [entry.data.get("sensor_entity_id")]))
    aggregation = entry.data.get("aggregation_method", AGGREGATION_MIN)
    _LOGGER.info("Report Temperature configured with %d sensor(s), %s aggregation, %d minute interval", 
                 sensor_count, aggregation, interval_minutes)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
