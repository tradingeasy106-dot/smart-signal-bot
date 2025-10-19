import { useEffect, useState } from 'react';
import { useInitData, useThemeParams } from "@telegram-apps/sdk";

function App() {
  const [signals, setSignals] = useState([]);
  const [selectedAsset, setSelectedAsset] = useState('All');
  const [analysisMode, setAnalysisMode] = useState('All');
  const { bg_color, text_color } = useThemeParams();

  // Подключение к WebSocket
  useEffect(() => {
    const wsUrl = import.meta.env.VITE_WS_URL || 'wss://smart-signal-bot-2c86.onrender.com/ws';
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => console.log('✅ Подключено к боту');
    ws.onmessage = (event) => {
      const signal = JSON.parse(event.data);
      setSignals(prev => [signal, ...prev.slice(0, 9)]); // Последние 10
    };
    ws.onerror = (error) => console.error('❌ Ошибка WebSocket:', error);

    return () => ws.close();
  }, []);

  // Фильтрация сигналов
  const filteredSignals = signals.filter(s => {
    const assetMatch = selectedAsset === 'All' || s.asset === selectedAsset;
    const modeMatch = analysisMode === 'All' || s.analysis_type === analysisMode;
    return assetMatch && modeMatch;
  });

  // Уникальные активы для кнопок
  const uniqueAssets = [...new Set(signals.map(s => s.asset))];

  return (
    <div style={{
      background: bg_color || '#0f0f1b',
      color: text_color || '#e6e6ff',
      fontFamily: 'Segoe UI, system-ui, sans-serif',
      padding: '16px',
      minHeight: '100vh'
    }}>
      {/* Шапка */}
      <header style={{ textAlign: 'center', marginBottom: '20px' }}>
        <h1 style={{ margin: '0 0 8px', fontSize: '24px' }}>🔥 SmartSignal Pro</h1>
        <div style={{
          background: '#1a1a2e',
          padding: '8px',
          borderRadius: '12px',
          display: 'flex',
          justifyContent: 'space-around',
          fontSize: '14px'
        }}>
          <span>✅ Win: 72%</span>
          <span>💰 +$142</span>
        </div>
      </header>

      {/* Фильтры: Активы */}
      <div style={{ marginBottom: '16px' }}>
        <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '8px' }}>
          <button
            onClick={() => setSelectedAsset('All')}
            style={{
              background: selectedAsset === 'All' ? '#4CAF50' : '#333',
              color: 'white',
              border: 'none',
              borderRadius: '20px',
              padding: '6px 12px',
              fontSize: '14px',
              whiteSpace: 'nowrap'
            }}
          >
            Все
          </button>
          {uniqueAssets.map(asset => (
            <button
              key={asset}
              onClick={() => setSelectedAsset(asset)}
              style={{
                background: selectedAsset === asset ? '#2196F3' : '#333',
                color: 'white',
                border: 'none',
                borderRadius: '20px',
                padding: '6px 12px',
                fontSize: '14px',
                whiteSpace: 'nowrap'
              }}
            >
              {asset}
            </button>
          ))}
        </div>
      </div>

      {/* Фильтры: Тип анализа */}
      <div style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            onClick={() => setAnalysisMode('All')}
            style={{
              background: analysisMode === 'All' ? '#9C27B0' : '#333',
              color: 'white',
              border: 'none',
              borderRadius: '20px',
              padding: '6px 12px',
              fontSize: '14px',
              flex: 1
            }}
          >
            Все сигналы
          </button>
          <button
            onClick={() => setAnalysisMode('smart_money')}
            style={{
              background: analysisMode === 'smart_money' ? '#FF9800' : '#333',
              color: 'white',
              border: 'none',
              borderRadius: '20px',
              padding: '6px 12px',
              fontSize: '14px',
              flex: 1
            }}
          >
            Smart Money
          </button>
          <button
            onClick={() => setAnalysisMode('ta')}
            style={{
              background: analysisMode === 'ta' ? '#00BCD4' : '#333',
              color: 'white',
              border: 'none',
              borderRadius: '20px',
              padding: '6px 12px',
              fontSize: '14px',
              flex: 1
            }}
          >
            Тех. анализ
          </button>
        </div>
      </div>

      {/* Сигналы */}
      {filteredSignals.length === 0 ? (
        <div style={{
          textAlign: 'center',
          padding: '40px 20px',
          color: '#888'
        }}>
          Нет сигналов по выбранным фильтрам.<br/>
          Попробуйте выбрать «Все».
        </div>
      ) : (
        filteredSignals.map((s, i) => (
          <div key={i} style={{
            background: s.type === 'CALL' ? 'rgba(76, 175, 80, 0.15)' : 'rgba(244, 67, 54, 0.15)',
            borderLeft: `4px solid ${s.type === 'CALL' ? '#4CAF50' : '#F44336'}`,
            padding: '16px',
            margin: '12px 0',
            borderRadius: '12px',
            fontSize: '15px'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <strong>{s.asset}</strong>
              <span style={{ color: s.type === 'CALL' ? '#4CAF50' : '#F44336', fontWeight: 'bold' }}>
                {s.type}
              </span>
            </div>
            <div>Зона входа: <b>{s.entry_zone}</b></div>
            <div>Доходность: <b>+{s.expected_payout}%</b></div>
            <div>Экспирация: <b>{s.expiry_minutes} мин</b></div>
            <div style={{ marginTop: '6px', fontSize: '13px', color: '#aaa' }}>
              Анализ: <b>{s.analysis_type === 'smart_money' ? 'Smart Money' : 'Тех. анализ'}</b>
            </div>
          </div>
        ))
      )}

      {/* Нижняя панель */}
      <div style={{
        display: 'flex',
        gap: '12px',
        marginTop: '20px'
      }}>
        <button
          onClick={() => alert('Аналитика скоро!')}
          style={{
            flex: 1,
            background: '#2196F3',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            padding: '12px',
            fontSize: '16px',
            fontWeight: 'bold'
          }}
        >
          📊 Аналитика
        </button>
        <button
          onClick={() => alert('Настройки')}
          style={{
            flex: 1,
            background: '#607D8B',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            padding: '12px',
            fontSize: '16px'
          }}
        >
          ⚙️ Настройки
        </button>
      </div>

      <footer style={{
        fontSize: '11px',
        color: '#777',
        marginTop: '20px',
        textAlign: 'center',
        lineHeight: 1.4
      }}>
        Торговля сопряжена с риском.<br/>
        Сигналы носят информационный характер.
      </footer>
    </div>
  );
}

export default App;