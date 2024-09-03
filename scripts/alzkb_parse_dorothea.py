import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri

# dorothea
# Defining the R script and loading the instance in Python (create and save R script in Rstudio)
r = robjects.r
r['source']('./dorothea.R')

# Loading the function we have defined in R.
#list(robjects.globalenv.keys())
net_r = robjects.globalenv['net']

#r to pandas dataframe 
import rpy2.robjects as ro
with (ro.default_converter + pandas2ri.converter).context():
  dorothea = ro.conversion.get_conversion().rpy2py(net_r)
#dorothea['source'].nunique() #643 TFs 


#trrust
trrust_rawdata = pd.read_csv('./trrust_rawdata.human.tsv', sep='\t', header=None, names=["TF","Gene","Interaction","PMID"])
#trrust_rawdata['TF'].nunique() #795 TFs matches with https://www.grnpedia.org/trrust/downloadnetwork.php


#combine
df_comb = trrust_rawdata.merge(dorothea, left_on=["TF","Gene"], right_on=["source","target"], how='inner')
df_comb['sourceDB'] ='DoRothEA & TRRUST'
df_comb.to_csv('./tf.tsv', sep="\t", header=True, index=False)