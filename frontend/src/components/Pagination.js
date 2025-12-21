import React from 'react';

function Pagination({ totalItems, itemsPerPage, currentPage, onPageChange }) {
  // Вычисляем общее количество страниц
  const totalPages = Math.ceil(totalItems / itemsPerPage);

  // Если страниц 0 или 1, пагинацию можно не показывать
  if (totalPages <= 1) return null;

  const pages = Array.from({ length: totalPages }, (_, i) => i + 1);

  return (
    <div style={styles.pagination}>
      <button 
        style={{ ...styles.button, opacity: currentPage === 1 ? 0.5 : 1 }} 
        disabled={currentPage === 1}
        onClick={() => onPageChange(currentPage - 1)}
      >
        Назад
      </button>

      {pages.map((page) => (
        <button
          key={page}
          onClick={() => onPageChange(page)}
          style={{
            ...styles.button,
            backgroundColor: currentPage === page ? "#05386B" : "#1976d2", // Подсветка активной страницы
            fontWeight: currentPage === page ? "bold" : "normal",
          }}
        >
          {page}
        </button>
      ))}

      <button 
        style={{ ...styles.button, opacity: currentPage === totalPages ? 0.5 : 1 }} 
        disabled={currentPage === totalPages}
        onClick={() => onPageChange(currentPage + 1)}
      >
        Вперёд
      </button>
    </div>
  );
}

const styles = {
  pagination: {
    display: "flex",
    justifyContent: "center",
    padding: "20px 0",
    gap: 10
  },
  button: {
    padding: "8px 15px",
    background: "#1976d2",
    border: "none",
    color: "#fff",
    cursor: "pointer",
    borderRadius: 6,
    transition: "0.3s"
  }
};

export default Pagination;