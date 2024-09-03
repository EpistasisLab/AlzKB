#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
from gqlalchemy import Memgraph
import owlready2


#read RDF
path = './data/alzkb_v2-populated.rdf'
onto = owlready2.get_ontology(path).load()


#Load node and property
def extract_node_details(label, node):
    details = {
        '_id': node.name,
        '_labels': label,
        'commonName': node.commonName if node.commonName else np.nan,
        'geneSymbol': node.geneSymbol if node.geneSymbol else np.nan,
        'pathwayId': node.pathwayId if node.pathwayId else np.nan,
        'pathwayName': node.pathwayName if node.pathwayName else np.nan,
        'sourceDatabase': node.sourceDatabase if node.sourceDatabase else np.nan,
        'typeOfGene': node.typeOfGene if node.typeOfGene else np.nan,
        'chromosome': node.chromosome if node.chromosome else np.nan,
        'TF': node.TF if node.TF else np.nan,
        'xrefCasRN': node.xrefCasRN if node.xrefCasRN else np.nan,
        'xrefDiseaseOntology': node.xrefDiseaseOntology if node.xrefDiseaseOntology else np.nan,
        'xrefDrugbank': node.xrefDrugbank if node.xrefDrugbank else np.nan,
        'xrefEnsembl': node.xrefEnsembl if node.xrefEnsembl else np.nan,
        'xrefGeneOntology': node.xrefGeneOntology if node.xrefGeneOntology else np.nan,
        'xrefHGNC': node.xrefHGNC if node.xrefHGNC else np.nan,
        'xrefMeSH': node.xrefMeSH if node.xrefMeSH else np.nan,
        'xrefNcbiGene': node.xrefNcbiGene if node.xrefNcbiGene else np.nan,
        'xrefNciThesaurus': node.xrefNciThesaurus if node.xrefNciThesaurus else np.nan,
        'xrefOMIM': node.xrefOMIM if node.xrefOMIM else np.nan,
        'xrefUberon': node.xrefUberon if node.xrefUberon else np.nan,
        'xrefUmlsCUI': node.xrefUmlsCUI if node.xrefUmlsCUI else np.nan
    }
    
    for key, value in details.items():
        if isinstance(value, list) and len(value) > 0:
            try:
                details[key] = str(value[-1])
            except ValueError:
                details[key] = np.nan
        elif isinstance(value, list):
            details[key] = np.nan
            
    return details


#Drug 
drug_details_list = []
for drug in onto.individuals():
    if onto.Drug in drug.is_a:
        drug_details_list.append(extract_node_details(':Drug', drug))
drug_details_df = pd.DataFrame(drug_details_list)


#Gene 
gene_details_list = []
for gene in onto.individuals():
    if onto.Gene in gene.is_a:
        gene_details_list.append(extract_node_details(':Gene', gene))
gene_details_df = pd.DataFrame(gene_details_list)


#BodyPart
bodypart_details_list = []
for bodypart in onto.individuals():
    if onto.BodyPart in bodypart.is_a:
        bodypart_details_list.append(extract_node_details(':BodyPart', bodypart))
bodypart_details_df = pd.DataFrame(bodypart_details_list)


#Disease
disease_details_list = []
for disease in onto.individuals():
    if onto.Disease in disease.is_a:
        disease_details_list.append(extract_node_details(':Disease', disease))
disease_details_df = pd.DataFrame(disease_details_list)


#DrugClass
drugclass_details_list = []
for drugclass in onto.individuals():
    if onto.DrugClass in drugclass.is_a:
        drugclass_details_list.append(extract_node_details(':DrugClass', drugclass))
drugclass_details_df = pd.DataFrame(drugclass_details_list)


#CellularComponent
cellular_details_list = []
for cellular in onto.individuals():
    if onto.CellularComponent in cellular.is_a:
        cellular_details_list.append(extract_node_details(':CellularComponent', cellular))
cellular_details_df = pd.DataFrame(cellular_details_list)


#MolecularFunction 
molecular_details_list = []
for molecular in onto.individuals():
    if onto.MolecularFunction in molecular.is_a:
        molecular_details_list.append(extract_node_details(':MolecularFunction', molecular))
molecular_details_df = pd.DataFrame(molecular_details_list)


