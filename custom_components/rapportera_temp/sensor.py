"""Sensor platform for Report Temperature."""
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities([RapporteraTempStatusSensor(hass, config_entry)], True)


class RapporteraTempStatusSensor(SensorEntity):
    """Representation of a Report Temperature Status sensor."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self._hass = hass
        self._config_entry = config_entry
        entity_name = config_entry.data.get("entity_name", f"Report Temperature ({config_entry.data['sensor_entity_id']})")
        self._attr_name = f"{entity_name} Status"
        self._attr_unique_id = f"{DOMAIN}_{config_entry.entry_id}_status"
        self._attr_icon = "mdi:cloud-upload"
        self._attr_should_poll = True

    @property
    def state(self):
        """Return the state of the sensor."""
        data = self._hass.data.get(DOMAIN, {}).get(self._config_entry.entry_id, {})
        return data.get("last_update_status", "pending")

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        data = self._hass.data.get(DOMAIN, {}).get(self._config_entry.entry_id, {})
        config = data.get("config", self._config_entry.data)
        
        attrs = {
            "sensor": config["sensor_entity_id"],
            "hash_code": config["hash_code"][:8] + "...",
            "interval_minutes": config.get("interval", 5),
            "last_update_status": data.get("last_update_status", "pending"),
            "last_update_message": data.get("last_update_message", "No updates yet"),
            "last_update_time": data.get("last_update_time"),
            "last_temperature": data.get("last_temperature"),
        }
        
        return attrs
    
    @property
    def icon(self):
        """Return the icon based on status."""
        data = self._hass.data.get(DOMAIN, {}).get(self._config_entry.entry_id, {})
        status = data.get("last_update_status", "pending")
        
        if status == "success":
            return "mdi:cloud-check"
        elif status == "failed":
            return "mdi:cloud-alert"
        else:
            return "mdi:cloud-upload"

