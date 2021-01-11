import csv
import json

# def readCsv():
#     f = open(
#         '/Users/mawenbo/PycharmProjects/uploadApi/upload_file/DataPreprocessAPI/DataPreprocessAPI/src/Data/tnn.csv',
#         'r')
#
#     reader = csv.reader(f)
#
#     dataTable = {}
#
#     for row in reader:
#         dataTable[row[0]] = {
#             'a': row[0],
#             'b': row[1],
#             'c': row[2],
#             'd': row[3],
#             'e': row[4],
#             'f': row[5],
#             'g': row[6],
#             'h': row[7],
#             'i': row[8],
#             'j': row[9],
#             'k': row[10],
#             'l': row[11],
#             'm': row[12],
#             'n': row[13],
#             'o': row[14],
#             'p': row[15],
#             'q': row[16],
#             'r': row[17],
#             's': row[18],
#             't': row[19],
#             'u': row[20],
#             'v': row[21],
#             'w': row[22],
#             'x': row[23],
#             'y': row[24],
#             'z': row[25],
#             'aa': row[26],
#             'ab': row[27],
#             'ac': row[28]
#         }
#
#     # print(dataTable.values())
#
#     k = 1
#     dataValue = []
#     for value in dataTable.values():
#         if k < 12:
#             print(value)
#             k = k + 1
#             dataValue.append(value)
#     dataValue.pop(0)
#     text = json.dumps(dataValue)
#     print(text)
#     # print(dataValue)
#
#
# readCsv()
import random
import xlrd


def readCsv():
    global dataValue1, dataValue2, dataValue3
    f1 = open(r"D:\课件\大三上\实验杜\Data\upload_file\static\分批测试数据\1\1_tnn.csv")
    f2 = open(r"D:\课件\大三上\实验杜\Data\upload_file\static\分批测试数据\2\2_tnn.csv")
    f3 = open(r"D:\课件\大三上\实验杜\Data\upload_file\static\分批测试数据\3\3_tnn.csv")

    reader1 = csv.reader(f1)
    reader2 = csv.reader(f2)
    reader3 = csv.reader(f3)
    dataTable1 = {}
    dataTable2 = {}
    dataTable3 = {}

    for row in reader1:
        dataTable1[row[0]] = {
            'a': row[0],
            'b': row[1],
            'c': row[2],
            'd': row[3],
            'e': row[4],
            'f': row[5],
            'g': row[6],
            'h': row[7],
            'i': row[8],
            'j': row[9],
            'k': row[10],
            'l': row[11],
            'm': row[12],
            'n': row[13],
            'o': row[14],
            'p': row[15],
            'q': row[16],
            'r': row[17],
            's': row[18],
            't': row[19],
            'u': row[20],
            'v': row[21],
            'w': row[22],
            'x': row[23],
            'y': row[24],
            'z': row[25],
            'aa': row[26],
            'ab': row[27],
            'ac': row[28]
        }
        k = 1
        dataValue1 = []
        for value in dataTable1.values():
            if k < 12:
                k = k + 1
                dataValue1.append(value)
        dataValue1.pop(0)

    for row in reader2:
        dataTable2[row[0]] = {
            'a': row[0],
            'b': row[1],
            'c': row[2],
            'd': row[3],
            'e': row[4],
            'f': row[5],
            'g': row[6],
            'h': row[7],
            'i': row[8],
            'j': row[9],
            'k': row[10],
            'l': row[11],
            'm': row[12],
            'n': row[13],
            'o': row[14],
            'p': row[15],
            'q': row[16],
            'r': row[17],
            's': row[18],
            't': row[19],
            'u': row[20],
            'v': row[21],
            'w': row[22],
            'x': row[23],
            'y': row[24],
            'z': row[25],
            'aa': row[26],
            'ab': row[27],
            'ac': row[28]
        }
        k = 1
        dataValue2 = []
        for value in dataTable2.values():
            if k < 12:
                k = k + 1
                dataValue2.append(value)
        dataValue2.pop(0)

    for row in reader3:
        dataTable3[row[0]] = {
            'a': row[0],
            'b': row[1],
            'c': row[2],
            'd': row[3],
            'e': row[4],
            'f': row[5],
            'g': row[6],
            'h': row[7],
            'i': row[8],
            'j': row[9],
            'k': row[10],
            'l': row[11],
            'm': row[12],
            'n': row[13],
            'o': row[14],
            'p': row[15],
            'q': row[16],
            'r': row[17],
            's': row[18],
            't': row[19],
            'u': row[20],
            'v': row[21],
            'w': row[22],
            'x': row[23],
            'y': row[24],
            'z': row[25],
            'aa': row[26],
            'ab': row[27],
            'ac': row[28]
        }
        k = 1
        dataValue3 = []
        for value in dataTable3.values():
            if k < 12:
                k = k + 1
                dataValue3.append(value)
        dataValue3.pop(0)

    dataTable = [dataValue1, dataValue2, dataValue3]

    # print(dataTable[random.randint(0, 2)])

    f = open(
        r'D:\课件\大三上\实验杜\Data\upload_file\DataPreprocessAPI\DataPreprocessAPI\src\Data\rnn_rise.csv',
        'r')

    # f = open(
    #     '/Users/mawenbo/PycharmProjects/uploadApi/upload_file/DataPreprocessAPI/DataPreprocessAPI/src/Data/rnn_rise.csv',
    #     'r')
    reader = csv.reader(f)

    dataTableLSTM = {}

    for row in reader:
        dataTableLSTM[row[0]] = {
            'a': row[0],
            'b': row[1],
            'c': row[2],
            'd': row[3],
            'e': row[4],
            'f': row[5],
            'g': row[6],
            'h': row[7],
            'i': row[8],
            'j': row[9],
            'k': row[10],
            'l': row[11],
            'm': row[12],
            'n': row[13],
        }
        k = 1
        dataValueLSTM = []
        for value in dataTableLSTM.values():
            if k < 100:
                k = k + 1
                dataValueLSTM.append(value)
        dataValueLSTM.pop(0)
    print(dataValueLSTM)


readCsv()
