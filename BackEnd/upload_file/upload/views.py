import os
import csv
import random
import pandas as pd
import numpy as np

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.

from upload_file import settings
from DataPreprocessAPI.DataPreprocessAPI.src.DataPreprocessAPI import DataPreprocessing, zipAddress

# from ModelAPI.PredictAPI import Pre_BPNN, modelName, dataCsv
from TNNModel.model import evaluate_model

from TNNModel.model import get_model_info


def form(request):
    return render(request, 'upload_form.html')


# 上传三个测试数据
# api地址: http://127.0.0.1:8000/upload/testData/
def uploadData(request):
    if request.method == 'GET':
        global dataValue1, dataValue2, dataValue3

        f1 = open(r"D:\课件\大三上\实验杜\Data\upload_file\static\分批测试数据\1\1_tnn.csv",encoding='utf-8')
        f2 = open(r"D:\课件\大三上\实验杜\Data\upload_file\static\分批测试数据\2\2_tnn.csv",encoding='utf-8')
        f3 = open(r"D:\课件\大三上\实验杜\Data\upload_file\static\分批测试数据\3\3_tnn.csv",encoding='utf-8')

        # f1 = open('/Users/mawenbo/PycharmProjects/uploadApi/upload_file/static/分批测试数据/1/1_tnn.csv')
        # f2 = open('/Users/mawenbo/PycharmProjects/uploadApi/upload_file/static/分批测试数据/2/2_tnn.csv')
        # f3 = open('/Users/mawenbo/PycharmProjects/uploadApi/upload_file/static/分批测试数据/3/3_tnn.csv')

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
        return JsonResponse(dataTable[random.randint(0, 2)], json_dumps_params={'ensure_ascii': False}, safe=False)


# 测试结果分析指标
def resultAnalysis(request):
    'D:/github/DuLab'
    if request.method == 'GET':
        test_file = 'D:/github/DuLab/BackEnd/upload_file/DataPreprocessAPI/DataPreprocessAPI/src/Data/tnn.csv'
        f = open(test_file, encoding='utf-8')
        # test_file = '/Users/mawenbo/PycharmProjects/uploadApi/upload_file/DataPreprocessAPI/DataPreprocessAPI/src/Data/tnn.csv'
        data = pd.read_csv(f, sep=',', header=0)
        cols = data.columns.values
        feature_cols = cols[:-3]
        target_col = cols[-1]
        df_x = data[feature_cols]
        series_y = data[target_col]
        array_y = np.array(series_y)
        evaluate_data = []
        evaluate_model(df_x, array_y, model_name='GABPNN_F', target_name='F')
        # print(series_y)
        # model_info = get_model_info('GABPNN_F_history')
        # print(model_info['test_mse'])
        evaluate_model(df_x, array_y, model_name='GABPNN_T', target_name='T')
        evaluate_model(df_x, array_y, model_name='GABPNN_S', target_name='S')
        print(evaluate_data)

        evaluate_data.append(
            {"test_mse": evaluate_model(df_x, array_y, model_name='GABPNN_F', target_name='F')["test_mse"],
             "test_r2_score": evaluate_model(df_x, array_y, model_name='GABPNN_F', target_name='F')["test_r2_score"]})
        evaluate_data.append(
            {"test_mse": evaluate_model(df_x, array_y, model_name='GABPNN_T', target_name='T')["test_mse"],
             "test_r2_score": evaluate_model(df_x, array_y, model_name='GABPNN_T', target_name='T')["test_r2_score"]})
        evaluate_data.append(
            {"test_mse": evaluate_model(df_x, array_y, model_name='GABPNN_S', target_name='S')["test_mse"],
             "test_r2_score": evaluate_model(df_x, array_y, model_name='GABPNN_S', target_name='S')["test_r2_score"]})
        return JsonResponse(evaluate_data, json_dumps_params={'ensure_ascii': False}, safe=False)


# 上传3*2数据预测结果{"r2": "data", "mean_squared_error": "data"}
# 接口地址: http://127.0.0.1:8000/upload/predictModel/
def predictModel(request):
    if request.method == 'POST':
        dataValue = []
        test_file = 'D:/github/DuLab\BackEnd/upload_file/DataPreprocessAPI/DataPreprocessAPI/src/Data/tnn.csv'
        # test_file = '/Users/mawenbo/PycharmProjects/uploadApi/upload_file/DataPreprocessAPI/DataPreprocessAPI/src/Data/tnn.csv'
        f = open(test_file, encoding='utf-8')
        data = pd.read_csv(f, sep=',', header=0)
        cols = data.columns.values
        feature_cols = cols[:-3]
        target_col = cols[-1]
        df_x = data[feature_cols]
        series_y = data[target_col]
        array_y = np.array(series_y)
        evaluate_model(df_x, array_y, model_name='GABPNN_S', target_name='S')
        return JsonResponse(dataValue, json_dumps_params={'ensure_ascii': False}, safe=False)


