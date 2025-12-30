# Next.js Frontend - MQTT WebSocket Client

Next.js frontend application for real-time MQTT message monitoring using WebSocket.

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Environment Configuration

Create a `.env.local` file:

```env
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws/mqtt/
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 3. Run Development Server

```bash
npm run dev
```

Application runs at: http://localhost:3000

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js app directory
│   │   ├── page.tsx           # Main page
│   │   ├── layout.tsx         # Root layout
│   │   └── globals.css        # Global styles
│   ├── components/             # React components
│   │   ├── MQTTMessages.tsx   # Main component
│   │   ├── MessageList.tsx    # Message list display
│   │   └── ConnectionStatus.tsx # Status indicator
│   ├── hooks/                  # Custom hooks
│   │   └── useWebSocket.ts    # WebSocket hook
│   └── types/                  # TypeScript types
│       └── mqtt.ts            # MQTT type definitions
├── package.json
├── tsconfig.json
└── tailwind.config.js
```

## Features

- **Real-time Message Display**: Shows MQTT messages as they arrive
- **Connection Status**: Visual indicator for WebSocket connection status
- **Message History**: Displays last 1000 messages with pagination
- **Auto-reconnection**: Automatically reconnects on disconnect
- **Clean UI**: Responsive design with Tailwind CSS

## Components

### MQTTMessages
Main component that orchestrates the message display and connection management.

### MessageList
Displays list of MQTT messages with:
- Topic display
- Payload (JSON formatted)
- QoS level
- Timestamp
- Clear button

### ConnectionStatus
Shows current WebSocket connection status with color-coded indicator.

## Custom Hooks

### useWebSocket
Custom React hook that manages WebSocket connection:
- Connection status tracking
- Message storage (last 1000 messages)
- Auto-reconnection with exponential backoff
- Ping/pong keepalive

## Dependencies

- Next.js 14.0.4
- React 18.2.0
- TypeScript 5.3.3
- Tailwind CSS 3.4.0

## Environment Variables

- `NEXT_PUBLIC_WS_URL`: WebSocket URL (default: `ws://localhost:8000/ws/mqtt/`)
- `NEXT_PUBLIC_API_URL`: API base URL (default: `http://localhost:8000/api`)

## Usage

1. Start the backend server (see `../backend/README.md`)
2. Start this frontend server: `npm run dev`
3. Open http://localhost:3000
4. Messages from MQTT broker will appear in real-time

## Troubleshooting

### WebSocket Connection Failed
- Ensure backend is running
- Check WebSocket URL in `.env.local`
- Verify backend WebSocket endpoint is accessible
- Check browser console for errors

### No Messages Appearing
- Verify MQTT broker is sending messages
- Check backend MQTT connection status
- Ensure backend is receiving and broadcasting messages
- Check browser console for WebSocket messages

### Build Errors
- Clear `.next` directory: `rm -rf .next`
- Reinstall dependencies: `rm -rf node_modules && npm install`
- Check Node.js version (requires 18+)

