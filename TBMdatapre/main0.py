import matplotlib
import pandas as pd
import os
import numpy as np
import zipfile
import matplotlib.pyplot as plt

from scipy import optimize

# 相对路径均为相对DataPreprocessing.py的路径
# 存放txt数据的文件夹
txtAddress = '/Users/shuangliz/Desktop/TBMModel/txtData'

# 存放预处理数据的文件夹
preDataAddress = '../TBMPreproData'

# 存放zip压缩包的文件夹
zipAddress = '/Users/shuangliz/Desktop/TBMModel/Data'

# 存放可视化图片
picDirAddress = '../DataPic'

class RF:
    def __init__(self):
        # 存放预处理数据地址
        self.dataPath = 'TBMdatapre'  # preDataAddress#

        # 预处理数据文件名
        self.DataFileName1 = 'riseFeature.csv'  # 'allIndexRF.csv'#
        self.DataFileName2 = 'stableFeature.csv'
        # Address为存放txt文件夹相对于DataPreprocessing.py的路径
        self.Address = txtAddress

        # zipAddress为存放原始zip文件的文件夹，为相对于该脚本的路径
        self.zipAddress = zipAddress

        # RFIndex为RF需要使用数据的列索引，即参数名称
        self.RFIndex = ['总推进力', '刀盘功率', '刀盘扭矩', '推进速度', '刀盘速度给定', '刀盘转速', '推进位移']

        # RFStableIndex为稳定段所需数据的列索引
        self.RFStableIndex = ['总推进力', '刀盘扭矩', '推进速度']
        self.resultList = []
        self.stableResultList = []
        # 处理原始数据的缺失和误差
        self.dataDict = AllTxtHandle(self.Address, self.RFIndex)

        # 记录每个上升段及其对应的稳定段信息
        self.parInfo = []

        # 记录稳定段和上升段信息文件
        self.parInfoFile = 'parInfo0.csv'

    def findList(self,dataNonOutliers,riseNum,flag,num):
        result = {}
        for index in self.RFIndex:
            if index != '推进位移':
                riseList = self.calculateRise(dataNonOutliers[index].values, riseNum + num)
                result['tag'] = flag
                result['rise_' + index + '均值'] = riseList[0]
                result['rise_' + index + '方差'] = riseList[1]
        self.resultList.append(result)

    def RFData(self):
        flag = 0
        for date in self.dataDict:
            data = self.dataDict[date]
            torque0 = data['刀盘扭矩'].values
            stableList = []
            i = 0
            while i < len(torque0):#对于循环段的提取
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
                while number < len(torque0)-9:
                    if torque0[number] > 5:
                        n = n + 1
                    else:
                        break
                    number = number + 1

                if number == len(torque0)-9:
                    break

                end = number - 1

                i = end + 1

                index = self.RFStableIndex
                # dataNonOutliers = errorHandle(data[origin:end + 2], index)
                x = errorHandle(data[origin:end + 2], index)#处理异常值
                if x[1] == 0:
                    continue
                else:
                    dataNonOutliers = x[0]

                torque = dataNonOutliers['刀盘扭矩'].values
                F = dataNonOutliers['总推进力'].values
                speed = dataNonOutliers['推进速度'].values

                flag += 1


                stableList = stable(speed)# 根据速度划分稳定段

                if stableList[0] < 40:
                    continue

                stableF = self.findFStable(F)

                if int(stableF) == 0:
                    continue

                riseNum = riseUpdate5(origin,torque, int(stableF), int(stableList[0]),torque0)
                if riseNum==0:
                    continue

                # print(riseNum)



                riseList = {}
                for x in range(24):
                    self.findList(dataNonOutliers, riseNum, flag, x)

                dataValues = calculateStable(dataNonOutliers[int(stableList[0]):int(stableList[1] + 1)]
                                             , self.RFStableIndex)
                stableResult = {}
                for index in self.RFStableIndex:

                    if index == '推进速度':
                        stableResult['tag'] = flag
                        stableResult['stable_S'] = np.mean(dataValues[index].values)

                    if index =='刀盘扭矩':
                        stableResult['tag'] = flag
                        stableResult['stable_T'] = np.mean(dataValues[index].values)

                    if index =='总推进力':
                        stableResult['tag'] = flag
                        stableResult['stable_F'] = np.mean(dataValues[index].values)

                if flag >= 1:
                    if stableList[0] < riseNum+29:
                        continue
                    # 将上升段和稳定段信息数据存入
                    # self.resultList.append(result)
                    self.stableResultList.append(stableResult)
                    self.parInfo.append([date[8:-4], riseNum, riseNum+29, stableList[0], stableList[1], origin, end])

        # dfrise = pd.DataFrame(self.resultList)
        # dfstable = pd.DataFrame(self.stableResultList)
        # # 生成预处理数文件
        # createPreproData(dfrise, self.dataPath, self.DataFileName1)
        # createPreproData(dfstable, self.dataPath, self.DataFileName2)
        # 生成循环段信息文件
        parInfoDf = pd.DataFrame(self.parInfo, columns=['date', 'riseStart', 'riseEnd', 'stableStart', 'stableEnd',
                                                        'start', 'end'])
        createPreproData(parInfoDf, self.dataPath, self.parInfoFile)

        # return df
        # print(self.dataDict)
        # for data_id in self.dataDict:
        #     data = self.dataDict[data_id]
        #     print(data.shape)
        #     print(data.columns.values)

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
            info = dataValue[i: i + interval]#原来给我写的[number:number+intervial]
            mean = np.mean(info)
            var = np.var(info)
            riseData.append((mean, var))

        return riseData


