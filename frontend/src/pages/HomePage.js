import React from 'react';
import Header from '../components/Header';
import Banner from '../components/Banner';
import Categories from '../components/Categories';
import RecommendedSlider from '../components/RecommendedSlider';
import ProductList from '../components/ProductList';
import Footer from '../components/Footer';
import { products } from "../mocks/products";
import { recommended } from "../mocks/recommended";

function HomePage() {
  return (
    <>
      <Header />
      <Banner />

      <main style={styles.main}>
        <Categories />

        <div style={styles.rightColumn}>
          <RecommendedSlider products={recommended} />
          <ProductList products={products} title="Популярные товары" />
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
