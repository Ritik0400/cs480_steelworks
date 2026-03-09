from __future__ import annotations

from playwright.sync_api import Page, expect


def test_dashboard_loads_and_displays_core_sections(page: Page, app_base_url: str):
    page.goto(app_base_url)

    expect(page.get_by_text("SteelWorks Operations Dashboard")).to_be_visible(
        timeout=20000
    )
    expect(page.get_by_text("Defects by Production Line")).to_be_visible(timeout=20000)
    expect(page.get_by_text("Defect Trends (weekly)")).to_be_visible(timeout=20000)
    expect(page.get_by_text("Lot Shipping Status")).to_be_visible(timeout=20000)


def test_lot_lookup_interaction(page: Page, app_base_url: str):
    page.goto(app_base_url)
    lot_input = page.get_by_label("Search lot ID")
    lot_input.fill("LOT100")
    lot_input.press("Enter")

    pending_match = page.get_by_text("Lot exists but has not shipped yet.")
    expect(pending_match).to_be_visible(timeout=20000)
