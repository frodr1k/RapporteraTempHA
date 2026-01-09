"""Sensor platform for Report Temperature."""
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities([RapporteraTempStatusSensor(config_entry)], True)


class RapporteraTempStatusSensor(SensorEntity):
    """Representation of a Report Temperature Status sensor."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self._config_entry = config_entry
        entity_name = config_entry.data.get("entity_name", f"Report Temperature ({config_entry.data['sensor_entity_id']})")
        self._attr_name = f"{entity_name} Status"
        self._attr_unique_id = f"{DOMAIN}_{config_entry.entry_id}_status"
        self._attr_icon = "mdi:thermometer-check"

    @property
    def state(self):
        """Return the state of the sensor."""
        return "active"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "sensor": self._config_entry.data["sensor_entity_id"],
            "hash_code": self._config_entry.data["hash_code"][:8] + "...",
            "interval_minutes": self._config_entry.data.get("interval", 5),
        }
