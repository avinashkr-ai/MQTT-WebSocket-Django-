# MQTT WebSocket Django NextJS Application

A complete Django application that subscribes to MQTT messages from ControlByWeb devices and broadcasts them to a Next.js frontend via WebSocket in real-time.

## Architecture

```
ControlByWeb Device (MQTT Publisher)
           │
           ▼
    MQTT Broker
           │
           ▼
    Django Backend (MQTT Subscriber)
    ├── MQTT Client (paho-mqtt)
    ├── Django Channels (WebSocket)
    └── REST API (DRF)
           │
           ▼
    Next.js Frontend (WebSocket Client)
```

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- Redis

### 1. Setup Redis

**macOS:**
```bash
brew install redis
brew services start redis
redis-cli ping  # Should return PONG
```

**Linux:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
redis-cli ping
```

### 2. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file and configure MQTT broker settings:
# MQTT_BROKER_HOST=fd6ad94a23dc48f7aadb2a1c9b3f5c65.s1.eu.hivemq.cloud
# MQTT_BROKER_PORT=8883
# MQTT_USERNAME=test1234
# MQTT_PASSWORD=Test1234
# MQTT_TOPICS=flash/sirens/+/status
# MQTT_USE_TLS=True
# MQTT_TLS_INSECURE=True

python manage.py migrate
python manage.py runserver
```

Backend runs at: http://localhost:8000

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:3000

### 4. Verify Setup

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/mqtt/status/
- **Swagger UI**: http://localhost:8000/swagger/
- **Admin Panel**: http://localhost:8000/admin/

## Postman Collection

Import `postman_collection.json` into Postman, or import directly from:
- **Swagger JSON**: http://localhost:8000/swagger.json

## API Endpoints

### MQTT Status
- `GET /api/mqtt/status/` - Get MQTT connection status

### MQTT Messages
- `GET /api/mqtt/messages/` - List messages (paginated)
- `GET /api/mqtt/messages/?topic=<topic>` - Filter by topic
- `GET /api/mqtt/messages/<id>/` - Get specific message
- `POST /api/mqtt/clear-history/` - Clear message history

### MQTT Configuration
- `GET /api/mqtt/config/` - List configurations
- `POST /api/mqtt/config/` - Create configuration
- `GET /api/mqtt/config/<id>/` - Get configuration
- `PUT /api/mqtt/config/<id>/` - Update configuration
- `PATCH /api/mqtt/config/<id>/` - Partial update
- `DELETE /api/mqtt/config/<id>/` - Delete configuration

### Documentation
- `GET /swagger/` - Swagger UI
- `GET /redoc/` - ReDoc documentation
- `GET /swagger.json` - OpenAPI JSON schema

## WebSocket

- **Endpoint**: `ws://localhost:8000/ws/mqtt/`
- **Message Format**: JSON

### Server to Client
```json
{
  "type": "mqtt_message",
  "data": {
    "topic": "device/temperature",
    "payload": {"temperature": 25.5},
    "qos": 0,
    "timestamp": "2024-01-01T12:00:00Z"
  }
}
```

### Client to Server
```json
{
  "type": "ping"
}
```

## Troubleshooting

### MQTT Connection Failed
- Verify MQTT broker is running and accessible
- Check credentials in backend `.env`
- Review backend logs for errors

### Redis Connection Error
- Ensure Redis is running: `redis-cli ping`
- Check Redis host/port in backend `.env`

### WebSocket Connection Failed
- Ensure backend is running
- Check WebSocket URL in frontend `.env.local`
- Check browser console for errors

## Testing MQTT Publisher

### Quick Test with Python Script

Use the provided test publisher script:

```bash
# Install paho-mqtt if not already installed
pip install paho-mqtt

# Run test publisher
python test_publisher.py
```

This will publish test messages to the MQTT broker. Check your Django backend logs and frontend to see the messages appear in real-time.

### Test Subscriber (Optional)

To verify messages are being published:

```bash
python test_subscriber.py
```

### MQTT Broker Information

- **Host**: `fd6ad94a23dc48f7aadb2a1c9b3f5c65.s1.eu.hivemq.cloud`
- **Port**: `8883` (TLS)
- **Username**: `test1234`
- **Password**: `Test1234`

For detailed publisher setup and ControlByWeb device configuration, see:
- `MQTT_PUBLISHER_GUIDE.md` - Complete MQTT publishing guide

## Project Structure

```
MQTT_WebSocket_Django/
├── backend/              # Django backend (see backend/README.md)
├── frontend/             # Next.js frontend (see frontend/README.md)
├── test_publisher.py     # Test script to publish MQTT messages
├── test_subscriber.py    # Test script to subscribe to MQTT messages
├── postman_collection.json
└── MQTT_PUBLISHER_GUIDE.md  # MQTT publishing guide
```

For detailed setup instructions, see:
- `backend/README.md` - Backend documentation
- `frontend/README.md` - Frontend documentation
- `MQTT_PUBLISHER_GUIDE.md` - MQTT publishing and ControlByWeb configuration
