import React, { useState, useEffect } from 'react';
import Header from '../components/headers/HeaderGuest';
import Footer from '../components/Footer';
import FilterPanel from '../components/FilterPanel';
import ProductCard from '../components/ProductCard';
import Pagination from '../components/Pagination';
import { products } from '../mocks/products';

function SearchResultsPage() {
  const [sortOption, setSortOption] = useState('popular');
  const [priceRange, setPriceRange] = useState({ min: '', max: '' });
  const [selectedBrands, setSelectedBrands] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState(products);

  // Функция для переключения бренда в фильтре
  const handleBrandToggle = (brand) => {
    if (selectedBrands.includes(brand)) {
      setSelectedBrands(selectedBrands.filter(b => b !== brand));
    } else {
      setSelectedBrands([...selectedBrands, brand]);
    }
  };

  // Функция для изменения цены
  const handlePriceChange = (field, value) => {
    setPriceRange({
      ...priceRange,
      [field]: value
    });
  };

  // Функция для сброса фильтров
  const handleResetFilters = () => {
    setSortOption('popular');
    setPriceRange({ min: '', max: '' });
    setSelectedBrands([]);
  };

  // Применение фильтров
  useEffect(() => {
    let result = [...products];

    // Фильтрация по цене
    if (priceRange.min !== '') {
      result = result.filter(product => product.price >= Number(priceRange.min));
    }
    if (priceRange.max !== '') {
      result = result.filter(product => product.price <= Number(priceRange.max));
    }

    // Сортировка
    switch (sortOption) {
      case 'price_desc':
        result.sort((a, b) => b.price - a.price);
        break;
      case 'price_asc':
        result.sort((a, b) => a.price - b.price);
        break;
      case 'popular':
        // Для демонстрации сортируем по ID (предполагая, что больший ID = новее товар)
        result.sort((a, b) => b.id - a.id);
        break;
      default:
        break;
    }

    setFilteredProducts(result);
  }, [sortOption, priceRange]);

  // Разделение товаров на ряды по 3
  const rows = [];
  for (let i = 0; i < filteredProducts.length; i += 3) {
    rows.push(filteredProducts.slice(i, i + 3));
  }

  return (
    <>
      <Header />

      <main style={styles.main}>
        <div style={styles.container}>
          <div style={styles.content}>
            <div style={styles.header}>
              <h1 style={styles.title}>Каталог</h1>
              <div style={styles.resultsCount}>
                Найдено товаров: <strong>{filteredProducts.length}</strong>
              </div>
            </div>

            <div style={styles.body}>
              {/* Левая панель фильтров */}
              <FilterPanel
                sortOption={sortOption}
                onSortChange={setSortOption}
                priceRange={priceRange}
                onPriceChange={handlePriceChange}
                selectedBrands={selectedBrands}
                onBrandToggle={handleBrandToggle}
                onResetFilters={handleResetFilters}
              />

              {/* Правая часть с товарами */}
              <div style={styles.productsSection}>
                <div style={styles.productsContainer}>
                  {/* Отображение товаров по 3 в ряду */}
                  {rows.map((row, rowIndex) => (
                    <div key={rowIndex} style={styles.row}>
                      {row.map(product => (
                        <ProductCard key={product.id} product={product} />
                      ))}
                      {/* Добавляем пустые места если в ряду меньше 3 товаров */}
                      {row.length < 3 &&
                        Array.from({ length: 3 - row.length }).map((_, index) => (
                          <div key={`empty-${rowIndex}-${index}`} style={styles.emptyCard} />
                        ))
                      }
                    </div>
                  ))}

                  {filteredProducts.length === 0 && (
                    <div style={styles.noResults}>
                      <h3>Товары не найдены</h3>
                      <p>Попробуйте изменить параметры фильтрации</p>
                      <button
                        onClick={handleResetFilters}
                        style={styles.resetFiltersBtn}
                      >
                        Сбросить фильтры
                      </button>
                    </div>
                  )}
                </div>

                {/* Пагинация (только если есть товары) */}
                {filteredProducts.length > 0 && <Pagination />}
              </div>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </>
  );
}

const styles = {
  main: {
    minHeight: '70vh',
    background: '#f5f5f5',
  },
  container: {
    width: '100%',
    maxWidth: 1300,
    margin: '0 auto',
    padding: '20px',
  },
  content: {
    background: '#fff',
    borderRadius: 8,
    padding: 25,
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 30,
    paddingBottom: 20,
    borderBottom: '1px solid #eee',
  },
  title: {
    fontSize: 28,
    fontWeight: 600,
    color: '#333',
    margin: 0,
  },
  resultsCount: {
    fontSize: 16,
    color: '#666',
  },
  body: {
    display: 'flex',
  },
  productsSection: {
    flex: 1,
  },
  productsContainer: {
    marginBottom: 30,
  },
  row: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: 20,
    gap: 10,
  },
  emptyCard: {
    width: 200,
    margin: 10,
    visibility: 'hidden',
  },
  noResults: {
    textAlign: 'center',
    padding: '60px 20px',
    color: '#666',
  },
  resetFiltersBtn: {
    padding: '12px 24px',
    background: '#1976d2',
    color: 'white',
    border: 'none',
    borderRadius: 6,
    cursor: 'pointer',
    fontSize: 15,
    marginTop: 15,
  },
};

export default SearchResultsPage;