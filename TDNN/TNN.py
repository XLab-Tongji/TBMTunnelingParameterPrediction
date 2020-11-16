# DNN NN Module
# from tensorflow.keras import Input,layers,models,optimizers,metrics,regularizers
from keras import Input, layers, models, optimizers, metrics, regularizers, backend
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import math
import csv
import codecs
import pandas as pd

from TDNN import *

TOTAL_INPUT_NUM = len(get_feature_name_list(target=TARGET))


def r_square(y_true, y_pred):
    SSR = backend.sum(backend.square(y_pred-y_true))
    SST = backend.sum(backend.square(y_true-backend.mean(y_true)))
    return 1-SSR/SST


class TNN:
    def __init__(self, nn_parameters=None):
        # nn_parameters info
        self.nn_parameters = nn_parameters
        self.leaf_input_num = nn_parameters['leaf_input_num']
        self.leaf_layer_num = nn_parameters['leaf_layer_num']
        self.leaf_layer_dims = list(nn_parameters['leaf_layer_dims'])
        self.leaf_activations = list(nn_parameters['leaf_activations'])

        self.aggre_layer_num = nn_parameters['aggre_layer_num']
        self.aggre_layer_dims = list(nn_parameters['aggre_layer_dims'])
        self.aggre_activations = list(nn_parameters['aggre_activations'])

        self.root_layer_num = nn_parameters['root_layer_num']
        self.root_layer_dims = list(nn_parameters['root_layer_dims'])
        self.root_activations = list(nn_parameters['root_activations'])

        self.optimizer = nn_parameters['optimizer']

        # computed parameters info
        self.leaf_NN_num = int(math.ceil(TOTAL_INPUT_NUM / self.leaf_input_num))
        self.aggre_NN_num = int(math.floor(self.leaf_NN_num / 2))
        self.leaf_last_NN_input_num = TOTAL_INPUT_NUM % self.leaf_input_num

        # 当最后一个leaf NN的输入只有一个时，将其同上一个NN进行合并
        if self.leaf_last_NN_input_num == 1:
            self.leaf_NN_num = self.leaf_NN_num - 1
            self.leaf_last_NN_input_num = self.leaf_input_num + 1

        self.model_name = "TBMTunnelingParametersPrediction"  # the model's name

    def load_model(self, name="default"):
        i = 0

    def predict(self):
        print("1")

    def build_model(self, model_name=None):
        if model_name is not None:
            self.model_name = model_name

        # leaf
        leaf_input_layer_list = list()
        leaf_last_layer_list = list()
        for i in range(self.leaf_NN_num):
            if i == self.leaf_NN_num - 1 and self.leaf_last_NN_input_num != 0:
                input_layer = keras.layers.Input(shape=(self.leaf_last_NN_input_num,))
            else:
                input_layer = keras.layers.Input(shape=(self.leaf_input_num, ))
            leaf_input_layer_list.append(input_layer)
            layer1 = None
            layer2 = None
            for j in range(self.leaf_layer_num - 1):
                if j == 0:
                    layer1 = input_layer
                if j == self.leaf_layer_num - 2:
                    layer2 = keras.layers.Dense(self.leaf_layer_dims[j])(layer1)
                else:
                    layer2 = keras.layers.Dense(self.leaf_layer_dims[j],
                                                activation=self.leaf_activations[j],
                                                use_bias=True,
                                                bias_initializer='zeros',
                                                bias_regularizer=regularizers.l2(1e-4),
                                                kernel_initializer='random_normal',
                                                kernel_regularizer=regularizers.l2(1e-4)
                                                # activity_regularizer=regularizers.l2(1e-5))(layer1)
                                                )(layer1)
                    # layer2 = keras.layers.LeakyReLU(alpha=0.01)(layer1)
                layer1 = layer2
            leaf_last_layer_list.append(layer2)

        # aggregation
        aggre_last_layer_list = list()
        for i in range(self.aggre_NN_num):
            input_layer = keras.layers.Add()([leaf_last_layer_list[i * 2], leaf_last_layer_list[i * 2 + 1]])
            layer1 = None
            layer2 = None
            for j in range(self.aggre_layer_num - 1):
                if j == 0:
                    layer1 = input_layer
                if j == self.aggre_layer_num - 2:
                    layer2 = keras.layers.Dense(self.aggre_layer_dims[j])(layer1)
                else:
                    layer2 = keras.layers.Dense(self.aggre_layer_dims[j],
                                                activation=self.aggre_activations[j],
                                                use_bias=True,
                                                bias_initializer='zeros',
                                                bias_regularizer=regularizers.l2(1e-4),
                                                kernel_initializer='random_normal',
                                                kernel_regularizer=regularizers.l2(1e-4)
                                                # activity_regularizer=regularizers.l2(1e-5)(layer1)
                                                )(layer1)
                    # layer2 = keras.layers.LeakyReLU(alpha=0.01)(layer1)
                layer1 = layer2
            aggre_last_layer_list.append(layer2)

        # root
        if self.leaf_NN_num % 2 != 0:
            aggre_last_layer_list.append(leaf_last_layer_list[-1])
        input_layer = keras.layers.Add()(aggre_last_layer_list)
        layer1 = None
        layer2 = None
        for j in range(self.root_layer_num-1):
            if j == 0:
                layer1 = input_layer
            if j == self.root_layer_num - 2:
                layer2 = keras.layers.Dense(self.root_layer_dims[j])(layer1)
            else:
                layer2 = keras.layers.Dense(self.root_layer_dims[j],
                                            activation=self.root_activations[j],
                                            use_bias=True, bias_initializer='zeros',
                                            bias_regularizer=regularizers.l2(1e-4),
                                            kernel_initializer='random_normal',
                                            kernel_regularizer=regularizers.l2(1e-4),
                                            # activity_regularizer=regularizers.l2(1e-5)
                                            )(layer1)
                # layer2 = keras.layers.LeakyReLU(alpha=0.01)(layer1)
            layer1 = layer2
        final_output_layer = layer2

        # build model
        model = keras.models.Model(inputs=leaf_input_layer_list, outputs=final_output_layer)
        model.compile(loss='mse', optimizer=self.get_optimizer(), metrics=[r_square])
        model.summary()

        train_leaf_X_list, train_y, test_leaf_X_list, test_y = data_preparation(self, data_csv, target=TARGET)
        history = model.fit(train_leaf_X_list, train_y, validation_data=(test_leaf_X_list, test_y),
                            batch_size=BATCH_SIZE,
                            epochs=EPOCHS,
                            verbose=2)

        model.save('Model/'+self.model_name)

        # 模型训练结果可视化
        # self.visualization(history, model, test_leaf_X_list, test_y, self.model_name)

        last_r2 = history.history['r_square'][-1]
        last_val_r2 = history.history['val_r_square'][-1]

        return last_val_r2

    # 对原始数据进行处理
    # def data_preparation(self):
    #     df_X, series_y = data_normalization(data_csv, target=TARGET)  # 数据归一化处理
    #     # 按8：2比例，构造训练集和测试集
    #     train_data_length = int(0.8 * df_X.count())
    #     train_X = df_X[:train_data_length]
    #     train_y = series_y[:train_data_length]
    #     test_X = df_X[train_data_length:]
    #     test_y = series_y[train_data_length:]
    #
    #     train_leaf_X_list = list()
    #     test_leaf_X_list = list()
    #     for i in range(self.leaf_NN_num - 1):
    #         cur_index = i * self.leaf_input_num
    #         train_leaf_X_list.append(train_X[:, cur_index: cur_index + self.leaf_input_num])
    #         test_leaf_X_list.append(test_X[:, cur_index: cur_index + self.leaf_input_num])
    #     train_leaf_X_list.append(train_X[:, (self.leaf_NN_num - 1) * self.leaf_input_num:])
    #     test_leaf_X_list.append(test_X[:, (self.leaf_NN_num - 1) * self.leaf_input_num:])
    #
    #     return train_leaf_X_list, train_y, test_leaf_X_list, test_y

    def visualization(self, history, model, test_input, test_output, model_name):
        test_pred = np.array(model.predict(test_input))
        loss = history.history['loss']
        val_loss = history.history['val_loss']
        r2 = history.history['r_square']
        val_r2 = history.history['val_r_square']
        i = 0
        for _ in r2:
            if r2[i] < 0:
                r2[i] = 0
            if val_r2[i] < 0:
                val_r2[i] = 0
            i += 1
        show_length = int(0.5 * test_pred.shape[0])
        plt.plot(test_pred[:show_length], color='red', label='prediction')
        plt.plot(test_output[:show_length], color='blue', label='Truth')
        plt.title('Prediction and Truth')
        plt.legend()
        # plt.save()
        plt.show()

        plt.figure()
        plt.plot(loss, color='red', label='Training loss')
        plt.plot(val_loss, color='blue', label='Validation loss')
        plt.title('Training and Validation Loss')
        plt.legend()
        plt.show()

        plt.figure()
        plt.plot(r2, color='red', label='Training r2')
        plt.plot(val_r2, color='blue', label='Validation r2')
        plt.title('Training and ValidationR-Squared')
        plt.legend()
        plt.show()

    def get_optimizer(self):
        lr_schedule = keras.optimizers.schedules.ExponentialDecay(
            initial_learning_rate=1e-4,
            decay_steps=10000,
            decay_rate=0.9)
        if self.optimizer == 'Adam':
            opt = keras.optimizers.Adam(learning_rate=lr_schedule)
        elif self.optimizer == 'Adagrad':
            opt = keras.optimizers.Adagrad(learning_rate=lr_schedule)
        elif self.optimizer == 'Adadelta':
            opt = keras.optimizers.Adadelta(learning_rate=lr_schedule)
        elif self.optimizer == 'RMSProp':
            opt = keras.optimizers.RMSprop(learning_rate=lr_schedule)
        elif self.optimizer == 'sgd':
            opt = keras.optimizers.SGD(learning_rate=lr_schedule)
        return opt


