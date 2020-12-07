# -*- coding:utf-8 -*-

# BPNN NN Module
from keras import regularizers, backend
from tensorflow import keras
import matplotlib.pyplot as plt
from BaselineModels.GABPNN import *

TOTAL_INPUT_NUM = len(get_feature_name_list(target=TARGET))


def r_square(y_true, y_pred):
    SSR = backend.sum(backend.square(y_pred-y_true))
    SST = backend.sum(backend.square(y_true-backend.mean(y_true)))
    return 1-SSR/SST


class BPNN:
    def __init__(self, nn_parameters=None):
        # nn_parameters info
        self.nn_parameters = nn_parameters
        self.layer_num = nn_parameters['layer_num']
        self.layer_dims = list(nn_parameters['layer_dims'])
        self.activations = list(nn_parameters['activations'])

        self.optimizer = nn_parameters['optimizer']

        # computed parameters info
        self.input_num = TOTAL_INPUT_NUM

        self.model_name = "GA_BPNN"  # the model's name

    def build_model(self, model_name=None):
        if model_name is not None:
            self.model_name = model_name

        input_layer = keras.layers.Input(shape=(self.input_num, ))
        layer1 = None
        layer2 = None
        for j in range(self.layer_num-1):
            if j == 0:
                layer1 = input_layer
                continue
            if j == self.layer_num - 2:
                layer2 = keras.layers.Dense(self.layer_dims[j])(layer1)
            else:
                layer2 = keras.layers.Dense(self.layer_dims[j],
                                            activation=self.activations[j],
                                            use_bias=True, bias_initializer='zeros',
                                            bias_regularizer=regularizers.l2(1e-4),
                                            kernel_initializer='random_normal',
                                            kernel_regularizer=regularizers.l2(1e-4),
                                            )(layer1)
            layer1 = layer2
        output_layer = layer2

        # build model
        model = keras.models.Model(inputs=input_layer, outputs=output_layer)
        model.compile(loss='mse', optimizer=self.get_optimizer(), metrics=[r_square])
        model.summary()

        train_X, train_y, test_X, test_y = data_preparation(self, data_csv, target=TARGET)
        train_y=np.array(train_y)
        test_y=np.array(test_y)
        history = model.fit(train_X, train_y, validation_data=(test_X, test_y),
                            batch_size=BATCH_SIZE,
                            epochs=EPOCHS,
                            verbose=2)

        # model.save('Model/'+self.model_name)

        # 模型训练结果可视化
        # self.visualization(history, model, test_leaf_X_list, test_y, self.model_name)

        last_r2 = history.history['r_square'][-1]
        last_val_r2 = history.history['val_r_square'][-1]
        print("")

        return last_val_r2

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
        else:
            opt = keras.optimizers.Adam(learning_rate=lr_schedule)
        return opt


