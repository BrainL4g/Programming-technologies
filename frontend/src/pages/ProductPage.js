import React, { useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";
import PriceChart from "../components/PriceChart";
import { products } from "../mocks/products";
import { recommended } from "../mocks/recommended";

export default function ProductPage() {
  const { id } = useParams();
  const all = [...products, ...recommended];
  const product = all.find(p => p.id === Number(id));

  const [selectedImage, setSelectedImage] = useState(0);
  const [activeTab, setActiveTab] = useState('description');

  if (!product) {
    return (
      <>
        <Header />
        <div style={{ padding: 20 }}>
          <h2>Товар не найден</h2>
        </div>
        <Footer />
      </>
    );
  }

  // Расширенные данные товара
  const productDetails = {
    ...product,
    description: "Смартфон Samsung Galaxy A54 5G — это смартфон, который сочетает в себе стильный дизайн, мощные характеристики и доступную цену. Смартфон оснащен 6.4-дюймовым Super AMOLED экраном с частотой обновления 120 Гц, что обеспечивает плавную анимацию и комфортный просмотр контента. Основная тройная камера 50 Мп позволяет делать качественные фото и видео в любых условиях.",
    specifications: [
      { name: "Экран", value: "6.4\", Super AMOLED, 120 Гц" },
      { name: "Процессор", value: "Exynos 1380" },
      { name: "Оперативная память", value: "8 ГБ" },
      { name: "Встроенная память", value: "256 ГБ" },
      { name: "Основная камера", value: "50 Мп + 12 Мп + 5 Мп" },
      { name: "Фронтальная камера", value: "32 Мп" },
      { name: "Аккумулятор", value: "5000 мАч" },
      { name: "Зарядка", value: "25 Вт" },
      { name: "ОС", value: "Android 13 с One UI 5.1" },
      { name: "Защита", value: "IP67" },
      { name: "Вес", value: "202 г" },
      { name: "Цвет", value: "Черный" },
    ],
    images: [
      "https://via.placeholder.com/400x400/05386B/ffffff?text=Фото+1",
      "https://via.placeholder.com/400x400/05386B/ffffff?text=Фото+2",
      "https://via.placeholder.com/400x400/05386B/ffffff?text=Фото+3",
      "https://via.placeholder.com/400x400/05386B/ffffff?text=Фото+4",
    ],
    prices: [
      { shop: "DNS", price: 29990, delivery: "Бесплатно", inStock: true },
      { shop: "М.Видео", price: 30500, delivery: "Бесплатно", inStock: true },
      { shop: "Эльдорадо", price: 29500, delivery: "Бесплатно", inStock: true },
      { shop: "Ситилинк", price: 30200, delivery: "+ 250 ₽", inStock: true },
      { shop: "OZON", price: 29800, delivery: "Бесплатно", inStock: false },
    ],
    rating: 4.5,
    reviews: 128
  };

  // Сортировка цен по возрастанию
  const sortedPrices = [...productDetails.prices].sort((a, b) => a.price - b.price);
  const lowestPrice = sortedPrices.find(p => p.inStock);

  return (
    <>
      <Header />

      <main style={styles.main}>
        <div style={styles.container}>
          {/* Хлебные крошки */}
          <div style={styles.breadcrumbs}>
            <span style={styles.breadcrumb}>Главная</span>
            <span style={styles.separator}>›</span>
            <span style={styles.breadcrumb}>Смартфоны</span>
            <span style={styles.separator}>›</span>
            <span style={styles.breadcrumbActive}>{product.title}</span>
          </div>

          {/* Верхний блок с фото и ценами */}
          <div style={styles.topSection}>
            {/* Левая колонка: Фото товара */}
            <div style={styles.photoSection}>
              <div style={styles.mainImage}>
                <img
                  src={productDetails.images[selectedImage]}
                  alt={product.title}
                  style={styles.mainImageImg}
                />
              </div>

              <div style={styles.thumbnails}>
                {productDetails.images.map((image, index) => (
                  <div
                    key={index}
                    style={{
                      ...styles.thumbnail,
                      border: selectedImage === index ? '2px solid #05386B' : '1px solid #ddd',
                    }}
                    onClick={() => setSelectedImage(index)}
                  >
                    <img src={image} alt={`Вид ${index + 1}`} style={styles.thumbnailImg} />
                  </div>
                ))}
              </div>
            </div>

            {/* Правая колонка: Цены в магазинах */}
            <div style={styles.priceSection}>
              <h1 style={styles.title}>{product.title}</h1>

              <div style={styles.rating}>
                <div style={styles.stars}>
                  {'★'.repeat(Math.floor(productDetails.rating))}
                  {'☆'.repeat(5 - Math.floor(productDetails.rating))}
                </div>
                <span style={styles.ratingText}>{productDetails.rating} ({productDetails.reviews} отзывов)</span>
              </div>

              <div style={styles.priceHeader}>
                <h3 style={styles.priceTitle}>Цены в магазинах</h3>
                {lowestPrice && (
                  <div style={styles.lowestPrice}>
                    От <span style={styles.lowestPriceValue}>{lowestPrice.price.toLocaleString('ru-RU')} ₽</span>
                  </div>
                )}
              </div>

              <div style={styles.priceList}>
                {sortedPrices.map((priceInfo, index) => (
                  <div
                    key={index}
                    style={{
                      ...styles.priceItem,
                      background: priceInfo.shop === lowestPrice?.shop ? '#f0f7ff' : 'white',
                      border: priceInfo.shop === lowestPrice?.shop ? '2px solid #05386B' : '1px solid #eee',
                    }}
                  >
                    <div style={styles.priceRow}>
                      <div style={styles.shopInfo}>
                        <div style={styles.shopName}>{priceInfo.shop}</div>
                        <div style={styles.delivery}>
                          {priceInfo.delivery}
                          {!priceInfo.inStock && <span style={styles.outOfStock}> — Нет в наличии</span>}
                        </div>
                      </div>
                      <div style={styles.priceInfo}>
                        <div style={styles.priceValue}>
                          {priceInfo.price.toLocaleString('ru-RU')} ₽
                        </div>
                        {priceInfo.inStock ? (
                          <button style={styles.buyButton}>
                            Купить
                          </button>
                        ) : (
                          <button style={styles.notifyButton}>
                            Уведомить
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div style={styles.priceActions}>
                <button style={styles.favoriteButton}>
                  ★ В избранное
                </button>
              </div>
            </div>
          </div>

          {/* Нижний блок: Описание и характеристики */}
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
              <button
                style={activeTab === 'reviews' ? styles.tabActive : styles.tab}
                onClick={() => setActiveTab('reviews')}
              >
                Отзывы ({productDetails.reviews})
              </button>
            </div>

            <div style={styles.tabContent}>
              {activeTab === 'description' && (
                <div style={styles.descriptionContent}>
                  <h3 style={styles.contentTitle}>Описание товара</h3>
                  <p style={styles.descriptionText}>{productDetails.description}</p>

                  <h4 style={styles.subtitle}>Ключевые особенности:</h4>
                  <ul style={styles.featureList}>
                    <li style={styles.featureItem}>Поддержка 5G для быстрого интернета</li>
                    <li style={styles.featureItem}>Стереодинамики с качественным звуком</li>
                    <li style={styles.featureItem}>NFC для бесконтактной оплаты</li>
                    <li style={styles.featureItem}>Сканер отпечатков пальцев в экране</li>
                    <li style={styles.featureItem}>Защита от воды и пыли IP67</li>
                    <li style={styles.featureItem}>Поддержка быстрой зарядки 25 Вт</li>
                  </ul>
                </div>
              )}

              {activeTab === 'specs' && (
                <div style={styles.specsContent}>
                  <h3 style={styles.contentTitle}>Технические характеристики</h3>
                  <div style={styles.specsTable}>
                    {productDetails.specifications.map((spec, index) => (
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

              {activeTab === 'reviews' && (
                <div style={styles.reviewsContent}>
                  <h3 style={styles.contentTitle}>Выжимка из отзовов</h3>
                  <div style={styles.reviewStats}>
                    <div style={styles.ratingSummary}>
                      <div style={styles.ratingNumber}>{productDetails.rating}</div>
                      <div style={styles.ratingStars}>
                        {'★'.repeat(Math.floor(productDetails.rating))}
                        {'☆'.repeat(5 - Math.floor(productDetails.rating))}
                      </div>
                      <div style={styles.ratingCount}>{productDetails.reviews} отзывов</div>
                    </div>
                  </div>

                </div>
              )}
            </div>
          </div>

          {/* График изменения цен */}
          <div style={styles.chartSection}>
            <PriceChart productId={product.id} productName={product.title} />
          </div>
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
    ':hover': {
      color: '#05386B',
    }
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
  },
  mainImageImg: {
    width: '100%',
    maxWidth: '500px',
    height: 'auto',
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
  notifyButton: {
    padding: '6px 12px',
    background: '#ff9800',
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
  compareButton: {
    padding: '10px',
    background: '#fff',
    color: '#05386B',
    border: '1px solid #05386B',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '500',
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
  featureList: {
    paddingLeft: '20px',
    marginBottom: '20px',
  },
  featureItem: {
    fontSize: '14px',
    color: '#444',
    marginBottom: '8px',
    lineHeight: '1.5',
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
  reviewsContent: {
    marginTop: '10px',
  },
  reviewStats: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: '20px',
    padding: '15px',
    background: '#f9f9f9',
    borderRadius: '6px',
  },
  ratingSummary: {
    textAlign: 'center',
    flex: '1',
  },
  ratingNumber: {
    fontSize: '36px',
    fontWeight: 'bold',
    color: '#333',
  },
  ratingStars: {
    fontSize: '18px',
    color: '#ffb300',
    margin: '5px 0',
  },
  ratingCount: {
    fontSize: '14px',
    color: '#666',
  },
  reviewsList: {
    marginTop: '20px',
  },
  reviewItem: {
    borderBottom: '1px solid #eee',
    padding: '15px 0',
  },
  reviewHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '5px',
  },
  reviewAuthor: {
    fontSize: '14px',
    fontWeight: '500',
    color: '#333',
  },
  reviewDate: {
    fontSize: '12px',
    color: '#666',
  },
  reviewRating: {
    fontSize: '14px',
    color: '#ffb300',
    marginBottom: '5px',
  },
  reviewText: {
    fontSize: '14px',
    color: '#444',
    lineHeight: '1.5',
  },
  chartSection: {
    marginTop: '20px',
  },
};