# 选取稳定段数据
def calculateStable(dataValue, index):
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


# 生成预处理数据文件
def createPreproData(df, address, name):
    # 存放预处理结果的文件夹
    resultDirPath = transAddress(address)
    # 不存在则创建
    if not os.path.exists(resultDirPath):
        os.makedirs(resultDirPath)
    # 预处理文件路径
    resultFilePath = os.path.join(resultDirPath, name)
    # 生成预处理文件
    df.to_csv(resultFilePath, encoding="utf_8_sig", index=False)

    return resultFilePath


# 调用该函数处理文件夹下所有txt文件，dirAddress为相对DataPreprocessing.py的路径，index为需要使用数据的列索引，即参数名称
def AllTxtHandle(dirAddress, index):
    # 因为python的相对路径默认为相对运行文件的路径，所以转为绝对路径
    address = transAddress(dirAddress)
    # if os.listdir(address) is None:
    #     AllUnZip(zipAddress, txtAddress)
    dataDict = {}
    # 便利文件夹下所有文件
    for root, dirs, files in os.walk(address):
        file_num = 0
        for file in files:
            path = os.path.join(root, file)
            # 处理单个txt文件
            if file.endswith('txt'):
                try:
                    dataDict[file] = oneTxtHandle(path, index)
                    file_num += 1
                    if file_num > 1:
                        break
                except:
                    print(file + ' has a problem in oneTxtHandle')
            else:
                print(file + ' is not a txt')
            break

    return dataDict


# 调用该函数读取单个txt文件数据，oneDataAddress为相对DataPreprocessing.py的路径，index为需要使用数据的列索引，即参数名称
def oneTxtHandle(oneDataAddress, index):
    # 因为python的相对路径默认为相对运行文件的路径，所以转为绝对路径
    address = transAddress(oneDataAddress)
    # 读入数据
    basicData = pd.read_csv(address, sep='\t', index_col=False)
    # 选取需要的列组成DataFrame
    # basicData = basicData.dropna(axis=1, how='all')
    # index = list(basicData.keys())[2:]
    frame = pd.DataFrame(basicData, columns=index)
    # frame = pd.DataFrame(basicData, columns=index)
    # 删除缺失行：当行中有任意一个值为缺失时，删除行
    # print(frame)
    data_del_lack_row = frame.dropna()
    # 处理误差
    # print(data_del_lack_row)
    oneTxtData = data_del_lack_row  # errorHandle(data_del_lack_row, index)
    return oneTxtData


