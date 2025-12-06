import React from "react";

export default function HeaderAuth() {
  return (
    <header style={styles.header}>

      <div style={styles.left}>
        <div style={styles.logo}>LOGO</div>
      </div>

      <div style={styles.center}>
        <div style={styles.searchWrapper}>
          <input type="text" placeholder="Поиск..." style={styles.search} />
          <button style={styles.searchBtn}>Поиск</button>
        </div>
      </div>

      <div style={styles.right}>
        <button style={styles.button}>Кабинет</button>
        <button style={styles.button}>Избранное</button>
      </div>
    </header>
  );
}

const styles = {
  header: {
    background: "#fff",
    height: 80,
    display: "flex",
    alignItems: "center",
    padding: "0 40px",
    borderBottom: "1px solid #ddd",
    justifyContent: "space-between",
  },

  left: {
    display: "flex",
    alignItems: "center",
    gap: 20,
    minWidth: 150
  },

  center: {
    flex: 1,
    display: "flex",
    justifyContent: "center",
  },

  right: {
    display: "flex",
    alignItems: "center",
    gap: 15,
    minWidth: 320,
    justifyContent: "flex-end"
  },

  logo: {
    fontWeight: "bold",
    fontSize: 24,
  },

  searchWrapper: {
    display: "flex",
    width: "60%",
    minWidth: 350,
    maxWidth: 650,
  },

  search: {
    flex: 1,
    height: 40,
    padding: "0 12px",
    border: "1px solid #e6e6e6",
    borderRight: "none",
    borderRadius: "6px 0 0 6px",
    background: "#fafafa",
    outline: "none",
  },

  searchBtn: {
    height: 40,
    padding: "0 16px",
    background: "#05386B",
    border: "none",
    color: "#fff",
    cursor: "pointer",
    borderRadius: "0 6px 6px 0",
  },

  button: {
    height: 40,
    padding: "0 18px",
    background: "#05386B",
    border: "none",
    color: "#fff",
    cursor: "pointer",
    borderRadius: 6,
  },
};