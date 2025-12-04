import React from 'react';

function Pagination() {
  return (
    <div style={styles.pagination}>
      <button style={styles.button}>Назад</button>
      <button style={styles.button}>1</button>
      <button style={styles.button}>2</button>
      <button style={styles.button}>3</button>
      <button style={styles.button}>Вперёд</button>
    </div>
  );
}

const styles = {
  pagination: {
    display: "flex",
    justifyContent: "center",
    padding: 20,
    gap: 10
  },
  button: {
    padding: "8px 15px",
    background: "#1976d2",
    border: "none",
    color: "#fff",
    cursor: "pointer",
    borderRadius: 6
  }
};

export default Pagination;
