# -*- coding:utf-8 -*-

import pandas as pd
import os
import zipfile

file_time = '20171113'

zip_address = '/Users/shuangliz/Desktop/TBMModel/Data'
par_info = [730,  12163]
zipfiles = os.listdir(zip_address)
for file in zipfiles:
    if str(file).index(file_time) != 0 and str(file).endswith('.zip'):
        zip_file = zip_address + '/' + file
        z = zipfile.ZipFile(zip_file, 'r')
        file_name = z.namelist()[0]
        df = pd.read_csv(z.open(file_name), sep='\t', index_col=False)
        df.dropna(how='any', axis=0, inplace=True)
        # new_df = pd.DataFrame(columns=df.columns.values)
        start = par_info[0]
        end = par_info[1]
        new_df = df[start:end+1]
        print(new_df.shape)
        new_df.to_csv(file_time+'.txt', encoding='utf_8_sig', index=False)
        break
