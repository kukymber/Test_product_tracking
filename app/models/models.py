from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

from mixsins import IdMixin, TimestampMixin, AuditMixin, SoftDeleteMixin

Base = declarative_base()


"""Add. relationship"""

components_products = Table(
    'components_products', Base.metadata,
    Column('component_id', ForeignKey('components.id'), primary_key=True),
    Column('product_id', ForeignKey('products.id'), primary_key=True)
)

semi_products_products = Table(
    'semi_products_products', Base.metadata,
    Column('semi_product_id', Integer, ForeignKey('semi_products.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)

"""Models"""


class Component(Base, IdMixin, TimestampMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'components'
    name = Column(String, unique=True)
    quantity = Column(Float)
    semi_products = relationship("SemiProduct", back_populates="component")
    products = relationship("Product", secondary=components_products, back_populates="components")
    invoices = relationship("Invoice", secondary=invoice_components, back_populates="components")


class SemiProduct(Base, IdMixin, TimestampMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'semi_products'
    name = Column(String, unique=True)
    component_id = Column(Integer, ForeignKey('components.id'))
    quantity = Column(Float)
    component = relationship("Component", back_populates="semi_products")
    products = relationship("Product", secondary=semi_products_products, back_populates="semi_products")


class Product(Base, IdMixin, TimestampMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'products'
    name = Column(String, unique=True)
    semi_products = relationship("SemiProduct", secondary=semi_products_products, back_populates="products")
    orders = relationship("Order", secondary=order_products, back_populates="products")


class Invoice(Base, IdMixin, TimestampMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'invoices'
    number = Column(Integer, unique=True)
    component_details = Column(Text)
    components = relationship("Component", secondary=invoice_components, back_populates="invoices")


class Order(Base, IdMixin, TimestampMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'orders'
    number = Column(Integer, unique=True)
    order_date = Column(DateTime, default=datetime.datetime.utcnow)
    product_details = Column(Text)
    products = relationship("Product", secondary=order_products, back_populates="orders")
