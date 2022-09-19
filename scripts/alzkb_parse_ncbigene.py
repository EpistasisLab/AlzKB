#!/usr/bin/env python3
## created by Van Truong @RitchieWherryLabs 2022
## This script parses NCBI human gene data and Bgee epxression data for knowledge related to Alzheimer's disease


my_set = set()

def processLargeTextFile(source, compare_index, separator):
    with open(source, "r") as r:
        for line in r:
            if 'brain' in line:
                columns = line.split(separator)
                my_set.add(columns[compare_index].replace('Ensembl:', '') )
    r.close()

def keepDesiredColums(row, keep_index, separator):
    columns = row.split(separator)

    output_str = []
    for index in keep_index:
        output_str.append(columns[index])

    return separator.join(output_str)

def filterLargeTextFile(source, destination, delimiter, keep_index):
    with open(source, "r") as r, open(destination, "w") as w:
        #load header row
        w.write(keepDesiredColums(r.readline(), keep_index, delimiter) + '\n')

        #load body
        for line in r:
            if line is not None:
                w.write(keepDesiredColums(line, keep_index, delimiter) + '\n')
    r.close(), w.close()

def fileIndexFinder(source, destination, keep_set, compare_column_index, separator):
    with open(source, "r") as r, open(destination, "w") as w:
        w.write('Ensembl' + separator +  r.readline())

        for line in r:
            columns = line.split(separator)
            parsed_column = columns[compare_column_index]

            if '|' in parsed_column:
                parsed_column_split = parsed_column.split('|')
                if len(parsed_column_split) > 2:
                    parsed_column = parsed_column_split[2].replace('Ensembl:', '')

            if parsed_column in keep_set:
                w.write(parsed_column + separator + line)
    r.close()


brain_file='./Homo_sapiens_expr_advanced_development.tsv' #https://bgee.org/?page=download&action=expr_calls#id1
gene_file='../Homo_sapiens.gene_info' #https://ftp.ncbi.nlm.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz
gene_dest_file='./Homo_sapiens.gene_info_filtered'

final_out='./output.tsv'

delimiter = '\t'
keep_index = [1,2,4,5,6,8,9]
compare_index = 0

processLargeTextFile(brain_file, compare_index, delimiter)

filterLargeTextFile(gene_file, gene_dest_file, delimiter, keep_index)

fileIndexFinder(gene_dest_file, final_out, my_set, 3,  delimiter)