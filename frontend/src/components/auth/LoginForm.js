import React, { useState } from 'react';
import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";

function LoginForm({ onSwitchToRegister }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState({});
  const [rememberMe, setRememberMe] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    let newErrors = {};

    if (!email) newErrors.email = 'Введите вашу почту';
    else if (!/\S+@\S+\.\S+/.test(email)) newErrors.email = 'Некорректный email';

    if (!password) newErrors.password = 'Введите пароль';
    else if (password.length < 6) newErrors.password = 'Пароль должен быть не менее 6 символов';

    setErrors(newErrors);

    if (Object.keys(newErrors).length === 0) {
      // console.log('Вход:', { email, password, rememberMe });
      // Здесь будет логика авторизации

      const result = login({ email, password });

      if (!result.success) {
        setErrors({ password: result.message });
      } else {
        navigate("/"); // успешный вход → на главную
      }
    }
  };

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>Вход в аккаунт</h3>

      <form onSubmit={handleSubmit}>
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
        <button
          type="button"
          onClick={() => navigate("/forgot")}
          style={{ 
            background: "none",
            border: "none",
            color: "#05386B",
            textDecoration: "underline",
            cursor: "pointer",
            marginBottom: 15
          }}
        >
          Забыли пароль?
        </button>

        <div style={styles.rememberGroup}>
          <input
            type="checkbox"
            id="remember"
            checked={rememberMe}
            onChange={(e) => setRememberMe(e.target.checked)}
            style={styles.checkbox}
          />
          <label htmlFor="remember" style={styles.rememberLabel}>
            Запомнить меня
          </label>
        </div>

        <button type="submit" style={styles.submitBtn}>
          Войти
        </button>
      </form>

      <div style={styles.switch}>
        <p style={styles.switchText}>
          Нет аккаунта?{' '}
          <button onClick={onSwitchToRegister} style={styles.switchBtn}>
            Зарегистрироваться
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
  rememberGroup: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: 20,
  },
  checkbox: {
    marginRight: 8,
    width: 16,
    height: 16,
  },
  rememberLabel: {
    fontSize: 14,
    color: '#555',
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
    color: '#05386B',
    cursor: 'pointer',
    fontSize: 14,
    textDecoration: 'underline',
    padding: 0,
  },
};

export default LoginForm;