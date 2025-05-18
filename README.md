# Magnetic Field in the Universe

A **Python‑based data manager** for working with tabulated data from publications of observational surveys of cosmic magnetic fields. Instead of hosting large data files, this repo gives you the **scripts, parsers, and notebooks** you need to download, standardize, and compare datasets from the literature (dust polarimetry, Zeeman splitting, Faraday rotation, and more).

---

## Goals

* Provide **reproducible Python pipelines** that turn publication data products into clean, science‑ready tables on your own machine.
* Make it simple to **build your data collection** and keep it in sync with new survey releases.
* Enable **cross‑comparison** between magnetic‑field-related quantities from different publications or surveys.
* Serve as a lightweight, community‑maintained magnetic-field-in-the-universe research knowledge base.

---
## Quick Start Notebook
github installation of magUniverse is available:

|                             **Logo**                              | **Platform** |                                    **Command**                                    |
|:-----------------------------------------------------------------:|:------------:|:---------------------------------------------------------------------------------:|
|     ![GitHub logo](https://simpleicons.org/icons/github.svg)      |    GitHub    | ``python -m pip install https://github.com/xli2522/magUniverse/archive/refs/heads/main.zip`` |

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
│── maguniverse/
│   ├── data/                  # Get raw data and convert to tidy CSV, TXT, … 
│   │   ├── polarization/      # CSO, JCMT, ALMA, Planck, …
│   │   ├── zeeman/            # Crutcher catalog, OH/NH3, …
│   │   ├── faraday/           # RM grids, LOFAR, ASKAP, …
│   │   └── gas/               # NRAO, Haystack, Effelsberg, …
│   │
│   ├── utils/                 # Python helpers
│   │   └── fetch_ascii.py      # Scripts to fetch raw ascii data from online repositories
│   │
│   └── datafiles/             # User copy of data
│
├── notebooks/                 # Jupyter demo notebooks
│   └── 00_quickstart.ipynb    # 15‑min tour of the toolbox
│
├── docs/                      # Longer‑form docs & rendered HTML
│   └── index.html
│
├── tests/                     # Unit tests for parsers
├── examples/                  # Mini‑projects / tutorials
├── requirements.txt           # Lists the Python dependencies for the project
├── CONTRIBUTING.md            # How to add code or docs
├── LICENSE                    # MIT
└── README.md                  # ← you are here
```
