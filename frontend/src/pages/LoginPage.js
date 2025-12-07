import React, { useState } from 'react';
import Header from '../components/headers/HeaderGuest';
import Footer from '../components/Footer';
import LoginForm from '../components/auth/LoginForm';
import RegisterForm from '../components/auth/RegisterForm';

function LoginPage() {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <>
      <Header />

      <main style={styles.page}>
        <div style={styles.box}>
          <div style={styles.tabs}>
            <button
              style={{ ...styles.tab, ...(isLogin ? styles.activeTab : {}) }}
              onClick={() => setIsLogin(true)}
            >
              Вход
            </button>
            <button
              style={{ ...styles.tab, ...(!isLogin ? styles.activeTab : {}) }}
              onClick={() => setIsLogin(false)}
            >
              Регистрация
            </button>
          </div>

          {isLogin ? (
            <LoginForm onSwitchToRegister={() => setIsLogin(false)} />
          ) : (
            <RegisterForm onSwitchToLogin={() => setIsLogin(true)} />
          )}
        </div>
      </main>

      <Footer />
    </>
  );
}

const styles = {
  page: {
    minHeight: '70vh',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    padding: '40px 20px',
    background: '#f5f5f5',
  },
  box: {
    width: '100%',
    maxWidth: '450px',
    background: 'white',
    borderRadius: 10,
    padding: '30px',
    boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
  },
  tabs: {
    display: 'flex',
    borderBottom: '1px solid #eee',
    marginBottom: 30,
  },
  tab: {
    flex: 1,
    padding: '15px 0',
    background: 'none',
    border: 'none',
    fontSize: 16,
    fontWeight: 500,
    color: '#666',
    cursor: 'pointer',
    position: 'relative',
  },
  activeTab: {
    color: '#1976d2',
    fontWeight: 600,
  }
};

export default LoginPage;