# 处理异常值
def errorHandle(data, Index):
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
            if (oneColumn.values[info] - mean) > (3 * sigma) or (mean - oneColumn.values[info]) > (3 * sigma):
                if rowIndex[info] not in toDel:
                    toDel.append(rowIndex[info])
    # 删除所有记录行
    data.drop(toDel, inplace=True)

    shift = data['推进位移'].values
    flag1 = 1
    if len(shift) == 0:
        flag1 = 0
    else:
        if (max(shift) <= 1600) or (min(shift) >= 200):
            flag1 = 0
    x = [data, flag1]
    # print(x)
    return x


# 将相对路径转绝对路径
def transAddress(relativePath):
    base_dir = os.path.dirname(os.path.abspath('__file__'))#绝对路径的父路径
    absolutePath = os.path.normpath(os.path.join(base_dir, relativePath))#目录和文件名合成为一个路径，并且规范path字符串格式
    return absolutePath


# 解压缩函数
def AllUnZip(zipAddress, txtAddress):
    print(zipAddress)
    zipDirPath = transAddress(zipAddress)
    txtDirPath = transAddress(txtAddress)
    print(zipDirPath)
    print(txtDirPath)
    # 不存在txt存放目录则创建
    if not os.path.exists(txtDirPath):
        os.makedirs(txtDirPath)
    # 遍历压缩包目录下所有压缩包
    for root, dirs, files in os.walk(zipDirPath):
        for file in files:
            filePath = os.path.join(root, file)
            # 解压单个压缩包
            r = zipfile.is_zipfile(filePath)
            if r:
                # 如果解压缩文件并不存在，解压缩该压缩包
                if not os.path.exists(txtDirPath + file[0:-4] + '.txt'):
                    fz = zipfile.ZipFile(filePath, 'r')
                    try:
                        for zipFile in fz.namelist():
                            fz.extract(zipFile, txtDirPath)
                            fz.close()
                    except:
                        print(file + ' has a problem in AllUnZip')
            else:
                print(file + ' is not zip')


def rise(torque, FStable, stableOri):#计算risenum的函数
    torque0 = torque[stableOri]
    slope = []#斜率
    for j in range(stableOri - 8):
        slope.append((torque[j] - torque0) / (j - stableOri))
    print(slope)
    sort = np.argsort(-np.array(slope))  #从小到大排列
    print(sort)
    sortList = sort
    validSlopeList = []
    for i in range(0, 5):
        if sortList[i] <= FStable:#FStable的意思应该是个数值
            validSlopeList.append(sortList[i])

    if len(validSlopeList) == 0:
        riseNum = FStable
    else:
        riseNum = max(validSlopeList)

    return riseNum


def f_1(x, A, B):
    return A * x + B





def riseUpdate1(torque, FStable, stableOri):#最小二乘法拟合斜率进行计算
    slope = []#斜率
    for j in range(stableOri - 40):
        # x0 = [j,j+1, j+2, j+3, j+4, j+5]
        # y0 = [torque[j],torque[j+1],torque[j+2],torque[j+3],torque[j+4],torque[j+5]]
        s1 = 0
        s2 = 0
        s3 = 0
        s4 = 0
        n = 40
        for i in range(j,j+n+1):
            s1 = s1 + i * torque[i]# xy的均值
            s2 = s2 + i     #x的均值
            s3 = s3 + torque[i]   #y的均值
            s4 = s4 + i*i    #x平方的均值

        # 计算斜率和截距
        b = (s2 * s3 - n * s1) / (s2 * s2 - s4 * n)


        slope.append(b)
    print(max(slope))
    print(len(slope))
    sort = np.argsort(-np.array(slope))  #从小到大排列
    print(sort)
    sortList = sort
    validSlopeList = []
    for i in range(0, 5):
        if sortList[i] <= FStable:#FStable的意思应该是个数值
            validSlopeList.append(sortList[i])

    if len(validSlopeList) == 0:
        riseNum = FStable
    else:
        riseNum = max(validSlopeList)
    return riseNum


