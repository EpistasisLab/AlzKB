import pandas as pd
import os


path = './data/alzkb_v2-populated.csv'
df= pd.read_csv(path)
df= pd.concat([df,pd.DataFrame(columns=['sourceDB','unbiased','affinity_nM','p_fisher','z_score','correlation','score','confidence'])])

# hetionet-custom-edges.tsv
data_dir = "./AlzKB_Raw_Data"
hetionet_custom = pd.read_table(os.path.join(data_dir,'hetionet/hetionet-custom-edges.tsv'))

hetio_custom = {
    'CbG':'CHEMICALBINDSGENE', 
    'DrD':'DISEASEASSOCIATESWITHDISEASE', # no results
    'DlA':'DISEASELOCALIZESTOANATOMY',
    'DpS':'SYMPTOMMANIFESTATIONOFDISEASE'
}


affinity_nM = hetionet_custom[hetionet_custom['metaedge']=='CbG']
affinity_nM['xrefDrugbank'] = affinity_nM['source'].str.split('::').str[-1]
affinity_nM['xrefNcbiGene'] = affinity_nM['target'].str.split('::').str[-1].astype(int)
affinity_nM = affinity_nM.merge(df[['_id','xrefDrugbank']].rename(columns={'_id':'_start'}), on='xrefDrugbank', how='left')
affinity_nM = affinity_nM.merge(df[['_id','xrefNcbiGene']].rename(columns={'_id':'_end'}), on='xrefNcbiGene', how='left')
affinity_nM['_type'] = hetio_custom['CbG']
merged_df = df.merge(affinity_nM, on=['_start', '_end', '_type'], suffixes=('', '_new'), how='left')
for column in ['sourceDB', 'unbiased', 'affinity_nM']:
    df[column] = merged_df[column + '_new'].combine_first(df[column])
df.shape


disgenet = pd.read_table('./AlzKB_Raw_Data/disgenet/CUSTOM/disease_mappings_alzheimer.tsv')
disgenet = disgenet[disgenet['vocabulary']=='DO']


p_fisher_DlA = hetionet_custom[hetionet_custom['metaedge']=='DlA']

p_fisher_DlA['do_id'] = p_fisher_DlA['source'].str.split('::').str[-1].str.split(':').str[-1]
p_fisher_DlA['xrefUberon'] = p_fisher_DlA['target'].str.split('::').str[-1]

p_fisher_DlA = p_fisher_DlA.merge(disgenet, left_on='do_id', right_on= 'code')
p_fisher_DlA['_start'] = 'disease_'+p_fisher_DlA['diseaseId'].str.lower()
p_fisher_DlA = p_fisher_DlA.merge(df[['_id','xrefUberon']].rename(columns={'_id':'_end'}), on='xrefUberon', how='left')
p_fisher_DlA['_type'] = hetio_custom['DlA']

p_fisher_DpS = hetionet_custom[hetionet_custom['metaedge']=='DpS']

p_fisher_DpS['xrefMeSH'] = p_fisher_DpS['target'].str.split('::').str[-1]
p_fisher_DpS['do_id'] = p_fisher_DpS['source'].str.split('::').str[-1].str.split(':').str[-1]

p_fisher_DpS = p_fisher_DpS.merge(df[['_id','xrefMeSH']].rename(columns={'_id':'_start'}), on='xrefMeSH', how='left')
p_fisher_DpS = p_fisher_DpS.merge(disgenet, left_on='do_id', right_on= 'code')
p_fisher_DpS['_end'] = 'disease_'+p_fisher_DpS['diseaseId'].str.lower()
p_fisher_DpS['_type'] = hetio_custom['DpS']

p_fisher = pd.concat([p_fisher_DlA, p_fisher_DpS])

merged_df = df.merge(p_fisher, on=['_start', '_end', '_type'], suffixes=('', '_new'), how='left')
for column in ['sourceDB', 'unbiased', 'p_fisher']:
    df[column] = merged_df[column + '_new'].combine_first(df[column])
df.shape


# hetionet-v1.0-edges.sif
#https://github.com/dhimmel/integrate/blob/master/integrate.ipynb

import hetio.hetnet
import hetio.readwrite
import hetio.stats

path = 'https://raw.githubusercontent.com/dhimmel/integrate/master/data/hetnet.json.bz2'
graph = hetio.readwrite.read_graph(path, formatting=None)


#https://github.com/hetio/hetnetpy/blob/main/hetnetpy/readwrite.py
import collections
import operator
import pandas as pd

def write_nodetable(graph):
    """Write a tabular encoding of the graph nodes."""
    rows = list()
    for node in graph.node_dict.values():
        row = collections.OrderedDict()
        row["kind"] = node.metanode.identifier
        row["id"] = str(node)
        row["name"] = node.name
        row["source"] = node.data['source']
        rows.append(row)
    rows.sort(key=operator.itemgetter("kind", "id"))
    fieldnames = ["id", "name", "kind", "source"]
    df_nodes_tsv = pd.DataFrame(rows, columns=fieldnames)
    print(df_nodes_tsv.shape)
    return df_nodes_tsv


