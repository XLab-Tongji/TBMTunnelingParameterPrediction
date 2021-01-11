# LSTM for international airline passengers problem with time step regression framing
import numpy
import matplotlib.pyplot as plt
from pandas import read_csv
from sklearn.metrics import mean_squared_error  # MSE
from sklearn.metrics import mean_absolute_error  # MAE
from sklearn.metrics import r2_score  # R 2
import math
from tensorflow import keras

import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
# convert an array of values into a dataset matrix
import pickle

model_dir = 'Model/'


def create_dataset(dataset, look_back=22):
    dataX, dataY = [], []
    for i in range(0, len(dataset) - look_back + 1, 22):
        a = dataset[i:(i + look_back), 0]
        dataX.append(a)

    # print(len(dataX))
    # print(len(numpy.array(dataX)))
    return numpy.array(dataX)


# fix random seed for reproducibility
numpy.random.seed(7)


# load the dataset
# 加载数据
def predict(model_name):
    count = 0
    if (model_name == "lstm_model_F"):
        count = 1
    if (model_name == "lstm_model_T"):
        count = 2
    if (model_name == "lstm_model_S"):
        count = 3
    dataframe_rise = read_csv('rnn_risetest.csv', sep=',', header=0)
    rise_col_names = dataframe_rise.columns.values.tolist()[1:]
    dataframe_rise = dataframe_rise[rise_col_names]
    dataframe_stable = read_csv('rnn_stabletest.csv', sep=',', header=0)
    stable_col_names = dataframe_stable.columns.values.tolist()[count]
    dataframe_stable = dataframe_stable[stable_col_names]
    dataset_rise = dataframe_rise.values
    dataset_rise = dataset_rise.astype('float32')
    dataset_stable = dataframe_stable.values
    dataset_stable = dataset_stable.astype('float32')
    # 缩放数据
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler2 = MinMaxScaler(feature_range=(0, 1))
    dataset_rise = scaler.fit_transform(dataset_rise)
    dataset_stable = scaler2.fit_transform(dataset_stable.reshape(-1, 1))
    # 分割2/3数据作为测试
    data_size = int(len(dataset_rise) / 22)
    # print(data_size)
    train, test = dataset_rise[0:data_size * 22, :], dataset_rise[data_size * 22:len(dataset_rise), :]
    # 预测数据步长为3,三个预测一个，3->1
    look_back = 22
    dataX = create_dataset(dataset_rise, look_back)
    # print(len(dataX))
    dataX = numpy.reshape(dataX, (dataX.shape[0], dataX.shape[1], 1))
    # print(len(dataX))
    model = keras.models.load_model(model_dir + model_name + ".h5")
    dataPredict = model.predict(dataX)
    MseScore = mean_squared_error(dataset_stable, dataPredict)
    r2Score = r2_score(dataset_stable, dataPredict)
    MaeScore = mean_absolute_error(dataset_stable, dataPredict)

    dataPredict = scaler2.inverse_transform(dataPredict)
    # print(len(dataPredict))

    return dataPredict, MseScore, r2Score, MaeScore


# def evaluate(model_name,Predict):
# 	count =0
# 	if (model_name=="lstm_model_F"):
# 		count = 1
# 	if (model_name == "lstm_model_T"):
# 		count = 2
# 	if (model_name == "lstm_model_S"):
# 		count = 3
# 	dataframe_stable = read_csv('rnn_stabletest.csv', usecols=[count], engine='python')
# 	dataset_stable = dataframe_stable.values
# 	dataset_stable = dataset_stable.astype('float32')
# 	scaler = MinMaxScaler(feature_range=(0, 1))
# 	dataset_stable = scaler.fit_transform(dataset_stable)
# 	Predict = scaler.fit_transform(Predict)
# 	MseScore = mean_squared_error(dataset_stable, Predict)
# 	r2Score = r2_score(dataset_stable, Predict)
# 	MaeScore = mean_absolute_error(dataset_stable, Predict)
# 	return MseScore,r2Score,MaeScore
# def get_model_info(model_history_name):
#     with open(model_dir + model_history_name + '.pkl', 'rb') as his_f:
#     	history = pickle.load(his_f)
#         training_loss=history['loss']
#         val_loss = history['val_loss']
#         test_mse = history['test_mean_squared_error']
#         test_r2_score = history['test_r2_score']
#         test_y = history['test_y']
#         pred_y = history['pred_y']
#         his_f.close()
#
#     model_info = {
#         "training_loss": training_loss,
#         "val_loss": val_loss,
#         "test_mse": test_mse,
#         "test_r2_score": test_r2_score,
#         "test_y": test_y,
#         "pred_y": pred_y
#     }
#     return model_info


if __name__ == '__main__':
    Predict, MseScore, r2Score, MaeScore = predict("lstm_model_S")

    f = open(model_dir + 'lstm_F_history' + '.pkl', 'rb')
    # info = pickle.load(f)
    # print(info)
    # info = info['loss']
    # print(info)
    # plt.plot(info)

    print(Predict)

    # X[:, 0]
    # 就是取所有行的第0个数据, X[:, 1]
    # 就是取所有行的第1个数据。
    # MseScore,r2Score,MaeScore=evaluate("lstm_model_F",Predict)
    print('MseScore:' + str(MseScore))
    print('R2Score:' + str(r2Score))
    print('MaeScore:' + str(MaeScore))
# plt.figure(figsize=(20, 5))

# plt.title('S_Predict')
# plt.plot(Predict, label='Predict', c='blue')
#
# plt.plot(dataset_stable, label='Original', c='orange')
# plt.legend("upper left")
#
# x = np.arange(0, 101, 1)
#
# print(len(x))
# print(len(Predict))
# plt.scatter(x,Predict, 5, color='red', zorder=2)  # 在第二层画点
# plt.scatter(x,dataset_stable, 5, color='red', zorder=2)  # 在第二层画点
# plt.show()

# get_model_info("lstm_F_history")
