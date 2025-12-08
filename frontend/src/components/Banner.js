import React from "react";
import banner from "../images/banner.png";

export default function Banner() {
  return (
    <div style={styles.banner}>
      <img src={banner} style={styles.image} alt="banner" />

      <div style={styles.textBlock}>
        <h1 style={styles.title}>BRO</h1>
        <p style={styles.text}>
          Мы не продаём технику, мы помогаем найти идеальный вариант по лучшей цене.
          Сравнивайте предложения, читайте отзывы и выбирайте уверенно. Экономия времени и денег начниается здесь.
        </p>
      </div>
    </div>
  );
}

const styles = {
  banner: {
    position: "relative",
    width: "100%",
    height: 250,
    overflow: "hidden"
  },
  image: {
    width: "100%",
    height: "100%",
    objectFit: "cover"
  },
  textBlock: {
    position: "absolute",
    top: "20%",
    left: "10%",
    color: "#fff",
    maxWidth: 500
  },
  title: {
    fontSize: 48,
    fontWeight: "bold",
    marginBottom: 10
  },
  text: {
    fontSize: 16,
    lineHeight: 1.4
  }
};
