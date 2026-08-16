# Smart Product Recommendation Engine

A lightweight, rule-based product recommendation engine for fashion catalogs stored as CSV files.

The maintained implementation is intentionally small and reusable. It loads a product catalog with pandas, maps a selected product type to complementary product types, and returns one available catalog item for each complementary category.

The repository also contains a larger exploratory Colab-exported script with experimental catalog deduplication, text/image embeddings, and reverse image-search workflows. The reusable and tested entry point is **`recommendation_engine.py`**.

---

## Project Status

| Component                     | Status       | Description                                                                                                     |
| ----------------------------- | ------------ | --------------------------------------------------------------------------------------------------------------- |
| Rule-based recommendations    | Maintained   | Tested and deterministic when a random seed is supplied. Suitable for reuse as a Python module.                 |
| CSV catalog loading           | Maintained   | Validates the required `id` and `articleType` columns and removes incomplete rows.                              |
| Exploratory notebook workflow | Experimental | Preserved in `smart_product_recommendation_engine (2).py`; includes additional ML and image-search experiments. |
| Automated tests               | Active       | Pytest suite covering normalization, filtering, validation, and error behavior.                                 |
| Continuous integration        | Active       | GitHub Actions runs the test suite on pushes to `main` and pull requests using Python 3.11.                     |

---

## Features

The maintained recommendation engine provides:

* Case-insensitive product-type matching
* Rule-based complementary product recommendations
* Configurable random selection
* Filtering to products that are actually available in the catalog
* Validation of required CSV columns
* A simple pandas DataFrame-based API
* Deterministic recommendations when `random_state` is provided
* Graceful handling of unknown product types
* Extensible recommendation rules through `RECOMMENDATION_RULES`

Unknown product types return an empty result instead of raising an exception.

The current recommendation rules cover common fashion categories including:

* Running Shoes
* Sports Shoes
* Casual Shoes
* Formal Shoes
* Jeans
* Shirts
* T-shirts
* Shorts
* Track Pants
* Sandals
* Socks
* Wallets
* Belts
* Dresses
* Handbags
* Watches
* Sweatshirts
* Kurtas
* Flip-flops

The recommendation table is defined in `RECOMMENDATION_RULES` and can be extended without changing the core recommendation algorithm.

---

## Repository Structure

```text
.
├── recommendation_engine.py
├── smart_product_recommendation_engine (2).py
├── styles.csv
├── data_labels.csv
├── requirements.txt
├── tests/
│   └── test_recommendation_engine.py
├── .github/
│   └── workflows/
│       └── tests.yml
└── README.md
```

---

## Maintained Implementation

The main reusable implementation is:

```text
recommendation_engine.py
```

It provides the following API:

### `load_catalog(path)`

Loads and validates a product catalog from a CSV file.

```python
from recommendation_engine import load_catalog

catalog = load_catalog("styles.csv")
```

### `recommended_types(product_type)`

Returns the complementary product types configured for the selected product category.

```python
from recommendation_engine import recommended_types

types = recommended_types("Running Shoes")

print(types)
```

### `recommend(catalog, product_type, random_state=None)`

Selects one available catalog item for each complementary product type.

```python
from recommendation_engine import load_catalog, recommend

catalog = load_catalog("styles.csv")

recommendations = recommend(
    catalog,
    "Running Shoes",
    random_state=42,
)

print(recommendations)
```

---

## Experimental Implementation

The file:

```text
smart_product_recommendation_engine (2).py
```

is retained as a notebook-style exploratory script.

According to its current contents, it includes experiments involving:

* Interactive product recommendations
* Image extraction and display
* CSV export
* Catalog deduplication
* Sentence embeddings
* FAISS-based similarity search
* Image embeddings
* Reverse product/image search
* Experimental multimodal recommendation workflows

The experimental script also contains notebook-specific installation cells and imports additional packages such as:

* NumPy
* Matplotlib
* Pillow
* FAISS
* Sentence Transformers
* OpenCLIP
* PyTorch

The experimental script is **not required** to use the maintained rule-based recommendation API and is not covered by the lightweight test suite.

Treat it as a research prototype until its individual workflows are separated into modules with explicit dependency management and automated tests.

---

## Requirements

The maintained engine requires:

* Python 3.9 or newer
* pandas
* pytest for running the test suite

The current `requirements.txt` contains:

```text
pandas>=2.0
pytest>=8.0
```

Python 3.11 is used by the repository's GitHub Actions workflow.

---

## Installation

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_NAME>
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

#### Linux / macOS

```bash
source .venv/bin/activate
```

#### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 5. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

---

## Quick Start

The following example loads the included `styles.csv` catalog and recommends complementary products for running shoes:

```python
from recommendation_engine import load_catalog, recommend

catalog = load_catalog("styles.csv")

recommendations = recommend(
    catalog,
    "Running Shoes",
    random_state=42,
)

print(
    recommendations[
        ["id", "articleType", "productDisplayName"]
    ]
)
```

The result contains at most one product for each complementary product type that is available in the catalog.

Using:

```python
random_state=42
```

ensures that repeated runs against the same catalog produce the same selections.

---

## Python API

### Load a Catalog

```python
from recommendation_engine import load_catalog

catalog = load_catalog("styles.csv")
```

`load_catalog()` reads the CSV file using pandas.

It:

1. Loads the catalog.
2. Skips malformed CSV rows using pandas' `on_bad_lines="skip"` behavior.
3. Verifies that the required `id` and `articleType` columns exist.
4. Removes rows where either required value is missing.
5. Resets the DataFrame index.
6. Preserves additional catalog columns.

The included `styles.csv` contains additional fashion metadata such as:

