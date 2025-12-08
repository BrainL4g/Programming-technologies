import { createContext, useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

const FavoriteContext = createContext();

export function FavoriteProvider({ children }) {
  const [favorites, setFavorites] = useState([]);
  const { isAuth } = useAuth();
  const navigate = useNavigate();

  const isFavorite = (id) => favorites.some((p) => p.id === id);

  const toggleFavorite = (product) => {
    if (!isAuth) {
      navigate("/login");
      return;
    }

    setFavorites((prev) =>
      isFavorite(product.id)
        ? prev.filter((p) => p.id !== product.id)
        : [...prev, product]
    );
  };

  return (
    <FavoriteContext.Provider value={{ favorites, toggleFavorite, isFavorite }}>
      {children}
    </FavoriteContext.Provider>
  );
}

export const useFavorites = () => useContext(FavoriteContext);
