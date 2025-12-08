import React from "react";
import { useParams } from "react-router-dom";
import { products } from "../mocks/products";
import { recommended } from "../mocks/recommended";

export default function ProductPage() {
  const { id } = useParams();
  const all = [...products, ...recommended];
  const product = all.find(p => p.id === Number(id));

  if (!product) return <h2>ТИПО СТРАНИЦА ТОВАРА</h2>;

  return (
    <div style={{ padding: 20 }}>
      <h2>{product.title}</h2>
      <img src={product.image} alt="" style={{ width: 300, borderRadius: 10 }} />
      <p style={{ fontSize: 20, marginTop: 10 }}>{product.price} ₽</p>
    </div>
  );
}
