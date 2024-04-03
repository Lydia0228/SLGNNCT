# SLGNNCT: Synthetic lethality prediction based on knowledge graph for different cancers types
![image](https://github.com/Lydia0228/SLGNNCT/blob/master/figures/framework.png)

# Installation
SLGNNCT is based on Python 3.9 and PyTorch 1.10.0
## Requirements
You will need the following packages to run the code:
* python==3.9.0
* torch==1.10.0
* dgl==0.7.2
* numpy==1.21.4
* pandas==1.3.5
* scikit_learn==1.0.1
* torch_scatter==2.0.9
# Data Description
The './data' folder contains all datasets used by our paper.

The raw data we use is stored in './data/SL/raw', and we put the data divided by cancer type in the cancertype_data folder.
The specific data used by the model is stored in './data/SL/fold_sl'.
# Data Preprocessing
## Take BRCA as an example:
### SL dataset
When processing SL data, you need to use three different folders, enter them respectively and run the corresponding code:

    $ cd data_preprocessing\preprocessing
    $ python sl_preprocessing.py
    $ cd data_preprocessing\furtherprocessing
    $ python BRCA_furtherprocessing.py
    $ cd data_preprocessing\fold
    $ python BRCA_fold.py
### KG dataset
You need to go into the preprocessing folder and execute the 'kg_preprocessing_BRCA' file:

    $ cd data_preprocessing\preprocessing
    $ python kg_preprocessing_BRCA.py
# Direct Usage of SLGNNCT
First, you need to clone the repository or download source codes and data files. 

    $ git clone https://github.com/Lydia0228/SLGNNCT.git

Then go to the folder '/src'

    $ cd src

You can directly run the following code to train the model:
  
    python train.py   --epoch 100 \
                      --batch_size 1024 \
                      --dim 64 \
                      --l2 0.0001 \
                      --lr 0.003 \
                      --sim_regularity 0.001 \
                      --inverse_r True \
                      --node_dropout_rate 0.5 \
                              
The rest of the hyperparameters can be viewed in the code.

If you need to switch the cancer type for prediction, please modify the cancer name in the 'dataloader' and 'utils' files.