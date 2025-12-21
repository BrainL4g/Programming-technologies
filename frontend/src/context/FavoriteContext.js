import { createContext, useState, useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./AuthContext";
import apiClient from "../api/apiClient";

const FavoriteContext = createContext();

export function FavoriteProvider({ children }) {
  const [favorites, setFavorites] = useState([]);
  const [trackingIds, setTrackingIds] = useState([]); // Состояние для отслеживания (фронтенд-онли)
  const { isAuth } = useAuth();
  const navigate = useNavigate();

  const toggleTracking = (productId) => {
  setTrackingIds((prev) =>
    prev.includes(productId)
      ? prev.filter((id) => id !== productId)
      : [...prev, productId]
    );
  };
    
  const isTracking = (productId) => trackingIds.includes(productId);

  useEffect(() => {
    const fetchFullFavorites = async () => {
      if (!isAuth) {
        setFavorites([]);
        return;
      }

      try {
        // 1. Получаем список избранного (допустим, там [ {product_id: 1}, {product_id: 2} ])
        const favLinks = await apiClient.get('/favorites');

        // 2. Создаем массив промисов для каждого товара
        // Предполагаем, что структура ответа API: [{ product_id: ... }] или просто список объектов с id
        const detailRequests = favLinks.map(item => 
          apiClient.get(`/products/${item.product_id || item.id}`)
            .catch(err => {
              console.error(`Ошибка загрузки товара ${item.id}:`, err);
              return null; // Возвращаем null, чтобы Promise.all не упал целиком
            })
        );

        // 3. Дожидаемся завершения всех запросов
        const fullProducts = await Promise.all(detailRequests);

        // 4. Фильтруем неудачные запросы и сохраняем в стейт
        setFavorites(fullProducts.filter(p => p !== null));
        
      } catch (err) {
        console.error("Ошибка загрузки списка избранного:", err);
      }
    };

    fetchFullFavorites();
  }, [isAuth]);

  const isFavorite = (id) => favorites.some((p) => p.id === id);

  const toggleFavorite = async (product) => {
    if (!isAuth) {
      navigate("/login");
      return;
    }

    const alreadyFavorite = isFavorite(product.id);

    try {
      if (alreadyFavorite) {
        // Удаляем из избранного
        await apiClient.delete(`/favorites/${product.id}`);
        setFavorites((prev) => prev.filter((p) => p.id !== product.id));
      } else {
        // Добавляем в избранное
        await apiClient.post(`/favorites/${product.id}`, { product_id: product.id });
        setFavorites((prev) => [...prev, product]);
      }
    } catch (error) {
      console.error("Ошибка при обновлении избранного:", error);
      alert("не удалось обновить список избранного");
    }
  };

  return (
    <FavoriteContext.Provider value={{ favorites, toggleFavorite, isFavorite, 
    toggleTracking, isTracking }}>
      {children}
    </FavoriteContext.Provider>
  );
}

export const useFavorites = () => useContext(FavoriteContext);