import React from 'react';

function LogoutModal({ open, onClose }) {
  if (!open) return null;

  return (
    <div style={styles.overlay}>
      <div style={styles.modal}>
        <h3>Выйти из аккаунта?</h3>

        <div style={styles.row}>
          <button style={styles.cancel} onClick={onClose}>Отмена</button>
          <button style={styles.logout}>Выйти</button>
        </div>
      </div>
    </div>
  );
}

const styles = {
  overlay: {
    position: 'fixed',
    inset: 0,
    background: 'rgba(0,0,0,0.4)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 10,
  },
  modal: {
    width: 350,
    background: 'white',
    padding: 20,
    borderRadius: 8,
    textAlign: 'center',
  },
  row: {
    marginTop: 20,
    display: 'flex',
    justifyContent: 'space-between',
  },
  cancel: {
    padding: '10px 18px',
  },
  logout: {
    padding: '10px 18px',
    background: 'red',
    color: 'white',
    border: 'none',
    borderRadius: 5,
  },
};

export default LogoutModal;
