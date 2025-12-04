import React from 'react';

function Banner() {
  return (
    <div style={styles.banner}>
      <h2>Наш логотип</h2>
      <p>Лучший агрегатор техники!</p>
    </div>
  );
}

const styles = {
  banner: {
    background: "#1976d2",
    color: "#fff",
    textAlign: "center",
    padding: "40px 0",
    marginBottom: 20
  }
};

export default Banner;
