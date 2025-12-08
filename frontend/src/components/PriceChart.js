import React, { useState, useEffect } from 'react';

function PriceChart({ productId, productName = "Товар" }) {
  // Моковые данные для графика
  const priceData = {
    'DNS': [
      { date: '2023-01-01', price: 29990 },
      { date: '2023-01-15', price: 29500 },
      { date: '2023-02-01', price: 28990 },
      { date: '2023-02-15', price: 28500 },
      { date: '2023-03-01', price: 27990 },
      { date: '2023-03-15', price: 27500 },
      { date: '2023-04-01', price: 26990 },
    ],
    'Ситилинк': [
      { date: '2023-01-01', price: 30500 },
      { date: '2023-01-15', price: 30000 },
      { date: '2023-02-01', price: 29500 },
      { date: '2023-02-15', price: 29000 },
      { date: '2023-03-01', price: 28500 },
      { date: '2023-03-15', price: 28000 },
      { date: '2023-04-01', price: 27500 },
    ],
    'М.Видео': [
      { date: '2023-01-01', price: 31000 },
      { date: '2023-01-15', price: 30500 },
      { date: '2023-02-01', price: 30000 },
      { date: '2023-02-15', price: 29500 },
      { date: '2023-03-01', price: 29000 },
      { date: '2023-03-15', price: 28500 },
      { date: '2023-04-01', price: 27990 },
    ],
    'Эльдорадо': [
      { date: '2023-01-01', price: 29500 },
      { date: '2023-01-15', price: 29000 },
      { date: '2023-02-01', price: 28500 },
      { date: '2023-02-15', price: 28000 },
      { date: '2023-03-01', price: 27500 },
      { date: '2023-03-15', price: 27000 },
      { date: '2023-04-01', price: 26500 },
    ]
  };

  const [selectedShop, setSelectedShop] = useState('DNS');
  const [viewMode, setViewMode] = useState('single');
  const shops = Object.keys(priceData);

  // Расчет масштабов графика
  const chartWidth = 600;
  const chartHeight = 300;
  const padding = { top: 20, right: 40, bottom: 40, left: 60 };

  const allPrices = Object.values(priceData).flat().map(item => item.price);
  const maxPrice = Math.max(...allPrices);
  const minPrice = Math.min(...allPrices);
  const priceRange = maxPrice - minPrice || 1;

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('ru-RU', {
      month: 'short',
      day: 'numeric'
    });
  };

  const formatPrice = (price) => {
    return price.toLocaleString('ru-RU') + ' ₽';
  };

  const scaleY = (price) => {
    return chartHeight - padding.bottom - ((price - minPrice) / priceRange) * (chartHeight - padding.top - padding.bottom);
  };

  const scaleX = (index, total) => {
    return padding.left + (index / (total - 1)) * (chartWidth - padding.left - padding.right);
  };

  const createPath = (data) => {
    if (!data || data.length === 0) return '';

    return data.map((point, index) => {
      const x = scaleX(index, data.length);
      const y = scaleY(point.price);
      return `${index === 0 ? 'M' : 'L'} ${x} ${y}`;
    }).join(' ');
  };

  const shopColors = {
    'DNS': '#05386B',
    'Ситилинк': '#d32f2f',
    'М.Видео': '#388e3c',
    'Эльдорадо': '#ff9800'
  };

  const currentData = viewMode === 'single' ? priceData[selectedShop] : [];

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h3 style={styles.title}>История цен: {productName}</h3>

        <div style={styles.controls}>
          {viewMode === 'single' && (
            <select
              value={selectedShop}
              onChange={(e) => setSelectedShop(e.target.value)}
              style={styles.select}
            >
              {shops.map(shop => (
                <option key={shop} value={shop}>{shop}</option>
              ))}
            </select>
          )}
          <div style={styles.viewToggle}>

            <button
              style={viewMode === 'single' ? styles.activeButton : styles.button}
              onClick={() => setViewMode('single')}
            >
              Один магазин
            </button>
            <button
              style={viewMode === 'all' ? styles.activeButton : styles.button}
              onClick={() => setViewMode('all')}
            >
              Все магазины
            </button>
          </div>


        </div>
      </div>

      <div style={styles.chartContainer}>
        <svg width={chartWidth} height={chartHeight} style={styles.chart}>
          {/* Сетка */}
          <g>
            {[0, 1, 2, 3, 4].map(i => {
              const price = minPrice + (priceRange * i / 4);
              const y = scaleY(price);
              return (
                <g key={`grid-y-${i}`}>
                  <line
                    x1={padding.left}
                    y1={y}
                    x2={chartWidth - padding.right}
                    y2={y}
                    stroke="#eee"
                    strokeWidth="1"
                  />
                  <text
                    x={padding.left - 10}
                    y={y}
                    textAnchor="end"
                    dominantBaseline="middle"
                    fontSize="12"
                    fill="#666"
                  >
                    {formatPrice(Math.round(price))}
                  </text>
                </g>
              );
            })}
          </g>

          {/* Оси */}
          <line
            x1={padding.left}
            y1={chartHeight - padding.bottom}
            x2={chartWidth - padding.right}
            y2={chartHeight - padding.bottom}
            stroke="#333"
            strokeWidth="2"
          />
          <line
            x1={padding.left}
            y1={padding.top}
            x2={padding.left}
            y2={chartHeight - padding.bottom}
            stroke="#333"
            strokeWidth="2"
          />

          {/* Подписи осей */}
          <text
            x={chartWidth / 2}
            y={chartHeight - 5}
            textAnchor="middle"
            fontSize="12"
            fill="#333"
          >
            Дата
          </text>
          <text
            x={10}
            y={chartHeight / 2}
            textAnchor="middle"
            fontSize="12"
            fill="#333"
            transform={`rotate(-90, 10, ${chartHeight / 2})`}
          >
            Цена (₽)
          </text>

          {/* График */}
          {viewMode === 'single' ? (
            <>
              <path
                d={createPath(currentData)}
                fill="none"
                stroke={shopColors[selectedShop]}
                strokeWidth="2"
              />
              {currentData.map((point, index) => {
                const x = scaleX(index, currentData.length);
                const y = scaleY(point.price);
                return (
                  <g key={`point-${index}`}>
                    <circle
                      cx={x}
                      cy={y}
                      r="4"
                      fill={shopColors[selectedShop]}
                      stroke="#fff"
                      strokeWidth="2"
                    />
                    <title>
                      {formatDate(point.date)}: {formatPrice(point.price)}
                    </title>
                  </g>
                );
              })}
            </>
          ) : (
            shops.map(shop => {
              const shopData = priceData[shop];
              return (
                <g key={`line-${shop}`}>
                  <path
                    d={createPath(shopData)}
                    fill="none"
                    stroke={shopColors[shop]}
                    strokeWidth="2"
                    opacity="0.8"
                  />
                </g>
              );
            })
          )}
        </svg>

        {/* Подписи дат */}
        <div style={styles.dates}>
          {(viewMode === 'single' ? currentData : priceData['DNS'] || [])
            .filter((_, index) => index % 2 === 0)
            .map((point, index) => (
              <div key={`date-${index}`} style={styles.dateLabel}>
                {formatDate(point.date)}
              </div>
            ))}
        </div>
      </div>

      {viewMode === 'all' && (
        <div style={styles.legend}>
          {shops.map(shop => (
            <div key={`legend-${shop}`} style={styles.legendItem}>
              <div
                style={{
                  ...styles.legendColor,
                  backgroundColor: shopColors[shop]
                }}
              />
              <span style={styles.legendText}>{shop}</span>
            </div>
          ))}
        </div>
      )}

      <div style={styles.info}>
        <div style={styles.priceInfo}>
          <div style={styles.priceItem}>
            <span style={styles.priceLabel}>Минимальная цена:</span>
            <span style={styles.minPrice}>{formatPrice(minPrice)}</span>
          </div>
        </div>
        <div style={styles.timeframe}>
          <span>Период: Январь 2023 — Апрель 2023</span>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    background: '#fff',
    borderRadius: '8px',
    padding: '20px',
    marginBottom: '20px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '20px',
    flexWrap: 'wrap',
  },
  title: {
    fontSize: '18px',
    fontWeight: '600',
    color: '#333',
    margin: 0,
  },
  controls: {
    display: 'flex',
    gap: '15px',
    alignItems: 'center',
    flexWrap: 'wrap',
  },
  viewToggle: {
    display: 'flex',
    background: '#f5f5f5',
    borderRadius: '6px',
    padding: '2px',
  },
  button: {
    padding: '6px 12px',
    background: 'transparent',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '13px',
    color: '#666',
  },
  activeButton: {
    padding: '6px 12px',
    background: '#05386B',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '13px',
    color: 'white',
  },
  select: {
    padding: '6px 12px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '13px',
    background: 'white',
    cursor: 'pointer',
    minWidth: '150px',
  },
  chartContainer: {
    position: 'relative',
    marginBottom: '10px',
  },
  chart: {
    display: 'block',
    margin: '0 auto',
  },
  dates: {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '0 60px',
    marginTop: '5px',
  },
  dateLabel: {
    fontSize: '11px',
    color: '#666',
    textAlign: 'center',
    minWidth: '40px',
  },
  legend: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '15px',
    justifyContent: 'center',
    marginTop: '15px',
    padding: '10px',
    background: '#f9f9f9',
    borderRadius: '6px',
  },
  legendItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
  },
  legendColor: {
    width: '12px',
    height: '12px',
    borderRadius: '2px',
  },
  legendText: {
    fontSize: '12px',
    color: '#666',
  },
  info: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: '20px',
    paddingTop: '15px',
    borderTop: '1px solid #eee',
    flexWrap: 'wrap',
  },
  priceInfo: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  priceItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
  },
  priceLabel: {
    fontSize: '13px',
    color: '#666',
  },
  minPrice: {
    fontSize: '14px',
    color: '#d32f2f',
    fontWeight: '500',
  },
  timeframe: {
    fontSize: '12px',
    color: '#888',
    fontStyle: 'italic',
  },
};

export default PriceChart;