**python version**: 3.6.5

**important modules**:

* tensorflow

* matplotlib

* math

* pandas

* numpy



#### 1. Run:

```
python GANN.py
```

#### 2. Result

The trained models are saved in ***Model/***

The preprocessed training data is in ***TBMData/***

If plot is on, the figures are saved in ***Figures/***

The best structure of model is shown in the terminal window. Here is an example:

```
leaf_input_num :  6
leaf_layer_num :  6
leaf_layer_dims :  [84, 32, 32, 16, 1]
leaf_activations :  ['relu', 'sigmoid', 'sigmoid', 'relu', 'None']
aggre_layer_num :  6
aggre_layer_dims :  [96, 196, 324, 96, 1]
aggre_activations :  ['relu', 'relu', 'sigmoid', 'tanh', 'None']
root_layer_num :  3
root_layer_dims :  [8, 1]
root_activations :  ['sigmoid', 'None']
optimizer :  Adagrad
Highest r2 score:  -57.38411545753479
```

#### 3. Modify

The parameters can be modified.

 ***_init_.py***:

```python
# model param
LEAF_OUTPUT_NUM = 1
AGGREGATION_OUTPUT_NUM = 1
ROOT_OUTPUT_NUM = 1
EPOCHS = 10
BATCH_SIZE = 100

# files
data_csv = 'TBMData/data.csv'
F_feature_imp_file = 'TBMData/FI_稳定段总推进力均值.txt'
T_feature_imp_file = 'TBMData/FI_稳定段刀盘扭矩均值.txt'
S_feature_imp_file = 'TBMData/FI_稳定段推进速度均值.txt'
normalization_info_file_dir = 'TBMData/'

# fixed variables
F_name = '稳定段总推进力均值'
T_name = '稳定段刀盘扭矩均值'
S_name = '稳定段推进速度均值'

TARGET = 'F'  # 当前模型的预测目标；F, T, S
```

***GANN.py***:

```python
GEN_LENGTH = 3  # the gen num in one population
RETAIN = 0.4
SELECT = 0.2
MUTATION = 0.2
NB_GENS = 1  # the generation of GA
```