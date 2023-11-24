from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

"""Mixins"""


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    update_at = Column(DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())


class AuditMixin:
    created_by = Column(String)
    updated_by = Column(String)


class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False)


class IdMixin:
    id = Column(Integerm, primary_key=True)


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
    unit_price = Column(Float)
    storage_conditions = Column(String)
    semi_products = relationship("SemiProduct", back_populates="component")
    products = relationship("Product", secondary=components_products, back_populates="components")


class SemiProduct(Base, IdMixin, TimestampMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'semi_products'

    name = Column(String, unique=True)
    component_id = Column(Integer, ForeignKey('components.id'))
    component = relationship("Component", back_populates="semi_products")


class Product(Base, IdMixin, TimestampMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    components = relationship("Component", secondary=components_products, back_populates="products")


class Invoice(Base, IdMixin, TimestampMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'invoices'

    number = Column(String)


class Order(Base, IdMixin, TimestampMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = 'orders'

    number = Column(String)
