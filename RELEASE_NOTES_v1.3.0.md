# Release Notes v1.3.0

## 🎉 Major Feature Update

### Multiple Sensor Support with Smart Aggregation

This release adds powerful new features for more accurate temperature reporting!

## ✨ New Features

### 1. Multiple Sensor Support (1-3 sensors)
- Select up to 3 temperature sensors in configuration
- Perfect for ensuring accurate shade temperature readings
- Each sensor's temperature is tracked individually

### 2. Aggregation Methods
Choose how multiple sensor readings are combined:

#### Minimum (Default - Recommended)
- **Guarantees shade temperature** in almost all cases
- When using 2-3 sensors, the lowest reading will typically be the one in shade
- Ideal for accurate weather reporting
- **Tip:** "Lägsta värdet garanterar nästan alltid skugga"

#### Mean (Average)
- Calculates average temperature from all sensors
- Useful for getting a general temperature reading
- Good for indoor temperature monitoring

### 3. Temperature Sensor Entity
- New dedicated temperature sensor entity created automatically
- Shows the aggregated temperature value
- Can be used in:
  - Automations
  - Graphs and history
  - Other integrations
  - Temperature statistics

### 4. Enhanced Status Tracking
Status sensor now includes:
- Individual temperatures from each sensor
- Aggregation method used
- Sensor count
- Last reported temperature

## 🔧 Technical Improvements

- Backward compatible with single sensor configurations
- Improved error handling for unavailable sensors
- Better logging with sensor count and aggregation info
- Configuration validation (max 3 sensors)

## 📋 Configuration Changes

**New fields:**
- `sensor_entity_ids` (replaces `sensor_entity_id`) - supports multiple selections
- `aggregation_method` - choice between "min" and "mean"

**Old configurations will be automatically migrated** to work with the new version.

## 🌡️ Why Use Multiple Sensors?

Using multiple sensors with minimum aggregation virtually guarantees accurate shade temperature reporting. Since different locations may be exposed to sunlight at different times of day, selecting the minimum value ensures you're always reporting the temperature that's truly in shade - not influenced by direct sun exposure.

This is especially important for:
- Weather stations
- Outdoor temperature monitoring
- Contributing to accurate community weather data

## 📦 Installation

Update through HACS or manually replace the custom_component folder.

After updating:
1. Restart Home Assistant
2. Go to integration settings to configure additional sensors
3. Select aggregation method (minimum recommended)

## 🐛 Breaking Changes

None - existing configurations continue to work!

## 📝 Example Use Cases

### Weather Station Setup
```yaml
Sensors: 
  - North side sensor
  - East side sensor  
  - West side sensor
Aggregation: Minimum
Result: Always reports true shade temperature
```

### Indoor Monitoring
```yaml
Sensors:
  - Living room
  - Bedroom
  - Kitchen
Aggregation: Mean
Result: Average home temperature
```

---

**Full Changelog:** https://github.com/frodr1k/RapporteraTempHA/compare/v1.0.1...v1.3.0
