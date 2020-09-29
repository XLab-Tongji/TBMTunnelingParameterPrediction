# -*- coding:utf-8 -*-

import zipfile
import os
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = ['Arial Unicode MS']  # 设置图中中英文可展示字体
import heapq
import numpy as np
import random
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# Zip数据文件夹的绝对路径
ZipDir = '/Users/shuangliz/Desktop/TBMModel/Data'
# 特征重要性排列时重要特征的数量
featureNum = 30
# 上升段-稳定段信息文件地址
parInfoFile = 'parInfo.csv'
# 存放图片的目录地址
parFigAddress = 'Figures/ParFig/'
dtFigAddress = 'Figures/DTFeatureAnalysis/'
pcFigAddress = 'Figures/PCFeatureAnalysis/'
# 存储的图片的文件格式
figForm = '.eps'  # .eps, .png, .pdf
# 最终提取出的特征数据文档
featureExtrAddress = 'featureInfo.csv'


# 生成随机字符串和数字
def getRandomSet(bits=26):
    num_set = [chr(i) for i in range(48,58)]
    char_set = [chr(i) for i in range(97,123)]
    total_set = num_set + char_set
    value_set = "".join(random.sample(total_set, bits))
    return value_set


# 处理异常值：对于异常的值，直接删除
def abnormalValueHaddle(data):
    colsName = data.columns.values.tolist()
    # 对每列数据依次进行处理
    ignoreColName = ['时间戳', '桩号', '运行时间']
    for colName in colsName:
        if colName in ignoreColName:
            continue
        # 获取该列数据
        col = data[colName]
        # 计算该列平均值
        mean = col.mean()
        # 计算该列标准差
        sigma = col.std()
        threeSigma = sigma * 3
        # 记录异常行的索引值
        abnormalIndexList = []
        # 判断是否单个数据与平均值差的绝对值大于三倍的标准差，是则对该行的异常值进行处理
        for curIndex in range(len(col)):
            curValue = col.tolist()[curIndex]
            if curValue - mean > threeSigma or mean - curValue > threeSigma:
                print('abnormal')
                # data.loc[curIndex, colName] = mean
                abnormalIndexList.append(curIndex)
        data.drop(abnormalIndexList, inplace=True)
        # return data


#  特征重要性分析：回归树法
def featureAnalysisDT(dataX, dataY, yName, x_colsName, figName=None, saveName=None):
    reg = DecisionTreeRegressor()
    reg.fit(dataX, dataY)
    _feat_importance = reg.tree_.compute_feature_importances(normalize=True)
    feat_importance = list(filter(lambda x: abs(x) > 0, _feat_importance))
    # 得到重要性排在前10的值及其索引
    global featureNum
    if featureNum > len(feat_importance):
        featureNum = len(feat_importance)
    re1 = list(map(_feat_importance.tolist().index, heapq.nlargest(featureNum, feat_importance)))  # 获得前10个最大值的索引
    re2 = heapq.nlargest(featureNum, feat_importance)  # 获得前n个最大的值
    select_feature_name = []
    print("DT feature importance analysis " + yName + " :")
    for index in range(featureNum):
        print(x_colsName[re1[index]] + ' : ' + str(re2[index]))
        select_feature_name.append(x_colsName[re1[index]])
    plotBarFig(featureNum, select_feature_name, re2, figName=figName, saveName=dtFigAddress + saveName)
    return [re1, re2]


#  特征重要性分析：Pearson correlation
def featureAnalysisPearsonCor(df, yName, figsizeX=12, figsizeY=12, figName=None, saveName=None):
    cor = df.corr()
    plt.figure(figsize=(figsizeX, figsizeY))
    sns.heatmap(cor, annot=False, square=True, linewidths=1)
    plt.title('Pearson Correlation')
    # plt.savefig(pcFigAddress + 'Pearson Correlation ' + str(getRandomSet(bits=6)) + figForm)
    plt.savefig(pcFigAddress + 'Pearson Correlation ' + figForm)
    plt.show()
    cor_target = abs(cor[yName])
    # 选择高相关的特征
    relevant_features = cor_target[cor_target > 0.10]
    relevant_features.drop(yName, axis=0, inplace=True)
    feature_name = []
    relevant_features_sorted = relevant_features.sort_values()
    for index, value in relevant_features_sorted.items():
        feature_name.append(index)
    # 绘制其他变量同所要研究的变量之间的关系柱状图
    print("PC feature importance analysis of " + yName + " :")
    print(relevant_features_sorted)  # type: Series
    save_name = saveName
    if save_name is not None:
        save_name = pcFigAddress + save_name
    plotBarFig(len(relevant_features), feature_name, relevant_features_sorted.tolist(), figName=figName,
               saveName=save_name, figSizeX=figsizeX, figsizeY=figsizeY)
    return relevant_features


