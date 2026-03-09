"""Business logic layer for operations reporting."""

from __future__ import annotations

import logging
from collections import defaultdict
from datetime import date
from typing import Optional

from .models import ShippingRecord
from .repository import Repository
from .utils import normalize_lot_id

logger = logging.getLogger(__name__)


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
        logger.info(
            "Running recurring defect analysis",
            extra={
                "analysis": "issues_by_line",
                "start_date": start_date,
                "end_date": end_date,
                "production_line": production_line,
            },
        )
        try:
            records = self.repository.get_inspection_records(
                start_date=start_date,
                end_date=end_date,
                production_line=production_line,
            )
        except Exception:
            logger.exception("Database query failure during recurring defect analysis")
            raise

        totals_by_line: dict[str, int] = defaultdict(int)
        missing_data_count = 0
        for record in records:
            defect_qty = record.defect_quantity or 0
            if record.defect_quantity is None:
                missing_data_count += 1
            if defect_qty > 1000:
                logger.warning(
                    "Suspicious defect pattern detected",
                    extra={
                        "part_id": record.lot_id,
                        "defect_type": record.defect_code,
                        "number_of_inspections": len(records),
                        "number_of_defects_detected": defect_qty,
                    },
                )
            if defect_qty <= 0:
                continue
            totals_by_line[record.production_line] += defect_qty

        if missing_data_count > 0:
            logger.warning(
                "Missing inspection data encountered",
                extra={
                    "number_of_inspections": len(records),
                    "missing_records": missing_data_count,
                },
            )

        result = sorted(totals_by_line.items(), key=lambda item: item[1], reverse=True)
        total_defects = sum(total for _, total in result)
        logger.info(
            "Recurring defect analysis completed",
            extra={
                "number_of_inspections": len(records),
                "number_of_recurring_defects_detected": total_defects,
            },
        )
        return result

    def defect_trends(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        production_line: Optional[str] = None,
    ) -> list[tuple[str, str, int]]:
        logger.info(
            "Running recurring defect analysis",
            extra={
                "analysis": "defect_trends",
                "start_date": start_date,
                "end_date": end_date,
                "production_line": production_line,
            },
        )
        try:
            records = self.repository.get_inspection_records(
                start_date=start_date,
                end_date=end_date,
                production_line=production_line,
            )
        except Exception:
            logger.exception("Database query failure during defect trend analysis")
            raise

        weekly_totals: dict[tuple[str, str], int] = defaultdict(int)
        for record in records:
            if not record.defect_code:
                logger.warning(
                    "Missing inspection data encountered",
                    extra={
                        "part_id": record.lot_id,
                        "number_of_inspections": len(records),
                    },
                )
                continue
            quantity = record.defect_quantity or 0
            if quantity <= 0:
                continue
            year, week, _ = record.inspection_date.isocalendar()
            week_key = f"{year}-W{week:02d}"
            weekly_totals[(week_key, record.defect_code)] += quantity

        trends = [
            (week_key, defect_code, total)
            for (week_key, defect_code), total in sorted(weekly_totals.items())
        ]
        total_defects = sum(total for _, _, total in trends)
        logger.info(
            "Recurring defect trend analysis completed",
            extra={
                "number_of_inspections": len(records),
                "number_of_recurring_defects_detected": total_defects,
            },
        )
        return trends

    def check_lot_shipped(self, lot_id: str) -> tuple[bool, Optional[date]]:
        try:
            normalized_lot_id = normalize_lot_id(lot_id)
            shipping_record: Optional[ShippingRecord] = (
                self.repository.get_shipping_record_for_lot(normalized_lot_id)
            )
        except Exception:
            logger.exception(
                "Unexpected exception while looking up lot shipping status"
            )
            raise
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
