import React, { useState } from 'react';

function ChangePasswordForm({ onCancel }) {
  const [current, setCurrent] = useState('');
  const [pass1, setPass1] = useState('');
  const [pass2, setPass2] = useState('');
  const [errors, setErrors] = useState({});

  const handleSave = () => {
    let newErrors = {};

    if (!current) newErrors.current = 'Введите текущий пароль';
    if (!pass1) newErrors.pass1 = 'Введите новый пароль';
    if (!pass2) newErrors.pass2 = 'Повторите новый пароль';
    if (pass1 && pass2 && pass1 !== pass2)
      newErrors.pass2 = 'Пароли не совпадают';

    setErrors(newErrors);

    if (Object.keys(newErrors).length === 0) {
      onCancel();
    }
  };

  return (
    <div>
      <h3>Смена пароля</h3>

      <input
        type="password"
        placeholder="Текущий пароль"
        style={{ ...styles.input, borderColor: errors.current ? 'red' : '#ccc' }}
        value={current}
        onChange={(e) => setCurrent(e.target.value)}
      />
      {errors.current && <p style={styles.error}>{errors.current}</p>}

      <input
        type="password"
        placeholder="Новый пароль"
        style={{ ...styles.input, borderColor: errors.pass1 ? 'red' : '#ccc' }}
        value={pass1}
        onChange={(e) => setPass1(e.target.value)}
      />
      {errors.pass1 && <p style={styles.error}>{errors.pass1}</p>}

      <input
        type="password"
        placeholder="Повторите новый пароль"
        style={{ ...styles.input, borderColor: errors.pass2 ? 'red' : '#ccc' }}
        value={pass2}
        onChange={(e) => setPass2(e.target.value)}
      />
      {errors.pass2 && <p style={styles.error}>{errors.pass2}</p>}

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

export default ChangePasswordForm;
