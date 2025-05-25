# Magnetic Field in the Universe

A **Python‑based data manager** for working with tabulated data from publications of observational surveys of cosmic magnetic fields. Instead of hosting large data files, this repo gives you the **scripts, parsers, and notebooks** you need to download, standardize, and compare datasets from the literature (dust polarimetry, Zeeman splitting, Faraday rotation, and more).

---

## Goals

* Provide **reproducible Python pipelines** that turn publication data products into clean, science‑ready tables on your own machine.
* Make it simple to **build your data collection** and keep it in sync with new survey releases.
* Enable **cross‑comparison** between magnetic‑field-related quantities from different publications or surveys.
* Serve as a lightweight, community‑maintained magnetic-field-in-the-universe research knowledge base.

---
## Download all the Data You Want In Your Browser
magUniverse now offers [browser-based data downloads](https://xli2522.github.io/magUniverse/) powered by [Pyodide](https://pyodide.org/en/stable/index.html). This eliminates the need for local Python installation or environment setup.

### Technical Details
* WebAssembly Python through Pyodide
* Automatic magUniverse installation via Pypi or the latest CI build wheel
* Direct file downloads inside your browser

---
## Quick Start Notebook
github installation of magUniverse is available:

|                             **Logo**                              | **Platform** |                                    **Command**                                    |
|:-----------------------------------------------------------------:|:------------:|:---------------------------------------------------------------------------------:|
|     ![GitHub logo](https://simpleicons.org/icons/github.svg)      |    GitHub    | ``python -m pip install https://github.com/xli2522/magUniverse/archive/refs/heads/main.zip`` |
|     ![Pypi logo](https://pypi.org/static/images/logo-small.8998e9d1.svg)      |    Pypi    | ``python pip install maguniverse`` |

Or setup the development repo via setup.py
```bash
$ cd ./magUniverse
$ python setup.py install
```

After installation, go through the examples in [notebooks\00_quickstart.ipynb](https://github.com/xli2522/magUniverse/blob/main/notebooks/00_quickstart.ipynb) for a quick start.

---
## Repository layout *(subject to change)*

```
magUniverse-master
├── .github/workflows          # Github workflow files
│   ├── main.yml               # Auto update manifest, CI build, and magUniverse Paper Collection Website
│   ├── python-publish.yml     # Auto publish to Pypi on release
│   └── deploy_gh_pages.yml    # Auto deploy magUniverse Paper Collection Website
│
│── maguniverse/
│   ├── data/                  # Get raw data and convert to tidy CSV, TXT, … 
│   │   ├── polarization/      # CSO, JCMT, ALMA, Planck, …
│   │   ├── zeeman/            # Crutcher catalog, OH/NH3, …
│   │   ├── faraday/           # RM grids, LOFAR, ASKAP, …
│   │   └── gas/               # NRAO, Haystack, Effelsberg, …
│   │
│   ├── utils/                 # Python helpers
│   │   ├── fetch_ascii.py     # Scripts to fetch raw ascii data from online repositories
│   │   └── ...                # other advanced tools
│   │
│   ├── service/               # Simplified minimalistic data table methods
│   │   └── get.py             # Minimalistic data table getters (wrappers of data/**/getters)
│   │
│   └── datafiles/             # User copy of data
│
├── notebooks/                 # Jupyter demo notebooks
│   └── 00_quickstart.ipynb    # 15‑min tour of the toolbox
│
├── docs/                      # Longer‑form docs & rendered HTML
│   ├── manifest.json/         # JSON of magUniverse metadata and getter methods
│   ├── docs/**.whl            # CI build latest wheel
│   └── index.html             # Main magUniverse website
│
├── examples/                  # Mini‑projects / tutorials
│   └── generate_manifest.py   # Manifest of all magUniverse getter methods
│
├── tests/                     # Unit tests for parsers
├── requirements.txt           # Lists the Python dependencies for the project
├── CONTRIBUTING.md            # How to add code or docs
├── LICENSE                    # MIT
├── setup.py                   # Allow pip-install via ZIP
└── README.md                  # ← you are here
```
