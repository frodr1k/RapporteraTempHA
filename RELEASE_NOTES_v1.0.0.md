# Release v1.0.0 - Initial Release

## 🎉 Features

### Core Functionality
- **Automatic temperature reporting** to Temperatur.nu
- **Configurable reporting interval** (1-60 minutes)
- **GUI-based configuration** - No YAML editing required
- **Entity selector** for easy sensor selection
- **Custom naming** with smart defaults

### Status Tracking & Monitoring
- **Full status tracking** with attributes:
  - `last_update_status` (success/failed/pending)
  - `last_update_message` (server response or error message)
  - `last_update_time` (timestamp of last report)
  - `last_temperature` (last reported temperature value)
- **Dynamic icons** based on status:
  - ✅ Cloud check (success)
  - ❌ Cloud alert (failed)
  - ⏳ Cloud upload (pending)

### Data Quality
- **Temperature formatting** with dot as decimal separator (X.x format)
- **Automatic rounding** to 1 decimal place
- **State validation** - Skips unavailable or invalid sensor states
- **Error handling** throughout

### Logging & Debugging
- **Server response logging** for debugging
- **URL logging** on errors for troubleshooting
- **Informative messages** in Home Assistant logs
- **Debug mode support**

### Configuration
- **Initial setup flow** with entity selector
- **Options flow** for reconfiguration
- **Hash code** from Temperatur.nu
- **Optional custom entity name**

## 📋 Requirements

- Home Assistant 2023.1.0 or newer
- Temperature sensor in Home Assistant
- Internet connection to Temperatur.nu
- Hash code from Temperatur.nu

## 🚀 Installation

### Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the menu in top right corner (three dots)
4. Select "Custom repositories"
5. Add URL: `https://github.com/frodr1k/RapporteraTempHA`
6. Select category: "Integration"
7. Click "Add"
8. Find "Report Temperature" and click "Download"
9. Restart Home Assistant

### Manual Installation

1. Copy `custom_components/rapportera_temp` to your `custom_components` folder
2. Restart Home Assistant

## 📊 Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **+ ADD INTEGRATION**
3. Search for "Report Temperature"
4. Enter:
   - Hash code from Temperatur.nu
   - Select temperature sensor
   - Set reporting interval (default: 5 minutes)
   - Optionally set custom name

## 📈 Usage

The integration creates a status sensor with the following attributes:

```yaml
sensor.report_[sensor_name]_status:
  state: success  # or failed/pending
  attributes:
    sensor: sensor.your_temperature_sensor
    hash_code: abc12345...
    interval_minutes: 5
    last_update_status: success
    last_update_message: "OK"
    last_update_time: "2026-01-12 18:00:00"
    last_temperature: 22.5
```

### Example Automation

Alert when temperature reporting fails:

```yaml
automation:
  - alias: "Alert on temperature report failure"
    trigger:
      - platform: state
        entity_id: sensor.report_[sensor_name]_status
        to: 'failed'
    action:
      - service: notify.mobile_app
        data:
          message: >
            Temperature report failed: 
            {{ state_attr('sensor.report_[sensor_name]_status', 'last_update_message') }}
```

## 🔧 Troubleshooting

### Check Status Sensor
Look at the `last_update_message` attribute for error details.

### Check Logs
Go to Settings → System → Logs and search for "rapportera_temp"

### Common Issues

**Sensor not found**
- Ensure the sensor entity ID is correct
- Check that the sensor is available in Home Assistant

**HTTP errors**
- Check the URL in logs
- Verify hash code is correct
- Ensure internet connectivity

**Invalid temperature**
- Check sensor provides numeric temperature value
- Sensor state must not be "unavailable" or "unknown"

## 🙏 Credits

Developed for reporting temperature data to [Temperatur.nu](http://www.temperatur.nu)

## 📝 License

MIT License - See LICENSE file for details
