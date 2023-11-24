from sqlalchemy import Column, DateTime, String, Integer, Boolean
import datetime


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    update_at = Column(DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())


class AuditMixin:
    created_by = Column(String)
    updated_by = Column(String)


class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False)


class IdMixin:
    id = Column(Integer, primary_key=True)
