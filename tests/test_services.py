"""Stub tests for the OperationsService.

These tests ensure the public API surface is defined and initially unimplemented
(raising `NotImplementedError`).  They mirror the acceptance criteria in the
user story but do not check any real results yet.
"""

from datetime import date

import pytest

from steelworks.services import OperationsService
from steelworks.repository import Repository
from steelworks.models import InspectionRecord


class FakeRepository(Repository):
    def __init__(self, records):
        self.records = records
        self.last_filters = None

    def get_inspection_records(
        self, start_date=None, end_date=None, production_line=None
    ):
        self.last_filters = {
            "start_date": start_date,
            "end_date": end_date,
            "production_line": production_line,
        }
        return self.records


@pytest.fixture
def service():
    # injecting a plain Repository; real tests may use a mock or fake later
    return OperationsService(repository=Repository())


def test_summarize_issues_by_line_returns_descending_totals():
    records = [
        InspectionRecord(1, "LOT1", date(2026, 1, 1), "L1", "D1", 1),
        InspectionRecord(2, "LOT2", date(2026, 1, 1), "L2", "D2", 5),
        InspectionRecord(3, "LOT3", date(2026, 1, 2), "L1", "D3", 2),
        InspectionRecord(4, "LOT4", date(2026, 1, 2), "L2", "D4", None),
        InspectionRecord(5, "LOT5", date(2026, 1, 3), "L3", "D5", 0),
    ]
    operations = OperationsService(repository=FakeRepository(records))

    result = operations.summarize_issues_by_line()

    assert result == [("L2", 5), ("L1", 3)]


def test_summarize_issues_by_line_passes_filters_to_repository():
    fake_repo = FakeRepository([])
    operations = OperationsService(repository=fake_repo)
    start = date(2026, 1, 1)
    end = date(2026, 1, 31)

    operations.summarize_issues_by_line(
        start_date=start,
        end_date=end,
        production_line="L2",
    )

    assert fake_repo.last_filters == {
        "start_date": start,
        "end_date": end,
        "production_line": "L2",
    }


@pytest.mark.skip(reason="scaffold stub - not implemented yet")
def test_defect_trends_stub(service):
    with pytest.raises(NotImplementedError):
        service.defect_trends()


@pytest.mark.skip(reason="scaffold stub - not implemented yet")
def test_check_lot_shipped_stub(service):
    with pytest.raises(NotImplementedError):
        service.check_lot_shipped("LOT1")
