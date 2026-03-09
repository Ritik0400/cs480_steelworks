"""Repository layer for data access against SQLAlchemy models."""

from __future__ import annotations

from datetime import date
from typing import Callable, ContextManager, List, Optional, cast

from sqlalchemy import Select, desc, select
from sqlalchemy.orm import Session

from . import database
from .models import InspectionRecord, ProductionRecord, ShippingRecord
from .orm_models import InspectionRow, Lot, ProductionLine, ProductionRow, ShippingRow


SessionFactory = Callable[[], ContextManager[Session]]


class Repository:
    """Database-backed repository for operations analytics queries."""

    def __init__(self, session_factory: SessionFactory = database.get_session):
        self._session_factory = session_factory

    def get_production_records(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        production_line: Optional[str] = None,
    ) -> List[ProductionRecord]:
        with self._session_factory() as session:
            stmt: Select[tuple[ProductionRow, Lot, ProductionLine]] = (
                select(ProductionRow, Lot, ProductionLine)
                .join(Lot, ProductionRow.lot_id == Lot.id)
                .join(
                    ProductionLine,
                    ProductionRow.production_line_id == ProductionLine.id,
                )
            )
            if start_date:
                stmt = stmt.where(ProductionRow.produced_at >= start_date)
            if end_date:
                stmt = stmt.where(ProductionRow.produced_at <= end_date)
            if production_line:
                stmt = stmt.where(ProductionLine.line_name == production_line)

            rows = session.execute(stmt).all()

        return [
            ProductionRecord(
                id=prod.id,
                lot_id=lot.lot_id,
                production_line=line.line_name,
                produced_at=prod.produced_at,
                quantity=prod.quantity,
            )
            for prod, lot, line in rows
        ]

    def get_inspection_records(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        production_line: Optional[str] = None,
    ) -> List[InspectionRecord]:
        with self._session_factory() as session:
            stmt: Select[tuple[InspectionRow, Lot, ProductionLine]] = (
                select(InspectionRow, Lot, ProductionLine)
                .join(Lot, InspectionRow.lot_id == Lot.id)
                .join(
                    ProductionLine,
                    InspectionRow.production_line_id == ProductionLine.id,
                )
            )
            if start_date:
                stmt = stmt.where(InspectionRow.inspection_date >= start_date)
            if end_date:
                stmt = stmt.where(InspectionRow.inspection_date <= end_date)
            if production_line:
                stmt = stmt.where(ProductionLine.line_name == production_line)

            rows = session.execute(stmt).all()

        return [
            InspectionRecord(
                id=inspection.id,
                lot_id=lot.lot_id,
                inspection_date=inspection.inspection_date,
                production_line=line.line_name,
                defect_code=inspection.defect_code,
                defect_quantity=inspection.defect_quantity,
            )
            for inspection, lot, line in rows
        ]

    def get_shipping_record_for_lot(self, lot_id: str) -> Optional[ShippingRecord]:
        with self._session_factory() as session:
            lot = session.execute(
                select(Lot).where(Lot.lot_id == lot_id)
            ).scalar_one_or_none()
            if lot is None:
                return None

            stmt = (
                select(ShippingRow)
                .where(ShippingRow.lot_id == lot.id)
                .order_by(desc(ShippingRow.shipped_at))
                .limit(1)
            )
            row = session.execute(stmt).scalar_one_or_none()
            if row is None:
                return None

        return ShippingRecord(
            id=row.id,
            lot_id=lot_id,
            shipped_at=cast(Optional[date], row.shipped_at),
            status=row.status,
        )
