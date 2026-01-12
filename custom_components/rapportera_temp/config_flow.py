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
)

from .const import DOMAIN

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
            # Validate sensor
            elif not user_input.get("sensor_entity_id"):
                errors["sensor_entity_id"] = "missing_sensor"
            else:
                # Generate default entity name if not provided
                if not user_input.get("entity_name"):
                    sensor_id = user_input["sensor_entity_id"]
                    # Remove "sensor." prefix and create friendly name
                    sensor_name = sensor_id.replace("sensor.", "")
                    user_input["entity_name"] = f"Report {sensor_name}"
                
                # Create the entry
                return self.async_create_entry(
                    title=user_input["entity_name"],
                    data=user_input,
                )

        # Get all temperature sensors
        data_schema = vol.Schema(
            {
                vol.Required("hash_code"): str,
                vol.Required("sensor_entity_id"): EntitySelector(
                    EntitySelectorConfig(
                        domain="sensor",
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
                "hash_info": "Get your hash code from Temperatur.nu"
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
            # Generate default entity name if not provided
            if not user_input.get("entity_name"):
                sensor_id = user_input.get("sensor_entity_id", "")
                sensor_name = sensor_id.replace("sensor.", "")
                user_input["entity_name"] = f"Report {sensor_name}" if sensor_name else "Report Temperature"
            
            # Update config entry with new data
            self.hass.config_entries.async_update_entry(
                self._config_entry,
                data={**self._config_entry.data, **user_input},
                title=user_input["entity_name"]
            )
            return self.async_create_entry(title="", data={})

        # Get current values
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "hash_code",
                        default=self._config_entry.data.get("hash_code", "")
                    ): str,
                    vol.Required(
                        "sensor_entity_id",
                        default=self._config_entry.data.get("sensor_entity_id", "")
                    ): str,
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
        )
