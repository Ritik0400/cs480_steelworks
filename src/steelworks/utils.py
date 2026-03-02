"""Utility helpers for SteelWorks domain logic.

This module contains minimal functions needed for the first unit tests. No
extraneous logic or additional helpers are included in the scaffold.
"""


def normalize_lot_id(lot_id: str) -> str:
    """Return a normalized lot identifier.

    Normalization rules are intentionally simple for the scaffold: uppercase the
    string and remove any non-alphanumeric characters.
    """
    # iterate through characters, keep only alphanumeric ones
    filtered = [ch for ch in lot_id if ch.isalnum()]
    return "".join(filtered).upper()
