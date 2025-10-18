import { useEffect, useState } from 'react';

function App() {
  const [signals, setSignals] = useState([]);

  useEffect(() => {
    // Получаем URL из .env
    const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8001/ws';
    const ws = new WebSocket(wsUrl);
    
    ws.onopen = () => console.log('✅ Подключено к боту');
    ws.onmessage = (event) => {
      const signal = JSON.parse(event.data);
      setSignals(prev => [signal, ...prev.slice(0, 4)]);
    };
    ws.onerror = (error) => console.error('❌ Ошибка WebSocket:', error);

    return () => ws.close();
  }, []);

  return (
    <div style={{ padding: 16, fontFamily: 'sans-serif', background: '#000', color: 'white' }}>
      <h2>SmartSignal Bot</h2>
      {signals.length === 0 ? (
        <p>Ожидание сигналов... (может занять 1-2 минуты)</p>
      ) : (
        signals.map((s, i) => (
          <div key={i} style={{ 
            background: s.type === 'CALL' ? '#0a3' : '#a00',
            margin: '8px 0',
            padding: '12px',
            borderRadius: '8px'
          }}>
            <strong>{s.asset}</strong> → {s.type}<br/>
            Зона: {s.entry_zone}<br/>
            RSI: <span style={{color: s.ta_details?.rsi < 30 ? 'lightgreen' : 'pink'}}>
              {s.ta_details?.rsi || 'N/A'}
            </span><br/>
            Доходность: +{s.expected_payout}% | ⏱️ {s.expiry_minutes} мин
          </div>
        ))
      )}
    </div>
  );
}

export default App;