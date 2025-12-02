from typing import Optional

from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.types import Text, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.db.database import Base
from datetime import datetime, timezone

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
        viewonly=True
    )

class Favorite(Base):
    __tablename__ = "favorite"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    notificate: Mapped[bool] = mapped_column(default=False)

    owner: Mapped["User"] = relationship(foreign_keys=[user_id], lazy="selectin")
    fav_product: Mapped["Product"] = relationship(foreign_keys=[product_id], lazy="selectin")


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
        viewonly=True
    )

    categories: Mapped[list["Category"]] = relationship(
        "Category",
        secondary="category_product",
        back_populates="products",
        cascade="all, delete",
        overlaps="product_categories",
        lazy="selectin"
    )

    features: Mapped[list["Feature"]] = relationship(
        back_populates="product",
        cascade="all, delete",
        lazy="selectin"
    )

    storelinks: Mapped[list["Storelink"]] = relationship(
        back_populates="product",
        cascade="all, delete",
        lazy="selectin"
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
        lazy="selectin"
    )

    parent: Mapped[Optional["Category"]] = relationship(
        "Category",
        remote_side=[id],
        backref="children",
        lazy="selectin"
    )

class Feature(Base):
    __tablename__ = "feature"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    unit: Mapped[str] = mapped_column(String(255))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))

    product: Mapped["Product"] = relationship(foreign_keys=[product_id], lazy="selectin")

class Storelink(Base):
    __tablename__ = "storelink"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Float)
    storename: Mapped[str] = mapped_column(String(255))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    product: Mapped["Product"] = relationship(foreign_keys=[product_id], lazy="selectin")


