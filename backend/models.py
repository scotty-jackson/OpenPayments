"""
SQLAlchemy models for Global Factor Lab database schema.
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Date, DateTime,
    ForeignKey, Text, JSON, Index, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Country(Base):
    """Country or region entity."""
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    region_group = Column(String(50))  # e.g., "Developed", "Emerging", "Global"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    factor_series = relationship("FactorSeries", back_populates="country")


class FactorDefinition(Base):
    """Factor definition with stable codes and groupings."""
    __tablename__ = 'factor_definition'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    group = Column(String(50), nullable=False, index=True)  # e.g., "Value", "Momentum", "Size"
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    factor_series = relationship("FactorSeries", back_populates="factor_definition")


class FactorSeries(Base):
    """A specific factor time series for a country."""
    __tablename__ = 'factor_series'

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey('country.id'), nullable=False, index=True)
    factor_definition_id = Column(Integer, ForeignKey('factor_definition.id'), nullable=False, index=True)
    source_name = Column(String(100), nullable=False)
    frequency = Column(String(20), nullable=False)  # "Daily", "Monthly"
    start_date = Column(Date)
    end_date = Column(Date)
    currency = Column(String(10))
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    country = relationship("Country", back_populates="factor_series")
    factor_definition = relationship("FactorDefinition", back_populates="factor_series")
    returns = relationship("FactorReturn", back_populates="factor_series", cascade="all, delete-orphan")

    # Constraints
    __table_args__ = (
        UniqueConstraint('country_id', 'factor_definition_id', 'frequency', 'source_name',
                        name='uq_country_factor_freq_source'),
        Index('ix_factor_series_country_factor', 'country_id', 'factor_definition_id'),
    )


class FactorReturn(Base):
    """Individual return observation for a factor series."""
    __tablename__ = 'factor_return'

    id = Column(Integer, primary_key=True, index=True)
    factor_series_id = Column(Integer, ForeignKey('factor_series.id'), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    return_value = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    factor_series = relationship("FactorSeries", back_populates="returns")

    # Constraints
    __table_args__ = (
        UniqueConstraint('factor_series_id', 'date', name='uq_factor_series_date'),
        Index('ix_factor_return_series_date', 'factor_series_id', 'date'),
    )
