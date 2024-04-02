from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
import os
import pandas as pd

data_path = '../../data/SL/further/LAML/sl2id.txt'
data = pd.read_csv(data_path, sep='\t')
save_path = '../../data/SL/fold_sl/LAML'

kf = KFold(n_splits=5, shuffle=True, random_state=28)

for fold_num, (train_index, test_index) in enumerate(kf.split(data)):
    fold_folder = os.path.join(save_path, f'fold_{fold_num + 1}')
    os.makedirs(fold_folder, exist_ok=True)
    fold_data = data.iloc[test_index]
    # fold_data.to_csv(os.path.join(fold_folder, 'fold_data.csv'), index=False)

    train_data, test_valid_data = train_test_split(fold_data, test_size=0.4, random_state=28)
    valid_data, test_data = train_test_split(test_valid_data, test_size=0.5, random_state=28)
    train_data.to_csv(os.path.join(fold_folder, 'train.txt'), index=False, sep='\t')
    test_data.to_csv(os.path.join(fold_folder, 'test.txt'), index=False, sep='\t')
    valid_data.to_csv(os.path.join(fold_folder, 'val.txt'), index=False, sep='\t')