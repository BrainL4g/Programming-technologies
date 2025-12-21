import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";
import PriceChart from "../components/PriceChart";
import apiClient from "../api/apiClient";
import { useFavorites } from "../context/FavoriteContext";

const BASE_URL = "http://127.0.0.1:8000";

export default function ProductPage() {
  const { id } = useParams();
  const { toggleFavorite, isFavorite } = useFavorites(); 
  const [product, setProduct] = useState(null);
  const [priceHistory, setPriceHistory] = useState(null);
  const [stores, setStores] = useState({});
  const [loading, setLoading] = useState(true);

  const [selectedImage, setSelectedImage] = useState(0);
  const [activeTab, setActiveTab] = useState('description');
  const isInFavorite = product ? isFavorite(product.id) : false;

  useEffect(() => {
    const fetchAllData = async () => {
      try {
        setLoading(true);
        
        // 1. Загружаем основные данные товара
        const productData = await apiClient.get(`/products/${id}`);
        setProduct(productData);

        // 2. Загружаем историю цен
        const historyData = await apiClient.get(`/products/${id}/prices`);
        setPriceHistory(historyData);

        // 3. Загружаем данные о магазинах для всех предложений
        if (productData.offers && productData.offers.length > 0) {
          const storeIds = [...new Set(productData.offers.map(o => o.store_id))];
          
          // Делаем запросы ко всем уникальным магазинам одновременно
          const storeRequests = storeIds.map(storeId => 
            apiClient.get(`/stores/${storeId}`).catch(() => ({ id: storeId, name: "Неизвестный магазин" }))
          );
          
          const storesData = await Promise.all(storeRequests);
          
          // Создаем карту для быстрого поиска: { "uuid": "Название" }
          const storesMap = {};
          storesData.forEach(s => {
            storesMap[s.id] = s.name;
          });
          setStores(storesMap);
        }
      } catch (error) {
        console.error("Ошибка при загрузке данных:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchAllData();
    console.log(stores.dictionary);

  }, [id]);

  if (loading || !product) {
    return <div style={{ textAlign: 'center', padding: '100px' }}>Загрузка...</div>;
  }

  const sortedOffers = product.offers ? [...product.offers].sort((a, b) => a.price - b.price) : [];
  const lowestOffer = sortedOffers.find(o => o.available);

  const specsArray = product.specifications 
    ? Object.entries(product.specifications).map(([key, value]) => ({
        name: key.charAt(0).toUpperCase() + key.slice(1), 
        value: value.toString()
      }))
    : [];

  return (
    <>
      <Header />

      <main style={styles.main}>
        <div style={styles.container}>
          <div style={styles.breadcrumbs}>
            <span style={styles.breadcrumb}>Главная</span>
            <span style={styles.separator}>›</span>
            <span style={styles.breadcrumb}>{product.category?.name || "Каталог"}</span>
            <span style={styles.separator}>›</span>
            <span style={styles.breadcrumbActive}>{product.name}</span>
          </div>

          <div style={styles.topSection}>
            <div style={styles.photoSection}>
              <div style={styles.mainImage}>
                {product.images?.length > 0 ? (
                  <img
                    src={`${BASE_URL}/uploads/${product.images[selectedImage].id}`}
                    alt={product.name}
                    style={styles.mainImageImg}
                  />
                ) : (
                  <div style={{ padding: '50px' }}>Нет фото</div>
                )}
              </div>

              <div style={styles.thumbnails}>
                {product.images?.map((imgObj, index) => (
                  <div
                    key={imgObj.id}
                    style={{
                      ...styles.thumbnail,
                      border: selectedImage === index ? '2px solid #05386B' : '1px solid #ddd',
                    }}
                    onClick={() => setSelectedImage(index)}
                  >
                    <img 
                      src={`${BASE_URL}/uploads/${imgObj.id}`} 
                      alt={`Вид ${index + 1}`} 
                      style={styles.thumbnailImg} 
                    />
                  </div>
                ))}
              </div>
            </div>

            <div style={styles.priceSection}>
              <h1 style={styles.title}>{product.name}</h1>

              <div style={styles.rating}>
                <div style={styles.stars}>★★★★☆</div>
                <span style={styles.ratingText}>4.0</span>
              </div>

              <div style={styles.priceHeader}>
                <h3 style={styles.priceTitle}>Предложения магазинов</h3>
                {lowestOffer && (
                  <div style={styles.lowestPrice}>
                    От <span style={styles.lowestPriceValue}>{Math.round(lowestOffer.price).toLocaleString('ru-RU')} ₽</span>
                  </div>
                )}
              </div>

              <div style={styles.priceList}>
              {sortedOffers.map((offer) => (
                <div
                  key={offer.id}
                  style={{
                    ...styles.priceItem,
                    background: 'white', // Убрали выделение цветом
                    border: '1px solid #eee', // Убрали синюю обводку
                  }}
                >
                  <div style={styles.priceRow}>
                    <div style={styles.shopInfo}>
                      <div style={styles.shopName}>
                        {stores[offer.store_id] || "Загрузка магазина..."}
                      </div>
                      <div style={styles.delivery}>
                        {offer.available ? "В наличии" : "Под заказ"}
                      </div>
                    </div>
                    <div style={styles.priceInfo}>
                      <div style={styles.priceValue}>
                        {Math.round(offer.price).toLocaleString('ru-RU')} ₽
                      </div>
                      <a href={offer.url} target="_blank" rel="noopener noreferrer">
                        <button style={styles.buyButton}>Перейти</button>
                      </a>
                    </div>
                  </div>
                </div>
              ))}
            </div>

              <div style={styles.priceActions}>
                <button 
                  style={{
                    ...styles.favoriteButton,
                    background: isInFavorite ? '#ffdada' : '#fff3cd', // Меняем цвет если в избранном
                    color: isInFavorite ? '#d32f2f' : '#856404',
                    borderColor: isInFavorite ? '#ffccd2' : '#ffeaa7'
                  }}
                  onClick={() => toggleFavorite(product)}
                >
                  {isInFavorite ? 'В избранном' : 'В избранное'}
                </button>
              </div>
            </div>
          </div>

          <div style={styles.bottomSection}>
            <div style={styles.tabs}>
              <button
                style={activeTab === 'description' ? styles.tabActive : styles.tab}
                onClick={() => setActiveTab('description')}
              >
                Описание
              </button>
              <button
                style={activeTab === 'specs' ? styles.tabActive : styles.tab}
                onClick={() => setActiveTab('specs')}
              >
                Характеристики
              </button>
            </div>

            <div style={styles.tabContent}>
              {activeTab === 'description' && (
                <div style={styles.descriptionContent}>
                  <h3 style={styles.contentTitle}>Описание товара</h3>
                  <p style={styles.descriptionText}>{product.description}</p>
                  
                  <h4 style={styles.subtitle}>Бренд: {product.brand}</h4>
                  <p style={styles.descriptionText}>Категория: {product.category?.name}</p>
                </div>
              )}

              {activeTab === 'specs' && (
                <div style={styles.specsContent}>
                  <h3 style={styles.contentTitle}>Технические характеристики</h3>
                  <div style={styles.specsTable}>
                    {specsArray.map((spec, index) => (
                      <div
                        key={index}
                        style={{
                          ...styles.specRow,
                          background: index % 2 === 0 ? '#f9f9f9' : 'white',
                        }}
                      >
                        <div style={styles.specName}>{spec.name}</div>
                        <div style={styles.specValue}>{spec.value}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

            {priceHistory && (
                <div style={styles.chartSection}>
                  <PriceChart 
                    productName={product.name}
                    // Передаем историю средних цен
                    averageHistory={priceHistory.price_history} 
                    // Передаем список предложений с названиями магазинов для селектора
                    offers={product.offers.map(o => ({
                      id: o.id,
                      storeName: stores[o.store_id] || "Магазин"
                    }))}
                  />
                </div>
              )}
        </div>
      </main>

      <Footer />
    </>
  );
}

const styles = {
  main: {
    background: '#f5f5f5',
    minHeight: 'calc(100vh - 160px)',
  },
  container: {
    width: '100%',
    maxWidth: 1300,
    margin: '0 auto',
    padding: '20px',
  },
  breadcrumbs: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    marginBottom: '20px',
    fontSize: '14px',
    color: '#666',
    flexWrap: 'wrap',
  },
  breadcrumb: {
    cursor: 'pointer',
    padding: '2px 4px',
  },
  breadcrumbActive: {
    color: '#05386B',
    fontWeight: '500',
  },
  separator: {
    color: '#999',
  },
  topSection: {
    display: 'flex',
    background: 'white',
    borderRadius: '8px',
    padding: '20px',
    marginBottom: '20px',
    gap: '30px',
    flexWrap: 'wrap',
  },
  photoSection: {
    flex: '1',
    minWidth: '300px',
  },
  mainImage: {
    marginBottom: '10px',
    border: '1px solid #eee',
    borderRadius: '8px',
    overflow: 'hidden',
    textAlign: 'center',
    height: '400px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  },
  mainImageImg: {
    maxWidth: '100%',
    maxHeight: '100%',
    objectFit: 'contain'
  },
  thumbnails: {
    display: 'flex',
    gap: '10px',
    flexWrap: 'wrap',
  },
  thumbnail: {
    width: '80px',
    height: '80px',
    borderRadius: '6px',
    overflow: 'hidden',
    cursor: 'pointer',
    border: '1px solid #ddd',
  },
  thumbnailImg: {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
  },
  priceSection: {
    flex: '1',
    minWidth: '300px',
  },
  title: {
    fontSize: '24px',
    fontWeight: '600',
    color: '#333',
    marginBottom: '10px',
    lineHeight: '1.3',
  },
  rating: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    marginBottom: '20px',
  },
  stars: {
    color: '#ffb300',
    fontSize: '18px',
  },
  ratingText: {
    fontSize: '14px',
    color: '#666',
  },
  priceHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '15px',
    paddingBottom: '10px',
    borderBottom: '1px solid #eee',
  },
  priceTitle: {
    fontSize: '18px',
    fontWeight: '600',
    color: '#333',
    margin: 0,
  },
  lowestPrice: {
    fontSize: '14px',
    color: '#666',
  },
  lowestPriceValue: {
    fontSize: '20px',
    fontWeight: 'bold',
    color: '#05386B',
  },
  priceList: {
    maxHeight: '400px',
    overflowY: 'auto',
    marginBottom: '15px',
  },
  priceItem: {
    borderRadius: '6px',
    padding: '12px',
    marginBottom: '8px',
  },
  priceRow: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  shopInfo: {
    flex: '1',
  },
  shopName: {
    fontSize: '15px',
    fontWeight: '500',
    color: '#333',
    marginBottom: '4px',
  },
  delivery: {
    fontSize: '12px',
    color: '#666',
  },
  outOfStock: {
    color: '#d32f2f',
    fontWeight: '500',
  },
  priceInfo: {
    textAlign: 'right',
  },
  priceValue: {
    fontSize: '18px',
    fontWeight: '600',
    color: '#05386B',
    marginBottom: '6px',
  },
  buyButton: {
    padding: '6px 12px',
    background: '#05386B',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '13px',
    fontWeight: '500',
  },
  priceActions: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
    marginTop: '15px',
  },
  favoriteButton: {
    padding: '10px',
    background: '#fff3cd',
    color: '#856404',
    border: '1px solid #ffeaa7',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '500',
  },
  bottomSection: {
    background: 'white',
    borderRadius: '8px',
    padding: '20px',
    marginBottom: '20px',
  },
  tabs: {
    display: 'flex',
    borderBottom: '1px solid #eee',
    marginBottom: '20px',
    flexWrap: 'wrap',
  },
  tab: {
    padding: '12px 20px',
    background: 'none',
    border: 'none',
    borderBottom: '2px solid transparent',
    cursor: 'pointer',
    fontSize: '15px',
    color: '#666',
  },
  tabActive: {
    padding: '12px 20px',
    background: 'none',
    border: 'none',
    borderBottom: '2px solid #05386B',
    cursor: 'pointer',
    fontSize: '15px',
    color: '#05386B',
    fontWeight: '500',
  },
  tabContent: {
    padding: '10px 0',
  },
  contentTitle: {
    fontSize: '18px',
    fontWeight: '600',
    color: '#333',
    marginBottom: '15px',
  },
  descriptionContent: {
    marginBottom: '20px',
  },
  descriptionText: {
    fontSize: '14px',
    lineHeight: '1.6',
    color: '#444',
    marginBottom: '20px',
  },
  subtitle: {
    fontSize: '16px',
    fontWeight: '600',
    color: '#333',
    marginBottom: '10px',
  },
  specsContent: {
    marginTop: '10px',
  },
  specsTable: {
    border: '1px solid #eee',
    borderRadius: '6px',
    overflow: 'hidden',
  },
  specRow: {
    display: 'flex',
    padding: '12px 15px',
  },
  specName: {
    flex: '1',
    fontSize: '14px',
    color: '#666',
  },
  specValue: {
    flex: '2',
    fontSize: '14px',
    fontWeight: '500',
    color: '#333',
  },
  chartSection: {
    background: 'white',
    borderRadius: '8px',
    padding: '20px',
    marginTop: '20px',
  },
};