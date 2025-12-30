# MQTT Publisher Guide

Guide for publishing messages to the HiveMQ Cloud MQTT broker for testing.

## Broker Information

- **Broker Host**: `fd6ad94a23dc48f7aadb2a1c9b3f5c65.s1.eu.hivemq.cloud`
- **Port**: `8883` (TLS/SSL)
- **Username**: `test1234`
- **Password**: `Test1234`
- **Protocol**: MQTT over TLS/SSL

## Publishing Messages

### Using mosquitto_pub (Command Line)

If you have mosquitto-clients installed:

```bash
# Install mosquitto-clients (if not installed)
# macOS:
brew install mosquitto

# Linux (Ubuntu/Debian):
sudo apt-get install mosquitto-clients

# Publish ControlByWeb format message
mosquitto_pub \
  -h fd6ad94a23dc48f7aadb2a1c9b3f5c65.s1.eu.hivemq.cloud \
  -p 8883 \
  -u test1234 \
  -P Test1234 \
  -t "flash/sirens/000CC80630E0/status" \
  -m '{"clientID": "000CC80630E0", "status": "active", "vin": "VIN123456789"}' \
  --tls-version tlsv1.2 \
  --insecure

# Publish with different status values
mosquitto_pub \
  -h fd6ad94a23dc48f7aadb2a1c9b3f5c65.s1.eu.hivemq.cloud \
  -p 8883 \
  -u test1234 \
  -P Test1234 \
  -t "flash/sirens/000CC80630E0/status" \
  -m '{"clientID": "000CC80630E0", "status": "inactive", "vin": "VIN123456789"}' \
  --tls-version tlsv1.2 \
  --insecure
```

### Using Python (paho-mqtt)

Create a test publisher script:

```python
import paho.mqtt.client as mqtt
import json
import time

# Broker configuration
BROKER_HOST = "fd6ad94a23dc48f7aadb2a1c9b3f5c65.s1.eu.hivemq.cloud"
BROKER_PORT = 8883
USERNAME = "test1234"
PASSWORD = "Test1234"

# Create client
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)

# Enable TLS
client.tls_set()
client.tls_insecure_set(True)  # Disable certificate verification

# Connect
client.connect(BROKER_HOST, BROKER_PORT, 60)

# ControlByWeb configuration
DEVICE_ID = "000CC80630E0"
CLIENT_ID = "000CC80630E0"
TOPIC = f"flash/sirens/{DEVICE_ID}/status"

# Publish ControlByWeb format messages
for i in range(10):
    # ControlByWeb payload format
    message = {
        "clientID": CLIENT_ID,
        "status": "active" if i % 2 == 0 else "inactive",
        "vin": f"VIN{i:09d}"
    }
    client.publish(TOPIC, json.dumps(message))
    print(f"Published: {message}")
    
    time.sleep(2)

client.disconnect()
```

### Using Node.js (mqtt library)

```javascript
const mqtt = require('mqtt');

const client = mqtt.connect('mqtts://fd6ad94a23dc48f7aadb2a1c9b3f5c65.s1.eu.hivemq.cloud:8883', {
  username: 'test1234',
  password: 'Test1234',
  rejectUnauthorized: false // Disable certificate verification for development
});

client.on('connect', () => {
  console.log('Connected to MQTT broker');
  
  // ControlByWeb configuration
  const deviceId = '000CC80630E0';
  const clientId = '000CC80630E0';
  const topic = `flash/sirens/${deviceId}/status`;
  
  // Publish ControlByWeb format message
  const message = {
    clientID: clientId,
    status: 'active',
    vin: 'VIN123456789'
  };
  
  client.publish(topic, JSON.stringify(message), (err) => {
    if (err) {
      console.error('Error publishing:', err);
    } else {
      console.log('Message published:', message);
    }
    client.end();
  });
});

client.on('error', (error) => {
  console.error('MQTT error:', error);
});
```

## ControlByWeb Device Configuration

To configure your ControlByWeb device to publish to this MQTT broker:

### 1. Access Device Configuration

1. Log into your ControlByWeb device's web interface
2. Navigate to **Settings** → **MQTT** or **Network** → **MQTT**

### 2. MQTT Broker Settings

Configure the following:

- **MQTT Broker Address**: `fd6ad94a23dc48f7aadb2a1c9b3f5c65.s1.eu.hivemq.cloud`
- **Port**: `8883`
- **Use TLS/SSL**: `Yes` or `Enabled`
- **Username**: `test1234`
- **Password**: `Test1234`
- **Client ID**: (optional, device will generate one if not specified)

### 3. Topic Configuration

Configure the publish topic as configured:
- **Topic Pattern**: `flash/sirens/{deviceID}/status`
  - Replace `{deviceID}` with your actual device identifier
  - Example: `flash/sirens/000CC80630E0/status`

### 4. Message Format

