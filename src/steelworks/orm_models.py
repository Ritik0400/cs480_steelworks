"""SQLAlchemy ORM models used by repository/database layers."""

from __future__ import annotations

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Declarative base class for ORM tables."""


class Lot(Base):
    __tablename__ = "lots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lot: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)

    inspections: Mapped[list["InspectionRow"]] = relationship(back_populates="lot")
    shipments: Mapped[list["ShippingRow"]] = relationship(back_populates="lot")


class ProductionLine(Base):
    __tablename__ = "production_lines"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    line: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)

    inspections: Mapped[list["InspectionRow"]] = relationship(back_populates="line")


class ProductionRow(Base):
    __tablename__ = "production_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lots.id"), nullable=False)
    production_line_id: Mapped[int] = mapped_column(
        ForeignKey("production_lines.id"),
        nullable=False,
    )
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    shift: Mapped[str] = mapped_column(String(32), nullable=False, default="Unknown")
    part_number: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    units_planned: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    units_actual: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    downtime_min: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    line_issue: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    primary_issue: Mapped[str | None] = mapped_column(String(255), nullable=True)
    supervisor_notes: Mapped[str | None] = mapped_column(String(255), nullable=True)


class DefectRow(Base):
    __tablename__ = "defects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    defect_code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)


class InspectionRow(Base):
    __tablename__ = "inspection_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lots.id"), nullable=False)
    production_line_id: Mapped[int] = mapped_column(
        ForeignKey("production_lines.id"),
        nullable=False,
    )
    inspection_date: Mapped[Date] = mapped_column(Date, nullable=False)
    inspection_time: Mapped[Time | None] = mapped_column(Time, nullable=True)
    inspector: Mapped[str] = mapped_column(
        String(64), nullable=False, default="Unknown"
    )
    part_number: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    defect_id: Mapped[int | None] = mapped_column(
        ForeignKey("defects.id"), nullable=True
    )
    defect_description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    severity: Mapped[str | None] = mapped_column(String(32), nullable=True)
    qty_checked: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    qty_defects: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    disposition: Mapped[str | None] = mapped_column(String(64), nullable=True)
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)

    lot: Mapped[Lot] = relationship(back_populates="inspections")
    line: Mapped[ProductionLine] = relationship(back_populates="inspections")
    defect: Mapped[DefectRow | None] = relationship()


class ShippingRow(Base):
    __tablename__ = "shipping_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lots.id"), nullable=False)
    ship_date: Mapped[Date] = mapped_column(Date, nullable=False)
    sales_order_no: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    customer: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    destination_state: Mapped[str] = mapped_column(
        String(2), nullable=False, default="NA"
    )
    carrier: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    bol_no: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    tracking_pro: Mapped[str | None] = mapped_column(String(64), nullable=True)
    qty_shipped: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ship_status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="pending"
    )
    hold_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    shipping_notes: Mapped[str | None] = mapped_column(String(255), nullable=True)

    lot: Mapped[Lot] = relationship(back_populates="shipments")
