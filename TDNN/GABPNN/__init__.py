# -*- coding:utf-8 -*-


import pandas as pd
import numpy as np


# model param
OUTPUT_NUM = 1
EPOCHS = 40
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


# 对原始数据进行处理
def data_preparation(model, data_csv, target='F'):
    # 数据归一化处理
    df_X, series_y = data_normalization(data_csv, target=target)

    # 按8：2比例，构造训练集和测试集
    train_data_length = int(0.8 * series_y.count())
    train_X = df_X[:train_data_length]
    train_y = series_y[:train_data_length]
    test_X = df_X[train_data_length:]
    test_y = series_y[train_data_length:]

    return train_X, train_y, test_X, test_y


def data_normalization(data_csv_file, target=None):
    if target is None:
        return
    x_name_list = get_feature_name_list(target=target)
    data = pd.read_csv(data_csv_file, sep=',', header=0)
    data = data.dropna(axis=0, how='any')  # drop all rows that have any NaN values
    if target == 'F':
        y_name = F_name
    elif target == 'T':
        y_name = T_name
    else:
        y_name = S_name

    _data_X = data[x_name_list]
    _data_y = data[y_name]

    data_X = dataframe_zscore(_data_X, target)
    data_y = series_zscore(_data_y, target)
    data_X = data_X.dropna(axis=0, how='any')
    data_y = data_y.dropna(axis=0, how='any')

    return data_X, data_y


def dataframe_zscore(df, y_name):
    cols = list(df.columns)
    new_df = pd.DataFrame(columns=cols)
    normalization_info_file = normalization_info_file_dir + y_name + '_norm_info.txt'
    with open(normalization_info_file, 'w') as norm_file:
        norm_file.write('data_X\tmean\tstd\n')
        for col in cols:
            mean = df[col].mean()
            std = df[col].std(ddof=0)
            new_df[col] = (df[col] - mean) / std
            norm_file.write(col + '\t' + str(mean) + '\t' + str(std) + '\n')
    norm_file.close()
    return new_df


def series_zscore(series, y_name):
    mean = series.mean()
    std = series.std(ddof=0)
    new_series = pd.Series((series - mean) / std)
    normalization_info_file = normalization_info_file_dir + y_name + '_norm_info.txt'
    with open(normalization_info_file, 'a') as norm_file:
        norm_file.write('data_y\tmean\tstd\n')
        norm_file.write(y_name + '\t' + str(mean) + '\t' + str(std))
    # print(new_series)
    # length = series.shape[0]
    # # cols_count = df_data.shape[1]
    # total = series.sum()
    # # total = reduce(lambda x, y: x+y, df_data)
    # data = series.values.tolist()
    # ave = float(total) / length
    # tempsum = np.nansum([pow(data[data_index] - ave, 2) for data_index in range(length)])
    # tempsum = pow(float(tempsum) / length, 0.5)
    # for data_index in range(length):
    #     data[data_index] = (data[data_index] - ave) / tempsum
    # print(data)
    # return data
    return new_series


# 按照特征重要性从大到小排列
def get_feature_name_list(target=None):
    if target is None:
        return
    feature_type = ['均值', '方差']
    if target == 'F':
        feature_imp_file = F_feature_imp_file
    elif target == 'T':
        feature_imp_file = T_feature_imp_file
    else:
        feature_imp_file = S_feature_imp_file
    with open(feature_imp_file, 'r') as imp_file:
        lines = imp_file.readlines()
        feature_name_list = list()
        for line in lines:
            feature_name = line.split('\t')[0].strip('均值')
            for f_type in feature_type:
                feature_name_list.append(feature_name + f_type)
    # print(feature_name_list)
    imp_file.close()
    return feature_name_list[::-1]


if __name__ == '__main__':
    # print(get_feature_name_list(target='F))
    # data_normalization(data_csv, target=TARGET)
    # data_preparation(data_csv)
    model = dict()
    model['leaf_NN_num'] = 5
    # model.leaf_last_input_num = 2
    model['leaf_input_num'] = 6
    data_preparation(model, data_csv)
    # pass
