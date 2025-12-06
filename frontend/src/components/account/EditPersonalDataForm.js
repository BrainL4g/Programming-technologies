import React, { useState } from 'react';

function EditPersonalDataForm({ onCancel }) {
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [errors, setErrors] = useState({});

  const handleSave = () => {
    let newErrors = {};

    if (!password) newErrors.password = 'Введите текущий пароль';
    if (!name) newErrors.name = 'Введите ваше имя';
    if (!email) newErrors.email = 'Введите вашу почту';

    setErrors(newErrors);

    if (Object.keys(newErrors).length === 0) {
      onCancel();
    }
  };

  return (
    <div>
      <h3>Смена личных данных</h3>

      <input
        type="password"
        placeholder="Текущий пароль"
        style={{ ...styles.input, borderColor: errors.password ? 'red' : '#ccc' }}
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      {errors.password && <p style={styles.error}>{errors.password}</p>}

      <input
        placeholder="Ваше имя"
        style={{ ...styles.input, borderColor: errors.name ? 'red' : '#ccc' }}
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      {errors.name && <p style={styles.error}>{errors.name}</p>}

      <input
        placeholder="Почта"
        style={{ ...styles.input, borderColor: errors.email ? 'red' : '#ccc' }}
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      {errors.email && <p style={styles.error}>{errors.email}</p>}

      <div style={styles.row}>
        <button style={styles.cancel} onClick={onCancel}>Отмена</button>
        <button style={styles.save} onClick={handleSave}>Изменить</button>
      </div>
    </div>
  );
}

const styles = {
  input: {
    width: '100%',
    padding: 10,
    marginBottom: 8,
    borderRadius: 5,
    border: '1px solid #ccc',
  },
  row: {
    display: 'flex',
    justifyContent: 'space-between',
    marginTop: 15,
  },
  cancel: { padding: '10px 20px' },
  save: {
    padding: '10px 20px',
    background: '#1976d2',
    color: 'white',
    border: 'none',
    borderRadius: 5,
  },
  error: { color: 'red', marginTop: -5, marginBottom: 10, fontSize: 14 },
};

export default EditPersonalDataForm;
