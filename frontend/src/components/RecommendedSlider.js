import React from 'react';
import { recommended } from '../mocks/recommended';
import ProductCard from './ProductCard';

function RecommendedSlider() {
  return (
    <div style={styles.slider}>
      <h3 style={{ marginBottom: 10 }}>Мы рекомендуем</h3>
      <div style={styles.row}>
        {recommended.map((p) => (
          <ProductCard key={p.id} product={p} />
        ))}
      </div>
    </div>
  );
}

const styles = {
  slider: {
    background: "#fff",
    padding: 20,
    borderRadius: 8,
    marginBottom: 20
  },
  row: {
    display: "flex",
    overflowX: "auto"
  }
};

export default RecommendedSlider;
