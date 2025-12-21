import React, { useState, useEffect, useMemo } from 'react';
import apiClient from "../api/apiClient";

function PriceChart({ offers = [], productName = "" }) {
  const [selectedOfferId, setSelectedOfferId] = useState('average');
  const [allHistories, setAllHistories] = useState({}); // { offerId: [data] }
  const [loading, setLoading] = useState(false);

  // 1. Загружаем историю для ВСЕХ предложений при монтировании
  useEffect(() => {
    const fetchAllHistories = async () => {
      if (offers.length === 0) return;
      setLoading(true);
      try {
        const historiesMap = {};
        await Promise.all(
          offers.map(async (offer) => {
            try {
              const data = await apiClient.get(`/offers/${offer.id}/price-history`);
              historiesMap[offer.id] = data;
            } catch (err) {
              console.error(`Ошибка загрузки истории для оффера ${offer.id}:`, err);
              historiesMap[offer.id] = [];
            }
          })
        );
        setAllHistories(historiesMap);
      } finally {
        setLoading(false);
      }
    };
    fetchAllHistories();
  }, [offers]);

  // 2. Динамическое вычисление данных для графика
  const chartData = useMemo(() => {
    if (loading || Object.keys(allHistories).length === 0) return [];

    if (selectedOfferId !== 'average') {
      // Если выбран конкретный магазин
      return (allHistories[selectedOfferId] || []).map(item => ({
        date: item.recorded_at,
        price: Math.round(item.price)
      }));
    } else {
      // ВЫЧИСЛЕНИЕ СРЕДНЕЙ ЦЕНЫ
      const dateMap = {}; // { "2023-10-01": [price1, price2] }

      Object.values(allHistories).forEach(history => {
        history.forEach(item => {
          const date = item.recorded_at.split('T')[0]; // Берем только дату без времени
          if (!dateMap[date]) dateMap[date] = [];
          dateMap[date].push(item.price);
        });
      });

      // Превращаем карту дат в массив со средними значениями
      return Object.entries(dateMap)
        .map(([date, prices]) => ({
          date: date,
          price: Math.round(prices.reduce((a, b) => a + b, 0) / prices.length)
        }))
        .sort((a, b) => new Date(a.date) - new Date(b.date));
    }
  }, [selectedOfferId, allHistories, loading]);

  // Параметры SVG
  const chartWidth = 800;
  const chartHeight = 350;
  const padding = { top: 40, right: 50, bottom: 60, left: 80 };

  const sortedData = [...chartData].sort((a, b) => new Date(a.date) - new Date(b.date));
  const prices = sortedData.map(d => d.price);
  
  const maxP = prices.length ? Math.max(...prices) : 1000;
  const minP = prices.length ? Math.min(...prices) : 0;
  const diff = maxP - minP || 1000;
  const displayMin = Math.max(0, minP - diff * 0.15);
  const displayMax = maxP + diff * 0.15;

  const getX = (idx) => padding.left + (idx / (sortedData.length - 1 || 1)) * (chartWidth - padding.left - padding.right);
  const getY = (price) => chartHeight - padding.bottom - ((price - displayMin) / (displayMax - displayMin)) * (chartHeight - padding.top - padding.bottom);

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h3 style={styles.title}>Мониторинг цен</h3>
        <div style={styles.controls}>
          <span style={{fontSize: '13px', color: '#666'}}>Показать: </span>
          <select 
            style={styles.select} 
            value={selectedOfferId} 
            onChange={(e) => setSelectedOfferId(e.target.value)}
          >
            <option value="average">Динамическая средняя цена</option>
            {offers.map(offer => (
              <option key={offer.id} value={offer.id}>{offer.storeName}</option>
            ))}
          </select>
        </div>
      </div>

      <div style={styles.chartWrapper}>
        {loading ? (
          <div style={{height: chartHeight, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            Вычисляю историю цен...
          </div>
        ) : sortedData.length === 0 ? (
          <div style={{height: chartHeight, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#999'}}>
            Нет данных для построения графика
          </div>
        ) : (
          <svg width={chartWidth} height={chartHeight} style={{display: 'block', margin: '0 auto'}}>
            {/* Сетка Y */}
            {[0, 0.25, 0.5, 0.75, 1].map(factor => {
              const val = displayMin + (displayMax - displayMin) * factor;
              return (
                <g key={factor}>
                  <line x1={padding.left} y1={getY(val)} x2={chartWidth - padding.right} y2={getY(val)} stroke="#f0f0f0" strokeDasharray="4" />
                  <text x={padding.left - 10} y={getY(val)} textAnchor="end" fontSize="11" fill="#999" dominantBaseline="middle">
                    {Math.round(val).toLocaleString()} ₽
                  </text>
                </g>
              );
            })}

            {/* Линия */}
            <path 
              d={sortedData.map((p, i) => `${i === 0 ? 'M' : 'L'} ${getX(i)} ${getY(p.price)}`).join(' ')} 
              fill="none" 
              stroke={selectedOfferId === 'average' ? "#05386B" : "#E74C3C"} 
              strokeWidth="3" 
              strokeLinejoin="round"
            />

            {/* Точки */}
            {sortedData.map((p, i) => (
              <g key={i}>
                <circle cx={getX(i)} cy={getY(p.price)} r="5" fill={selectedOfferId === 'average' ? "#05386B" : "#E74C3C"} stroke="white" strokeWidth="2" />
                <title>{new Date(p.date).toLocaleDateString()}: {p.price.toLocaleString()} ₽</title>
              </g>
            ))}

            {/* Даты X */}
            {sortedData.map((p, i) => {
              if (sortedData.length > 10 && i % Math.ceil(sortedData.length / 8) !== 0) return null;
              return (
                <text key={i} x={getX(i)} y={chartHeight - 20} textAnchor="middle" fontSize="10" fill="#666">
                  {new Date(p.date).toLocaleDateString('ru-RU', {day: 'numeric', month: 'short'})}
                </text>
              );
            })}
          </svg>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: { background: '#fff', padding: '24px', borderRadius: '12px', boxShadow: '0 4px 20px rgba(0,0,0,0.08)' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '25px' },
  title: { fontSize: '20px', fontWeight: '700', color: '#1a1a1a', margin: 0 },
  controls: { display: 'flex', alignItems: 'center', gap: '10px' },
  select: { padding: '10px 15px', borderRadius: '8px', border: '1px solid #dee2e6', background: '#f8f9fa', color: '#495057', fontSize: '14px', cursor: 'pointer', outline: 'none' },
  chartWrapper: { width: '100%', overflowX: 'auto' }
};

export default PriceChart;