# 画上升段-稳定段折线图
def plotParFig(FCol, TCol, VCol, startPoint, endPoint, figSizeX=20, figSizeY=5,
            stableStart=None, stableEnd=None, riseStart=None, riseEnd=None,
               figName=None, saveName=None):
    plt.figure(figsize=(figSizeX, figSizeY))  # 设置画像大小
    plt.plot(FCol / 4, label='F/4', c='b')
    plt.plot(TCol, label='T', c='g')
    plt.plot(VCol * 25, label='S*25', c='r')
    # 画稳定段
    if stableStart is not None and stableEnd is not None:
        plt.axvline(x=stableStart, ls='-', lw=2, c='black', label='Stable')
        plt.axvline(x=stableEnd, ls='-', lw=2, c='black')
    # 画上升段
    if riseStart is not None and riseEnd is not None:
        plt.axvline(x=riseStart, ls='-', lw=2, c='purple', label='Rise')
        plt.axvline(x=riseEnd, ls='-', lw=2, c='purple')
    plt.legend(loc='upper right')  # 展示图例
    plt.xlim([startPoint, endPoint])
    plt.xlabel('time/s')
    plt.ylabel('')
    if figName is not None:
        plt.title(figName)
    if saveName is not None:
        # if figName is None:
        #     figName = getRandomSet()
        plt.savefig(parFigAddress + saveName + figForm)
    # plt.show()


# 画特征柱状图
def plotBarFig(featureNum, featureName, featureImporartance, figSizeX=10, figsizeY=10, figName=None, saveName=None):
    plt.figure(figsize=(figSizeX, figsizeY))
    # 包含每个柱子下标的序列
    index = np.arange(featureNum)
    # 柱子的宽度
    width = 0.45
    # 绘制柱状图，每根柱子的颜色为白色
    # plt.axvline(y=0.2, ls='-', lw=2, c='red')
    # plt.hline(0.2, -2, 10, colors='red', linestyles='--')
    barfig = plt.bar(index, featureImporartance, width, color='#eee', edgecolor='black')
    plt.xlabel('features')
    plt.ylabel('importance')
    # 设置横轴刻度
    rotation = 270
    if featureNum < 6:
        rotation = 0
    plt.xticks(index, featureName, rotation=rotation)
    # plt.xticks(index, featureName)
    # 展示每个柱状图的数值
    for a, b in zip(index, featureImporartance):
        plt.text(a, b+0.01, '%4f' % b, ha='center', va='bottom', fontsize=10)
    # 设置y轴范围
    plt.ylim(0, 1.0)
    if figName is not None:
        plt.title(figName)
    if saveName is not None:
        # if figName is None:
        #     figName = getRandomSet()
        plt.savefig(saveName + '3' + figForm)
    # 展示结果
    plt.show()


