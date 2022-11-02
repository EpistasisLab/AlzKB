# AlzKB (http://alzkb.ai/)

A knowledge base for AI research in Alzheimer Disease, based on graph databases. 

### Authors

AlzKB is designed and developed by the following authors (in alphabetical order):

- Britney Graham, PhD (Cedars-Sinai)
- Yun Hao, MS (UPenn)
- Rachit Kumar (UPenn)
- Xi Li, MD (Cedars-Sinai)
- Nick Matsumoto (Cedars-Sinai)
- Jason H. Moore, PhD, FACMI (Cedars-Sinai)
- Marylyn Ritchie, PhD (UPenn)
- Joseph D. Romano, PhD (UPenn)
- Li Shen, PhD, FAIMBE (UPenn)
- Van Truong, MS (UPenn)
- Mythreye Venkatesan, MS (Cedars-Sinai)
- Paul Wang, PhD (Cedars-Sinai)


## Prerequisites

- Python (version 3.7 or later)
- Instance of Neo4j with `n10s` (v4.2 or greater) plugin installed

## Installation

To build a copy of AlzKB's graph database, you can either:

- Download a dump of the Neo4j database and import it into Neo4j

- Build the knowledge base from its original third-party sources and populate
  an empty Neo4j graph database

### Install from database dump (easy)

- Before doing anything else, make sure you have an up-to-date version of Neo4j
  installed on the new database server. This can be Neo4j Desktop or Neo4j
  Server, depending on your intended use.

- Visit the [Releases page](https://github.com/EpistasisLab/AlzKB/releases) and
  find the version of AlzKB you want to install. Unless you have a particular
  reason to do otherwise, this should probably be the most recent release.
  Follow the link in the release notes to the corresponding database dump (it
  will redirect to an external page).

- Once you have downloaded the dump, extract the archive. 

- If you haven't already done so, create an empty database in Neo4j.

- Stop any running Neo4j database instances (you can only import the dump when
  the destination database is shut down).

- Use the `neo4j-admin` utility (included with Neo4j) to import the database
  from the dump. You may need to add the program to your `PATH` variable or
  similar; if using Neo4j Desktop you can open a terminal window from within the
  application and use `cd bin` to access the directory where the `neo4j-admin`
  program is located. **(If you are installing on Neo4j Server the following
  command needs to be run by the appropriate user; this is often `neo4j`)**
  Assuming that `neo4j-admin` is accessible in your current directory, an
  example import command for UNIX-based operating systems could look like this
  (substitute database name and dump location as needed):

  `$ neo4j-admin load --verbose --force --database=neo4j --from=~/Downloads/alzkb.dump`

- Start the Neo4j database and open it to verify everything looks good.

### Build from scratch (less easy)

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