def write_edgetable(graph):
    """Write a tsv of the graph edges."""
    rows = list()
    edge_properties=["sourceDB", "unbiased", "affinity_nM", "z_score", "p_fisher", "correlation"]
    fieldnames =["source", "metaedge", "target"]
    fieldnames = fieldnames+edge_properties
    metaedge_to_edges = graph.get_metaedge_to_edges(exclude_inverts=True)
    for metaedge, edges in metaedge_to_edges.items():
        for edge in edges:
            row = collections.OrderedDict()
            row["source"] = edge.source
            row["metaedge"] = edge.metaedge.abbrev
            row["target"] = edge.target
            for pro in edge_properties:
                if pro =='sourceDB':
                    if 'source' in edge.data.keys():
                        row[pro]=edge.data['source']
                    else:
                        row[pro]=None
                else:
                    if pro in edge.data.keys():
                        row[pro]=edge.data[pro]
                    else:
                        row[pro]=None
            rows.append(row)
    df_edges_tsv = pd.DataFrame(rows, columns=fieldnames)
    print(df_edges_tsv.shape)
    return df_edges_tsv

hetionet = write_edgetable(graph)
hetionet['source']=hetionet['source'].astype(str)
hetionet['target']=hetionet['target'].astype(str)
hetionet

hetio = {
    'CuG':'CHEMICALINCREASESEXPRESSION', 
    'CdG':'CHEMICALDECREASESEXPRESSION',
    'GcG':'GENECOVARIESWITHGENE',
    'Gr>G':'GENEREGULATESGENE'
}


z_score = hetionet[hetionet['metaedge']=='CuG']
z_score['xrefDrugbank'] = z_score['source'].str.split('::').str[-1]
z_score['xrefNcbiGene'] = z_score['target'].str.split('::').str[-1].astype(int)

z_score = z_score.merge(df[['_id','xrefDrugbank']].rename(columns={'_id':'_start'}), on='xrefDrugbank', how='left')
z_score = z_score.merge(df[['_id','xrefNcbiGene']].rename(columns={'_id':'_end'}), on='xrefNcbiGene', how='left')
z_score['_type'] = hetio['CuG']

z_score_all = z_score

z_score = hetionet[hetionet['metaedge']=='CdG']
z_score['xrefDrugbank'] = z_score['source'].str.split('::').str[-1]
z_score['xrefNcbiGene'] = z_score['target'].str.split('::').str[-1].astype(int)

z_score = z_score.merge(df[['_id','xrefDrugbank']].rename(columns={'_id':'_start'}), on='xrefDrugbank', how='left')
z_score = z_score.merge(df[['_id','xrefNcbiGene']].rename(columns={'_id':'_end'}), on='xrefNcbiGene', how='left')
z_score['_type'] = hetio['CdG']

z_score_all = pd.concat([z_score_all,z_score])

merged_df = df.merge(z_score_all, on=['_start', '_end', '_type'], suffixes=('', '_new'), how='left')
for column in ['sourceDB', 'unbiased', 'z_score']:
    df[column] = merged_df[column + '_new'].combine_first(df[column])
df.shape


correlation = pd.read_table(os.path.join(data_dir,'hetionet/geneCovariesWithGene_correlation.tsv'))

correlation = correlation.merge(df[['_id','xrefNcbiGene']].rename(columns={'_id':'_start'}), left_on='source_entrez', right_on='xrefNcbiGene', how='left')
correlation = correlation.merge(df[['_id','xrefNcbiGene']].rename(columns={'_id':'_end'}), left_on='target_entrez', right_on='xrefNcbiGene', how='left')
correlation['_type'] = hetio['GcG']
correlation['sourceDB'] = 'Hetionet - ERC'
correlation['unbiased'] = True

merged_df = df.merge(correlation, on=['_start', '_end', '_type'], suffixes=('', '_new'), how='left')
for column in ['sourceDB', 'unbiased', 'correlation']:
    df[column] = merged_df[column + '_new'].combine_first(df[column])
df.shape
df.loc[~df['correlation'].isna()]


#DisGeNET
score = pd.read_table('./AlzKB_Raw_Data/disgenet/curated_gene_disease_associations.tsv')
score['sourceDB'] = 'DisGeNET - '+score['source']

score = score.merge(df[['_id','xrefNcbiGene']].rename(columns={'_id':'_start'}), left_on='geneId', right_on='xrefNcbiGene', how='left')
score['_end'] = 'disease_'+score['diseaseId'].str.lower()
score['_type'] = 'GENEASSOCIATESWITHDISEASE'

merged_df = df.merge(score, on=['_start', '_end', '_type'], suffixes=('', '_new'), how='left')
for column in ['sourceDB', 'score']:
    df[column] = merged_df[column + '_new'].combine_first(df[column])
df.shape


#TF
confidence = pd.read_table('./AlzKB_Raw_Data/dorothea/tf.tsv')
confidence

confidence = pd.read_table('./AlzKB_Raw_Data/dorothea/tf.tsv')

confidence = confidence.merge(df[['_id','TF']].rename(columns={'_id':'_start'}), on='TF', how='left')
confidence = confidence.merge(df[['_id','geneSymbol']].rename(columns={'_id':'_end'}), left_on='Gene', right_on='geneSymbol', how='left')

confidence['_type'] = 'TRANSCRIPTIONFACTORINTERACTSWITHGENE'

merged_df = df.merge(confidence, on=['_start', '_end', '_type'], suffixes=('', '_new'), how='left')
for column in ['sourceDB', 'confidence']:
    df[column] = merged_df[column + '_new'].combine_first(df[column])
df.shape

#save data file
df.to_csv('./data/alzkb_v2.0.0_with_edge_properties.csv')



