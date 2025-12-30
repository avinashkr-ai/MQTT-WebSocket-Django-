# Django Backend - MQTT WebSocket Server

Django backend that subscribes to MQTT messages and broadcasts them via WebSocket.

## Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the `backend` directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True

# MQTT Configuration (HiveMQ Cloud with TLS - ControlByWeb)
MQTT_BROKER_HOST=fd6ad94a23dc48f7aadb2a1c9b3f5c65.s1.eu.hivemq.cloud
MQTT_BROKER_PORT=8883
MQTT_USERNAME=test1234
MQTT_PASSWORD=Test1234
MQTT_TOPICS=flash/sirens/+/status  # ControlByWeb topic pattern (use + as wildcard for deviceID)
MQTT_KEEPALIVE=60
MQTT_USE_TLS=True
MQTT_TLS_INSECURE=True  # Set to False in production for certificate verification

# Redis Configuration
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
```

**Note**: The topic pattern `flash/sirens/+/status` uses `+` as a wildcard to match any deviceID. The ControlByWeb device will publish to `flash/sirens/{deviceID}/status` where `{deviceID}` is your actual device identifier.

### 4. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Run Server

```bash
python manage.py runserver
```

## Project Structure

```
backend/
├── backend/              # Django project settings
│   ├── settings.py      # Main settings with MQTT & Channels config
│   ├── urls.py          # URL routing with Swagger
│   ├── asgi.py          # ASGI config for WebSocket
│   └── wsgi.py          # WSGI config
├── mqtt_app/            # Main MQTT application
│   ├── models.py        # MQTTMessage & MQTTConfig models
│   ├── views.py         # REST API views
│   ├── serializers.py   # DRF serializers
│   ├── mqtt_client.py   # MQTT subscriber service
│   ├── consumers.py     # WebSocket consumer
│   ├── routing.py       # WebSocket routing
│   ├── urls.py          # API URLs
│   └── admin.py         # Admin interface
└── manage.py
```

## Features

- **MQTT Client**: Subscribes to MQTT broker on startup
- **WebSocket Broadcasting**: Broadcasts MQTT messages to connected clients
- **REST API**: Full CRUD operations for configurations and message history
- **Swagger Documentation**: Auto-generated API documentation
- **Admin Interface**: Django admin for managing data

## API Endpoints

### Base URL: `http://localhost:8000/api`

- `GET /mqtt/status/` - MQTT connection status
- `GET /mqtt/messages/` - List messages (paginated, filter by topic)
- `GET /mqtt/messages/<id>/` - Get specific message
- `POST /mqtt/clear-history/` - Clear message history
- `GET /mqtt/config/` - List configurations
- `POST /mqtt/config/` - Create configuration
- `GET /mqtt/config/<id>/` - Get configuration
- `PUT /mqtt/config/<id>/` - Update configuration
- `PATCH /mqtt/config/<id>/` - Partial update
- `DELETE /mqtt/config/<id>/` - Delete configuration

### Documentation

- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
- OpenAPI JSON: http://localhost:8000/swagger.json

## WebSocket Endpoint

- **URL**: `ws://localhost:8000/ws/mqtt/`
- **Consumer**: `mqtt_app.consumers.MQTTConsumer`

## Dependencies

- Django 4.2.7
- Django REST Framework 3.14.0
- Django Channels 4.0.0
- channels-redis 4.1.0
- paho-mqtt 1.6.1
- drf-yasg 1.21.7
- django-cors-headers 4.3.1
- redis 5.0.1
- python-dotenv 1.0.0

## How It Works

1. **MQTT Client**: On Django startup, the MQTT client connects to the broker and subscribes to configured topics
2. **Message Reception**: When messages arrive, they're stored in the database and broadcast via Django Channels
3. **WebSocket Broadcasting**: All connected WebSocket clients receive messages in real-time
4. **REST API**: Provides endpoints for querying message history and managing configuration

## Troubleshooting

### MQTT Not Connecting
- Check MQTT broker is accessible
- Verify credentials in `.env`
- Check backend logs for connection errors

### Redis Connection Issues
- Ensure Redis is running: `redis-cli ping`
- Verify Redis host/port in `.env`

### WebSocket Not Working
- Ensure Redis is running (required for Channels)
- Check ASGI application is configured correctly
- Review browser console for WebSocket errors

