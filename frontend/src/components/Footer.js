import React from 'react';

function Footer() {
  return (
    <footer style={styles.footer}>
      <div style={styles.inner}>

        <div style={styles.about}>
          <h2 style={styles.title}>О компании</h2>
          <p style={styles.text}>
            Мы BRO - современный онлайн-агрегатор, который революционирует процесс покупки электроники 
            и бытовой техники. Мы создали платформу, где собраны предложения от сотен интернет-магазинов, 
            крупных розничных сетей и официальных дилеров в одном месте. Наша миссия: сделать покупку техники 
            простой, выгодной и осознанной для каждого. Мы экономим ваше время и деньги, предоставляя всю 
            необходимую информацию для принятия верного решения.
          </p>
        </div>

        <div style={styles.contacts}>
          <h2 style={styles.title}>Контакты</h2>
          <p style={styles.contactItem}>📞 +7 (000) 000-00-00</p>
          <p style={styles.contactItem}>📞 +7 (001) 000-00-00</p>
          <p style={styles.contactItem}>✉️ BRO@pochta.ru</p>
        </div>

      </div>
    </footer>
  );
}

const styles = {
  footer: {
    width: '100%',
    background: '#1d1d1d',
    color: 'white',
    padding: '50px 0',
    display: 'flex',
    justifyContent: 'center',
  },

  inner: {
    width: '80%',
    maxWidth: '1200px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },

  about: {
    maxWidth: '60%',
  },

  contacts: {
    minWidth: '200px',
    textAlign: 'left',
  },

  title: {
    fontSize: '28px',
    marginBottom: '15px',
    fontWeight: '600',
  },

  text: {
    lineHeight: '1.6',
    opacity: 0.9,
    fontSize: '15px',
  },

  contactItem: {
    fontSize: '16px',
    marginBottom: '10px',
  }
};

export default Footer;
