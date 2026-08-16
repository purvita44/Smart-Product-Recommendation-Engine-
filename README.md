# Smart Product Recommendation Engine



A lightweight, rule-based product recommendation engine for fashion catalogs stored as CSV files. The maintained implementation is intentionally small and reusable: it loads a catalog with pandas, maps a selected product type to complementary product types, and returns one available catalog item for each complement.



The repository also contains a larger exploratory Colab-exported script with experimental catalog deduplication, text/image embedding, and reverse image-search workflows. The reusable and tested entry point is **`recommendation_engine.py`**.



## Project status



| Component | Status | Description |

|---|---|---|

| Rule-based recommendations | Maintained | Tested, deterministic when a random seed is supplied, and suitable for reuse as a Python module |

| CSV catalog loading | Maintained | Validates the required `id` and `articleType` columns and removes incomplete rows |

| Exploratory notebook workflow | Experimental | Preserved in `smart_product_recommendation_engine (2).py`; includes additional ML and image-search experiments |

| Automated tests | Active | Pytest suite covering normalization, filtering, validation, and error behavior |

| Continuous integration | Active | GitHub Actions runs the test suite on pushes to `main` and pull requests using Python 3.11 |



## Features



The maintained engine provides case-insensitive product-type matching, configurable random selection, filtering to products that are actually available in the catalog, validation of required input columns, and a simple DataFrame-based API. Unknown product types return an empty result rather than raising an exception.



The current recommendation rules cover common product categories including running shoes, sports shoes, casual shoes, formal shoes, jeans, shirts, T-shirts, shorts, track pants, sandals, socks, wallets, belts, dresses, handbags, watches, sweatshirts, kurtas, and flip-flops. The rule table is defined in `RECOMMENDATION_RULES` and can be extended without changing the recommendation algorithm.



## Repository structure



```text

.

├── recommendation_engine.py

├── smart_product_recommendation_engine (2).py

├── styles.csv

├── data_labels.csv

├── requirements.txt

├── tests/

│   └── test_recommendation_engine.py

├── .github/workflows/

│   └── tests.yml

└── README.md

```



### Maintained implementation



`recommendation_engine.py` contains the reusable API:



- `load_catalog(path)` loads and validates a catalog CSV.
- 
- `recommended_types(product_type)` returns the complementary product types configured for the input category.
- 
- `recommend(catalog, product_type, random_state=None)` selects one available catalog row for each complementary type.
- 


### Experimental implementation



`smart_product_recommendation_engine (2).py` is retained as a notebook-style exploratory script. According to its current contents, it includes interactive recommendation experiments, image extraction/display, CSV export, catalog deduplication using sentence embeddings and FAISS, and reverse product search using image embeddings. It also contains notebook-specific installation cells and imports additional packages such as NumPy, Matplotlib, Pillow, FAISS, Sentence Transformers, OpenCLIP, and PyTorch.



The experimental script is **not required** to use the maintained rule-based API and is not covered by the lightweight test suite. Treat it as a research prototype until its workflows are separated into modules with explicit dependency management and tests.



## Requirements



The maintained engine requires Python 3.9 or newer because it uses modern type-annotation syntax. The repository’s current dependency file contains:



```text

pandas>=2.0

pytest>=8.0

```



Python 3.11 is the version used by the repository’s GitHub Actions workflow.



## Installation



Create a virtual environment, activate it, and install the repository dependencies:



```bash

python -m venv .venv

source .venv/bin/activate

python -m pip install --upgrade pip

python -m pip install -r requirements.txt

```



On Windows PowerShell, activate the environment with:



```powershell

.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip

python -m pip install -r requirements.txt

```



## Quick start



The following example loads the included `styles.csv` catalog and recommends complementary products for running shoes:



```python

from recommendation_engine import load_catalog, recommend



catalog = load_catalog("styles.csv")

recommendations = recommend(

    catalog,

    "Running Shoes",

    random_state=42,

)



print(recommendations[["id", "articleType", "productDisplayName"]])

```



The output contains at most one row for each complementary product type that is available in the catalog. With `random_state=42`, repeated runs against the same catalog produce the same selections.



## Python API



### Load a catalog



```python

from recommendation_engine import load_catalog



catalog = load_catalog("styles.csv")

```



`load_catalog()` reads the CSV with pandas, skips malformed rows using pandas’ `on_bad_lines="skip"` behavior, verifies that `id` and `articleType` exist, removes rows where either required value is missing, and resets the DataFrame index.



The included `styles.csv` contains richer fashion metadata, including fields such as `gender`, `masterCategory`, `subCategory`, `articleType`, `baseColour`, `season`, `year`, `usage`, and `productDisplayName`. Only `id` and `articleType` are required by the maintained engine; the additional columns are preserved in the returned DataFrame.



### Inspect recommendation rules



```python

from recommendation_engine import recommended_types