* `gender`
* `masterCategory`
* `subCategory`
* `articleType`
* `baseColour`
* `season`
* `year`
* `usage`
* `productDisplayName`

Only the following columns are required by the maintained engine:

```text
id
articleType
```

---

## Inspect Recommendation Rules

You can inspect the complementary product categories associated with a product type using `recommended_types()`:

```python
from recommendation_engine import recommended_types

print(recommended_types("Running Shoes"))
```

For example, a product type may return complementary categories such as:

```text
['Track Pants', 'T-shirts', 'Socks']
```

The exact output depends on the rules defined in `RECOMMENDATION_RULES`.

---

## Make Recommendations

```python
from recommendation_engine import load_catalog, recommend

catalog = load_catalog("styles.csv")

result = recommend(
    catalog,
    "Running Shoes",
    random_state=42,
)

print(result)
```

The recommendation algorithm:

1. Normalizes the requested product type.
2. Looks up its complementary product types.
3. Filters the catalog to products matching each complementary type.
4. Removes unavailable or incomplete records.
5. Selects at most one product for each category.
6. Returns the selected products as a pandas DataFrame.

---

## Example Workflow

```text
CSV Product Catalog
        │
        ▼
   load_catalog()
        │
        ▼
 Validate Required Columns
        │
        ▼
 Normalize Product Type
        │
        ▼
 RECOMMENDATION_RULES
        │
        ▼
 Find Complementary Categories
        │
        ▼
 Filter Available Products
        │
        ▼
 Select One Product per Category
        │
        ▼
 Recommendations DataFrame
```

---

## Handling Unknown Product Types

If the requested product type does not exist in the recommendation rules, the engine returns an empty result rather than raising an exception.

Example:

```python
from recommendation_engine import load_catalog, recommend

catalog = load_catalog("styles.csv")

result = recommend(
    catalog,
    "Unknown Product",
    random_state=42,
)

print(result)
```

This makes the API safer for applications where product types may come from user input.

---

## Testing

The repository uses `pytest` for automated testing.

Run the complete test suite with:

```bash
pytest
```

You can also run:

```bash
python -m pytest
```

The tests cover areas including:

* Product-type normalization
* Recommendation rule lookup
* CSV validation
* Missing required columns
* Missing values
* Product filtering
* Unknown product types
* Recommendation output behavior
* Random-state behavior

---

## Continuous Integration

GitHub Actions is configured to run the test suite automatically.

The workflow is located at:

```text
.github/workflows/tests.yml
```

Tests run on:

* Pushes to `main`
* Pull requests targeting `main`

The CI environment currently uses:

```text
Python 3.11
```

This helps ensure that changes do not break the maintained implementation.

---

## Extending Recommendation Rules

The recommendation system is intentionally rule-based so that new product relationships can be added without modifying the core recommendation algorithm.

The rules are stored in:

```python
RECOMMENDATION_RULES
```

A new rule can be added by defining a product type and its complementary categories.

For example:

```python
RECOMMENDATION_RULES = {
    "Running Shoes": [
        "Track Pants",
        "T-shirts",
        "Socks",
    ],

    "Formal Shoes": [
        "Formal Trousers",
        "Shirts",
        "Belts",
    ],
}
```

After adding a new rule, corresponding tests should also be added to verify the expected behavior.

---

## Design Philosophy

The maintained implementation intentionally avoids unnecessary complexity.

Instead of requiring a machine-learning pipeline, embeddings, or deep-learning models, it uses:

```text
CSV Catalog
    ↓
Product Type
    ↓
Recommendation Rules
    ↓
Catalog Filtering
    ↓
Random Selection
    ↓
Recommended Products
```

This makes the engine:

* Lightweight
* Easy to understand
* Easy to test
* Easy to deploy
* Easy to extend
* Suitable for small fashion catalogs
* Suitable as a foundation for a larger recommendation system

---

## Future Improvements

Potential future improvements include:

* User preference-based recommendations
* Product similarity scoring
* Price-aware recommendations
* Brand compatibility
* Colour matching
* Size availability
* Popularity-based ranking
* Collaborative filtering
* Content-based recommendation
* Image similarity
* Text embeddings
* Multimodal product embeddings
* Personalized recommendations
* Recommendation confidence scores
* REST API integration
* Web-based recommendation interface

These features can be developed separately without changing the lightweight rule-based implementation.

---

## Limitations

The maintained engine is intentionally simple and therefore has several limitations:

* It does not learn from user behaviour.
* It does not use historical purchase data.
* It does not calculate personalized recommendations.
* It does not perform semantic product similarity.
* It does not analyze product images.
* Recommendations depend on manually defined product-type rules.
* Product availability is limited to the supplied CSV catalog.

The experimental notebook contains approaches that may address some of these limitations, but those workflows are not currently part of the maintained API.

---

## Contributing

When contributing to the maintained implementation:

1. Keep the core API small and reusable.
2. Add tests for new behavior.
3. Avoid introducing experimental dependencies into the maintained implementation unless necessary.
4. Update the recommendation rules carefully.
5. Run the complete test suite before submitting changes.

Run:

```bash
pytest
```

before creating a pull request.

---

## License

Add the project's license information here.

For example:

```text
MIT License
```

If the repository does not currently have a license, add a `LICENSE` file before publishing the project for external use.

---

## Summary

The project provides a lightweight and reusable rule-based recommendation engine for fashion product catalogs.

The main implementation is:

```text
recommendation_engine.py
```

The experimental research workflow is:

```text
smart_product_recommendation_engine (2).py
```

For normal usage, testing, and integration, use **`recommendation_engine.py`**.
