import React from 'react';

function ProductCard({ product }) {
  return (
    <div style={styles.card}>
      <img src={product.image} alt="" style={styles.image} />

      <h4 style={styles.title}>{product.title}</h4>
      <div style={styles.price}>{product.price} ₽</div>

      <button style={styles.fav}>★ В избранное</button>
    </div>
  );
}

const styles = {
  card: {
    background: "#fff",
    padding: 15,
    borderRadius: 8,
    width: 200,
    margin: 10,
    textAlign: "center"
  },
  image: {
    width: "100%",
    borderRadius: 6
  },
  title: {
    fontSize: 16,
    margin: "10px 0"
  },
  price: {
    fontWeight: "bold",
    marginBottom: 10
  },
  fav: {
    width: "100%",
    padding: "8px 0",
    background: "#1976d2",
    color: "#fff",
    border: "none",
    cursor: "pointer",
    borderRadius: 6
  }
};

export default ProductCard;
