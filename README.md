# AlzKB (http://alzkb.ai/)

A knowledge base for AI research in Alzheimer Disease, based on graph databases. 
![image](https://github.com/user-attachments/assets/4106ebe7-0d36-4fc6-a360-5174597f6f7b)

_Please note DRUGCAUSESEFFECT in AlzKB refers to drug causes of side effects._

### Authors

AlzKB is designed and developed by the following authors (in alphabetical order):

- Britney Graham, PhD (Cedars-Sinai)
- Yun Hao, MS (UPenn)
- Rachit Kumar (UPenn)
- Xi Li, MD (Cedars-Sinai)
- Nick Matsumoto (Cedars-Sinai)
- Jason H. Moore, PhD, FACMI (Cedars-Sinai)
- Jay Moran, MS (Cedars-Sinai)
- Marylyn Ritchie, PhD (UPenn)
- Joseph D. Romano, PhD (UPenn)
- Li Shen, PhD, FAIMBE (UPenn)
- Van Truong, MS (UPenn)
- Mythreye Venkatesan, MS (Cedars-Sinai)
- Paul Wang, PhD (Cedars-Sinai)


## Deprication Note
Versions of AlzKB prior to v1.3.0 used Neo4j. Use of Neo4j is now depricated. Legacy versions of the knowledge graph will continue to be provided in the Releases page to support existing research.  

## Prerequisites
- Memgraph Lab (Desktop application)
    - Starting with AlzKB v1.3.0, Memgraph is used as the knowledge graph server.
    - Memgraph offers a variety of [installation options](https://memgraph.com/docs/getting-started/install-memgraph).
    - Memgraph Lab is the easiest way to get up and running with AlzKB. But you may use Memgraph Server if your deployment requires it.
- Python (version 3.7 or later)

## Installation

To build a copy of AlzKB's graph database, you can either:
- Download a copy of the latest CYPHERL file and import it into Memgraph
- Build the knowledge base from its original third-party sources and import it into Memgraph

### Install from CYPHERL file (easy)
- Visit the [Releases page](https://github.com/EpistasisLab/AlzKB/releases) and find the version of AlzKB you want to install. Unless you have a particular reason to do otherwise, this should probably be the most recent release. Follow the link in the release notes to the corresponding database dump (it will redirect to an external page).
- Using Memgraph Lab, import the downloaded CYPHERL file by navigating to _Import & Export_ and then click the _Import Data_ button.
    - For other ways to import the CYPHERL file into a Memgraph server, see [here](https://memgraph.com/docs/data-migration/cypherl)
- In Memgraph Lab, navigate to _Query execution_ to start querying the knowledge graph.

### Build from scratch (less easy)

**For detailed instructions on building AlzKB from scratch, see [here](https://github.com/EpistasisLab/AlzKB/blob/master/BUILD.org)**

Start by installing the Python package, which includes the necessary scripts:

```{bash}
$ git clone https://github.com/EpistasisLab/AlzKB
$ cd AlzKB
$ pip install .
```

#### Download the third-party database sources

First, install MySQL and make sure it is running, as some of the source
databases are only available as MySQL dumps.

We've created a script that will fetch all of the source files and put them into
the expected directory structure. We will try to keep this script as updated as
possible, but if you encounter any issues we suggest looking at the script and
making sure it points to entities that still exist.

```{bash}
$ alzkb bootstrap
```

#### Populate the ontology

We use the external `ista` library to populate the OWL ontology. This should
be pretty much entirely automated:

```{bash}
$ alzkb build
```

#### Load the ontology contents into Neo4j

This script will import the OWL 2 ontology contents into an empty Neo4j database
and clean up unnecessary artifacts left over by the OWL 2 standard:

```{bash}
$ alzkb install
```

After this, check the Neo4j database (which will now be turned on) and make sure
everything looks alright.
