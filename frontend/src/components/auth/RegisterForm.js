import React, { useState } from 'react';
import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";

function RegisterForm({ onSwitchToLogin }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errors, setErrors] = useState({});

  const { register, login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    let newErrors = {};

    if (!name.trim()) newErrors.name = 'Введите ваше имя';
    else if (name.length < 2) newErrors.name = 'Имя должно быть не менее 2 символов';

    if (!email) newErrors.email = 'Введите вашу почту';
    else if (!/\S+@\S+\.\S+/.test(email)) newErrors.email = 'Некорректный email';

    if (!password) newErrors.password = 'Введите пароль';
    else if (password.length < 6) newErrors.password = 'Пароль должен быть не менее 6 символов';

    if (!confirmPassword) newErrors.confirmPassword = 'Подтвердите пароль';
    else if (password !== confirmPassword) newErrors.confirmPassword = 'Пароли не совпадают';

    setErrors(newErrors);

    if (Object.keys(newErrors).length === 0) {
      console.log('Регистрация:', { name, email, password });
      
      const result = await register({name, email, password});
      if (result.success) {
        await login({ email, password });
        navigate("/");
      }
    }
  };

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>Регистрация</h3>

      <form onSubmit={handleSubmit}>
        <div style={styles.inputGroup}>
          <input
            type="text"
            placeholder="Ваше имя"
            style={{ ...styles.input, borderColor: errors.name ? 'red' : '#ccc' }}
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          {errors.name && <p style={styles.error}>{errors.name}</p>}
        </div>

        <div style={styles.inputGroup}>
          <input
            type="email"
            placeholder="Почта"
            style={{ ...styles.input, borderColor: errors.email ? 'red' : '#ccc' }}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          {errors.email && <p style={styles.error}>{errors.email}</p>}
        </div>

        <div style={styles.inputGroup}>
          <input
            type="password"
            placeholder="Пароль"
            style={{ ...styles.input, borderColor: errors.password ? 'red' : '#ccc' }}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {errors.password && <p style={styles.error}>{errors.password}</p>}
        </div>

        <div style={styles.inputGroup}>
          <input
            type="password"
            placeholder="Повторите пароль"
            style={{ ...styles.input, borderColor: errors.confirmPassword ? 'red' : '#ccc' }}
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
          {errors.confirmPassword && <p style={styles.error}>{errors.confirmPassword}</p>}
        </div>

        <div style={styles.agreement}>
          <input
            type="checkbox"
            id="agreement"
            required
            style={styles.checkbox}
          />
          <label htmlFor="agreement" style={styles.agreementLabel}>
            Я соглашаюсь с условиями использования и политикой конфиденциальности
          </label>
        </div>

        <button type="submit" style={styles.submitBtn}>
          Зарегистрироваться
        </button>
      </form>

      <div style={styles.switch}>
        <p style={styles.switchText}>
          Уже есть аккаунт?{' '}
          <button onClick={onSwitchToLogin} style={styles.switchBtn}>
            Войти
          </button>
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: {
    width: '100%',
    maxWidth: '400px',
  },
  title: {
    marginBottom: 25,
    fontSize: 20,
    fontWeight: 600,
    textAlign: 'center',
  },
  inputGroup: {
    marginBottom: 15,
  },
  input: {
    width: '100%',
    padding: '12px 15px',
    borderRadius: 5,
    border: '1px solid #ccc',
    fontSize: 15,
    boxSizing: 'border-box',
  },
  error: {
    color: 'red',
    fontSize: 13,
    marginTop: 5,
    marginBottom: 0,
  },
  agreement: {
    display: 'flex',
    alignItems: 'flex-start',
    marginBottom: 20,
  },
  checkbox: {
    marginRight: 8,
    marginTop: 3,
    minWidth: 16,
    minHeight: 16,
  },
  agreementLabel: {
    fontSize: 14,
    color: '#555',
    lineHeight: 1.4,
  },
  submitBtn: {
    width: '100%',
    padding: '12px 20px',
    background: '#1976d2',
    color: 'white',
    border: 'none',
    borderRadius: 5,
    fontSize: 16,
    cursor: 'pointer',
    fontWeight: 600,
    marginBottom: 20,
  },
  switch: {
    textAlign: 'center',
    paddingTop: 15,
    borderTop: '1px solid #eee',
  },
  switchText: {
    fontSize: 14,
    color: '#666',
  },
  switchBtn: {
    background: 'none',
    border: 'none',
    color: '#1976d2',
    cursor: 'pointer',
    fontSize: 14,
    textDecoration: 'underline',
    padding: 0,
  },
};

export default RegisterForm;