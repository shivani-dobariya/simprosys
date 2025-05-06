import enum
import time

from sqlalchemy import Integer, Column, String, Boolean, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship

from product_service.models import Base


class Status(enum.Enum):
    active = 'active'
    deactive = 'deactive'


def get_timestamp():
    return time.time()


class Common:
    status = Column(Enum(Status), default=Status.active)
    created_ts = Column(Integer, default=get_timestamp())
    updated_ts = Column(Integer, default=get_timestamp())
    is_deleted = Column(Boolean, default=False)


class Categories(Base, Common):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    products = relationship("Products", back_populates="category")


class Products(Base, Common):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship("Categories", back_populates="products", uselist=False)


class User(Base, Common):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    auth_token = Column(String)
    refresh_token = Column(String)
