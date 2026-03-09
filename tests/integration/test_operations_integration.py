from __future__ import annotations

import os
from datetime import date
from pathlib import Path

import pytest
from dotenv import dotenv_values

from steelworks import database, services
from steelworks.orm_models import InspectionRow, Lot, ProductionLine, ShippingRow


def _test_database_url() -> str:
    env_url = os.getenv("DATABASE_TEST_URL")
    if env_url:
        return env_url

    env_file = Path(".env.test")
    if env_file.exists():
        values = dotenv_values(env_file)
        file_url = values.get("DATABASE_TEST_URL")
        if isinstance(file_url, str) and file_url:
            return file_url

    pytest.skip("DATABASE_TEST_URL is not configured (.env.test or env var).")
    raise AssertionError("unreachable")


@pytest.fixture(scope="module", autouse=True)
def integration_database():
    database.configure_database(_test_database_url())
    database.drop_db()
    database.init_db()

    with database.get_session() as session:
        lot_a = Lot(lot_id="LOT001")
        lot_b = Lot(lot_id="LOT002")
        line_a = ProductionLine(line_name="LINE-A")
        line_b = ProductionLine(line_name="LINE-B")
        session.add_all([lot_a, lot_b, line_a, line_b])
        session.flush()

        session.add_all(
            [
                InspectionRow(
                    lot_id=lot_a.id,
                    production_line_id=line_a.id,
                    inspection_date=date(2026, 3, 1),
                    defect_code="DENT",
                    defect_quantity=2,
                ),
                InspectionRow(
                    lot_id=lot_b.id,
                    production_line_id=line_a.id,
                    inspection_date=date(2026, 3, 8),
                    defect_code="DENT",
                    defect_quantity=3,
                ),
                InspectionRow(
                    lot_id=lot_b.id,
                    production_line_id=line_b.id,
                    inspection_date=date(2026, 3, 9),
                    defect_code="SCRATCH",
                    defect_quantity=1,
                ),
                ShippingRow(
                    lot_id=lot_a.id,
                    shipped_at=date(2026, 3, 10),
                    status="shipped",
                ),
            ]
        )

    yield


def test_integration_summary_by_line():
    result = services.get_defect_summary(
        start=date(2026, 3, 1),
        end=date(2026, 3, 31),
    )
    assert result == [("LINE-A", 5), ("LINE-B", 1)]


def test_integration_weekly_trends():
    trends = services.get_defect_trends(
        start=date(2026, 3, 1),
        end=date(2026, 3, 31),
    )
    assert ("2026-W09", "DENT", 2) in trends
    assert ("2026-W10", "DENT", 3) in trends
    assert ("2026-W11", "SCRATCH", 1) in trends


def test_integration_shipping_lookup():
    shipped = services.lookup_shipment("lot-001")
    missing = services.lookup_shipment("LOT999")
    assert shipped == (True, date(2026, 3, 10))
    assert missing is None
