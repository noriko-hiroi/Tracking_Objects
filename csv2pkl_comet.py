'''
This converts the csv file showing the trajectory of the comet into a pkl file for transformer
csv column is
"cometNo","time[msec]","X","Y","Velocity[nm/sec]","angle[degree]","normpix",Distance
'''
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
#sys.path.append("..")
#import utils
import pickle
import copy
import csv
from datetime import datetime
import time
from io import StringIO
from tqdm import tqdm as tqdm
import datetime

Output_Dir = "C:/Users/dread/PycharmProjects/GeoTrackNet/work/comet/"
Output_Name = "comet_num_time.pkl"
l_csv_filename =["comet_num_time.csv"]
pkl_filename = ["_train.pkl","_valid.pkl","_test.pkl"]


COMETNO, TIME, X, Y, VELO, ANGLE, NORMPIX, DIST = list(range(8))

## LOADING CSV FILES
#======================================
print('Loading...')
l_l_record = [] # list of comet record
n_error = 0
for csv_filename in l_csv_filename:
    data_path = os.path.join(Output_Dir,csv_filename)
    with open(data_path,"r") as f:
        print("Reading ", csv_filename, "...")
        csvReader = csv.reader(f)
        next(csvReader) # skip the legend row
        count = 1
        for row in csvReader:
            if count%1000000 == 0:
                print(count)
            count += 1
            try:
                l_l_record.append([int(row[0]),int(row[1]),
                               int(row[2]),int(row[3]),
                               float(row[4]),float(row[5]),
                               int(row[6]),float(row[7])])
            except:
                n_error += 1
                print('column error:'+ data_path + ' ' + count + 'row')
                continue

## Sorting
#======================================
print('Sorting...')
m_record = np.array(l_l_record)
#del l_l_msg
print("Total number of conet records: ",m_record.shape[0])
X_min = np.min(m_record[:,X])
X_max = np.max(m_record[:,X])
Y_min = np.min(m_record[:,Y])
Y_max = np.max(m_record[:,Y])
Speed_max = np.max(m_record[:,VELO])
print("X min: ",X_min, "X max: ",X_max)
print("Y min: ",Y_min, "Y max: ",Y_max)

sorted_indices = np.lexsort(((m_record[:, 1]), (m_record[:, 0])))
m_record = m_record[sorted_indices]

## Splitting
#======================================
print('Splitting...')
unique = np.unique(m_record[:, COMETNO])
ratios = [1, 2, 7] #[train, valid, test]
total = len(unique)
split_sizes = [int(total*ratio/sum(ratios)) for ratio in ratios]
split_sizes[-1] = total - sum(split_sizes[:-1])
split_unique_values = np.split(unique, np.cumsum(split_sizes)[:-1])
test, valid, train = [m_record[np.isin(m_record[:, 0], uv)] for uv in split_unique_values]

## Converting
#======================================
print('Converting...')
Dic_train = dict()
for v_msg in tqdm(train):
    No = int(v_msg[COMETNO])
    if not (No in list(Dic_train.keys())):
        Dic_train[No] = np.empty((0,8))
    Dic_train[No] = np.concatenate((Dic_train[No], np.expand_dims(v_msg[:8],0)), axis = 0)

Dic_valid = dict()
for v_msg in tqdm(valid):
    No = int(v_msg[COMETNO])
    if not (No in list(Dic_valid.keys())):
        Dic_valid[No] = np.empty((0,8))
    Dic_valid[No] = np.concatenate((Dic_valid[No], np.expand_dims(v_msg[:8],0)), axis = 0)

Dic_test = dict()
for v_msg in tqdm(test):
    No = int(v_msg[COMETNO])
    if not (No in list(Dic_test.keys())):
        Dic_test[No] = np.empty((0,8))
    Dic_test[No] = np.concatenate((Dic_test[No], np.expand_dims(v_msg[:8],0)), axis = 0)

data = [Dic_train, Dic_valid, Dic_test]
## NORMALISATION
#======================================
print('Normalisation...')
for dic in data:
    for k in tqdm(list(dic.keys())):
        v = dic[k]
        v[:,Y] = (v[:,Y] - Y_min)/(Y_max-Y_min)
        v[:,X] = (v[:,X] - X_min)/(X_max-X_min)
        v[:,VELO] = v[:,VELO]/Speed_max
        v[:,ANGLE] = v[:,ANGLE]/360.0

## output
#======================================
new_dict_list = []
print('Outputing...')
for temp in data:
    new_temp = []  # Create a new dictionary to hold modified messages

    for id, v_msg in temp.items():
        updated_v_msg = v_msg[:, [Y, X, VELO, ANGLE, TIME, COMETNO, NORMPIX, DIST]]
        columns_to_remove = [NORMPIX, DIST]
        # 列を削除
        updated_v_msg = np.delete(updated_v_msg, columns_to_remove, axis=1)

        # Store the updated message in the new dictionary
        dict = {"mmsi": int(updated_v_msg[0, 5]), "traj": updated_v_msg}
        new_temp.append(dict)
    new_dict_list.append(new_temp)

for pk, temp in zip(pkl_filename,new_dict_list):
    file_name = os.path.splitext(Output_Name)[0] + pk
    output_filepath = os.path.join(Output_Dir, file_name)
    with open(output_filepath, "wb") as f:
        pickle.dump(temp, f)
print('Finish')

