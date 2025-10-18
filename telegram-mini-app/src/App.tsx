import { useEffect, useState } from 'react';

interface Signal {
  asset: string;
  type: string;
  entry_zone: string;
  expiry_minutes: number;
  expected_payout: number;
  confidence: string;
  ta_details: {
    rsi: number;
    macd: number;
    macd_signal: number;
    ema9: number;
    ema21: number;
    bb_width_pct: number;
    volatility_ok: boolean;
  };
}

function App() {
  const [signals, setSignals] = useState<Signal[]>([]);
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected'>('connecting');

  useEffect(() => {
    const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      setConnectionStatus('connected');
    };

    ws.onmessage = (event) => {
      try {
        const signal: Signal = JSON.parse(event.data);
        setSignals(prev => [signal, ...prev.slice(0, 4)]);
      } catch (error) {
        console.error('Error parsing signal:', error);
      }
    };

    ws.onerror = () => {
      setConnectionStatus('disconnected');
    };

    ws.onclose = () => {
      setConnectionStatus('disconnected');
    };

    return () => ws.close();
  }, []);

  return (
    <div style={{
      padding: 16,
      fontFamily: 'sans-serif',
      background: '#0f0f0f',
      color: 'white',
      minHeight: '100vh'
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 16
      }}>
        <h2 style={{ margin: 0 }}>SmartSignal Pro</h2>
        <div style={{
          width: 10,
          height: 10,
          borderRadius: '50%',
          backgroundColor: connectionStatus === 'connected' ? '#4caf50' :
                          connectionStatus === 'connecting' ? '#ff9800' : '#f44336'
        }} />
      </div>

      {signals.length === 0 ? (
        <div style={{
          textAlign: 'center',
          padding: 40,
          color: '#888'
        }}>
          {connectionStatus === 'connected' ? 'Ожидание сигналов...' : 'Подключение...'}
        </div>
      ) : (
        signals.map((s, i) => (
          <div key={i} style={{
            border: '1px solid #333',
            borderRadius: 8,
            padding: 12,
            margin: '8px 0',
            backgroundColor: s.type === 'CALL' ? '#1a3a2a' : '#3a1a1a'
          }}>
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              marginBottom: 8
            }}>
              <strong style={{ fontSize: 18 }}>{s.asset}</strong>
              <span style={{
                color: s.type === 'CALL' ? '#4caf50' : '#f44336',
                fontWeight: 'bold',
                fontSize: 18
              }}>
                {s.type}
              </span>
            </div>

            <div style={{ fontSize: 14, lineHeight: 1.6 }}>
              <div>Зона входа: <strong>{s.entry_zone}</strong></div>
              <div>
                RSI: <span style={{
                  color: s.ta_details.rsi > 75 ? '#f44336' :
                        s.ta_details.rsi < 25 ? '#4caf50' : 'white'
                }}>
                  {s.ta_details.rsi}
                </span>
              </div>
              <div>
                Доходность: <span style={{ color: '#4caf50' }}>+{s.expected_payout}%</span>
              </div>
              <div>Экспирация: {s.expiry_minutes} мин</div>
              <div style={{
                marginTop: 8,
                paddingTop: 8,
                borderTop: '1px solid #444',
                color: '#4caf50',
                fontWeight: 'bold'
              }}>
                {s.confidence}
              </div>
            </div>
          </div>
        ))
      )}
    </div>
  );
}

export default App;
