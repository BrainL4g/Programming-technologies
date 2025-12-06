import React, { useState } from 'react';
import Header from '../components/headers/HeaderAuth';
import Footer from '../components/Footer';
import EditPersonalDataForm from '../components/account/EditPersonalDataForm';
import ChangePasswordForm from '../components/account/ChangePasswordForm';
import LogoutModal from '../components/account/LogoutModal';

function AccountPage() {
  const [mode, setMode] = useState('default');
  const [isLogoutOpen, setIsLogoutOpen] = useState(false);

  return (
    <>
      <Header isAuth={true} />

      <main style={styles.page}>
        <div style={styles.box}>
          <h2 style={styles.title}>Персональные данные</h2>

          {mode === 'default' && (
            <div style={styles.buttons}>
              <button style={styles.btn} onClick={() => setMode('edit')}>
                Изменить
              </button>

              <button style={styles.btn} onClick={() => setMode('pass')}>
                Сменить пароль
              </button>

              <button style={styles.btn} onClick={() => setIsLogoutOpen(true)}>
                Выйти из аккаунта
              </button>
            </div>
          )}

          {mode === 'edit' && (
            <EditPersonalDataForm onCancel={() => setMode('default')} />
          )}

          {mode === 'pass' && (
            <ChangePasswordForm onCancel={() => setMode('default')} />
          )}
        </div>
      </main>

      <LogoutModal open={isLogoutOpen} onClose={() => setIsLogoutOpen(false)} />

      <Footer />
    </>
  );
}

const styles = {
  page: {
    minHeight: '50.5vh',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: 40,
    paddingBottom: 40,
  },

  box: {
    width: '450px',
    border: '2px solid #8b8b8bff',
    borderRadius: 6,
    padding: '30px 25px',
    background: 'white',
    textAlign: 'center',
  },

  title: {
    marginBottom: 25,
    fontSize: 20,
    fontWeight: 600,
  },

  buttons: {
    display: 'flex',
    flexDirection: 'column',
    gap: 15,
    marginTop: 10,
  },

  btn: {
    padding: '12px 16px',
    background: '#003B78',
    border: 'none',
    color: 'white',
    borderRadius: 6,
    cursor: 'pointer',
    fontSize: 15,
  },
};

export default AccountPage;
