# DNN NN Module
# from tensorflow.keras import Input,layers,models,optimizers,metrics,regularizers
from keras import Input,layers,models,optimizers,metrics,regularizers
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import math
import csv
import codecs
import pandas as pd
# from DNN.rbfLayer import RBFLayer, InitCentersRandom


class TNN:
    def __init__(self, nn_parameters=None):
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

        self.leafSize = 0 # the features' num of the standard leaf model's input
        self.name="default" # the model's name
        self.featureNum=0 # the number of features
        self.branchShape=() # the layers' parameter of the standard branch model
        self.leafShape=() # the layers' parameter of the standard leaf model

    def load_model(self, name="default"):
        i=0

    def predict(self):
        print("1")

    def design_model(self,origin_data,input_shape=26,leaf_size=3,leaf_shape_multi=(1,2,3,2,1),branch_shape=(2,4,3,1),name="default"):
        self.leafSize=leaf_size
        self.featureNum=input_shape
        self.leafShape=leaf_shape_multi
        self.branchShape=branch_shape
        self.name=name
        train_input, train_output,test_input,test_output, leaf_num, last_leaf_size=self._data_preparation(origin_data)
        branch_num = math.floor(leaf_num / self.branchShape[0])
        branch_add=leaf_num % self.branchShape[0]
        leaves=[]
        branches=[]
        leaves_Inputs=[]
        leaves_Outputs = []
        branches_Inputs=[]
        branches_Outputs = []
        root_Input=[]

        # 叶节点生成
        for i in range(leaf_num-1):
            leaves.append(self._leaf_generator(self.leafSize))
        if(last_leaf_size!=0):
            leaves.append(self._leaf_generator(last_leaf_size))
        else:
            leaves.append(self._leaf_generator(self.leafSize))

        # 叶节点输入生成 输出整合
        for i in range(leaf_num-1):
            In=Input(shape=(self.leafSize,))
            leaves_Inputs.append(In)
            leaves_Outputs.append(leaves[i](In))
        if (last_leaf_size != 0):
            In = Input(shape=(last_leaf_size,))
            leaves_Inputs.append(In)
            leaves_Outputs.append(leaves[-1](In))
        else:
            In = Input(shape=(self.leafSize,))
            leaves_Inputs.append(In)
            leaves_Outputs.append(leaves[-1](In))


        # 枝干节点生成
        for i in range(branch_num):
            branches.append(self._branch_generator())
        # 枝干节点输入生成 输出整合
        for i in range(branch_num):
            con=leaves_Outputs[i*self.branchShape[0]:(i+1)*self.branchShape[0]]
            In=layers.concatenate(con,axis=-1)
            branches_Inputs.append(In)
            branches_Outputs.append(branches[i](In))

        # 根节点输入生成
        if(branch_num*self.branchShape[0]==leaf_num):
            In=layers.concatenate(branches_Outputs,axis=-1)
            root_Input.append(In)
        else:
            for k in range(branch_add):
                branches_Outputs.append(leaves_Outputs[-1-k])
            In = layers.concatenate(branches_Outputs, axis=-1)
            root_Input.append(In)


        # 根节点生成 输出
        root_Output=self._root_generator(len(branches_Outputs))(root_Input[0])
        # 模型整合
        model=keras.Model(leaves_Inputs,root_Output)

        base_learning_rate=0.0001
        model.compile(optimizer=keras.optimizers.Adam(lr=base_learning_rate),loss='mse',metrics='mae')
        model.summary()

        history=model.fit(train_input, train_output,validation_data=(test_input,test_output),
                  batch_size=50,
                  epochs=300,
                  verbose=1)
        test_pred = model.predict(test_input)

        self._visualization(history, test_pred, test_output)




    def _data_preparation(self,origin_data):
        leaf_num = math.ceil(self.featureNum / self.leafSize)
        last_leaf_size = self.featureNum % self.leafSize
        # 训练数据
        train_input = origin_data[:-100,:-3]
        train_output = origin_data[:-100,-3]
        # 训练数据归一化处理
        mean_in=np.mean(train_input,axis=0)
        train_input-=mean_in
        std_in=train_input.std(axis=0)
        train_input/=std_in
        train_input=np.around(train_input, decimals=4)
        mean_out=np.mean(train_output)
        train_output-=mean_out
        std_out=train_output.std()
        train_output/=std_out
        train_output = np.around(train_output, decimals=4)
        train_leaf_input=[]
        for i in range(leaf_num-1):
            train_leaf_input.append(train_input[:,i*self.leafSize:i*self.leafSize+self.leafSize])
        train_leaf_input.append(train_input[:,(leaf_num-1)*self.leafSize:])

        # 验证数据
        input = origin_data[-100:, :-3]
        output = origin_data[-100:, -3]
        # 验证数据归一化处理
        input-=mean_in
        input/=std_in
        input = np.around(input, decimals=4)
        output-=mean_out
        output/=std_out
        output = np.around(output, decimals=4)
        leaf_input = []
        for i in range(leaf_num - 1):
            leaf_input.append(input[:, i * self.leafSize:i * self.leafSize + self.leafSize])
        leaf_input.append(input[:, (leaf_num - 1) * self.leafSize:])

        return train_leaf_input,train_output,leaf_input, output, leaf_num, last_leaf_size


    def _visualization(self,history,test_pred,test_output):
        loss = history.history['loss']
        val_loss = history.history['val_loss']
        mae = history.history['mae']
        val_mae = history.history['val_mae']
        epochs = range(1, len(loss) + 1)
        plt.plot(epochs[:100], test_pred, color='red', label='prediction')
        plt.plot(epochs[:100], test_output, color='blue', label='Truth')
        plt.title('Prediction and Truth')
        plt.legend()

        plt.figure()
        plt.plot(epochs, loss, color='red', label='Training loss')
        plt.plot(epochs, val_loss, color='blue', label='Validation loss')
        plt.title('Training and validation loss')
        plt.legend()

        plt.figure()
        plt.plot(epochs, mae, color='red', label='Training mae')
        plt.plot(epochs, val_mae, color='blue', label='Validation mae')
        plt.title('Training and validation mae')
        plt.legend()

        plt.show()
        i = 0
    def _leaf_generator(self,x):
        leaf_input=Input(shape=(x,))

        leaf_output = layers.Dense(self.leafShape[0] * x)(leaf_input)
        leaf_output = layers.LeakyReLU(alpha=0.1)(leaf_output)

        for i in range(len(self.leafShape)-2):
            leaf_output = layers.Dense(self.leafShape[i+2] * x)(leaf_output)
            leaf_output = layers.LeakyReLU(alpha=0.1)(leaf_output)

        leaf_output = layers.Dense(1)(leaf_output)
        final_output = layers.LeakyReLU(alpha=0.1)(leaf_output)
        model=keras.Model(leaf_input,final_output)
        return model

    def _branch_generator(self):
        branch_input = Input(shape=(self.branchShape[0],))
        branch_output = layers.Dense(self.branchShape[0])(branch_input)
        branch_output = layers.LeakyReLU(alpha=0.1)(branch_output)

        for i in range(len(self.branchShape)-2):
            branch_output = layers.Dense(self.branchShape[i+2])(branch_output)
            branch_output = layers.LeakyReLU(alpha=0.1)(branch_output)

        branch_output = layers.Dense(1)(branch_output)
        final_output = layers.LeakyReLU(alpha=0.1)(branch_output)
        model = keras.Model(branch_input, final_output)
        return model

    def _root_generator(self,size):
        root_input=Input(shape=(size,))
        root_output=layers.Dense(1)(root_input)
        model=keras.Model(root_input,root_output)
        return model


# if __name__ == '__main__':
#     path="featureInfo.csv"
#     data=pd.read_csv(path)
#     data=np.array(data)
#     data_rebuild=[]
#     for i in data:
#         if np.isnan(i[0])==0:
#             data_rebuild.append(i)
#     data_rebuild=np.array(data_rebuild)
#     tdnn=TNN()
#
#     tdnn.design_model(origin_data=data_rebuild,
#                       input_shape=26,
#                       leaf_size=4,
#                       leaf_shape_multi=(1,3,9,3,1),
#                       branch_shape=(3,6,9,6,3,1))








