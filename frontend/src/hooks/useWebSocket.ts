import { useEffect, useRef, useState, useCallback } from 'react';
import { WebSocketMessage, ConnectionStatus, MQTTMessage } from '@/types/mqtt';

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws/mqtt/';

interface UseWebSocketReturn {
  connectionStatus: ConnectionStatus;
  messages: MQTTMessage[];
  sendMessage: (message: any) => void;
  clearMessages: () => void;
  lastMessage: MQTTMessage | null;
}

export function useWebSocket(): UseWebSocketReturn {
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>('disconnected');
  const [messages, setMessages] = useState<MQTTMessage[]>([]);
  const [lastMessage, setLastMessage] = useState<MQTTMessage | null>(null);
  const ws = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const reconnectAttempts = useRef(0);
  const maxReconnectAttempts = 5;

  const connect = useCallback(() => {
    try {
      setConnectionStatus('connecting');
      ws.current = new WebSocket(WS_URL);

      ws.current.onopen = () => {
        console.log('WebSocket connected');
        setConnectionStatus('connected');
        reconnectAttempts.current = 0;
      };

      ws.current.onmessage = (event) => {
        try {
          const data: WebSocketMessage = JSON.parse(event.data);
          
          if (data.type === 'mqtt_message' && data.data) {
            const mqttMessage: MQTTMessage = {
              ...data.data,
              timestamp: data.data.timestamp || new Date().toISOString(),
            };
            setLastMessage(mqttMessage);
            setMessages((prev) => [mqttMessage, ...prev].slice(0, 1000)); // Keep last 1000 messages
          } else if (data.type === 'connection') {
            console.log('WebSocket connection established');
          } else if (data.type === 'pong') {
            console.log('Received pong');
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      ws.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        setConnectionStatus('error');
      };

      ws.current.onclose = () => {
        console.log('WebSocket disconnected');
        setConnectionStatus('disconnected');
        
        // Attempt to reconnect
        if (reconnectAttempts.current < maxReconnectAttempts) {
          reconnectAttempts.current += 1;
          const delay = Math.min(1000 * Math.pow(2, reconnectAttempts.current), 30000); // Exponential backoff, max 30s
          
          reconnectTimeoutRef.current = setTimeout(() => {
            console.log(`Attempting to reconnect (${reconnectAttempts.current}/${maxReconnectAttempts})...`);
            connect();
          }, delay);
        } else {
          console.error('Max reconnection attempts reached');
          setConnectionStatus('error');
        }
      };
    } catch (error) {
      console.error('Error creating WebSocket connection:', error);
      setConnectionStatus('error');
    }
  }, []);

  const sendMessage = useCallback((message: any) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket is not connected');
    }
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setLastMessage(null);
  }, []);

  useEffect(() => {
    connect();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [connect]);

  // Send ping every 30 seconds to keep connection alive
  useEffect(() => {
    if (connectionStatus === 'connected') {
      const pingInterval = setInterval(() => {
        sendMessage({ type: 'ping' });
      }, 30000);

      return () => clearInterval(pingInterval);
    }
  }, [connectionStatus, sendMessage]);

  return {
    connectionStatus,
    messages,
    sendMessage,
    clearMessages,
    lastMessage,
  };
}

