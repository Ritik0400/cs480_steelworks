"""Stub tests for the Repository class.

At this scaffold stage, the repository methods simply raise
`NotImplementedError`.  The tests assert that the methods exist and behave as
expected (i.e. they raise) so that later development can replace the stub
implementations with real queries.
"""

import pytest

from steelworks.repository import Repository


@pytest.fixture
def repo():
    return Repository()


@pytest.mark.skip(reason="scaffold stub - not implemented yet")
def test_get_production_records_stub(repo):
    with pytest.raises(NotImplementedError):
        repo.get_production_records()


@pytest.mark.skip(reason="scaffold stub - not implemented yet")
def test_get_inspection_records_stub(repo):
    with pytest.raises(NotImplementedError):
        repo.get_inspection_records()


@pytest.mark.skip(reason="scaffold stub - not implemented yet")
def test_get_shipping_record_stub(repo):
    with pytest.raises(NotImplementedError):
        repo.get_shipping_record_for_lot("ANY")
