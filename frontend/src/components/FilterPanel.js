import React from 'react';

function FilterPanel({
  sortOption,
  onSortChange,
  priceRange,
  onPriceChange,
  selectedBrands,
  onBrandToggle,
  onResetFilters
}) {
  const brands = ['Samsung', 'Apple', 'Xiaomi', 'Lenovo', 'Asus', 'HP', 'Dell'];

  const sortOptions = [
    { id: 'price_desc', label: 'Сначала дороже' },
    { id: 'price_asc', label: 'Сначала дешевле' },
    { id: 'popular', label: 'Сначала популярнее' }
  ];

  return (
    <div style={styles.panel}>
      <div style={styles.section}>
        <h3 style={styles.sectionTitle}>Сортировка</h3>
        {sortOptions.map((option) => (
          <div key={option.id} style={styles.radioGroup}>
            <input
              type="radio"
              id={option.id}
              name="sort"
              checked={sortOption === option.id}
              onChange={() => onSortChange(option.id)}
              style={styles.radio}
            />
            <label htmlFor={option.id} style={styles.radioLabel}>
              {option.label}
            </label>
          </div>
        ))}
      </div>

      <div style={styles.section}>
        <h3 style={styles.sectionTitle}>Фильтрация</h3>

        <div style={styles.filterBlock}>
          <h4 style={styles.filterTitle}>Производители</h4>
          <div style={styles.brandsList}>
            {brands.map((brand) => (
              <div key={brand} style={styles.checkboxGroup}>
                <input
                  type="checkbox"
                  id={`brand-${brand}`}
                  checked={selectedBrands.includes(brand)}
                  onChange={() => onBrandToggle(brand)}
                  style={styles.checkbox}
                />
                <label htmlFor={`brand-${brand}`} style={styles.checkboxLabel}>
                  {brand}
                </label>
              </div>
            ))}
          </div>
        </div>

        <div style={styles.filterBlock}>
          <h4 style={styles.filterTitle}>Цена</h4>
          <div style={styles.priceInputs}>
            <input
              type="number"
              placeholder="От"
              value={priceRange.min || ''}
              onChange={(e) => onPriceChange('min', e.target.value)}
              style={styles.priceInput}
              min="0"
            />
            <span style={styles.priceSeparator}>—</span>
            <input
              type="number"
              placeholder="До"
              value={priceRange.max || ''}
              onChange={(e) => onPriceChange('max', e.target.value)}
              style={styles.priceInput}
              min="0"
            />
          </div>
        </div>
      </div>

      <button onClick={onResetFilters} style={styles.resetBtn}>
        Сбросить фильтры
      </button>
    </div>
  );
}

const styles = {
  panel: {
    width: 280,
    background: '#fff',
    padding: 20,
    marginRight: 20,
    borderRadius: 8,
    height: 'fit-content',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
  },
  section: {
    marginBottom: 25,
    paddingBottom: 20,
    borderBottom: '1px solid #eee',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 600,
    marginBottom: 15,
    color: '#333',
  },
  radioGroup: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: 12,
    cursor: 'pointer',
  },
  radio: {
    marginRight: 10,
    width: 16,
    height: 16,
    cursor: 'pointer',
  },
  radioLabel: {
    fontSize: 14,
    color: '#555',
    cursor: 'pointer',
    userSelect: 'none',
  },
  filterBlock: {
    marginBottom: 20,
  },
  filterTitle: {
    fontSize: 16,
    fontWeight: 500,
    marginBottom: 12,
    color: '#444',
  },
  brandsList: {
    maxHeight: 200,
    overflowY: 'auto',
    paddingRight: 5,
  },
  checkboxGroup: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: 10,
    cursor: 'pointer',
  },
  checkbox: {
    marginRight: 8,
    width: 16,
    height: 16,
    cursor: 'pointer',
  },
  checkboxLabel: {
    fontSize: 14,
    color: '#555',
    cursor: 'pointer',
    userSelect: 'none',
  },
  priceInputs: {
    display: 'flex',
    alignItems: 'center',
    gap: 8,
  },
  priceInput: {
    flex: 1,
    width: 100,
    padding: '8px 10px',
    border: '1px solid #ddd',
    borderRadius: 4,
    fontSize: 14,
  },
  priceSeparator: {
    color: '#888',
    fontSize: 14,
  },
  resetBtn: {
    width: '100%',
    padding: '10px',
    background: '#f0f0f0',
    border: '1px solid #ddd',
    borderRadius: 6,
    color: '#333',
    fontSize: 14,
    cursor: 'pointer',
    marginTop: 10,
  },
};

export default FilterPanel;