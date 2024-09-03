import pandas as pd
from pathlib import Path

df = pd.read_csv('./drug_links.csv')
print(df.shape)

# add "data_source" colomn
df['data_resource'] ='DrugBank'

# if we don't have the CUSTOM subdirectory, create it
Path("CUSTOM").mkdir(exist_ok=True)

df.to_csv("./CUSTOM/drug_links.tsv", sep="\t", header=True, index=False)
print(df.shape)