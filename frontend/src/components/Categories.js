import React from 'react';
import { useNavigate } from "react-router-dom";

const categories = [
  "Смартфоны",
  "Ноутбуки",
  "Комплектующие",
  "Красота и здоровье",
  "Инструменты",
  "Фототехника"
];

// Маппинг: название → ключ категории в URL
const categoryMap = {
  "Смартфоны": "smartphones",
  "Ноутбуки": "laptops",
  "Комплектующие": "components",
  "Красота и здоровье": "beauty",
  "Инструменты": "tools",
  "Фототехника": "photo"
};

function Categories() {
  const navigate = useNavigate();

  const handleClick = (c) => {
    const key = categoryMap[c];
    navigate(`/search?category=${key}`);
  };

  return (
    <div style={styles.box}>
      <h3>Категории</h3>
      {categories.map((c) => (
        <div
          key={c}
          style={styles.item}
          onClick={() => handleClick(c)}
        >
          {c}
        </div>
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
