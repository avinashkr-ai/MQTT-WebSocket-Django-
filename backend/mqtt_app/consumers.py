"""
WebSocket consumers for MQTT messages
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import logging

logger = logging.getLogger(__name__)


class MQTTConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for broadcasting MQTT messages"""
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.group_name = 'mqtt_messages'
        
        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        logger.info(f"WebSocket client connected: {self.channel_name}")
        
        # Send welcome message
        await self.send(text_data=json.dumps({
            'type': 'connection',
            'message': 'Connected to MQTT WebSocket'
        }))
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        logger.info(f"WebSocket client disconnected: {self.channel_name}")
    
    async def receive(self, text_data):
        """Handle messages received from WebSocket client"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type', 'unknown')
            
            logger.info(f"Received WebSocket message: {message_type}")
            
            # Echo back or handle client messages
            if message_type == 'ping':
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'message': 'pong'
                }))
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON received from WebSocket client")
        except Exception as e:
            logger.error(f"Error handling WebSocket message: {e}")
    
    async def mqtt_message(self, event):
        """Receive message from room group and send to WebSocket"""
        message = event['message']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'mqtt_message',
            'data': message
        }))

