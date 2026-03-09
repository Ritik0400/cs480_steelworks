from __future__ import annotations

import os
import subprocess
import sys
import time
from datetime import date
from pathlib import Path
from urllib.request import urlopen

import pytest
from dotenv import dotenv_values

from steelworks import database
from steelworks.orm_models import (
    DefectRow,
    InspectionRow,
    Lot,
    ProductionLine,
    ShippingRow,
)


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

    pytest.skip("DATABASE_TEST_URL is not configured for e2e tests.")
    raise AssertionError("unreachable")


def _wait_for_http(url: str, timeout_seconds: int = 30) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            with urlopen(url, timeout=2) as response:
                if response.status == 200:
                    return
        except Exception:
            time.sleep(0.5)
    raise RuntimeError(f"Timed out waiting for app at {url}")


@pytest.fixture(scope="session")
def app_base_url() -> str:
    return "http://127.0.0.1:8505"


@pytest.fixture(scope="session", autouse=True)
def running_streamlit_app(app_base_url: str):
    test_db_url = _test_database_url()
    database.configure_database(test_db_url)
    database.drop_db()
    database.init_db()

    with database.get_session() as session:
        lot = Lot(lot="LOT100")
        line = ProductionLine(line="LINE-Z")
        defect = DefectRow(defect_code="CRACK")
        session.add_all([lot, line, defect])
        session.flush()
        session.add(
            InspectionRow(
                lot_id=lot.id,
                production_line_id=line.id,
                inspection_date=date.today(),
                defect_id=defect.id,
                qty_defects=4,
                qty_checked=100,
                inspector="I1",
                part_number="P1",
            )
        )
        session.add(
            ShippingRow(
                lot_id=lot.id,
                ship_date=date.today(),
                ship_status="Pending",
                sales_order_no="SO100",
                customer="C1",
                destination_state="WA",
                carrier="Carrier",
                bol_no="BOL-100",
                qty_shipped=10,
            )
        )

    env = os.environ.copy()
    env["DATABASE_URL"] = test_db_url

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "src/steelworks/app.py",
            "--server.headless",
            "true",
            "--server.port",
            "8505",
            "--browser.gatherUsageStats",
            "false",
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        _wait_for_http(app_base_url)
        yield
    finally:
        process.terminate()
        process.wait(timeout=10)
