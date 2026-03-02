"""Unit tests for the domain model classes.

These tests are intentionally trivial and exist to ensure the scaffolding
produces usable types.  No business rules are verified here.
"""

from datetime import date

import pytest

from steelworks import models


@pytest.mark.skip(reason="scaffold stub - no behavior to verify yet")
def test_production_record_instantiation():
    # we only care that attributes can be set and read
    rec = models.ProductionRecord(
        id=1,
        lot_id="LOT1",
        production_line="L1",
        produced_at=date.today(),
        quantity=100,
    )
    assert rec.lot_id == "LOT1"
    assert isinstance(rec.produced_at, date)


@pytest.mark.skip(reason="scaffold stub - no behavior to verify yet")
def test_inspection_record_instantiation():
    rec = models.InspectionRecord(
        id=1,
        lot_id="LOT1",
        inspection_date=date.today(),
        production_line="L1",
        defect_code=None,
        defect_quantity=None,
    )
    assert rec.production_line == "L1"


@pytest.mark.skip(reason="scaffold stub - no behavior to verify yet")
def test_shipping_record_instantiation():
    rec = models.ShippingRecord(
        id=1,
        lot_id="LOT1",
        shipped_at=None,
        status="pending",
    )
    assert rec.status == "pending"
