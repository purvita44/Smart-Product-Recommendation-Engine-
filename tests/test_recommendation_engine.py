import pandas as pd
import pytest

from recommendation_engine import load_catalog, recommend, recommended_types


def test_recommended_types_is_case_insensitive():
    assert recommended_types(" running shoes ") == (
        "Sports Sandals",
        "Track Pants",
        "Socks",
    )


def test_recommend_returns_available_complements_only():
    catalog = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "articleType": ["Sports Sandals", "Socks", "Jeans"],
        }
    )

    result = recommend(catalog, "Running Shoes", random_state=7)

    assert result["articleType"].tolist() == ["Sports Sandals", "Socks"]


def test_recommend_requires_article_type():
    with pytest.raises(ValueError, match="articleType"):
        recommend(pd.DataFrame({"id": [1]}), "Jeans")


def test_load_catalog_requires_id_and_article_type(tmp_path):
    path = tmp_path / "catalog.csv"
    path.write_text("id,name\n1,shirt\n", encoding="utf-8")

    with pytest.raises(ValueError, match="articleType"):
        load_catalog(str(path))
