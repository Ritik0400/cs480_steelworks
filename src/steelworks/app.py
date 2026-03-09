"""Streamlit dashboard for SteelWorks operations reporting."""

from __future__ import annotations

from datetime import date

import streamlit as st

from steelworks import database, services


def main() -> None:
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
