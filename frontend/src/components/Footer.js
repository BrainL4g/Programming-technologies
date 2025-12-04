import React from 'react';

function Footer() {
  return (
    <footer style={styles.footer}>
      © 2025 Агрегатор товаров. Все права защищены.
    </footer>
  );
}

const styles = {
  footer: {
    textAlign: "center",
    padding: 20,
    background: "#fff",
    marginTop: 20,
    borderTop: "1px solid #ddd"
  }
};

export default Footer;
