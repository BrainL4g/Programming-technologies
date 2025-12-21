import React, { useState } from 'react';
import apiClient from '../../api/apiClient';
import { useAuth } from '../../context/AuthContext';

function EditPersonalDataForm({ onCancel }) {
  const { user, setUser } = useAuth();
  console.log(user);
  const [password, setPassword] = useState(''); // Бэкенд может требовать для подтверждения личности
  const [name, setName] = useState(user.username || '');
  const [email, setEmail] = useState(user.email || '');
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  

  const handleSave = async () => {
    let newErrors = {};

    if (!password) newErrors.password = 'Введите текущий пароль';
    if (!name) newErrors.name = 'Введите ваше имя';
    if (!email) newErrors.email = 'Введите вашу почту';

    setErrors(newErrors);

    if (Object.keys(newErrors).length === 0) {
      setLoading(true);
      try {
        const updatedUser = await apiClient.patch('/users/me', {
          email: email,
          username: name
        });
        if (updatedUser) setUser({ username: name, email: email });
        alert('Данные успешно изменены');
        onCancel();
      } catch (err) {
        setErrors({ server: err.message || 'Ошибка при обновлении данных' });
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div>
      <h3>Смена личных данных</h3>
      
      {errors.server && <p style={styles.error}>{errors.server}</p>}

      <input
        type="password"
        placeholder="Текущий пароль"
        style={{ ...styles.input, borderColor: errors.password ? 'red' : '#ccc' }}
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        disabled={loading}
      />
      {errors.password && <p style={styles.error}>{errors.password}</p>}

      <input
        placeholder="Ваше имя"
        style={{ ...styles.input, borderColor: errors.name ? 'red' : '#ccc' }}
        value={name}
        onChange={(e) => setName(e.target.value)}
        disabled={loading}
      />
      {errors.name && <p style={styles.error}>{errors.name}</p>}

      <input
        placeholder="Почта"
        style={{ ...styles.input, borderColor: errors.email ? 'red' : '#ccc' }}
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        disabled={loading}
      />
      {errors.email && <p style={styles.error}>{errors.email}</p>}

      <div style={styles.row}>
        <button style={styles.cancel} onClick={onCancel} disabled={loading}>
          Отмена
        </button>
        <button style={styles.save} onClick={handleSave} disabled={loading}>
          {loading ? 'Сохранение...' : 'Изменить'}
        </button>
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
    boxSizing: 'border-box', // Добавил для корректной ширины
  },
  row: {
    display: 'flex',
    justifyContent: 'space-between',
    marginTop: 15,
  },
  cancel: { padding: '10px 20px', cursor: 'pointer' },
  save: {
    padding: '10px 20px',
    background: '#1976d2',
    color: 'white',
    border: 'none',
    borderRadius: 5,
    cursor: 'pointer',
  },
  error: { color: 'red', marginTop: -5, marginBottom: 10, fontSize: 14 },
};

export default EditPersonalDataForm;