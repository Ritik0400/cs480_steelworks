"""Business logic layer for operations reporting."""

from __future__ import annotations

from collections import defaultdict
from datetime import date
from typing import Optional

from .models import ShippingRecord
from .repository import Repository
from .utils import normalize_lot_id


class OperationsService:
    """Service methods implementing Operations acceptance criteria."""

    def __init__(self, repository: Repository):
        self.repository = repository

    def summarize_issues_by_line(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        production_line: Optional[str] = None,
    ) -> list[tuple[str, int]]:
        records = self.repository.get_inspection_records(
            start_date=start_date,
            end_date=end_date,
            production_line=production_line,
        )

        totals_by_line: dict[str, int] = defaultdict(int)
        for record in records:
            defect_qty = record.defect_quantity or 0
            if defect_qty <= 0:
                continue
            totals_by_line[record.production_line] += defect_qty

        return sorted(totals_by_line.items(), key=lambda item: item[1], reverse=True)

    def defect_trends(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        production_line: Optional[str] = None,
    ) -> list[tuple[str, str, int]]:
        records = self.repository.get_inspection_records(
            start_date=start_date,
            end_date=end_date,
            production_line=production_line,
        )

        weekly_totals: dict[tuple[str, str], int] = defaultdict(int)
        for record in records:
            if not record.defect_code:
                continue
            quantity = record.defect_quantity or 0
            if quantity <= 0:
                continue
            year, week, _ = record.inspection_date.isocalendar()
            week_key = f"{year}-W{week:02d}"
            weekly_totals[(week_key, record.defect_code)] += quantity

        return [
            (week_key, defect_code, total)
            for (week_key, defect_code), total in sorted(weekly_totals.items())
        ]

    def check_lot_shipped(self, lot_id: str) -> tuple[bool, Optional[date]]:
        normalized_lot_id = normalize_lot_id(lot_id)
        shipping_record: Optional[ShippingRecord] = (
            self.repository.get_shipping_record_for_lot(normalized_lot_id)
        )
        if shipping_record is None:
            return False, None

        has_shipped = shipping_record.status.strip().lower() == "shipped"
        return has_shipped, shipping_record.shipped_at


def _default_service() -> OperationsService:
    return OperationsService(repository=Repository())


def get_defect_summary(
    start: Optional[date] = None,
    end: Optional[date] = None,
    line: Optional[str] = None,
) -> list[tuple[str, int]]:
    return _default_service().summarize_issues_by_line(
        start_date=start,
        end_date=end,
        production_line=line,
    )


def get_defect_trends(
    start: Optional[date] = None,
    end: Optional[date] = None,
    line: Optional[str] = None,
) -> list[tuple[str, str, int]]:
    return _default_service().defect_trends(
        start_date=start,
        end_date=end,
        production_line=line,
    )


def lookup_shipment(lot_id: str) -> Optional[tuple[bool, Optional[date]]]:
    normalized_lot_id = normalize_lot_id(lot_id)
    record = _default_service().repository.get_shipping_record_for_lot(
        normalized_lot_id
    )
    if record is None:
        return None
    return record.status.strip().lower() == "shipped", record.shipped_at
