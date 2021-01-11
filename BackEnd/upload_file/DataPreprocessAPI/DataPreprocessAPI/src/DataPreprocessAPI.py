# -*- coding:utf-8 -*-

import pandas as pd
import os
import numpy as np
import zipfile
import matplotlib.pyplot as plt
import warnings
from scipy import optimize
import sys
import copy

warnings.filterwarnings("ignore")
# 存放预处理数据的文件夹，可按需修改
preDataAddress = 'DataPreprocessAPI/DataPreprocessAPI/src/Data'
par_info_file = 'parInfo.csv'
tnn_data_file = 'tnn.csv'
rnn_data_rise_file = 'rnn_rise.csv'
rnn_data_stable_file = 'rnn_stable.csv'
fig_dir = 'Figs'
fig_form = '.png'  # .eps
# 存放zip压缩包的文件夹
# zipAddress = '/Users/shuangliz/Desktop/TBMModel/Data'  # 本地地址
zipAddress = 'DataPreprocessAPI/DataPreprocessAPI/Data'  # 服务器容器内地址

# Variables
stable_features = ['总推进力', '刀盘扭矩', '推进速度']
par_info_cols = ['date', 'riseStart', 'riseEnd', 'stableStart', 'stableEnd', 'start', 'end']
bad_file_names = ['20160417', '20170708', '20170129', '20151223']
succeed_loop_num = 800
draw_file_num = 2


