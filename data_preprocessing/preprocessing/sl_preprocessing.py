import pandas as pd

human_sl_path = '../../data/SL/raw/sl_data'
id2name_path = '../../data/SL/raw/dbid2name.csv'
train_path = '../../data/SL/raw/train_pairs.csv'
test_path = '../../data/SL/raw/test_pairs.csv'

slid2name_save = '../../data/SL/cancertype_data/slid2name.csv'
sl2cancertypes_save = '../../data/SL/cancertype_data/sl2cancertypes.csv'

sl2BRCA_save = '../../data/SL/cancertype_data/sl2BRCA.csv'
sl2CESC_save = '../../data/SL/cancertype_data/sl2CESC.csv'
sl2COAD_save = '../../data/SL/cancertype_data/sl2COAD.csv'
sl2KIRC_save = '../../data/SL/cancertype_data/sl2KIRC.csv'
sl2LAML_save = '../../data/SL/cancertype_data/sl2LAML.csv'
sl2LUAD_save = '../../data/SL/cancertype_data/sl2LUAD.csv'
sl2OV_save = '../../data/SL/cancertype_data/sl2OV.csv'
sl2SKCM_save = '../../data/SL/cancertype_data/sl2SKCM.csv'

human_SL = pd.read_csv(human_sl_path, sep=' ')
human_SL = human_SL[['gene_a.identifier','gene_b.identifier']]
id_name = pd.read_csv(id2name_path)
train_pairs = pd.read_csv(train_path)
test_pairs = pd.read_csv(test_path)
sl_cancertypes = pd.concat([train_pairs, test_pairs], ignore_index=True).drop_duplicates()
sl_cancertypes = sl_cancertypes[sl_cancertypes['class'] == 1]
#---------------------------------------------Add gene names to the data in sl_data------------------------------
slid2name = pd.merge(human_SL, id_name, left_on='gene_a.identifier', right_on='_id')
slid2name = pd.merge(slid2name, id_name, left_on='gene_b.identifier', right_on='_id')
slid2name = slid2name.sort_values(by='gene_a.identifier')

slid2name.rename(columns={'name_x': 'gene_a.name'}, inplace=True)
slid2name.rename(columns={'name_y': 'gene_b.name'}, inplace=True)
slid2name = slid2name[['gene_a.identifier', 'gene_a.name', 'gene_b.identifier', 'gene_b.name']]

print("Number of rows in human_sl:", len(human_SL))
print("Number of rows in slid2name:", len(slid2name))

slid2name.to_csv(slid2name_save, index=False)
#---------------------------------------------Retrieve the data from sldata with cancer classification------------------------------
index_list = []
for index, row in slid2name.iterrows():
    gene_a = row['gene_a.name']
    gene_b = row['gene_b.name']
    index_list.append(sl_cancertypes[(sl_cancertypes['gene1'] == gene_a)&(sl_cancertypes['gene2'] == gene_b)].index.tolist())
    index_list.append(sl_cancertypes[(sl_cancertypes['gene2'] == gene_a)&(sl_cancertypes['gene1'] == gene_b)].index.tolist())

list_same = []
for a in index_list:
    for b in a:
        list_same.append(b)

cancertypes_delete = sl_cancertypes[sl_cancertypes.index.isin(list_same)]

print("Number of rows in sl_cancertypes:", len(sl_cancertypes))
print("Number of rows in cancertypes_delete:", len(cancertypes_delete))
# cancertypes_delete.to_csv('cancertypes_delete.csv', index=False)
#---------------------------------------------Classify the data in sl_data by cancer types------------------------------
sl2cancertypes_ab = pd.merge(slid2name, cancertypes_delete, left_on=['gene_a.name', 'gene_b.name'], right_on=['gene1', 'gene2'])
sl2cancertypes_ba = pd.merge(slid2name, cancertypes_delete, left_on=['gene_a.name', 'gene_b.name'], right_on=['gene2', 'gene1'])

sl2cancertypes_ab = sl2cancertypes_ab[['gene_a.identifier', 'gene_a.name', 'gene_b.identifier', 'gene_b.name', 'cancer']]
sl2cancertypes_ba = sl2cancertypes_ba[['gene_a.identifier', 'gene_a.name', 'gene_b.identifier', 'gene_b.name', 'cancer']]
sl2cancertypes = pd.concat([sl2cancertypes_ab, sl2cancertypes_ba], ignore_index=True).drop_duplicates()
sl2cancertypes = sl2cancertypes.sort_values(by='cancer')

# print("Number of rows in sl2cancertypes_ab:", len(sl2cancertypes_ab))
# print("Number of rows in sl2cancertypes_ba:", len(sl2cancertypes_ba))
print("Number of rows in sl2cancertypes:", len(sl2cancertypes))

print('The first 10 rows of sl2cancertypes: ')
print(sl2cancertypes[:10])
sl2cancertypes.to_csv(sl2cancertypes_save, index=False)
#---------------------------------------------Divide sl_data into 8 files based on cancer types------------------------------
sl2BRCA = sl2cancertypes[sl2cancertypes['cancer'] == 'BRCA'].sort_values(by='gene_a.identifier')
sl2CESC = sl2cancertypes[sl2cancertypes['cancer'] == 'CESC'].sort_values(by='gene_a.identifier')
sl2COAD = sl2cancertypes[sl2cancertypes['cancer'] == 'COAD'].sort_values(by='gene_a.identifier')
sl2KIRC = sl2cancertypes[sl2cancertypes['cancer'] == 'KIRC'].sort_values(by='gene_a.identifier')
sl2LAML = sl2cancertypes[sl2cancertypes['cancer'] == 'LAML'].sort_values(by='gene_a.identifier')
sl2LUAD = sl2cancertypes[sl2cancertypes['cancer'] == 'LUAD'].sort_values(by='gene_a.identifier')
sl2OV = sl2cancertypes[sl2cancertypes['cancer'] == 'OV'].sort_values(by='gene_a.identifier')
sl2SKCM = sl2cancertypes[sl2cancertypes['cancer'] == 'SKCM'].sort_values(by='gene_a.identifier')

# print('The first 10 rows of sl2BRCA: ')
# print(sl2BRCA[:10])

print("Number of SL in BRCA:", len(sl2BRCA))
print("Number of SL in CESC:", len(sl2CESC))
print("Number of SL in COAD:", len(sl2COAD))
print("Number of SL in KIRC:", len(sl2KIRC))
print("Number of SL in LAML:", len(sl2LAML))
print("Number of SL in LUAD:", len(sl2LUAD))
print("Number of SL in OV:", len(sl2OV))
print("Number of SL in SKCM:", len(sl2SKCM))

sl2BRCA.to_csv(sl2BRCA_save, index=False)
sl2CESC.to_csv(sl2CESC_save, index=False)
sl2COAD.to_csv(sl2COAD_save, index=False)
sl2KIRC.to_csv(sl2KIRC_save, index=False)
sl2LAML.to_csv(sl2LAML_save, index=False)
sl2LUAD.to_csv(sl2LUAD_save, index=False)
sl2OV.to_csv(sl2OV_save, index=False)
sl2SKCM.to_csv(sl2SKCM_save, index=False)