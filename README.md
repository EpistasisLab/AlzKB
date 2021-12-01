# AlzKB

A knowledge base for AI research in Alzheimer Disease, based on graph databases.

### Authors

AlzKB is designed and developed by the following authors (in alphabetical order):

- Yun Hao (UPenn)
- Jason H. Moore, PhD, FACMI (Cedars-Sinai)
- Joseph D. Romano, PhD (UPenn)
- Li Shen, PhD (UPenn)
- Van Truong (UPenn)

## Prerequisites

- Python (version 3.7 or later)
- Instance of Neo4j with `n10s` (v4.2 or greater) plugin installed

## Installation

(Note: Implementation not yet complete)

Install AlzKB:
```{bash}
$ pip install .
```

Download public data sources:
```{bash}
$ alzkb bootstrap
```

Build the RDF/XML knowledge base
```{bash}
$ alzkb build
```

Install knowledge base to an instance of Neo4j
```{bash}
$ alzkb install
```