"""Config flow for Report Temperature integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import DOMAIN, AGGREGATION_MIN, AGGREGATION_MEAN

_LOGGER = logging.getLogger(__name__)

class RapporteraTempConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Report Temperature."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate hash code
            if not user_input.get("hash_code"):
                errors["hash_code"] = "missing_hash"
            # Validate sensors (now a list)
            elif not user_input.get("sensor_entity_ids"):
                errors["sensor_entity_ids"] = "missing_sensor"
            else:
                # Ensure sensors is a list and limit to 3
                sensors = user_input["sensor_entity_ids"]
                if not isinstance(sensors, list):
                    sensors = [sensors]
                user_input["sensor_entity_ids"] = sensors[:3]
                
                # Set default aggregation if not provided
                if "aggregation_method" not in user_input:
                    user_input["aggregation_method"] = AGGREGATION_MIN
                
                # Generate default entity name if not provided
                if not user_input.get("entity_name"):
                    sensor_count = len(sensors)
                    user_input["entity_name"] = f"Report Temperature ({sensor_count} sensor{'s' if sensor_count > 1 else ''})"
                
                # Create the entry
                return self.async_create_entry(
                    title=user_input["entity_name"],
                    data=user_input,
                )

        # Get all temperature sensors
        data_schema = vol.Schema(
            {
                vol.Required("hash_code"): str,
                vol.Required("sensor_entity_ids"): EntitySelector(
                    EntitySelectorConfig(
                        domain="sensor",
                        multiple=True,
                    )
                ),
                vol.Required("aggregation_method", default=AGGREGATION_MIN): SelectSelector(
                    SelectSelectorConfig(
                        options=[
                            {"value": AGGREGATION_MIN, "label": "Lägsta värdet (rekommenderat för skugga)"},
                            {"value": AGGREGATION_MEAN, "label": "Medelvärde"},
                        ],
                        mode=SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Optional("entity_name", default=""): str,
                vol.Optional("interval", default=5): NumberSelector(
                    NumberSelectorConfig(
                        min=1,
                        max=60,
                        step=1,
                        unit_of_measurement="minutes",
                        mode=NumberSelectorMode.BOX,
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "hash_info": "Get your hash code from Temperatur.nu",
                "aggregation_info": "Lägsta värdet garanterar nästan alltid skugga"
            }
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return RapporteraTempOptionsFlowHandler(config_entry)


class RapporteraTempOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Report Temperature."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            # Ensure sensors is a list and limit to 3
            if "sensor_entity_ids" in user_input:
                sensors = user_input["sensor_entity_ids"]
                if not isinstance(sensors, list):
                    sensors = [sensors]
                user_input["sensor_entity_ids"] = sensors[:3]
            
            # Generate default entity name if not provided
            if not user_input.get("entity_name"):
                sensor_count = len(user_input.get("sensor_entity_ids", []))
                user_input["entity_name"] = f"Report Temperature ({sensor_count} sensor{'s' if sensor_count > 1 else ''})"
            
            # Update config entry with new data
            self.hass.config_entries.async_update_entry(
                self._config_entry,
                data={**self._config_entry.data, **user_input},
                title=user_input["entity_name"]
            )
            return self.async_create_entry(title="", data={})

        # Get current values
        current_sensors = self._config_entry.data.get("sensor_entity_ids", 
                                                        [self._config_entry.data.get("sensor_entity_id", "")])
        if not isinstance(current_sensors, list):
            current_sensors = [current_sensors] if current_sensors else []
        
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "hash_code",
                        default=self._config_entry.data.get("hash_code", "")
                    ): str,
                    vol.Required(
                        "sensor_entity_ids",
                        default=current_sensors
                    ): EntitySelector(
                        EntitySelectorConfig(
                            domain="sensor",
                            multiple=True,
                        )
                    ),
                    vol.Required(
                        "aggregation_method",
                        default=self._config_entry.data.get("aggregation_method", AGGREGATION_MIN)
                    ): SelectSelector(
                        SelectSelectorConfig(
                            options=[
                                {"value": AGGREGATION_MIN, "label": "Lägsta värdet (rekommenderat för skugga)"},
                                {"value": AGGREGATION_MEAN, "label": "Medelvärde"},
                            ],
                            mode=SelectSelectorMode.DROPDOWN,
                        )
                    ),
                    vol.Optional(
                        "entity_name",
                        default=self._config_entry.data.get("entity_name", "")
                    ): str,
                    vol.Optional(
                        "interval",
                        default=self._config_entry.data.get("interval", 5)
                    ): int,
                }
            ),
            description_placeholders={
                "aggregation_info": "Lägsta värdet garanterar nästan alltid skugga"
            }
        )
