import React, { createContext, useContext, useState } from 'react';
import { mockUser } from '../mocks/mockUser'; // <-- Подключаем твои данные

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuth, setIsAuth] = useState(false);

  const [forgotEmail, setForgotEmail] = useState('');
  const [confirmCode, setConfirmCode] = useState('');

  const login = ({ email, password }) => {
    // теперь сверяем с твоим mockUser
    if (email === mockUser.email && password === mockUser.password) {
      setUser({ name: mockUser.name, email: mockUser.email });
      setIsAuth(true);
      return { success: true };
    }

    return { success: false, message: "Неверная почта или пароль" };
  };

  const register = ({ name, email, password }) => {
    setUser({ name, email });
    setIsAuth(true);
    return { success: true };
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
