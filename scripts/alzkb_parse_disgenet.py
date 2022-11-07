# !/usr/bin/env python
## created by Yun Hao and Joe Romano @MooreLab 2022
## This script parses DisGeNET gene-disease relationship data to extract relationships specific to Alzheimer's disease

# NOTE: This file must be run from the `disgenet/` directory containing the original TSV files referenced below!
# Both output files will be deposited into the `disgenet/CUSTOM/` directory.

import pandas as pd

from pathlib import Path

disgenet_df = pd.read_csv("./disease_mappings_to_attributes.tsv", sep="\t", header=0)
disgenet_do_df = pd.read_csv("./disease_mappings.tsv", sep="\t", header=0)

disgenet_ad_df = disgenet_df.loc[disgenet_df["name"].str.contains("Alzheimer"),:]
cuis = list(disgenet_ad_df.diseaseId.unique())

# For adding disease ontology identifiers
disgenet_ad_do_df = disgenet_do_df.loc[disgenet_do_df.diseaseId.isin(cuis),:]

# if we don't have the CUSTOM subdirectory, create it
Path("CUSTOM").mkdir(exist_ok=True)

disgenet_ad_df.to_csv("./CUSTOM/disease_mappings_to_attributes_alzheimer.tsv", sep="\t", header=True, index=False)
disgenet_ad_do_df.to_csv("./CUSTOM/disease_mappings_alzheimer.tsv", sep="\t", header=True, index=False)