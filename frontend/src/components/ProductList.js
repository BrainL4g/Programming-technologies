import React from "react";
import ProductCard from "./ProductCard";

export default function ProductList({ products, title }) {
  return (
    <div>
      {title && <h2 style={styles.title}>{title}</h2>}

      <div style={styles.grid}>
        {products.map((p) => (
          <ProductCard key={p.id} product={p} />
        ))}
      </div>
    </div>
  );
}

const styles = {
  title: {
    fontSize: 24,
    marginBottom: 10
  },
  grid: {
    display: "flex",
    flexWrap: "wrap",
    gap: 20
  }
};