#Pathway
pathway_details_list = []
for pathway in onto.individuals():
    if onto.Pathway in pathway.is_a:
        pathway_details_list.append(extract_node_details(':Pathway', pathway))
pathway_details_df = pd.DataFrame(pathway_details_list)


#BiologicalProcess
biological_details_list = []
for biological in onto.individuals():
    if onto.BiologicalProcess in biological.is_a:
        biological_details_list.append(extract_node_details(':BiologicalProcess', biological))
biological_details_df = pd.DataFrame(biological_details_list)


#Symptom
symptom_details_list = []
for symptom in onto.individuals():
    if onto.Symptom in symptom.is_a:
        symptom_details_list.append(extract_node_details(':Symptom', symptom))
symptom_details_df = pd.DataFrame(symptom_details_list)


# TranscriptionFactor
transcription_details_list = []
for transcriptionfactor in onto.individuals():
    if onto.TranscriptionFactor in transcriptionfactor.is_a:
        transcription_details_list.append(extract_node_details(':TranscriptionFactor', transcriptionfactor))
transcription_details_df = pd.DataFrame(transcription_details_list)


#Merge all nodes df
merged_node_df = pd.concat([drug_details_df, gene_details_df, bodypart_details_df, disease_details_df, 
                       drugclass_details_df, cellular_details_df, molecular_details_df, pathway_details_df, 
                       biological_details_df, symptom_details_df, transcription_details_df], ignore_index=True)
merged_node_df.reset_index(drop=True, inplace=True)
merged_node_df.shape 


#Load relationship

#Drug
relations = []
def extract_rel_details_from_drug(node):
    for gene in node.chemicalBindsGene:
        relations.append({
            '_start': node.name,
            '_end': gene.name,
            '_type': 'CHEMICALBINDSGENE'})
    for gene in node.chemicalDecreasesExpression:
        relations.append({
            '_start': node.name,
            '_end': gene.name,
            '_type': 'CHEMICALDECREASESEXPRESSION'})
    for gene in node.chemicalIncreasesExpression:
        relations.append({
            '_start': node.name,
            '_end': gene.name,
            '_type': 'CHEMICALINCREASESEXPRESSION'})
    for disease in node.drugCausesEffect:
        relations.append({
            '_start': node.name,
            '_end': disease.name,
            '_type': 'DRUGCAUSESEFFECT'})
    for disease in node.drugTreatsDisease:
        relations.append({
            '_start': node.name,
            '_end': disease.name,
            '_type': 'DRUGTREATSDISEASE'})
    for drugclass in node.drugInClass:
        relations.append({
            '_start': node.name,
            '_end': drugclass.name,
            '_type': 'DRUGINCLASS'})
            

for drug in onto.individuals():
    if onto.Drug in drug.is_a:
        extract_rel_details_from_drug(drug)

drug_rel = pd.DataFrame(relations)


#Gene
relations = []
def extract_rel_details_from_gene(node):
    for cellular in node.geneAssociatedWithCellularComponent:
        relations.append({
            '_start': node.name,
            '_end': cellular.name,
            '_type': 'GENEASSOCIATEDWITHCELLULARCOMPONENT'})
    for disease in node.geneAssociatesWithDisease:
        relations.append({
            '_start': node.name,
            '_end': disease.name,
            '_type': 'GENEASSOCIATESWITHDISEASE'})
    for molecular in node.geneHasMolecularFunction:
        relations.append({
            '_start': node.name,
            '_end': molecular.name,
            '_type': 'GENEHASMOLECULARFUNCTION'})
    for biological in node.geneParticipatesInBiologicalProcess:
        relations.append({
            '_start': node.name,
            '_end': biological.name,
            '_type': 'GENEPARTICIPATESINBIOLOGICALPROCESS'})
            

for gene in onto.individuals():
    if onto.Gene in gene.is_a:
        extract_rel_details_from_gene(gene)

gene_rel = pd.DataFrame(relations)


# #### geneInteractsWithGene (to avoid inverse property problem)
from rdflib import Graph, URIRef

g = Graph()

rdf_file = path
g.parse(rdf_file, format='xml')

