# -*- coding:utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
plt.rcParams['font.sans-serif'] = ['Source Han Sans CN']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

file_paeh = '/Users/shuangliz/Desktop/xlab-土木/11月/data_11.xlsx'
save_fig_dir = 'Figures/ZhuSanJiao/'
fig_form = '.png'


def plotFeature(data, title=None, name=None):
    plt.figure()
    plt.plot(data, color='r')
    # plt.legend(loc='upper right')
    plt.xlabel('time/s')
    plt.title(title)
    plt.savefig(save_fig_dir + name + fig_form)
    plt.show()


# from matplotlib.font_manager import FontManager
# import subprocess
#
# fm = FontManager()
# mat_fonts = set(f.name for f in fm.ttflist)
# #print(mat_fonts)
# output = subprocess.check_output('fc-list :lang=zh -f "%{family}\n"', shell=True)
# #print( '*' * 10, '系统可用的中文字体', '*' * 10)
# #print (output)
# zh_fonts = set(f.split(',', 1)[0] for f in output.decode('utf-8').split('\n'))
# available = mat_fonts & zh_fonts
# print ('*' * 10, '可用的字体', '*' * 10)
# for f in available:
#      print (f)


data = pd.read_excel(file_paeh, header=0, index_col=None)
# columns = data.columns.values  # [3:]
# print('The num of features: ' + str(len(columns)))
# print(columns)
# print(len(columns))
# # date = data['时间']
# dropna_data = data.dropna(axis=1, how='all')
# dropna_columns = dropna_data.columns.values
# print(dropna_columns)
# print(len(dropna_columns))
#
# na_columns = [col for col in columns if col not in dropna_columns]
# print(na_columns)
# print(len(na_columns))

date = data['时间'].map(lambda x: x.split(' ')[0])
print(date.drop_duplicates())
# for col in columns:
#     plotFeature(data[col], title=col, name=col)
    # break