# Compute the var and mean of the features
def feature_extraction_for_analysis():
    #  从文档中读取稳定段信息
    parInfo = pd.read_csv(parInfoFile, sep=',')
    # 对每个数据文件进行处理
    zipFiles = os.listdir(ZipDir)
    file_num = 0
    # 特征名列表
    cols = []
    # target名
    stable_cols = ['总推进力', '刀盘扭矩', '推进速度']
    # 存储最终构造的数据的列名
    final_cols = []
    # 最终构造的特征数据
    final_feature_data = []
    for file in zipFiles:
        # print(file)
        # if file_num > 1:
        #     break
        try:
            file_num = file_num + 1
            # 判断是否为zip文件，是则进行处理
            if file.endswith('.zip'):
                z = zipfile.ZipFile(ZipDir + '/' + file, 'r')
                file_name = z.namelist()[0]
                # if file_name != 'CREC188_20150709.txt':
                #     continue
                file_name_suffix = str(file_name).strip().split('.txt')[0]
                # content = z.read(file_name)
                df = pd.read_csv(z.open(file_name), sep='\t', index_col=False)
                df.dropna(how='any', inplace=True)  # 删除所有含缺失值的行
                if df.empty:
                    continue
                FCol = df['总推进力']
                TCol = df['刀盘扭矩']
                VCol = df['推进速度']
                # timeCol = (df['时间戳'] - df['时间戳'][0])/10e6
                # 基于人为判断去掉其余因变量和无关变量参数列
                if len(cols) == 0:
                    cols = df.columns.values.tolist()
                    _cols = cols[:]
                    exclude_name = ['#', '百分比', '最小', '最大', '流量', '浓度', '设定值',
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
                    for col in cols:
                        final_cols.append("上升段"+col+"均值")
                        final_cols.append("上升段"+col+"方差")
                        # final_cols.append("上升段"+col+"斜率")
                    for col in stable_cols:
                        final_cols.append("稳定段"+col+"均值")
                    print('num of features: ' + str(len(cols)))
                print("deal with file " + str(file_num) + ": " + file)
                # 画一整天的掘进情况数据图
                if file_num < 5:
                    plotParFig(FCol, TCol, VCol, 0, df.shape[0], figName=file_name_suffix, saveName=file_name_suffix)
                # 对单个循环段的数据进行处理
                file_date = file_name_suffix.split('_')[1].strip()
                cir_parts = parInfo[(parInfo['date'].isin([file_date]))]
                for row_index in range(cir_parts.shape[0]):
                    start_point = cir_parts.iloc[row_index, 5]
                    end_point = cir_parts.iloc[row_index, 6]
                    # rise_start = cir_parts.iloc[row_index, 1] + start_point
                    # rise_end = cir_parts.iloc[row_index, 2] + start_point
                    rise_start = 120 + start_point
                    rise_end = 150 + start_point
                    stable_start = start_point + (end_point - start_point) / 2 - 25
                    if stable_start < start_point:
                        continue
                    stable_end = stable_start + 50
                    if stable_end > end_point:
                        stable_end = end_point
                    # 画上升段-稳定段数据图
                    sub_f_col = FCol.loc[start_point:end_point+1]
                    sub_t_col = TCol.loc[start_point:end_point+1]
                    sub_v_col = VCol.loc[start_point:end_point+1]
                    fig_name = file_name_suffix + ':' + str(start_point) + '-' + str(end_point)
                    if file_num < 5:
                        plotParFig(sub_f_col, sub_t_col, sub_v_col, start_point, end_point-1, figSizeX=10,
                                figName=fig_name, saveName=fig_name,
                                stableStart=stable_start, stableEnd=stable_end, riseStart=rise_start, riseEnd=rise_end)
                    # 提取上升段、稳定段数据
                    # 上升段数据的均值、方差与拟合直线（x：时间，y：参数数据）的斜率；稳定段F, T数据的均值
                    rise_data = df.loc[rise_start:rise_end, cols]
                    stable_data = df.loc[stable_start:stable_end, stable_cols]
                    # 存储上升段每个参数的均值、方差与拟合直线斜率, 稳定段每个target的均值
                    dealt_feature_data = []
                    for _col_name in cols:
                        col_series = rise_data[_col_name]
                        cor = col_series.var()
                        mean = col_series.mean()
                        dealt_feature_data.append(mean)
                        dealt_feature_data.append(cor)
                        # polyfit_x = col_series.values
                        # polyfit_y = np.array([i for i in range(rise_start, rise_end+1)])
                        # model = np.polyfit(polyfit_x, polyfit_y, 1)  # model is an np array([k, b])
                        # line_k = model[0]
                        # dealt_feature_data.append(line_k)
                    for _col_name in stable_cols:
                        col_series = stable_data[_col_name]
                        mean = col_series.mean()
                        dealt_feature_data.append(mean)
                    final_feature_data.append(dealt_feature_data)
        except Exception:
            print("error when dealing with file " + str(file_num) + file)
            continue
    # final_df: 存储每个循环段上升段数据的均值、方差、拟合直线斜率，稳定段数据（F、T、V）对应的均值
    final_df = pd.DataFrame(final_feature_data, columns=final_cols)
    final_df.to_csv(featureExtrAddress, encoding='utf_8_sig', index=False)


def feature_importance_analysis_from_file(file_name):
    df = pd.read_csv(file_name, sep=',')
    df.dropna(how='any', inplace=True)
    # cols_name = df.columns.values.tolist()
    y_name_list = ['稳定段总推进力均值', '稳定段刀盘扭矩均值', '稳定段推进速度均值']
    for y_name in y_name_list:
        cols_name = df.columns.values.tolist()
        cols_name = filter(lambda x: "方差" not in x, cols_name)
        cols_name = filter(lambda x: "上升段" in x or x == y_name, cols_name)
        featureAnalysisPearsonCor(df[cols_name], y_name, saveName='PC_result_for_' + y_name)


if __name__ == '__main__':
    # feature_extraction_for_analysis()
    feature_importance_analysis_from_file(featureExtrAddress)
