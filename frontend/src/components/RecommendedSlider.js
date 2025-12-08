import React, { useState } from "react";
import ProductCard from "./ProductCard";

export default function RecommendedSlider({ products }) {
  const [index, setIndex] = useState(0);

  const visibleCount = 3;
  const maxIndex = products.length - visibleCount;

  const next = () => {
    setIndex((prev) => Math.min(prev + 1, maxIndex));
  };

  const prev = () => {
    setIndex((prev) => Math.max(prev - 1, 0));
  };

  const visibleProducts = products.slice(index, index + visibleCount);

  return (
    <div style={styles.wrap}>
      <h2 style={styles.title}>Мы рекомендуем</h2>

      <div style={styles.slider}>
        <button style={styles.arrowLeft} onClick={prev} disabled={index === 0}>
          ‹
        </button>

        <div style={styles.cards}>
          {visibleProducts.map((p) => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>

        <button
          style={styles.arrowRight}
          onClick={next}
          disabled={index >= maxIndex}
        >
          ›
        </button>
      </div>
    </div>
  );
}

const styles = {
  wrap: {
    background: "#fff",
    padding: 20,
    borderRadius: 8,
    width: "100%",
  },
  title: {
    marginBottom: 15,
    fontSize: 24,
  },
  slider: {
    position: "relative",
    display: "flex",
    alignItems: "center",
  },
  cards: {
    display: "flex",
    gap: 20,
    width: "100%",
    overflow: "hidden",
  },
  arrowLeft: {
    fontSize: 30,
    padding: "0 10px",
    cursor: "pointer",
    background: "none",
    border: "none",
  },
  arrowRight: {
    fontSize: 30,
    padding: "0 10px",
    cursor: "pointer",
    background: "none",
    border: "none",
  },
};
