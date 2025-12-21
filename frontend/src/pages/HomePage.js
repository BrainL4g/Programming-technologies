import React from 'react';
import Header from '../components/Header';
import Banner from '../components/Banner';
import Categories from '../components/Categories';
import RecommendedSlider from '../components/RecommendedSlider';
import ProductList from '../components/ProductList';
import Footer from '../components/Footer';
import { useState, useEffect } from "react";
import apiClient from "../api/apiClient";

function HomePage() {
  const [popularProducts, setPopularProducts] = useState([]);
  const [recommendedProducts, setRecommendedProducts] = useState([]);

  useEffect(() => {
    // Загружаем популярные
    apiClient.get('/products')
      .then(data => setPopularProducts(data))
      .catch(err => console.error(err));

    // Загружаем рекомендации
    apiClient.get('/products')
      .then(data => setRecommendedProducts(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <>
      <Header />
      <Banner />
      <main style={styles.main}>
        <Categories />
        <div style={styles.rightColumn}>
          <RecommendedSlider products={recommendedProducts} />
          <ProductList products={popularProducts} title="Популярные товары" />
        </div>
      </main>
      <Footer />
    </>
  );
}

 const styles = {
  main: {
    display: 'flex',
    width: '100%',
    maxWidth: 1200,
    margin: '20px auto',
    gap: 20
  },
  rightColumn: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    gap: 20
  }
}; 

export default HomePage;
