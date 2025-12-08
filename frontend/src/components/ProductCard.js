import React from "react";
import { useNavigate } from "react-router-dom";
import { useFavorites } from "../context/FavoriteContext";
import { useAuth } from "../context/AuthContext";

export default function ProductCard({ product, showTracking }) {
  const navigate = useNavigate();
  const { isFavorite, toggleFavorite } = useFavorites();
  const { isAuth } = useAuth();

  const fav = isFavorite(product.id);

  return (
    <div
      style={styles.card}
      onClick={() => navigate(`/product/${product.id}`)}
    >
      <img src={product.image} alt={product.title} style={styles.image} />

      <h4 style={styles.title}>{product.title}</h4>
      <div style={styles.price}>{product.price} ₽</div>

      <button
        style={fav ? styles.removeBtn : styles.addBtn}
        onClick={(e) => {
          e.stopPropagation();
          toggleFavorite(product); // редирект в контексте
        }}
      >
        {fav ? "Удалить из избранного" : "В избранное"}
      </button>

      {fav && showTracking && (
        <button
          style={styles.trackBtn}
          onClick={(e) => {
            e.stopPropagation();
            alert("Вы начали отслеживать товар!");
          }}
        >
          Отслеживать
        </button>
      )}
    </div>
  );
}

const styles = {
  /* твои стили сохранены */
  card: {
    width: 220,
    background: "#fff",
    borderRadius: 8,
    padding: 15,
    cursor: "pointer",
    textAlign: "center",
    border: "1px solid #eee",
  },
  image: {
    width: "100%",
    height: 140,
    objectFit: "cover",
    borderRadius: 6,
  },
  title: { fontSize: 16, margin: "10px 0" },
  price: { fontWeight: "bold", fontSize: 18, marginBottom: 8 },

  addBtn: {
    width: "100%",
    background: "#05386B",
    color: "#fff",
    border: "none",
    padding: "8px 0",
    borderRadius: 6,
    cursor: "pointer",
    marginTop: 10,
  },

  removeBtn: {
    width: "100%",
    background: "#b80404",
    color: "#fff",
    border: "none",
    padding: "8px 0",
    borderRadius: 6,
    cursor: "pointer",
    marginTop: 10,
  },

  trackBtn: {
    width: "100%",
    background: "#ffb300",
    color: "#000",
    border: "none",
    padding: "8px 0",
    borderRadius: 6,
    cursor: "pointer",
    marginTop: 10,
    fontWeight: "bold",
  },
};
