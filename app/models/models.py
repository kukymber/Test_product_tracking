from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

from app.database import Base
from app.mixsins.mixins import IdMixin, TimestampMixin, AuditMixin, SoftDeleteMixin

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

semi_products_components = Table(
    'semi_products_components', Base.metadata,
    Column('semi_product_id', Integer, ForeignKey('semi_products.id'), primary_key=True),
    Column('component_id', Integer, ForeignKey('components.id'), primary_key=True)
)

invoice_components = Table(
    'invoice_components', Base.metadata,
    Column('invoice_id', Integer, ForeignKey('invoices.id'), primary_key=True),
    Column('component_id', Integer, ForeignKey('components.id'), primary_key=True)
)

order_products = Table(
    'order_products', Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)
order_items = Table(
    'order_items',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('quantity', Integer, nullable=False)
)

"""Models"""


class Component(Base, IdMixin, TimestampMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'components'
    name = Column(String, unique=True)
    quantity = Column(Float)
    semi_products = relationship("SemiProduct", secondary=semi_products_components, back_populates="components")
    products = relationship("Product", secondary=components_products, back_populates="components")
    invoices = relationship("Invoice", secondary=invoice_components, back_populates="components")


class SemiProduct(Base, IdMixin, TimestampMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'semi_products'
    name = Column(String, unique=True)
    quantity = Column(Float)
    components = relationship("Component", secondary=semi_products_components, back_populates="semi_products")
    products = relationship("Product", secondary=semi_products_products, back_populates="semi_products")


class Product(Base, IdMixin, TimestampMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'products'
    name = Column(String, unique=True)
    semi_products = relationship("SemiProduct", secondary=semi_products_products, back_populates="products")
    orders = relationship("Order", secondary=order_products, back_populates="products")
    components = relationship("Component", secondary=components_products, back_populates="products")
    items = relationship("Order", secondary=order_items, back_populates="products")


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
    items = relationship("Product", secondary=order_items, back_populates="orders")
