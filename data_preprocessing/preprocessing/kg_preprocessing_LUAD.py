import pandas as pd

kg_path = '../../data/SL/raw/kg_triplet.csv'
sl_path = '../../data/SL/cancertype_data/sl2LUAD.csv'

kg_save = '../../data/SL/cancertype_data/kg2LUAD.csv'

print('Read kg:')
kg = pd.read_csv(kg_path, sep=',')
sl = pd.read_csv(sl_path, sep=',')

print('The number of rows in kg_triplet: ',len(kg))
# -------------------------------------remove relationship types unrelated to genes-------------------------------------------
kg_unrelated = kg[(kg['type(r)'] == 'RESEMBLES_CrC')
               |(kg['type(r)'] == 'INCLUDES_PCiC')
               |(kg['type(r)'] == 'CAUSES_CcSE')
               |(kg['type(r)'] == 'PALLIATES_CpD')
               |(kg['type(r)'] == 'TREATS_CtD')
               |(kg['type(r)'] == 'RESEMBLES_DrD')
               |(kg['type(r)'] == 'LOCALIZES_DlA')
               |(kg['type(r)'] == 'PRESENTS_DpS')]
kg_delete = kg[~kg.isin(kg_unrelated)].dropna()

print('The number of rows in kg_triplet unrelated to genes: ',len(kg_unrelated))
print('The number of rows in kg_triplet related to genes: ',len(kg_delete))
# --------------------------------------delect relations not involving genes in sl-------------------------------------------
kg_delete = kg_delete.reset_index(drop=True)
set_gene_a = set(sl['gene_a.identifier'])
set_gene_b = set(sl['gene_b.identifier'])
set_sl = set_gene_a | set_gene_b

row_delete_gene_1 = []  
for index, row in kg_delete.iterrows():
    if(row['ID(a)'] not in set_sl and row['ID(b)'] not in set_sl):
        row_delete_gene_1.append(index)
kg_delete = kg_delete.drop(kg_delete.index[row_delete_gene_1])

kg_delete_same = kg_delete[(kg_delete['type(r)'] == 'SL_GsG')
                           |(kg_delete['type(r)'] == 'REGULATES_GrG')
                           |(kg_delete['type(r)'] == 'INTERACTS_GiG')
                           |(kg_delete['type(r)'] == 'COVARIES_GcG')
                           |(kg_delete['type(r)'] == 'NONSL_GnsG')
                           |(kg_delete['type(r)'] == 'SR_GsrG')]
kg_delete_unsame = kg_delete[~kg_delete.isin(kg_delete_same)].dropna()
kg_delete_same = kg_delete_same.reset_index(drop=True)

row_delete_gene_2 = []  
for index, row in kg_delete_same.iterrows():
    if(row['ID(a)'] not in set_sl or row['ID(b)'] not in set_sl):
        row_delete_gene_2.append(index)
kg_delete_same = kg_delete_same.drop(kg_delete_same.index[row_delete_gene_2])

print('The number of rows in kg_triplet to delete (genes not in the sl): ', len(row_delete_gene_1)+len(row_delete_gene_2))
kg_delete = pd.concat([kg_delete_same, kg_delete_unsame], ignore_index=True).drop_duplicates()
print('length of kg_delete related to genes after delect: ',len(kg_delete))
# --------------------------------delect relations not involving other entities in sl-------------------------------------------
kg_unrelated = kg_unrelated.reset_index(drop=True)
# Anatomy
kg_delete_anatomy = kg_delete[(kg_delete['type(r)'] == 'DOWNREGULATES_AdG')
                              |(kg_delete['type(r)'] == 'EXPRESSES_AeG')
                              |(kg_delete['type(r)'] == 'UPREGULATES_AuG')]
print('The number of rows in kg_delete related to anatomy: ',len(kg_delete_anatomy))
set_anatomy = set(kg_delete_anatomy['ID(a)'])

# Disease
kg_delete_disease = kg_delete[(kg_delete['type(r)'] == 'ASSOCIATES_DaG')
                              |(kg_delete['type(r)'] == 'UPREGULATES_DuG')
                              |(kg_delete['type(r)'] == 'DOWNREGULATES_DdG')]
print('The number of rows in kg_delete related to disease: ',len(kg_delete_disease))
set_disease = set(kg_delete_disease['ID(a)'])

# Compound
kg_delete_compound = kg_delete[(kg_delete['type(r)'] == 'BINDS_CbG')
                               |(kg_delete['type(r)'] == 'DOWNREGULATES_CdG')
                               |(kg_delete['type(r)'] == 'UPREGULATES_CuG')]
print('The number of rows in kg_delete related to compound: ',len(kg_delete_compound))
set_compound = set(kg_delete_compound['ID(a)'])

set_entity = set_anatomy | set_disease | set_compound

# kg_delete_dia = kg_delete[(kg['type(r)'] == 'LOCALIZES_DlA')]
row_delete_1 = []  
for index, row in kg_unrelated.iterrows():
    if(row['ID(a)'] not in set_entity and row['ID(b)'] not in set_entity):
        row_delete_1.append(index)
kg_unrelated = kg_unrelated.drop(kg_unrelated.index[row_delete_1])

kg_unrelated_same = kg_unrelated[(kg_unrelated['type(r)'] == 'LOCALIZES_DlA')
                               |(kg_unrelated['type(r)'] == 'PALLIATES_CpD')
                               |(kg_unrelated['type(r)'] == 'TREATS_CtD')
                               |(kg_unrelated['type(r)'] == 'RESEMBLES_CrC')
                               |(kg_unrelated['type(r)'] == 'RESEMBLES_DrD')]
kg_unrelated_unsame = kg_unrelated[~kg_unrelated.isin(kg_unrelated_same)].dropna()
kg_unrelated_same = kg_unrelated_same.reset_index(drop=True)

row_delete_2 = []  
for index, row in kg_unrelated_same.iterrows():
    if(row['ID(a)'] not in set_entity or row['ID(b)'] not in set_entity):
        row_delete_2.append(index)
kg_unrelated_same = kg_unrelated_same.drop(kg_unrelated_same.index[row_delete_2])

print('The number of rows in kg_triplet to delete (entities not in the sl): ', len(row_delete_1)+len(row_delete_2))
kg_unrelated = pd.concat([kg_unrelated_same, kg_unrelated_unsame], ignore_index=True).drop_duplicates()
print('length of kg_unrelated related to genes after delect: ',len(kg_unrelated))
# -------------------------------------------------generate gew knowledge graph-------------------------------------------
kg_new = pd.concat([kg_delete, kg_unrelated], ignore_index=True).drop_duplicates()
print('The number of rows in new kg_triplet: ',len(kg_new))
print('The first 10 rows of kg_new: ')
print(kg_new[:10])

kg_new.to_csv(kg_save, index=False)