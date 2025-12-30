import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'MQTT WebSocket Monitor',
  description: 'Real-time MQTT message monitoring with WebSocket',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

