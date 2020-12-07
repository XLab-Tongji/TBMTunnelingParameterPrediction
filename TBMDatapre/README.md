### Environment:

```python3.6.5
python1.6.5
pandas1.0.4
numpy1.18.5
matplotlib3.0.2
```

Main file: ***DataPreprocessing.py***

### RUN

```
python DataPreprocessing.py
```

***Attention:***

Before running, please check the file dir path of your zips. According to your requirement, modify the corresponding variables.

```python
# 存放预处理数据的文件夹，可按需修改
preDataAddress = 'Data'
par_info_file = 'parInfo.csv'
tnn_data_file = 'tnn.csv'
rnn_data_rise_file = 'rnn_rise.csv'
rnn_data_stable_file = 'rnn_stable.csv'
fig_dir = 'Figs'
fig_form = '.png'  # .eps
# 存放zip压缩包的文件夹
# zipAddress = '/Users/shuangliz/Desktop/TBMModel/Data'  # 本地地址
zipAddress = '../Data'  # 服务器容器内地址
```