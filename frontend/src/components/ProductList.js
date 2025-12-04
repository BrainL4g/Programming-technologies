import React from 'react';
import { products } from '../mocks/products';
import ProductCard from './ProductCard';

function ProductList() {
  return (
    <div style={styles.list}>
      {products.map((p) => (
        <ProductCard key={p.id} product={p} />
      ))}
    </div>
  );
}

const styles = {
  list: {
    display: "flex",
    flexWrap: "wrap"
  }
};

export default ProductList;
