import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../api/authService';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuth, setIsAuth] = useState(false);

  const [forgotEmail, setForgotEmail] = useState('');
  const [confirmCode, setConfirmCode] = useState('');

  useEffect(() => {
    const initAuth = async () => {
      if (authService.isAuthenticated()) {
        try {
          // Опционально: можно запросить свежие данные пользователя с бэкенда
          const userData = await authService.getCurrentUser();
          setUser(userData);
          setIsAuth(true);
        } catch (err) {
          console.error("Session restoration failed", err);
          logout(); // Если токен протух
        }
      }
    };
    initAuth();
  }, []);

  const login = async ({ email, password }) => {
    try {
      await authService.login(email, password);
      setIsAuth(true);
      return { success: true };
    } catch (err) {
      return { success: false, message: "Неверная почта или пароль" };
    }
    };

  const register = async ({ name, email, password }) => {
    try {
      await authService.register(
        email,
        password,
        password, 
        name
      );
      await authService.login(email, password);
      setUser({ username: name, email: email });
      return { success: true };
    } catch (err) {
      return { success: false, message: "Неверная почта или пароль" };
    }
  };

  const logout = () => {
    setUser(null);
    setIsAuth(false);
    setForgotEmail('');
    setConfirmCode('');
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        setUser,
        isAuth,
        login,
        register,
        logout,
        forgotEmail,
        setForgotEmail,
        confirmCode,
        setConfirmCode
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
