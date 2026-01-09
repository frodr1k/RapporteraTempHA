"""Report Temperature to Temperatur.nu integration."""
import logging
from datetime import timedelta

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
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Schedule temperature reporting
    async def report_temperature(now):
        """Report temperature to Temperatur.nu."""
        sensor_entity_id = entry.data["sensor_entity_id"]
        hash_code = entry.data["hash_code"]
        
        state = hass.states.get(sensor_entity_id)
        if state is None:
            _LOGGER.warning("Sensor %s not found, will retry at next interval", sensor_entity_id)
            return
        
        # Check if state is unavailable or unknown
        if state.state in ["unavailable", "unknown", "none", None]:
            _LOGGER.warning("Sensor %s state is %s, skipping report", sensor_entity_id, state.state)
            return
        
        try:
            temperature = float(state.state)
        except (ValueError, TypeError) as err:
            _LOGGER.warning("Invalid temperature value from sensor %s: %s (error: %s)", 
                         sensor_entity_id, state.state, err)
            return
        
        url = f"http://www.temperatur.nu/rapportera.php?hash={hash_code}&t={temperature}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        _LOGGER.info("Successfully reported temperature %.1f°C from %s to Temperatur.nu", 
                                   temperature, sensor_entity_id)
                    else:
                        _LOGGER.error("Failed to report temperature. Status: %d", 
                                    response.status)
        except Exception as err:
            _LOGGER.error("Error reporting temperature: %s", err)

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
