import React from 'react';

function Header() {
  return (
    <header style={styles.header}>
      <div style={styles.logo}>LOGO</div>

      <input type="text" placeholder="Поиск..." style={styles.search} />
      <button style={styles.button}>Поиск</button>

      <button style={styles.button}>Войти</button>
      <button style={styles.button}>Корзина</button>
    </header>
  );
}

const styles = {
  header: {
    background: "#fff",
    height: 60,
    display: "flex",
    alignItems: "center",
    padding: "0 20px",
    gap: 10,
    borderBottom: "1px solid #ddd"
  },
  logo: {
    fontWeight: "bold",
    fontSize: 20,
    marginRight: 20
  },
  search: {
    flex: 1,
    height: 35,
    padding: "0 10px"
  },
  button: {
    height: 35,
    padding: "0 15px",
    background: "#1976d2",
    border: "none",
    color: "#fff",
    cursor: "pointer"
  }
};

export default Header;