# # 接收zip文件并进行预处理，返回LSTM的预处理结果
# # 接口地址: http://127.0.0.1:8000/upload/zipFileLSTM/
# def zipFileLSTM(request):
#     if request.method == 'POST':
#         zipFile = request.FILES['zipFile']
#         zipFile = os.path.join(settings.MEDIA_ROOT, zipFile.name)
#         print(zipFile)
#         with open(zipFile, 'wb') as f:
#             for zipFile_Part in request.FILES['zipFile'].chunks():
#                 f.write(zipFile_Part)
#         rf = DataPreprocessing()
#         rf.read_from_zips(zipAddress, is_save=True, is_draw=True)
#         f = open(
#             '/Users/mawenbo/PycharmProjects/uploadApi/upload_file/DataPreprocessAPI/DataPreprocessAPI/src/Data/rnn_rise.csv',
#             'r')
#         reader = csv.reader(f)
#
#         dataTable = {}
#
#         for row in reader:
#             dataTable[row[0]] = {
#                 'a': row[0],
#                 'b': row[1],
#                 'c': row[2],
#                 'd': row[3],
#                 'e': row[4],
#                 'f': row[5],
#                 'g': row[6],
#                 'h': row[7],
#                 'i': row[8],
#                 'j': row[9],
#                 'k': row[10],
#                 'l': row[11],
#                 'm': row[12],
#                 'n': row[13],
#             }
#         k = 1
#         dataValueLSTM = []
#         dataTableLSTM = {}
#         for value in dataTableLSTM.values():
#             if k < 100:
#                 k = k + 1
#                 dataValueLSTM.append(value)
#         dataValueLSTM.pop(0)
#         return JsonResponse(dataValueLSTM, json_dumps_params={'ensure_ascii': False}, safe=False)
#     else:
#         return HttpResponse('method 方法 错误')


# 合理接口
# 接口地址: http://127.0.0.1:8000/LSTMStable/
def LSTMStable(request):
    if request.method == 'GET':
        stable = [{'a': '0', 'b': '14950.5359', 'c': '2880.938546', 'd': '69.03053947'},
                  {'a': '1', 'b': '16850.62708', 'c': '2997.375354', 'd': '69.73435191'},
                  {'a': '2', 'b': '13832.66146', 'c': '2517.061998', 'd': '61.15596538'},
                  {'a': '3', 'b': '14730.40937', 'c': '3413.381918', 'd': '75.33280103'},
                  {'a': '4', 'b': '17564.49935', 'c': '3224.498436', 'd': '72.4002861'},
                  {'a': '5', 'b': '15270.25531', 'c': '2890.581071', 'd': '70.15883018'},
                  {'a': '6', 'b': '15652.45748', 'c': '3015.421035', 'd': '71.47093185'},
                  {'a': '7', 'b': '14971.26691', 'c': '2456.816534', 'd': '70.25122398'},
                  {'a': '8', 'b': '16530.52372', 'c': '3018.013597', 'd': '61.0776142'},
                  {'a': '9', 'b': '17895.66755', 'c': '3022.644051', 'd': '62.73174808'},
                  {'a': '10', 'b': '15721.55502', 'c': '2843.800123', 'd': '64.67181337'},
                  {'a': '11', 'b': '16032.68698', 'c': '3012.146365', 'd': '66.8221002'},
                  {'a': '12', 'b': '15812.80745', 'c': '2823.337554', 'd': '71.5299052'},
                  {'a': '13', 'b': '15583.85842', 'c': '2895.118402', 'd': '66.16974526'},
                  {'a': '14', 'b': '14433.4185', 'c': '2633.778398', 'd': '75.633279'},
                  {'a': '15', 'b': '16293.67591', 'c': '2807.11451', 'd': '69.20145728'},
                  {'a': '16', 'b': '15825.24255', 'c': '2876.40764', 'd': '69.03472491'},
                  {'a': '17', 'b': '16523.77633', 'c': '3102.155339', 'd': '66.78030013'},
                  ]
        return JsonResponse(stable, json_dumps_params={'ensure_ascii': False}, safe=False)


# LSTM预处理数据接口 http://127.0.0.1:8000/LSTMPreData
def LSTMPreData(request):
    global dataValueLSTM
    if request.method == 'GET':
        # f = open(
        #     '/Users/mawenbo/PycharmProjects/uploadApi/upload_file/DataPreprocessAPI/DataPreprocessAPI/src/Data/rnn_rise.csv',
        #     'r')
        f = open(
            r'D:/github/DuLab\BackEnd/upload_file/DataPreprocessAPI/DataPreprocessAPI/src/Data/rnn_rise.csv',
            'r',encoding='utf-8')

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
        return JsonResponse(dataValueLSTM, json_dumps_params={'ensure_ascii': False}, safe=False)


# 接收zip文件并进行预处理，返回预处理结果
# 接口地址: http://127.0.0.1:8000/upload/zipFile/
def zipFile(request):
    if request.method == 'POST':
        zipFile = request.FILES['zipFile']
        zipFile = os.path.join(settings.MEDIA_ROOT, zipFile.name)
        print(zipFile)
        with open(zipFile, 'wb') as f:
            for zipFile_Part in request.FILES['zipFile'].chunks():
                f.write(zipFile_Part)
        rf = DataPreprocessing()
        rf.read_from_zips(zipAddress, is_save=True, is_draw=True)

        f = open(
            r'D:/github/DuLab\BackEnd/upload_file/DataPreprocessAPI/DataPreprocessAPI/src/Data/tnn.csv',
            'r',encoding='utf-8')
        # f = open(
        #     '/Users/mawenbo/PycharmProjects/uploadApi/upload_file/DataPreprocessAPI/DataPreprocessAPI/src/Data/tnn.csv',
        #     'r')

        reader = csv.reader(f)

        dataTable = {}

        for row in reader:
            dataTable[row[0]] = {
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

        # print(dataTable.values())

        k = 1
        dataValue = []
        for value in dataTable.values():
            if k < 12:
                print(value)
                k = k + 1
                dataValue.append(value)
        dataValue.pop(0)
        return JsonResponse(dataValue, json_dumps_params={'ensure_ascii': False}, safe=False)
    else:
        return HttpResponse('method 方法 错误')
