"""SQLAlchemy ORM models used by repository/database layers."""

from __future__ import annotations

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Declarative base class for ORM tables."""


class Lot(Base):
    __tablename__ = "lots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lot_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)

    inspections: Mapped[list["InspectionRow"]] = relationship(back_populates="lot")
    shipments: Mapped[list["ShippingRow"]] = relationship(back_populates="lot")


class ProductionLine(Base):
    __tablename__ = "production_lines"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    line_name: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)

    inspections: Mapped[list["InspectionRow"]] = relationship(back_populates="line")


class ProductionRow(Base):
    __tablename__ = "production_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lots.id"), nullable=False)
    production_line_id: Mapped[int] = mapped_column(
        ForeignKey("production_lines.id"),
        nullable=False,
    )
    produced_at: Mapped[Date] = mapped_column(Date, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class InspectionRow(Base):
    __tablename__ = "inspection_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lots.id"), nullable=False)
    production_line_id: Mapped[int] = mapped_column(
        ForeignKey("production_lines.id"),
        nullable=False,
    )
    inspection_date: Mapped[Date] = mapped_column(Date, nullable=False)
    defect_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    defect_quantity: Mapped[int | None] = mapped_column(Integer, nullable=True)

    lot: Mapped[Lot] = relationship(back_populates="inspections")
    line: Mapped[ProductionLine] = relationship(back_populates="inspections")


class ShippingRow(Base):
    __tablename__ = "shipping_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lots.id"), nullable=False)
    shipped_at: Mapped[Date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")

    lot: Mapped[Lot] = relationship(back_populates="shipments")
