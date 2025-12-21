import React from 'react';

// Маппинг для красивых названий ключей (опционально)
const specLabels = {
  processor: "Процессор",
  ram: "Оперативная память",
  storage: "Накопитель",
  camera: "Камера",
  display: "Экран"
};

function FilterPanel({
  sortOption,
  onSortChange,
  priceRange,
  onPriceChange,
  selectedBrands,
  onBrandToggle,
  availableBrands,
  availableSpecs,
  selectedSpecs,
  onSpecToggle,
  onResetFilters
}) {
  return (
    <div style={styles.panel}>
      <div style={styles.section}>
        <h3 style={styles.sectionTitle}>Сортировка</h3>
        {['price_desc', 'price_asc', 'popular'].map(opt => (
          <div key={opt} style={styles.group} onClick={() => onSortChange(opt)}>
            <input type="radio" readOnly checked={sortOption === opt} style={styles.input} />
            <label style={styles.label}>{opt === 'popular' ? 'Популярные' : opt === 'price_asc' ? 'Дешевле' : 'Дороже'}</label>
          </div>
        ))}
      </div>

      <div style={styles.section}>
        <h3 style={styles.sectionTitle}>Производители</h3>
        <div style={styles.scrollList}>
          {availableBrands.map(brand => (
            <div key={brand} style={styles.group} onClick={() => onBrandToggle(brand)}>
              <input type="checkbox" readOnly checked={selectedBrands.includes(brand)} style={styles.input} />
              <label style={styles.label}>{brand}</label>
            </div>
          ))}
        </div>
      </div>

      {/* ДИНАМИЧЕСКИЕ ХАРАКТЕРИСТИКИ */}
      {Object.entries(availableSpecs).map(([specKey, values]) => (
        <div key={specKey} style={styles.section}>
          <h3 style={styles.sectionTitle}>{specLabels[specKey] || specKey}</h3>
          <div style={styles.scrollList}>
            {values.map(val => (
              <div key={val} style={styles.group} onClick={() => onSpecToggle(specKey, val)}>
                <input 
                  type="checkbox" 
                  readOnly 
                  checked={selectedSpecs[specKey]?.includes(val)} 
                  style={styles.input} 
                />
                <label style={styles.label}>{val}</label>
              </div>
            ))}
          </div>
        </div>
      ))}

      <div style={styles.section}>
        <h3 style={styles.sectionTitle}>Цена</h3>
        <div style={{display: 'flex', gap: 5}}>
          <input type="number" placeholder="От" value={priceRange.min} onChange={(e) => onPriceChange('min', e.target.value)} style={styles.priceInput} />
          <input type="number" placeholder="До" value={priceRange.max} onChange={(e) => onPriceChange('max', e.target.value)} style={styles.priceInput} />
        </div>
      </div>

      <button onClick={onResetFilters} style={styles.resetBtn}>Сбросить всё</button>
    </div>
  );
}

const styles = {
  panel: { width: 250, background: '#fff', paddingRight: 20 },
  section: { marginBottom: 20, paddingBottom: 15, borderBottom: '1px solid #f0f0f0' },
  sectionTitle: { fontSize: 15, fontWeight: 600, marginBottom: 12 },
  group: { display: 'flex', alignItems: 'center', marginBottom: 8, cursor: 'pointer' },
  input: { marginRight: 10, cursor: 'pointer' },
  label: { fontSize: 14, cursor: 'pointer', color: '#444' },
  scrollList: { maxHeight: 150, overflowY: 'auto' },
  priceInput: { width: '100%', padding: '6px', border: '1px solid #ddd', borderRadius: 4 },
  resetBtn: { width: '100%', padding: '10px', background: '#f8f9fa', border: 'none', borderRadius: 6, cursor: 'pointer' }
};

export default FilterPanel;