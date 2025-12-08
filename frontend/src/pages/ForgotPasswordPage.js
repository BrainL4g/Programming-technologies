import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function ForgotPasswordPage() {
  const [step, setStep] = useState(1);
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [newPass, setNewPass] = useState("");
  const [newPassConfirm, setNewPassConfirm] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  // 1) Отправка почты
  const handleEmailSubmit = (e) => {
    e.preventDefault();

    if (!email) {
      setError("Введите вашу почту");
      return;
    }

    // имитация отправки письма
    setError("");
    setStep(2);
  };

  // 2) Ввод кода
  const handleCodeSubmit = (e) => {
    e.preventDefault();

    if (code.length < 4) {
      setError("Некорректный код");
      return;
    }

    setError("");
    setStep(3);
  };

  // 3) Ввод нового пароля
  const handleNewPassSubmit = (e) => {
    e.preventDefault();

    if (newPass.length < 6) {
      setError("Пароль должен быть не менее 6 символов");
      return;
    }
    if (newPass !== newPassConfirm) {
      setError("Пароли не совпадают");
      return;
    }

    // успешная смена пароля
    setError("");
    navigate("/");
  };

  return (
    <div style={styles.wrapper}>
      <div style={styles.card}>
        {step === 1 && (
          <>
            <h2 style={styles.title}>Введите вашу почту</h2>

            <form onSubmit={handleEmailSubmit}>
              <input
                type="email"
                placeholder="Электронная почта*"
                style={styles.input}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />

              {error && <p style={styles.error}>{error}</p>}

              <p style={styles.desc}>
                Введите вашу почту для того, чтобы сбросить пароль на вашем
                аккаунте. После этого вам нужно будет ввести присланный код для
                завершения сброса пароля и начала ввода нового.
              </p>

              <button type="submit" style={styles.buttonDark}>
                Далее
              </button>
            </form>
          </>
        )}

        {step === 2 && (
          <>
            <h2 style={styles.title}>Подтвердите сброс пароля</h2>

            <form onSubmit={handleCodeSubmit}>
              <input
                type="text"
                placeholder="Введите код*"
                style={styles.input}
                value={code}
                onChange={(e) => setCode(e.target.value)}
              />

              {error && <p style={styles.error}>{error}</p>}

              <p style={styles.desc}>
                На вашу почту был отправлен код подтверждения сброса. Если код
                не пришел в течение нескольких минут — нажмите “Отправить
                повторно”.
              </p>

              <div style={styles.row}>
                <button
                  type="button"
                  style={styles.buttonLight}
                  onClick={() => setStep(1)}
                >
                  Назад
                </button>

                <button type="button" style={styles.buttonLight}>
                  Отправить повторно
                </button>

                <button type="submit" style={styles.buttonDark}>
                  Сбросить
                </button>
              </div>
            </form>
          </>
        )}

        {step === 3 && (
          <>
            <h2 style={styles.title}>Введите новый пароль</h2>

            <form onSubmit={handleNewPassSubmit}>
              <input
                type="password"
                placeholder="Пароль*"
                style={styles.input}
                value={newPass}
                onChange={(e) => setNewPass(e.target.value)}
              />

              <input
                type="password"
                placeholder="Подтверждение пароля*"
                style={styles.input}
                value={newPassConfirm}
                onChange={(e) => setNewPassConfirm(e.target.value)}
              />

              {error && <p style={styles.error}>{error}</p>}

              <button type="submit" style={styles.buttonDark}>
                Войти
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  );
}

const styles = {
  wrapper: {
    width: "100%",
    display: "flex",
    justifyContent: "center",
    padding: "60px 20px",
  },
  card: {
    width: "100%",
    maxWidth: "600px",
    padding: 40,
    background: "#fff",
    borderRadius: 10,
    boxShadow: "0 0 20px rgba(0,0,0,0.08)",
  },
  title: {
    fontSize: 26,
    fontWeight: 600,
    marginBottom: 25,
    textAlign: "center",
  },
  input: {
    width: "100%",
    padding: "12px 15px",
    borderRadius: 5,
    border: "1px solid #ccc",
    fontSize: 16,
    marginBottom: 15,
  },
  error: {
    color: "red",
    fontSize: 14,
    marginBottom: 10,
  },
  desc: {
    fontSize: 14,
    color: "#555",
    textAlign: "center",
    marginBottom: 20,
  },
  row: {
    display: "flex",
    justifyContent: "space-between",
    gap: 10,
    marginTop: 10,
  },
  buttonDark: {
    background: "#05386B",
    color: "#fff",
    padding: "12px 20px",
    border: "none",
    borderRadius: 5,
    width: "100%",
    fontSize: 16,
    cursor: "pointer",
    marginTop: 10,
  },
  buttonLight: {
    background: "#ddd",
    color: "#000",
    padding: "12px 20px",
    border: "none",
    borderRadius: 5,
    fontSize: 15,
    cursor: "pointer",
    flex: 1,
  },
};

export default ForgotPasswordPage;