pred_uri_1 = URIRef('http://jdr.bio/ontologies/alzkb.owl#geneCovariesWithGene')
pred_uri_2 = URIRef('http://jdr.bio/ontologies/alzkb.owl#geneInteractsWithGene')
pred_uri_3 = URIRef('http://jdr.bio/ontologies/alzkb.owl#geneRegulatesGene')
pred_uri_4 = URIRef('http://jdr.bio/ontologies/alzkb.owl#geneInPathway')

def extract_last_part(uri):
    return uri.split('#')[-1]

triples = []
for subj, pred, obj in g:
    if pred == pred_uri_1:
        triples.append([extract_last_part(subj), 'GENECOVARIESWITHGENE', extract_last_part(obj)])
    elif pred == pred_uri_2:
        triples.append([extract_last_part(subj), 'GENEINTERACTSWITHGENE', extract_last_part(obj)])
    elif pred == pred_uri_3:
        triples.append([extract_last_part(subj), 'GENEREGULATESGENE', extract_last_part(obj)])
    elif pred == pred_uri_4:
        triples.append([extract_last_part(subj), 'GENEINPATHWAY', extract_last_part(obj)])

gene_rel2 = pd.DataFrame(triples, columns=['_start', '_type', '_end'])

#Merge gene rel and rel2
gene_rel2 = gene_rel2[gene_rel.columns]
gene_rel = pd.concat([gene_rel, gene_rel2], ignore_index=True)


#Body Part
relations = []
def extract_rel_details_from_bodypart(node):
    for gene in node.bodyPartOverexpressesGene:
        relations.append({
            '_start': node.name,
            '_end': gene.name,
            '_type': 'BODYPARTOVEREXPRESSESGENE'})
    for gene in node.bodyPartUnderexpressesGene:
        relations.append({
            '_start': node.name,
            '_end': gene.name,
            '_type': 'BODYPARTUNDEREXPRESSESGENE'})
            

for bodypart in onto.individuals():
    if onto.BodyPart in bodypart.is_a:
        extract_rel_details_from_bodypart(bodypart)

bodypart_rel = pd.DataFrame(relations)


#Disease
relations = []
def extract_rel_details_from_disease(node):
    for disease in node.diseaseAssociatesWithDisease:
        relations.append({
            '_start': node.name,
            '_end': disease.name,
            '_type': 'DISEASEASSOCIATESWITHDISEASE'})
    for bodypart in node.diseaseLocalizesToAnatomy:
        relations.append({
            '_start': node.name,
            '_end': bodypart.name,
            '_type': 'DISEASELOCALIZESTOANATOMY'})
            

for disease in onto.individuals():
    if onto.Disease in disease.is_a:
        extract_rel_details_from_disease(disease)

disease_rel = pd.DataFrame(relations)


#Symptom
relations = []
def extract_rel_details_from_symptom(node):
    for disease in node.symptomManifestationOfDisease:
        relations.append({
            '_start': node.name,
            '_end': disease.name,
            '_type': 'SYMPTOMMANIFESTATIONOFDISEASE'})
            

for symptom in onto.individuals():
    if onto.Symptom in symptom.is_a:
        extract_rel_details_from_symptom(symptom)

symptom_rel = pd.DataFrame(relations)


# Transcription Factor
relations = []
def extract_rel_details_from_transcriptionfactor(node):
    for transcriptionfactor in node.transcriptionFactorInteractsWithGene:
        relations.append({
            '_start': node.name,
            '_end': transcriptionfactor.name,
            '_type': 'TRANSCRIPTIONFACTORINTERACTSWITHGENE'})
            

for transcriptionfactor in onto.individuals():
    if onto.TranscriptionFactor in transcriptionfactor.is_a:
        extract_rel_details_from_transcriptionfactor(transcriptionfactor)

transcriptionfactor_rel = pd.DataFrame(relations)


#Merge all rels df
merged_rel_df = pd.concat([drug_rel, gene_rel, bodypart_rel, disease_rel, symptom_rel, transcriptionfactor_rel], ignore_index=True)
merged_rel_df.reset_index(drop=True, inplace=True)
merged_rel_df.shape 


#Merge node and rel
df_all = pd.concat([merged_node_df, merged_rel_df], axis=0, ignore_index=True)
df_all.to_csv('./data/alzkb_v2-populated.csv', index=False)




