"""Streamlit dashboard for SteelWorks operations reporting."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from datetime import date
from pathlib import Path

import streamlit as st

from steelworks import database, services

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "steelworks.log"
MAX_LOG_BYTES = 5 * 1024 * 1024
BACKUP_COUNT = 3


def _configure_logging() -> None:
    root_logger = logging.getLogger()
    if any(isinstance(h, RotatingFileHandler) for h in root_logger.handlers):
        return

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_LOG_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    handler.setFormatter(formatter)

    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)


logger = logging.getLogger(__name__)


def main() -> None:
    _configure_logging()
    logger.info("Application startup")
    database.init_db()

    st.title("SteelWorks Operations Dashboard")
    st.sidebar.header("Filters")

    start_date = st.sidebar.date_input("Start date", value=date.today())
    end_date = st.sidebar.date_input("End date", value=date.today())
    line_filter = st.sidebar.text_input("Production line (optional)")

    st.header("Defects by Production Line")
    summary = services.get_defect_summary(
        start=start_date,
        end=end_date,
        line=line_filter or None,
    )
    if summary:
        st.table(summary)
    else:
        st.info("No data for selected filters.")

    st.header("Defect Trends (weekly)")
    logger.info('User opened "Recurring Defects" page')
    trends = services.get_defect_trends(
        start=start_date,
        end=end_date,
        line=line_filter or None,
    )
    if trends:
        st.table(trends)
    else:
        st.info("No trends for selected filters.")

    st.header("Lot Shipping Status")
    lot_input = st.text_input("Search lot ID")
    if lot_input:
        result = services.lookup_shipment(lot_input)
        if result is None:
            st.warning("No shipping record found for this lot.")
        else:
            shipped, shipped_at = result
            if shipped:
                st.success(f"Lot shipped on {shipped_at}")
            else:
                st.info("Lot exists but has not shipped yet.")


if __name__ == "__main__":
    main()
