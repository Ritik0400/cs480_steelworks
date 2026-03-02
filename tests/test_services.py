"""Stub tests for the OperationsService.

These tests ensure the public API surface is defined and initially unimplemented
(raising `NotImplementedError`).  They mirror the acceptance criteria in the
user story but do not check any real results yet.
"""

import pytest

from steelworks.services import OperationsService
from steelworks.repository import Repository


@pytest.fixture
def service():
    # injecting a plain Repository; real tests may use a mock or fake later
    return OperationsService(repository=Repository())


@pytest.mark.skip(reason="scaffold stub - not implemented yet")
def test_summarize_issues_by_line_stub(service):
    with pytest.raises(NotImplementedError):
        service.summarize_issues_by_line()


@pytest.mark.skip(reason="scaffold stub - not implemented yet")
def test_defect_trends_stub(service):
    with pytest.raises(NotImplementedError):
        service.defect_trends()


@pytest.mark.skip(reason="scaffold stub - not implemented yet")
def test_check_lot_shipped_stub(service):
    with pytest.raises(NotImplementedError):
        service.check_lot_shipped("LOT1")
