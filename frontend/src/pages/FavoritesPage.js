import React from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import { useFavorites } from "../context/FavoriteContext";
import ProductCard from "../components/ProductCard";

export default function FavoritesPage() {
  const { favorites } = useFavorites();

  return (
    <>
      <Header />

      <main style={styles.main}>
        <h2 style={styles.title}>Избранное</h2>

        {favorites.length === 0 ? (
          <h3 style={{ marginTop: 20 }}>Нет избранных товаров</h3>
        ) : (
          <div style={styles.grid}>
            {favorites.map((p) => (
              <ProductCard key={p.id} product={p} showTracking={true} />
            ))}
          </div>
        )}
      </main>

      <Footer />
    </>
  );
}

const styles = {
  main: {
    maxWidth: 1200,
    margin: "20px auto",
    padding: "0 20px",
  },
  title: {
    fontSize: 32,
    fontWeight: "bold",
    marginBottom: 20,
  },
  grid: {
    display: "flex",
    flexWrap: "wrap",
    gap: 20,
  },
};
