import apiClient from './apiClient';

export const productService = {
  /**
   * Получение списка продуктов с фильтрацией
   * @param {Object} params - Параметры запроса (skip, limit, brand, sort_by, sort_order)
   */
  async getProducts(params) {
    // Формируем query string, исключая пустые параметры
    const queryParams = new URLSearchParams();
    
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        queryParams.append(key, value);
      }
    });

    try {
      const response = await apiClient.get(`/products/?${queryParams.toString()}`);
      return response;
    } catch (error) {
      console.error("Error fetching products:", error);
      throw error;
    }
  },

  /**
   * Получение всех доступных брендов (если есть такой эндпоинт, 
   * иначе можно извлекать из общего списка товаров)
   */
  async getBrands() {
    return ['Apple', 'Samsung', 'Xiaomi', 'Sony', 'Huawei'];
  }
};