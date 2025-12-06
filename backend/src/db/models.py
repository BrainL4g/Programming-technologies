from datetime import timezone
from typing import Optional

from uuid import uuid4
from datetime import datetime
from sqlalchemy import Boolean,JSON, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Float, Text
from src.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(128))
    username: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    fav_products: Mapped[list["Product"]] = relationship(
        "Product",
        secondary="favorite",
        primaryjoin="User.id == Favorite.user_id",
        secondaryjoin="Favorite.product_id == Product.id",
        back_populates="users_who_favorited",
        lazy="selectin",
        viewonly=True,
    )


class Favorite(Base):
    __tablename__ = "favorite"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    notificate: Mapped[bool] = mapped_column(default=False)

    owner: Mapped["User"] = relationship(foreign_keys=[user_id], lazy="selectin")
    fav_product: Mapped["Product"] = relationship(
        foreign_keys=[product_id], lazy="selectin"
    )


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    brand: Mapped[str] = mapped_column(String(100))

    users_who_favorited: Mapped[list["User"]] = relationship(
        "User",
        secondary="favorite",
        primaryjoin="Product.id == Favorite.product_id",
        secondaryjoin="Favorite.user_id == User.id",
        back_populates="fav_products",
        lazy="selectin",
        viewonly=True,
    )

    categories: Mapped[list["Category"]] = relationship(
        "Category",
        secondary="category_product",
        back_populates="products",
        cascade="all, delete",
        overlaps="product_categories",
        lazy="selectin",
    )

    features: Mapped[list["Feature"]] = relationship(
        back_populates="product", cascade="all, delete", lazy="selectin"
    )

    storelinks: Mapped[list["Storelink"]] = relationship(
        back_populates="product", cascade="all, delete", lazy="selectin"
    )


class CategoryProduct(Base):
    __tablename__ = "category_product"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category.id"))

    products: Mapped[list["Product"]] = relationship(
        "Product",
        secondary="category_product",
        back_populates="categories",
        overlaps="categories",
        lazy="selectin",
    )

    parent: Mapped[Optional["Category"]] = relationship(
        "Category", remote_side=[id], backref="children", lazy="selectin"
    )


class Feature(Base):
    __tablename__ = "feature"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    unit: Mapped[str] = mapped_column(String(255))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))

    product: Mapped["Product"] = relationship(
        foreign_keys=[product_id], lazy="selectin"
    )


class Storelink(Base):
    __tablename__ = "storelink"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Float)
    storename: Mapped[str] = mapped_column(String(255))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    product: Mapped["Product"] = relationship(
        foreign_keys=[product_id], lazy="selectin"
    )


class Store(Base):
    __tablename__ = "stores"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    domain: Mapped[str] = mapped_column(String(255), unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_sync: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    offers: Mapped[list["Offer"]] = relationship("Offer", back_populates="store", cascade="all, delete-orphan", lazy="selectin")


class Offer(Base):
    __tablename__ = "offers"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    external_id: Mapped[str] = mapped_column(String(255), index=True)
    product_name: Mapped[str] = mapped_column(String(512))
    store_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"))
    price: Mapped[float] = mapped_column(Numeric(12, 2))
    old_price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="RUB")
    available: Mapped[bool] = mapped_column(Boolean, default=True)
    in_stock: Mapped[int] = mapped_column(default=0)
    category: Mapped[str | None] = mapped_column(String(255), nullable=True)
    brand: Mapped[str | None] = mapped_column(String(255), nullable=True)
    url: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    specifications: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    store: Mapped["Store"] = relationship("Store", back_populates="offers")
    price_history: Mapped[list["PriceHistory"]] = relationship("PriceHistory", back_populates="offer", cascade="all, delete-orphan", lazy="selectin")


class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    offer_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("offers.id", ondelete="CASCADE"))
    price: Mapped[float] = mapped_column(Numeric(12, 2))
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, index=True)

    offer: Mapped["Offer"] = relationship("Offer", back_populates="price_history")