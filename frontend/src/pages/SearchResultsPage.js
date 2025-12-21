import React, { useState, useEffect, useCallback, useMemo } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import FilterPanel from '../components/FilterPanel';
import ProductCard from '../components/ProductCard';
import Pagination from '../components/Pagination';
import { productService } from '../api/productService';
import apiClient from '../api/apiClient';
import { useSearchParams } from 'react-router-dom';

function SearchResultsPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const categoryId = searchParams.get('category_id');

  const [sortOption, setSortOption] = useState('popular');
  const [priceRange, setPriceRange] = useState({ min: '', max: '' });
  const [selectedBrands, setSelectedBrands] = useState([]);
  const [selectedSpecs, setSelectedSpecs] = useState({});
  
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 12;

  useEffect(() => {
    apiClient.get('/categories/')
      .then(res => setCategories(res))
      .catch(err => console.error("Ошибка категорий", err));
  }, []);

  const fetchProducts = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const sortMap = {
        'price_asc': { sort_by: 'price', sort_order: 'asc' },
        'price_desc': { sort_by: 'price', sort_order: 'desc' },
        'popular': { sort_by: 'id', sort_order: 'desc' }
      };
      const { sort_by, sort_order } = sortMap[sortOption] || sortMap['popular'];

      const params = {
        skip: (currentPage - 1) * itemsPerPage,
        limit: itemsPerPage,
        category_id: categoryId || null,
        sort_by,
        sort_order,
      };

      const data = await productService.getProducts(params);
      setProducts(data);
    } catch (err) {
      setError("Не удалось загрузить товары.");
    } finally {
      setLoading(false);
    }
  }, [currentPage, sortOption, categoryId, itemsPerPage]);

  useEffect(() => { fetchProducts(); }, [fetchProducts]);

  useEffect(() => {
    setCurrentPage(1);
    setSelectedBrands([]);
    setSelectedSpecs({});
    setPriceRange({ min: '', max: '' });
  }, [categoryId]);

  const { availableBrands, availableSpecs } = useMemo(() => {
    const brands = new Set();
    const specs = {};
    products.forEach(p => {
      if (p.brand) brands.add(p.brand);
      if (p.specifications) {
        Object.entries(p.specifications).forEach(([key, value]) => {
          if (!specs[key]) specs[key] = new Set();
          specs[key].add(value);
        });
      }
    });
    const formattedSpecs = {};
    Object.keys(specs).forEach(key => {
      formattedSpecs[key] = [...specs[key]].sort();
    });
    return { availableBrands: [...brands].sort(), availableSpecs: formattedSpecs };
  }, [products]);

  const filteredProducts = useMemo(() => {
    return products.filter(product => {
      const matchesBrand = selectedBrands.length === 0 || selectedBrands.includes(product.brand);
      const price = product.min_price || 0;
      const matchesMinPrice = priceRange.min === '' || price >= Number(priceRange.min);
      const matchesMaxPrice = priceRange.max === '' || price <= Number(priceRange.max);
      const matchesSpecs = Object.entries(selectedSpecs).every(([specKey, selectedValues]) => {
        if (!selectedValues || selectedValues.length === 0) return true;
        return selectedValues.includes(product.specifications?.[specKey]);
      });
      return matchesBrand && matchesMinPrice && matchesMaxPrice && matchesSpecs;
    });
  }, [products, selectedBrands, priceRange, selectedSpecs]);

  const handleSpecToggle = (specKey, value) => {
    setSelectedSpecs(prev => {
      const currentValues = prev[specKey] || [];
      const newValues = currentValues.includes(value)
        ? currentValues.filter(v => v !== value)
        : [...currentValues, value];
      return { ...prev, [specKey]: newValues };
    });
    setCurrentPage(1);
  };

  const handleCategorySelect = (id) => {
    const newParams = new URLSearchParams(searchParams);
    if (id === null) newParams.delete('category_id');
    else newParams.set('category_id', id);
    setSearchParams(newParams);
  };

  return (
    <>
      <Header />
      <main style={styles.main}>
        <div style={styles.container}>
          <div style={styles.content}>
            <div style={styles.categoryBar}>
              <button onClick={() => handleCategorySelect(null)} style={{ ...styles.chip, ...(categoryId === null ? styles.activeChip : {}) }}>Все товары</button>
              {categories.map(cat => (
                <button key={cat.id} onClick={() => handleCategorySelect(cat.id)} style={{ ...styles.chip, ...(String(categoryId) === String(cat.id) ? styles.activeChip : {}) }}>{cat.name}</button>
              ))}
            </div>

            <div style={styles.header}>
              <h1 style={styles.title}>Каталог</h1>
              <div style={styles.resultsCount}>Найдено: <strong>{filteredProducts.length}</strong></div>
            </div>

            <div style={styles.body}>
              <FilterPanel
                sortOption={sortOption}
                onSortChange={setSortOption}
                priceRange={priceRange}
                onPriceChange={(f, v) => { setPriceRange(p => ({ ...p, [f]: v })); setCurrentPage(1); }}
                selectedBrands={selectedBrands}
                onBrandToggle={(b) => { setSelectedBrands(p => p.includes(b) ? p.filter(x => x !== b) : [...p, b]); setCurrentPage(1); }}
                availableBrands={availableBrands}
                availableSpecs={availableSpecs}
                selectedSpecs={selectedSpecs}
                onSpecToggle={handleSpecToggle}
                onResetFilters={() => { setSortOption('popular'); setPriceRange({ min: '', max: '' }); setSelectedBrands([]); setSelectedSpecs({}); }}
              />

              <div style={styles.productsSection}>
                {loading ? (
                  <div style={styles.centerBox}><h3>Загрузка...</h3></div>
                ) : filteredProducts.length > 0 ? (
                  <div style={styles.grid}>
                    {filteredProducts.map(product => (
                      <ProductCard key={product.id} product={product} />
                    ))}
                  </div>
                ) : (
                  <div style={styles.centerBox}><h3>Ничего не найдено</h3></div>
                )}
                
                {!loading && filteredProducts.length > 0 && (
                  <div style={styles.paginationWrapper}>
                    <Pagination currentPage={currentPage} totalItems={filteredProducts.length} itemsPerPage={itemsPerPage} onPageChange={setCurrentPage} />
                  </div>
                )}
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
  main: { minHeight: '70vh', background: '#f5f5f5', padding: '20px 0' },
  container: { width: '100%', maxWidth: 1400, margin: '0 auto', padding: '0 20px' },
  content: { background: '#fff', borderRadius: 12, padding: '25px', boxShadow: '0 4px 20px rgba(0,0,0,0.05)' },
  categoryBar: { display: 'flex', overflowX: 'auto', gap: '10px', marginBottom: '25px', paddingBottom: '10px', borderBottom: '1px solid #f0f0f0' },
  chip: { padding: '10px 20px', background: '#f0f2f5', border: 'none', borderRadius: '30px', cursor: 'pointer', whiteSpace: 'nowrap', fontSize: '14px', transition: '0.2s' },
  activeChip: { background: '#05386B', color: '#fff' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 25 },
  title: { fontSize: 28, margin: 0, fontWeight: 700, color: '#1a1a1a' },
  resultsCount: { fontSize: 15, color: '#888' },
  body: { display: 'flex', alignItems: 'flex-start', gap: '30px' },
  productsSection: { flex: 1, minWidth: 0 },
  grid: { 
    display: 'grid', 
    gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', 
    gap: '20px',
    width: '100%'
  },
  centerBox: { textAlign: 'center', padding: '50px 0', color: '#666' },
  paginationWrapper: { marginTop: '40px', display: 'flex', justifyContent: 'center' }
};

export default SearchResultsPage;