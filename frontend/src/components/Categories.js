import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import apiClient from '../api/apiClient'; // Используем ваш настроенный клиент

function Categories() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  // Загрузка категорий при монтировании
  useEffect(() => {
    apiClient.get('/categories/')
      .then(data => {
        setCategories(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Ошибка загрузки категорий:", err);
        setError("Не удалось загрузить категории");
        setLoading(false);
      });
  }, []);

  const handleClick = (id) => {
    // Передаем числовой ID, который ожидает бэкенд в параметре category_id
    navigate(`/search?category_id=${id}`);
  };

  if (loading) return <div style={styles.box}>Загрузка...</div>;

  return (
    <div style={styles.box}>
      <h3 style={styles.title}>Категории</h3>
      {categories.map((category) => (
        <div
          key={category.id}
          style={styles.item}
          onClick={() => handleClick(category.id)}
        >
          {category.name}
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
    height: "fit-content",
    boxShadow: "0 2px 8px rgba(0,0,0,0.05)"
  },
  title: {
    marginTop: 0,
    marginBottom: 15,
    fontSize: 18,
    borderBottom: "2px solid #05386B",
    paddingBottom: 8
  },
  item: {
    padding: "12px 0",
    borderBottom: "1px solid #eee",
    cursor: "pointer",
    fontSize: 15,
    transition: "color 0.2s",
    // Эффект при наведении можно добавить через CSS-класс, 
    // либо оставить так для простоты
  }
};

export default Categories;