ControlByWeb payload format (JSON):

```json
{
  "clientID": "000CC80630E0",
  "status": "${alertvalue}",
  "vin": "${vin}"
}
```

**Field Descriptions:**
- `clientID`: Your device/client identifier (e.g., "000CC80630E0")
- `status`: Alert/status value from ControlByWeb (e.g., "active", "inactive", "alert")
- `vin`: Vehicle Identification Number or identifier

**Example Published Message:**
```json
{
  "clientID": "000CC80630E0",
  "status": "active",
  "vin": "VIN123456789"
}
```

### 5. Publish Interval

Configure how often the device publishes:
- **Publish Interval**: `60` seconds (or your preferred interval)
- **Publish on Change**: Enable if you want messages only when values change

### 6. Save and Test

1. Save the configuration
2. Check the device logs for MQTT connection status
3. Verify messages are being published using an MQTT client

## Testing Your Publisher

### Subscribe to Topics (Using mosquitto_sub)

To verify messages are being published:

```bash
# Subscribe to all topics
mosquitto_sub \
  -h fd6ad94a23dc48f7aadb2a1c9b3f5c65.s1.eu.hivemq.cloud \
  -p 8883 \
  -u test1234 \
  -P Test1234 \
  -t "#" \
  --tls-version tlsv1.2 \
  --insecure

# Subscribe to ControlByWeb status topic (all devices)
mosquitto_sub \
  -h fd6ad94a23dc48f7aadb2a1c9b3f5c65.s1.eu.hivemq.cloud \
  -p 8883 \
  -u test1234 \
  -P Test1234 \
  -t "flash/sirens/+/status" \
  --tls-version tlsv1.2 \
  --insecure

# Subscribe to specific device
mosquitto_sub \
  -h fd6ad94a23dc48f7aadb2a1c9b3f5c65.s1.eu.hivemq.cloud \
  -p 8883 \
  -u test1234 \
  -P Test1234 \
  -t "flash/sirens/000CC80630E0/status" \
  --tls-version tlsv1.2 \
  --insecure
```

### Using MQTT Explorer (GUI Tool)

1. Download MQTT Explorer: https://mqtt-explorer.com/
2. Add a new connection:
   - **Name**: HiveMQ Cloud
   - **Server**: `fd6ad94a23dc48f7aadb2a1c9b3f5c65.s1.eu.hivemq.cloud`
   - **Port**: `8883`
   - **Protocol**: `mqtts://` (MQTT over TLS)
   - **Username**: `test1234`
   - **Password**: `Test1234`
   - **TLS**: Enable, disable certificate verification (for development)
3. Connect and view published messages

### Verify in Django Application

1. Start your Django backend
2. Check backend logs for MQTT connection status
3. Open frontend at http://localhost:3000
4. Messages should appear in real-time

## Topic Configuration

### ControlByWeb Topic Pattern

- **Topic**: `flash/sirens/{deviceID}/status`
  - `{deviceID}` will be replaced with your actual device ID
  - Example: `flash/sirens/000CC80630E0/status`

### Django Backend Subscription

Configure your Django backend `.env` file to subscribe to:
```
MQTT_TOPICS=flash/sirens/+/status
```

The `+` wildcard will match any deviceID in the topic pattern.

### Example Topics

- `flash/sirens/000CC80630E0/status` - Specific device status
- `flash/sirens/+/status` - All device statuses (wildcard subscription)
- `flash/sirens/#` - All flash/sirens messages (multi-level wildcard)

## Troubleshooting

### Connection Issues

1. **Verify TLS/SSL is enabled**: Port 8883 requires TLS
2. **Check credentials**: Username and password are case-sensitive
3. **Firewall**: Ensure port 8883 is not blocked
4. **Certificate**: For development, disable certificate verification

### Messages Not Appearing

1. **Check topic**: Ensure the topic matches what Django is subscribed to
2. **Verify connection**: Check device/broker connection status
3. **Check Django logs**: Look for MQTT connection errors
4. **Test with mosquitto_sub**: Verify messages are reaching the broker

### ControlByWeb Device Issues

1. **Check device logs**: Review MQTT connection status in device interface
2. **Verify network**: Ensure device can reach the broker (port 8883)
3. **TLS settings**: Ensure TLS/SSL is enabled for port 8883
4. **Topic format**: Verify topic matches expected format

## Security Notes

- **Development**: TLS certificate verification is disabled (`--insecure` flag)
- **Production**: Enable certificate verification for secure connections
- **Credentials**: Keep username and password secure
- **Topics**: Use specific topics, avoid `#` wildcard in production

## Additional Resources

- HiveMQ Cloud Documentation: https://www.hivemq.com/docs/hivemq-cloud/
- MQTT Protocol: https://mqtt.org/
- ControlByWeb Documentation: Check your device's user manual for MQTT configuration