def riseUpdate2(torque, FStable, stableOri):#最大斜率次数计算斜率
    torque0 = torque[stableOri]
    slope = []#斜率
    count = []
    for j in range(stableOri - 8):
        count0 = 0
        slope.append((torque[j] - torque0) / (j - stableOri))
        intervial=3
        for i in range(j,j+intervial):
            slope0=(torque[i] - torque[i+1]) / (i - i-1)
            if slope0>0:
                count0-1
        count.append(count0)

    sort = np.argsort(-np.array(count))  # 从小到大排列
    print(sort)
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


def fit(j,torque):
    x0 = [j+i for i in range(29)]
    y0 = [torque[j+i] for i in range(29)]
    # x0 = [j, j + 1, j + 2, j + 3, j + 4, j + 5]
    # y0 = [torque[j], torque[j + 1], torque[j + 2], torque[j + 3], torque[j + 4], torque[j + 5]]
    A1, B1 = optimize.curve_fit(f_1, x0, y0)[0]
    return A1


def riseUpdate3(origin,torque, FStable, stableOri):  # 最小二乘法拟合斜率进行计算
    slope = []  # 斜率
    a=len(torque)
    for j in range(origin,origin+a-1):
        slope.append(fit(j,torque))
    print(max(slope))
    print(len(slope))
    sort = np.argsort(-np.array(slope))  # 从小到大排列
    print(sort)
    sortList = sort
    validSlopeList = []

    for i in range(0, 5):
        if sortList[i] <= FStable:  # FStable的意思应该是个数值
            validSlopeList.append(sortList[i])

    if len(validSlopeList) == 0:
        riseNum = FStable
    else:
        riseNum = max(validSlopeList)
    print(riseNum)
    print(FStable)

    print(torque[riseNum],torque[riseNum+1],torque[riseNum+2],torque[riseNum+3],torque[riseNum+4],torque[riseNum+5])
    return riseNum


def riseUpdate4(torque, FStable, stableOri):  # 最小二乘法拟合斜率进行计算
    slope = []  # 斜率

    for j in range(stableOri):
        slope.append(fit(j, torque))
    print(max(slope))
    print(len(slope))
    sort = np.argsort(-np.array(slope))  #从小到大排列
    print(sort)
    sortList = sort
    validSlopeList = []

    for i in range(0, 5):
        if sortList[i] <= FStable:  # FStable的意思应该是个数值
            validSlopeList.append(sortList[i])

    if len(validSlopeList) == 0:
        riseNum = FStable
    else:
        riseNum = max(validSlopeList)
    print(riseNum)
    print(FStable)

    print(torque[riseNum],torque[riseNum+1],torque[riseNum+2],torque[riseNum+3],torque[riseNum+4],torque[riseNum+5])
    return riseNum


def riseUpdate5(origin,torque, FStable, stableOri,torque0):  # 最小二乘法拟合斜率进行计算
    slope = []#斜率
    for j in range(stableOri-30):
        slope.append(fit(j,torque))
    print(max(slope))
    print(len(slope))
    print(slope)
    # print(len(slope))
    sort = np.argsort(-np.array(slope))  #从小到大排列
    # print(sort)
    sortList = sort
    validSlopeList = []

    for i in range(0, 5):
        if sortList[i] <= FStable:#FStable的意思应该是个数值
            validSlopeList.append(sortList[i])

    if len(validSlopeList) == 0:
        riseNum = FStable
    else:
        riseNum = max(validSlopeList)
    print(riseNum)
    # print(FStable)

    print(torque[riseNum],torque[riseNum+1],torque[riseNum+2],torque[riseNum+3],torque[riseNum+4],torque[riseNum+5])
    print(origin)
    # print(stableOri)
    order = []
    Num = 0
    for x in range(origin,origin+stableOri):
        # print(torque0[x])
        if torque0[x] == torque[riseNum]:
            print(x)
            print(torque0[x])
            Num = x-origin
            order.append(Num)

            print(riseNum)
            print(order)
            # break
            Num = max(order)
    print(Num)
    return Num


def stable(speed):
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


if __name__ == '__main__':
    rf = RF()
    rf.RFData()
