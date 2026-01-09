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
            _LOGGER.error("Sensor %s not found", sensor_entity_id)
            return
        
        try:
            temperature = float(state.state)
        except (ValueError, TypeError):
            _LOGGER.error("Invalid temperature value from sensor %s: %s", 
                         sensor_entity_id, state.state)
            return
        
        url = f"http://www.temperatur.nu/rapportera.php?hash={hash_code}&t={temperature}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        _LOGGER.info("Successfully reported temperature %.1f°C to Temperatur.nu", 
                                   temperature)
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
    
    # Report immediately on startup
    await report_temperature(None)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
