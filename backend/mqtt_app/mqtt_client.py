"""
MQTT Client for subscribing to ControlByWeb MQTT broker
"""
import paho.mqtt.client as mqtt
import json
import logging
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import MQTTMessage

logger = logging.getLogger(__name__)

# Global MQTT client instance
mqtt_client_instance = None

class MQTTClient:
    def __init__(self):
        self.client = None
        self.is_connected = False
        self.channel_layer = get_channel_layer()
        
    def on_connect(self, client, userdata, flags, rc):
        """Callback when MQTT client connects"""
        if rc == 0:
            self.is_connected = True
            logger.info("MQTT Client connected successfully")
            
            # Subscribe to topics
            topics = getattr(settings, 'MQTT_TOPICS', ['#'])
            for topic in topics:
                topic = topic.strip()
                if topic:
                    client.subscribe(topic)
                    logger.info(f"Subscribed to topic: {topic}")
        else:
            self.is_connected = False
            logger.error(f"MQTT Connection failed with code {rc}")
    
    def on_disconnect(self, client, userdata, rc):
        """Callback when MQTT client disconnects"""
        self.is_connected = False
        logger.warning("MQTT Client disconnected")
    
    def on_message(self, client, userdata, msg):
        """Callback when MQTT message is received"""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            qos = msg.qos
            
            logger.info(f"Received MQTT message - Topic: {topic}, Payload: {payload}")
            
            # Try to parse payload as JSON
            try:
                payload_json = json.loads(payload)
            except json.JSONDecodeError:
                payload_json = payload
            
            # Prepare message data
            message_data = {
                'topic': topic,
                'payload': payload_json if isinstance(payload_json, dict) else payload,
                'qos': qos,
                'timestamp': None,  # Will be set on frontend
            }
            
            # Store message in database (optional)
            try:
                MQTTMessage.objects.create(
                    topic=topic,
                    payload=payload if isinstance(payload, str) else json.dumps(payload_json),
                    qos=qos
                )
            except Exception as e:
                logger.error(f"Error saving message to database: {e}")
            
            # Broadcast message to WebSocket clients
            async_to_sync(self.channel_layer.group_send)(
                'mqtt_messages',
                {
                    'type': 'mqtt_message',
                    'message': message_data
                }
            )
            
        except Exception as e:
            logger.error(f"Error processing MQTT message: {e}")
    
    def on_log(self, client, userdata, level, buf):
        """Callback for MQTT logging"""
        logger.debug(f"MQTT Log: {buf}")
    
    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client = mqtt.Client()
            
            # Set callbacks
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_message = self.on_message
            self.client.on_log = self.on_log
            
            # Set credentials if provided
            username = getattr(settings, 'MQTT_USERNAME', '')
            password = getattr(settings, 'MQTT_PASSWORD', '')
            if username:
                self.client.username_pw_set(username, password)
            
            # Get connection settings
            broker_host = getattr(settings, 'MQTT_BROKER_HOST', 'localhost')
            broker_port = getattr(settings, 'MQTT_BROKER_PORT', 1883)
            keepalive = getattr(settings, 'MQTT_KEEPALIVE', 60)
            use_tls = getattr(settings, 'MQTT_USE_TLS', False)
            tls_insecure = getattr(settings, 'MQTT_TLS_INSECURE', False)
            
            # Enable TLS if configured or if port is 8883 (standard TLS port)
            if use_tls or broker_port == 8883:
                logger.info(f"Configuring TLS for MQTT connection")
                # Configure TLS
                # For HiveMQ Cloud and most cloud MQTT brokers
                if tls_insecure:
                    # Development mode: disable certificate verification
                    self.client.tls_set()
                    self.client.tls_insecure_set(True)
                    logger.warning("TLS certificate verification is disabled (development mode)")
                else:
                    # Production mode: use default CA certificates
                    self.client.tls_set_context(ssl.create_default_context(ssl.Purpose.SERVER_AUTH))
                    logger.info("TLS with certificate verification enabled")
            
            logger.info(f"Connecting to MQTT broker: {broker_host}:{broker_port} (TLS: {use_tls or broker_port == 8883})")
            self.client.connect(broker_host, broker_port, keepalive)
            
            # Start the loop in a non-blocking way
            self.client.loop_start()
            
        except Exception as e:
            logger.error(f"Error connecting to MQTT broker: {e}")
            self.is_connected = False
    
    def disconnect(self):
        """Disconnect from MQTT broker"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            self.is_connected = False
            logger.info("MQTT Client disconnected")
    
    def get_status(self):
        """Get connection status"""
        return {
            'connected': self.is_connected,
            'broker_host': getattr(settings, 'MQTT_BROKER_HOST', ''),
            'broker_port': getattr(settings, 'MQTT_BROKER_PORT', 1883),
            'topics': getattr(settings, 'MQTT_TOPICS', []),
        }

# Global instance
_mqtt_client = MQTTClient()

def get_mqtt_client():
    """Get the global MQTT client instance"""
    return _mqtt_client

def start_mqtt_client():
    """Start the MQTT client"""
    global mqtt_client_instance
    if mqtt_client_instance is None:
        mqtt_client_instance = get_mqtt_client()
        mqtt_client_instance.connect()
    return mqtt_client_instance

