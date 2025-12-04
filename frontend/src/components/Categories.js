import React from 'react';

const categories = [
  "Смартфоны",
  "Ноутбуки",
  "Комплектующие",
  "Красота и здоровье",
  "Инструменты",
  "Фототехника"
];

function Categories() {
  return (
    <div style={styles.box}>
      <h3>Категории</h3>
      {categories.map((c) => (
        <div key={c} style={styles.item}>{c}</div>
      ))}
    </div>
  );
}

const styles = {
  box: {
    width: 250,
    background: "#fff",
    padding: 20,
    marginRight: 20,
    borderRadius: 8,
    height: "fit-content"
  },
  item: {
    padding: "10px 0",
    borderBottom: "1px solid #eee",
    cursor: "pointer"
  }
};

export default Categories;
