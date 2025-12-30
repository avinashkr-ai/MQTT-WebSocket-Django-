export interface MQTTMessage {
  id?: number;
  topic: string;
  payload: any;
  qos: number;
  timestamp?: string;
}

export interface MQTTStatus {
  connected: boolean;
  broker_host: string;
  broker_port: number;
  topics: string[];
}

export interface WebSocketMessage {
  type: 'connection' | 'mqtt_message' | 'pong' | 'error';
  message?: string;
  data?: MQTTMessage;
}

export type ConnectionStatus = 'connecting' | 'connected' | 'disconnected' | 'error';

