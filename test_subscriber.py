#!/usr/bin/env python3
"""
Simple MQTT Subscriber Script for Testing

This script subscribes to topics on the HiveMQ Cloud MQTT broker.
Use this to verify messages are being published correctly.

Usage:
    python test_subscriber.py
"""

import paho.mqtt.client as mqtt
import json
import ssl

# MQTT Broker Configuration
BROKER_HOST = "fd6ad94a23dc48f7aadb2a1c9b3f5c65.s1.eu.hivemq.cloud"
BROKER_PORT = 8883
USERNAME = "test1234"
PASSWORD = "Test1234"

# Topics to subscribe to (ControlByWeb topic pattern)
TOPICS = [
    "flash/sirens/+/status",  # ControlByWeb status topic (use + as wildcard for deviceID)
    # "#",  # Or subscribe to all topics
]

def on_connect(client, userdata, flags, rc):
    """Callback when connected to MQTT broker"""
    if rc == 0:
        print(f"✓ Connected to MQTT broker: {BROKER_HOST}:{BROKER_PORT}")
        print("\nSubscribing to topics...")
        for topic in TOPICS:
            client.subscribe(topic)
            print(f"  ✓ Subscribed to: {topic}")
        print("\n" + "="*50)
        print("Waiting for messages... (Press Ctrl+C to exit)")
        print("="*50 + "\n")
    else:
        print(f"✗ Connection failed with code {rc}")

def on_message(client, userdata, msg):
    """Callback when message is received"""
    try:
        topic = msg.topic
        payload = msg.payload.decode('utf-8')
        
        # Try to parse as JSON
        try:
            payload_json = json.loads(payload)
            payload_formatted = json.dumps(payload_json, indent=2)
        except json.JSONDecodeError:
            payload_formatted = payload
        
        print(f"\n{'='*50}")
        print(f"Topic: {topic}")
        print(f"QoS: {msg.qos}")
        print(f"Payload:")
        print(payload_formatted)
        print(f"{'='*50}\n")
        
    except Exception as e:
        print(f"Error processing message: {e}")

def on_disconnect(client, userdata, rc):
    """Callback when disconnected from MQTT broker"""
    print(f"\n✗ Disconnected from MQTT broker (code: {rc})")

def subscribe_to_topics():
    """Subscribe to MQTT topics"""
    
    # Create MQTT client
    client = mqtt.Client()
    client.username_pw_set(USERNAME, PASSWORD)
    
    # Set callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    # Enable TLS (required for port 8883)
    client.tls_set()
    client.tls_insecure_set(True)  # Disable certificate verification for development
    
    try:
        # Connect to broker
        print(f"Connecting to {BROKER_HOST}:{BROKER_PORT}...")
        client.connect(BROKER_HOST, BROKER_PORT, 60)
        
        # Start the loop (this blocks until disconnected)
        client.loop_forever()
        
    except KeyboardInterrupt:
        print("\n\nStopping subscriber...")
        client.loop_stop()
        client.disconnect()
        print("✓ Disconnected")
    except Exception as e:
        print(f"✗ Error: {e}")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    print("\n" + "="*50)
    print("MQTT Test Subscriber")
    print("="*50)
    print(f"Broker: {BROKER_HOST}:{BROKER_PORT}")
    print(f"Username: {USERNAME}")
    print(f"Topics: {', '.join(TOPICS)}")
    print("="*50 + "\n")
    
    subscribe_to_topics()