class DataPreprocessing:
    def __init__(self):
        # 存放预处理数据地址
        self.dataPath = preDataAddress

        # 记录稳定段和上升段信息文件
        self.parInfoFile = par_info_file
        self.par_num = 0

        # 记录处理后的特征数据
        self.data_dict = dict()
        self.feature_col_names = list()
        # 需存入文档的数据
        self.tnn_features = None  # Dataframe
        self.rnn_rise_features = None  # Dataframe
        self.rnn_stable_features = None  # Dataframe
        self.tnn_feature_names = list()
        self.rnn_rise_feature_names = list()
        self.rnn_stable_feature_names = list()

    def read_from_zip(self, zip_file, is_save=True, is_draw=True, is_initial=True):

        if zip_file.endswith('.zip'):
            print("reading zip file " + zip_file)
            z = None
            try:
                z = zipfile.ZipFile(zip_file, 'r')
            except:
                print("error shows when reading this zip file")
                print(sys.exc_info()[0])
                return
            file_name = z.namelist()[0]
            df = pd.read_csv(z.open(file_name), sep='\t', index_col=False)
            if is_initial:
                self.set_feature_names(df)
            df.dropna(how='any', inplace=True)
            if df is None:
                return None

            par_info_list = self.separate_rise_stable(df, file_name)
            data_key = str(file_name).split('.txt')[0]
            if par_info_list is None or len(par_info_list) == 0:
                print("extract 0 par")
                return None
            else:
                self.build_features_dayly(df, data_key, par_info_list)
                if is_save:
                    print('saving file ... ...')
                    self.save_par_info(par_info_list, preDataAddress + par_info_file)
                    self.save_feature_data(preDataAddress, tnn_data_file, rnn_data_rise_file, rnn_data_stable_file)
                    print('finish saving')
                if is_draw:
                    f_col = df['总推进力']
                    t_col = df['刀盘扭矩']
                    s_col = df['推进速度']
                    self.draw_day_fig(f_col, t_col, s_col, file_name[:-4], is_save=True)
                    for cur_par in par_info_list:
                        self.draw_par_fig(f_col, t_col, s_col, cur_par, is_save=True)
                return par_info_list

    def read_from_zips(self, zip_dir, is_save=True, is_draw=True):
        zipfiles = os.listdir(zip_dir)
        read_file_num = 0
        dealt_file_num = 0
        par_info_total_list = list()
        for file in zipfiles:
            read_file_num += 1
            zip_file = zip_dir + '/' + file
            # 控制self的相关变量初始化
            if len(self.feature_col_names) == 0:
                is_initial = True
            else:
                is_initial = False
            is_continue = False
            # 排除会让程序陷入死循环的文件
            for bad_file_name in bad_file_names:
                if str(file).find(bad_file_name) != -1:
                    is_continue = True
                    break
            if is_continue:
                continue
            # if file.find('20151223') == -1:
            #     continue
            cur_par_info_list = self.read_from_zip(zip_file, is_save=False, is_draw=is_draw, is_initial=is_initial)
            print("finish reading file " + str(read_file_num))
            if cur_par_info_list is None:
                continue
            else:
                dealt_file_num += 1
                print("\033[1;32;47msucceed in dealing file " + str(dealt_file_num) + "\033[0m")
                # 控制程序的运行次数
                if dealt_file_num > succeed_loop_num:
                    break
                # 控制程序的绘画文件数
                if dealt_file_num > draw_file_num:
                    is_draw = False
                par_info_total_list += cur_par_info_list
        if is_save:
            print("saving files ... ...")
            self.save_par_info(par_info_total_list, preDataAddress, par_info_file)
            self.save_feature_data(preDataAddress, tnn_data_file, rnn_data_rise_file, rnn_data_stable_file)
            print("finish saving")
        return par_info_total_list

    def save_par_info(self, par_info_list, file_address, file_name):
        if par_info_list is None or len(par_info_list) == 0:
            return False
        # 生成循环段信息文件
        parInfoDf = pd.DataFrame(par_info_list, columns=par_info_cols)
        # 存放预处理结果的文件夹
        resultDirPath = self.transAddress(file_address)
        # 不存在则创建
        if not os.path.exists(resultDirPath):
            os.makedirs(resultDirPath)
        # 预处理文件路径
        resultFilePath = os.path.join(resultDirPath, file_name)
        # 生成预处理文件
        parInfoDf.to_csv(resultFilePath, encoding="utf_8_sig", index=False)
        return True

    def save_feature_data(self, file_address, tnn_file_name, rnn_rise_file_name, rnn_stable_file_name):
        if self.tnn_features is None or self.rnn_rise_features is None or self.rnn_stable_features is None:
            return False
        # 存放预处理结果的文件夹
        resultDirPath = self.transAddress(file_address)
        # 不存在则创建
        if not os.path.exists(resultDirPath):
            os.makedirs(resultDirPath)
        result_tnn_file_path = os.path.join(resultDirPath, tnn_file_name)
        result_rnn_rise_file_path = os.path.join(resultDirPath, rnn_rise_file_name)
        result_rnn_stable_file_path = os.path.join(resultDirPath, rnn_stable_file_name)
        self.tnn_features.to_csv(result_tnn_file_path, encoding="utf_8_sig", index=False)
        self.rnn_rise_features.to_csv(result_rnn_rise_file_path, encoding='utf_8_sig', index=False)
        self.rnn_stable_features.to_csv(result_rnn_stable_file_path, encoding="utf_8_sig", index=False)
        return True

    def separate_rise_stable(self, df_data, df_id):
        par_info_list = list()
        torque0 = df_data['刀盘扭矩'].values
        # stable_features = ['总推进力', '刀盘扭矩', '推进速度']

        i = 0
        while i < len(torque0):  # 对于循环段的提取
            # 取单个循环段
            origin = i
            while origin < len(torque0):
                if torque0[origin] > 5:
                    break
                origin = origin + 1

            if origin == len(torque0):
                break
            number = origin
            n = 0
            while number < len(torque0) - 9:
                if torque0[number] > 5:
                    n = n + 1
                else:
                    break
                number = number + 1

            if number == len(torque0) - 9:
                break

            end = number - 1

            i = end + 1
            x = self.errorHandle(df_data[origin:end + 2], stable_features)  # 处理异常值
            if x[1] == 0:
                continue
            else:
                dataNonOutliers = x[0]

            torque = dataNonOutliers['刀盘扭矩'].values
            F = dataNonOutliers['总推进力'].values
            speed = dataNonOutliers['推进速度'].values
            stableList = self.stable(speed)  # 根据速度划分稳定段
            if stableList[0] < 40:
                continue
            stableF = self.findFStable(F)
            if int(stableF) == 0:
                continue
            riseNum = self.riseUpdate5(origin, torque, int(stableF), int(stableList[0]), torque0)
            if riseNum == 0:
                continue
            # data_values = self.calculateStable(dataNonOutliers[int(stableList[0]):int(stableList[1] + 1)],
            #                                    stable_features)
            # if stableList[0] < riseNum+29:
            #     stableList[0] = riseNum + 29 + 30
            #     stableList[1] += 30
            # if stableList[1] - stableList[0] < 20:
            #     stableList[1] = stableList[0] + 20
            #     if origin+stableList[1] > end:
            #         stableList[1] = end - origin - 5
            par_size = end - origin
            stableList[0] = int(par_size / 2)
            stableList[1] = int(par_size / 3 * 2)
            if stableList[0] < riseNum + 29:
                continue

            par_info_list.append([df_id[8:-4], riseNum, riseNum + 29, stableList[0], stableList[1], origin, end])
        return par_info_list

    # 处理一天的循环段数据
    def build_features_dayly(self, df, df_key, par_info_list):
        tnn_feature_values = list()
        rnn_rise_feature_values = list()
        rnn_stable_feature_values = list()
        new_df = df[self.feature_col_names]
        self.data_dict[df_key] = new_df

        #  分别处理每个掘进循环段
        for cur_par in par_info_list:
            sub_tnn_feature_values = []
            sub_rnn_rise_feature_values = []
            sub_rnn_stable_feature_values = []

            par_start = cur_par[-2]
            rise_start = cur_par[1] + par_start
            rise_end = cur_par[2] + par_start
            stable_start = cur_par[3] + par_start
            stable_end = cur_par[4] + par_start
            rise_df = new_df[rise_start:rise_end + 1]
            stable_df = new_df[stable_start:stable_end + 1]

            # 上升段特征数据处理
            # rnn上升段计算所需变量
            window_size = 8
            tag_series = pd.Series([self.par_num for _ in range(rise_start, rise_end - window_size + 1)])
            for col in self.feature_col_names:
                cur_series = rise_df[col]
                # tnn: 计算上升段特征数据
                mean = cur_series.mean()
                var = cur_series.var()
                sub_tnn_feature_values.append(mean)
                sub_tnn_feature_values.append(var)
                # rnn: 计算某一特征列窗口特征列
                # cur_series = rise_df[col]
                temps = pd.Series(cur_series.values)
                shifted = temps.shift(1)
                window = shifted.rolling(window=window_size)
                means = window.mean()
                means = means.dropna()
                sub_rnn_rise_feature_values.append(means)
            if sub_rnn_rise_feature_values is None or len(sub_rnn_rise_feature_values) == 0:
                return
            _means_df = pd.concat([rnn_rise_features for rnn_rise_features in sub_rnn_rise_feature_values], axis=1)
            sub_cols = copy.deepcopy(self.rnn_rise_feature_names)
            sub_cols.pop(0)
            means_df = pd.DataFrame(_means_df.values.tolist(), columns=sub_cols)
            means_df.insert(0, "tag", tag_series, True)
            # 稳定段特征数据处理
            sub_rnn_stable_feature_values.append(self.par_num)
            for col in stable_features:
                cur_series = stable_df[col]
                mean = cur_series.mean()
                sub_tnn_feature_values.append(mean)
                sub_rnn_stable_feature_values.append(mean)
            self.par_num += 1
            tnn_feature_values.append(sub_tnn_feature_values)
            rnn_stable_feature_values.append(sub_rnn_stable_feature_values)
            rnn_rise_feature_values.append(means_df)
        self.build_feature_to_self_dayly(tnn_feature_values, rnn_rise_feature_values, rnn_stable_feature_values)

    def build_feature_to_self_dayly(self, tnn_features_list, rnn_rise_features_list, rnn_stable_features_list):
        tnn_features_df = pd.DataFrame(tnn_features_list, columns=self.tnn_feature_names)
        rnn_rise_features_df = pd.concat([means_df for means_df in rnn_rise_features_list])
        rnn_rise_features_df.columns = self.rnn_rise_feature_names
        rnn_stable_features_df = pd.DataFrame(rnn_stable_features_list, columns=self.rnn_stable_feature_names)
        if self.tnn_features is None:
            self.tnn_features = tnn_features_df
        else:
            # self.tnn_features.append(tnn_features_df)
            self.tnn_features = pd.concat([self.tnn_features, tnn_features_df], axis=0)
        if self.rnn_rise_features is None:
            self.rnn_rise_features = rnn_rise_features_df
        else:
            self.rnn_rise_features = pd.concat([self.rnn_rise_features, rnn_rise_features_df], axis=0)
            # self.rnn_rise_features.append(rnn_rise_features_df)
        if self.rnn_stable_features is None:
            self.rnn_stable_features = rnn_stable_features_df
        else:
            # self.rnn_stable_features.append(rnn_stable_features_df)
            self.rnn_stable_features = pd.concat([self.rnn_stable_features, rnn_stable_features_df], axis=0)

    def get_tnn_features(self):
        feature_values = self.tnn_features.values.tolist()
        return self.tnn_feature_names, feature_values

    def get_rnn_rise_features(self):
        feature_values = self.rnn_rise_features.values.tolist()
        return self.rnn_rise_feature_names, feature_values

    def get_rnn_stable_features(self):
        feature_values = self.rnn_stable_features.values.tolist()
        return self.rnn_stable_feature_names, feature_values

    def findFStable(self, F):
        l = len(F)
        if l > 12:
            b = np.zeros((l - 11, 3))
            for j in range(10, l - 11):
                b[j, 1] = np.mean(F[j - 10:j + 11])
            for j in range(l - 11):
                b[j, 2] = j

            c = b[np.lexsort(-b[:, ::-1].T)]
            c0 = np.nonzero(c[:, 1])

            if len(c0[0]) != 0:

                c1 = c[0: max(c0[0]) + 1]

                p = np.polyfit(b[10:max(c0[0]) + 11, 2], c1[:, 1], 20)

                y1 = np.polyval(p, b[:, 2])

                ddd = np.diff(y1, 2)

                st = np.std(ddd[round(0.2 * l):round(0.5 * l)])
                ma = max(ddd[round(0.2 * l):round(0.5 * l)]) + 3 * st
                mi = min(ddd[round(0.2 * l):round(0.5 * l)]) - 3 * st

                t = np.where((ddd < mi) | (ddd > ma))

                for j in range(len(t)):
                    if t[0][j] < round(0.4 * l):
                        t[0][j] = l

                I = min(t[0])

                if c[I, 2] > len(b) - 3:
                    yuzhi = b[int(c[I, 2]), 1]
                else:
                    yuzhi = b[int(c[I, 2] + 2), 1]

                sta = []
                for i in range(len(b)):
                    if b[i, 1] >= yuzhi:
                        sta.append(b[i, 2])

                begin = min(sta)
            else:
                begin = 0
        else:
            begin = 0

        return begin

    # 判断上升段，并选取上升段数据
    def calculateRise(self, dataValue, number):
        info = dataValue[number:number + 5]
        mean = np.mean(info)
        var = np.var(info)
        return [mean, var]

    def calculateRiseUpdate(self, dataValue, number):
        riseData = []
        interval = 6
        for i in range(number, number + 25):
            info = dataValue[i: i + interval]  # 原来给我写的[number:number+intervial]
            mean = np.mean(info)
            var = np.var(info)
            riseData.append((mean, var))

        return riseData

    # 选取稳定段数据
    def calculateStable(self, dataValue, index):
        result = {}
        toDel = []
        rowIndex = dataValue.index
        for i in index:
            rowDataValue = dataValue[i].values
            std = np.std(rowDataValue)
            mean0 = np.mean(rowDataValue)
            # 判断是否单个数据与平均值差的绝对值大于三倍的标准差，是则记录该行
            for info in range(len(rowDataValue)):
                # 记录该行索引值
                if (rowDataValue[info] - mean0) > (3 * std) or (mean0 - rowDataValue[info]) > (3 * std):
                    if rowIndex[info] not in toDel:
                        toDel.append(rowIndex[info])

        dataValue.drop(toDel, inplace=True)

        return dataValue

    # 处理异常值
    def errorHandle(self, data, Index):
        # 行索引列表
        rowIndex = data.index
        # 待删除的行索引列表
        toDel = []
        # 循环每一列
        for columnName in Index:
            # 获取该列数据
            oneColumn = data[columnName]
            # 计算该列平均值
            mean = oneColumn.mean()
            # 计算该列标准差
            sigma = oneColumn.std()
            # 判断是否单个数据与平均值差的绝对值大于三倍的标准差，是则记录该行
            for info in range(len(oneColumn)):
                # 记录该行索引值
                if abs(oneColumn.values[info] - mean) > (3 * sigma):
                    if rowIndex[info] not in toDel:
                        toDel.append(rowIndex[info])
        # 删除所有记录行
        # data.drop(toDel, inplace=True)
        data = data.drop(labels=toDel, axis=0)

        shift = data['推进位移'].values
        flag1 = 1
        if len(shift) == 0:
            flag1 = 0
        else:
            if (max(shift) <= 1600) or (min(shift) >= 200):
                flag1 = 0
        x = [data, flag1]
        return x

    # 将相对路径转绝对路径
    def transAddress(self, relativePath):
        base_dir = os.path.dirname(os.path.abspath('__file__'))  # 绝对路径的父路径
        absolutePath = os.path.normpath(os.path.join(base_dir, relativePath))  # 目录和文件名合成为一个路径，并且规范path字符串格式
        return absolutePath

    def rise(self, torque, FStable, stableOri):  # 计算risenum的函数
        torque0 = torque[stableOri]
        slope = []  # 斜率
        for j in range(stableOri - 8):
            slope.append((torque[j] - torque0) / (j - stableOri))
        sort = np.argsort(-np.array(slope))  # 从小到大排列
        sortList = sort
        validSlopeList = []
        for i in range(0, 5):
            if sortList[i] <= FStable:  # FStable的意思应该是个数值
                validSlopeList.append(sortList[i])

        if len(validSlopeList) == 0:
            riseNum = FStable
        else:
            riseNum = max(validSlopeList)

        return riseNum

    def f_1(self, x, A, B):
        return A * x + B

    def fit(self, j, torque):
        x0 = [j + i for i in range(29)]
        y0 = [torque[j + i] for i in range(29)]
        # x0 = [j, j + 1, j + 2, j + 3, j + 4, j + 5]
        # y0 = [torque[j], torque[j + 1], torque[j + 2], torque[j + 3], torque[j + 4], torque[j + 5]]
        A1, B1 = optimize.curve_fit(self.f_1, x0, y0)[0]
        return A1

    def riseUpdate1(self, torque, FStable, stableOri):  # 最小二乘法拟合斜率进行计算
        slope = []  # 斜率
        for j in range(stableOri - 40):
            # x0 = [j,j+1, j+2, j+3, j+4, j+5]
            # y0 = [torque[j],torque[j+1],torque[j+2],torque[j+3],torque[j+4],torque[j+5]]
            s1 = 0
            s2 = 0
            s3 = 0
            s4 = 0
            n = 40
            for i in range(j, j + n + 1):
                s1 = s1 + i * torque[i]  # xy的均值
                s2 = s2 + i  # x的均值
                s3 = s3 + torque[i]  # y的均值
                s4 = s4 + i * i  # x平方的均值

            # 计算斜率和截距
            b = (s2 * s3 - n * s1) / (s2 * s2 - s4 * n)

            slope.append(b)
        sort = np.argsort(-np.array(slope))  # 从小到大排列
        sortList = sort
        validSlopeList = []
        for i in range(0, 5):
            if sortList[i] <= FStable:  # FStable的意思应该是个数值
                validSlopeList.append(sortList[i])

        if len(validSlopeList) == 0:
            riseNum = FStable
        else:
            riseNum = max(validSlopeList)

        return riseNum

    def riseUpdate2(self, torque, FStable, stableOri):  # 最大斜率次数计算斜率
        torque0 = torque[stableOri]
        slope = []  # 斜率
        count = []

        for j in range(stableOri - 8):
            count0 = 0
            slope.append((torque[j] - torque0) / (j - stableOri))
            intervial = 3
            for i in range(j, j + intervial):
                slope0 = (torque[i] - torque[i + 1]) / (i - i - 1)
                if slope0 > 0:
                    count0 - 1
            count.append(count0)

        sort = np.argsort(-np.array(count))  # 从小到大排列
        sortList = sort
        validSlopeList = []
        for i in range(0, 5):
            if sortList[i] <= FStable:  # FStable的意思应该是个数值
                validSlopeList.append(sortList[i])

        if len(validSlopeList) == 0:
            riseNum = FStable
        else:
            riseNum = max(validSlopeList)

        return riseNum

    def riseUpdate3(self, origin, torque, FStable, stableOri):  # 最小二乘法拟合斜率进行计算
        slope = []  # 斜率
        a = len(torque)
        for j in range(origin, origin + a - 1):
            slope.append(self.fit(j, torque))
        sort = np.argsort(-np.array(slope))  # 从小到大排列
        sortList = sort
        validSlopeList = []

        for i in range(0, 5):
            if sortList[i] <= FStable:  # FStable的意思应该是个数值
                validSlopeList.append(sortList[i])

        if len(validSlopeList) == 0:
            riseNum = FStable
        else:
            riseNum = max(validSlopeList)

        return riseNum

    def riseUpdate4(self, torque, FStable, stableOri):  # 最小二乘法拟合斜率进行计算
        slope = []  # 斜率

        for j in range(stableOri):
            slope.append(self.fit(j, torque))
        sort = np.argsort(-np.array(slope))  # 从小到大排列
        sortList = sort
        validSlopeList = []

        for i in range(0, 5):
            if sortList[i] <= FStable:  # FStable的意思应该是个数值
                validSlopeList.append(sortList[i])

        if len(validSlopeList) == 0:
            riseNum = FStable
        else:
            riseNum = max(validSlopeList)

        return riseNum

    def riseUpdate5(self, origin, torque, FStable, stableOri, torque0):  # 最小二乘法拟合斜率进行计算
        slope = []  # 斜率
        for j in range(stableOri - 30):
            slope.append(self.fit(j, torque))
        sort = np.argsort(-np.array(slope))  # 从小到大排列
        sortList = sort
        validSlopeList = []

        for i in range(0, 5):
            if sortList[i] <= FStable:  # FStable的意思应该是个数值
                validSlopeList.append(sortList[i])

        if len(validSlopeList) == 0:
            riseNum = FStable
        else:
            riseNum = max(validSlopeList)

        order = []
        Num = 0
        for x in range(origin, origin + stableOri):
            if torque0[x] == torque[riseNum]:
                Num = x - origin
                order.append(Num)
                # break
                Num = max(order)
        return Num

    def stable(self, speed):
        l = len(speed)
        if l > 17:
            b = np.zeros((l - 16, 3))  # 初始化一个全部为零的列表

            for j in range(15, l - 16):
                b[j, 1] = np.mean(speed[j - 15:j + 16])
            for j in range(l - 16):
                b[j, 2] = j

            c = b[np.lexsort(-b[:, ::-1].T)]
            c0 = np.nonzero(c[:, 1])

            if len(c0[0]) != 0:

                c1 = c[0: max(c0[0]) + 1]

                p = np.polyfit(b[15:max(c0[0]) + 16, 2], c1[:, 1], 20)

                y1 = np.polyval(p, b[:, 2])

                ddd = np.diff(y1, 2)

                st = np.std(ddd[round(0.2 * l):round(0.5 * l)])
                ma = max(ddd[round(0.2 * l):round(0.5 * l)]) + 3 * st
                mi = min(ddd[round(0.2 * l):round(0.5 * l)]) - 3 * st

                t = np.where((ddd < mi) | (ddd > ma))

                for j in range(len(t)):
                    if t[0][j] < round(0.4 * l):
                        t[0][j] = l

                I = min(t[0])

                if c[I, 2] > len(b) - 3:
                    yuzhi = b[int(c[I, 2]), 1]
                else:
                    yuzhi = b[int(c[I, 2] + 2), 1]

                sta = []
                for i in range(len(b)):
                    if b[i, 1] >= yuzhi:
                        sta.append(b[i, 2])

                begin = min(sta)
                end = max(sta)
                x = [begin, end, sta]
            else:
                x = [0, 1, []]
        else:
            x = [0, 1, []]

        return x

    def draw_par_fig(self, f_col, t_col, s_col, cur_par_info, fig_size_x=20, fig_size_y=5, is_save=True):
        plt.figure(figsize=(fig_size_x, fig_size_y))
        plt.plot(f_col / 4, label='F/4', c='b')
        plt.plot(t_col, label='T', c='g')
        plt.plot(s_col * 25, label='S', c='y')
        par_start = cur_par_info[-2]
        par_end = cur_par_info[-1]
        par_name = str(cur_par_info[0]) + "_" + str(par_start) + "~" + str(par_end)
        stable_start = cur_par_info[3] + par_start
        stable_end = cur_par_info[4] + par_start
        rise_start = cur_par_info[1] + par_start
        rise_end = cur_par_info[2] + par_start
        # 画稳定段
        plt.axvline(x=stable_start, ls='-', lw=2, c='black', label='Stable')
        plt.axvline(x=stable_end, ls='-', lw=2, c='black')
        # 画上升段
        plt.axvline(x=rise_start, ls='-', lw=2, c='red', label='Rise')
        plt.axvline(x=rise_end, ls='-', lw=2, c='red')
        plt.legend(loc='upper right')
        plt.xlim([par_start, par_end])
        plt.xlabel('time/s')
        plt.ylabel('')
        plt.title(par_name)
        if is_save:
            result_dir_path = self.transAddress(fig_dir)
            if not os.path.exists(result_dir_path):
                os.makedirs(result_dir_path)
            plt.savefig(result_dir_path + '/' + par_name + fig_form)
        # plt.show()

    def draw_day_fig(self, f_col, t_col, s_col, day_name, fig_size_x=20, fig_size_y=5, is_save=True):
        plt.figure(figsize=(fig_size_x, fig_size_y))
        plt.plot(f_col / 4, label='F/4', c='b')
        plt.plot(t_col, label='T', c='g')
        plt.plot(s_col * 25, label='S', c='y')
        plt.xlim([0, len(f_col)])
        plt.xlabel('time/s')
        plt.ylabel('')
        plt.title(day_name)
        plt.legend(loc='upper right')
        if is_save:
            result_dir_path = self.transAddress(fig_dir)
            if not os.path.exists(result_dir_path):
                os.makedirs(result_dir_path)
            plt.savefig(result_dir_path + '/' + day_name + fig_form)
        # plt.show()

    def set_feature_names(self, df):
        cols = df.columns.values.tolist()
        _cols = cols[:]
        exclude_name = ['#', '时间戳', '运行时间', '桩号', '百分比', '最小', '最大', '流量', '浓度', '设定值',
                        '温度', '报警值', '停机值', '显示值', '压力液位', '液位', '给定',
                        '润滑压力', '密封压力', '时间', '桩号', '预警设置', '出口压力',
                        '检测', '油缸压力', '护盾压力', '油缸伸出压力', '油缸回收压力', '支撑压力',
                        '油缸位移', '喷水压力', '水泵压力', '频率设置', '最低转速设置', '电机电流',
                        '俯仰角', '滚动角', '油缸压力', '控制油路', '换步泵', '泵压力', 'EP2次数',
                        '腔压力', '给定频率', '.1', '偏差', '护盾位移', '主驱动加压压力', '撑靴压力设定', '贯入度设置']
        for col_name in cols:
            for _name in exclude_name:
                if str(col_name).find(_name) != -1:
                    _cols.remove(col_name)
                    break
        cols = _cols
        self.feature_col_names = cols
        self.rnn_rise_feature_names.append('tag')
        self.rnn_stable_feature_names.append('tag')
        for col in cols:
            self.tnn_feature_names.append("上升段" + col + "均值")
            self.tnn_feature_names.append("上升段" + col + "方差")
            self.rnn_rise_feature_names.append("上升段" + col)
        for col in stable_features:
            self.tnn_feature_names.append("稳定段" + col + "均值")
            self.rnn_stable_feature_names.append("稳定段" + col)
        return True


if __name__ == '__main__':
    # 调用API
    rf = DataPreprocessing()
    rf.read_from_zips(zipAddress, is_save=True, is_draw=True)
