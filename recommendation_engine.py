"""Reusable, rule-based product recommendation utilities."""

from __future__ import annotations

from typing import Mapping, Sequence

import pandas as pd

RECOMMENDATION_RULES: Mapping[str, Sequence[str]] = {
    "Running Shoes": ("Sports Sandals", "Track Pants", "Socks"),
    "Sports Shoes": ("Track Pants", "Socks", "Sports Sandals"),
    "Casual Shoes": ("Jeans", "Tshirts", "Wallets"),
    "Formal Shoes": ("Shirts", "Belts", "Trousers"),
    "Jeans": ("Tshirts", "Belts", "Casual Shoes"),
    "Tshirts": ("Jeans", "Casual Shoes", "Shorts"),
    "Shirts": ("Formal Shoes", "Belts", "Trousers"),
    "Shorts": ("Tshirts", "Casual Shoes"),
    "Track Pants": ("Running Shoes", "Sports Sandals", "Socks"),
    "Sports Sandals": ("Track Pants", "Socks"),
    "Socks": ("Running Shoes", "Sports Shoes"),
    "Wallets": ("Casual Shoes", "Belts"),
    "Belts": ("Jeans", "Formal Shoes"),
    "Sandals": ("Dresses", "Handbags"),
    "Flip Flops": ("Shorts", "Tshirts"),
    "Sweatshirts": ("Track Pants", "Sports Shoes"),
    "Kurtas": ("Leggings", "Sandals"),
    "Dresses": ("Heels", "Handbags"),
    "Handbags": ("Dresses", "Heels"),
    "Watches": ("Shirts", "Jeans", "Wallets"),
}


def load_catalog(path: str) -> pd.DataFrame:
    """Load a catalog CSV and return rows with the fields needed for recommendations."""
    catalog = pd.read_csv(path, on_bad_lines="skip")
    required = {"id", "articleType"}
    missing = required.difference(catalog.columns)
    if missing:
        raise ValueError(f"Catalog is missing required columns: {', '.join(sorted(missing))}")
    return catalog.dropna(subset=["id", "articleType"]).reset_index(drop=True)


def recommended_types(product_type: str) -> tuple[str, ...]:
    """Return complementary product types for a user-provided product type."""
    normalized = product_type.strip().casefold()
    for source, targets in RECOMMENDATION_RULES.items():
        if source.casefold() == normalized:
            return tuple(targets)
    return ()


def recommend(
    catalog: pd.DataFrame, product_type: str, *, random_state: int | None = None
) -> pd.DataFrame:
    """Return one catalog item for each complementary type that is available."""
    if "articleType" not in catalog.columns:
        raise ValueError("Catalog is missing required column: articleType")

    selections: list[pd.DataFrame] = []
    for offset, target_type in enumerate(recommended_types(product_type)):
        matches = catalog.loc[
            catalog["articleType"].astype(str).str.casefold() == target_type.casefold()
        ]
        if not matches.empty:
            state = None if random_state is None else random_state + offset
            selections.append(matches.sample(n=1, random_state=state))

    if not selections:
        return catalog.iloc[0:0].copy()
    return pd.concat(selections, ignore_index=True)
