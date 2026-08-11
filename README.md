# Smart Product Recommendation Engine

A rule-based product recommendation engine for a CSV catalog. The original Colab export remains in the repository; the reusable implementation is in `recommendation_engine.py`.

## Setup

```bash
python -m pip install -r requirements.txt
python -m pytest
```

## Example

```python
from recommendation_engine import load_catalog, recommend

catalog = load_catalog("styles.csv")
recommendations = recommend(catalog, "Running Shoes", random_state=42)
print(recommendations[["id", "articleType"]])
```

The result includes one available catalog item for each complementary product type. Product-type matching is case-insensitive, and an unknown type returns an empty result.
