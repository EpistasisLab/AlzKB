# !/usr/bin/env python
## created by Yun Hao and Joe Romano @MooreLab 2022
## This script parses DisGeNET gene-disease relationship data to extract relationships specific to Alzheimer's disease

# NOTE: This file must be run from the `disgenet/` directory containing the original TSV files referenced below!
# Both output files will be deposited into the `disgenet/CUSTOM/` directory.

import pandas as pd

from pathlib import Path

disgenet_df = pd.read_csv("./disease_mappings_to_attributes.tsv", sep="\t", header=0)
disgenet_do_df = pd.read_csv("./disease_mappings.tsv", sep="\t", header=0)

# case insensitive match
disgenet_ad_df = disgenet_df.loc[disgenet_df["name"].str.contains("Alzheimer",case=False),:]
cuis = list(disgenet_ad_df.diseaseId.unique())

# For adding disease ontology identifiers
disgenet_ad_do_df = disgenet_do_df.loc[disgenet_do_df.diseaseId.isin(cuis),:]

# clean data 
# Creutzfeldt-jakob disease (CJD) and Familial Alzheimer Disease (FAD) are different diseases but got merged to the same node in AlzKB because of disease mappings in DisGeNET file “UMLS CUI to several disease vocabularies” in which the DO of Creutzfeldt-Jakob disease is mapped to FAD. 
disgenet_ad_do_df = disgenet_ad_do_df[~((disgenet_ad_do_df['name']=='Familial Alzheimer Disease (FAD)') & (disgenet_ad_do_df['vocabularyName']=='Creutzfeldt-Jakob disease'))]

# add "data_source" & "unbiased" colomns
disgenet_ad_do_df['data_source'] ='DisGeNET'
disgenet_ad_df['data_source'] ='DisGeNET'

# if we don't have the CUSTOM subdirectory, create it
Path("CUSTOM").mkdir(exist_ok=True)

disgenet_ad_df.to_csv("./CUSTOM/disease_mappings_to_attributes_alzheimer.tsv", sep="\t", header=True, index=False)
disgenet_ad_do_df.to_csv("./CUSTOM/disease_mappings_alzheimer.tsv", sep="\t", header=True, index=False)