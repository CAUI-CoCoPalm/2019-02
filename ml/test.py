# numpy ver...

import numpy as np
import os
import pickle
import argparse
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

UP2DOWN = 0
RIGHT2LEFT = 1
LEFT2RIGHT = 2
CLOCKWISE = 3
RCLOCKWISE = 4

def get_directory(dataset_dir):
    directory = []

    for name in os.listdir(dataset_dir):
        if os.path.isdir(dataset_dir + name):
            directory.append(os.path.abspath(dataset_dir + name) + '/')

    return directory

def make_data(dataset_dir='./dataset/'):
    motions = get_directory(dataset_dir)
    data = np.empty((6, 200, 0), float)
    label = np.empty((1, 0), int)

    print (len(motions), "motions found!")

    for motion in motions:
        motion_data, motion_label = load_dataset(motion)
        #data = np.append(data, motion_data, axis=0)
        #label = np.append(label, motion_label, axis=0)

    return data, label

def load_dataset(path_dir):
    motion = path_dir.split('/')[-2]
    data_shape = (34, 6)

    if motion == 'up2down':
        data_shape = (17, 6)

    data = np.empty((6, 0), float)
    label = []
    err_cnt = 0

    file_list = os.listdir(path_dir)
    print ("There're ", len(file_list), " files in '", motion, "'")

    for one_file in file_list:
        file_path = path_dir + one_file
        one_motion = np.load(file_path)

        if one_motion.shape != data_shape:
            err_cnt += 1
            print ("Shape Error:", one_file, ":", one_motion.shape)
            continue
        
        data = np.append(data, one_motion.transpose(), axis=1)
        
        if motion == 'up2down':
            label.append(UP2DOWN)
        elif motion == 'right2left':
            label.append(RIGHT2LEFT)
        elif motion == 'left2right':
            label.append(LEFT2RIGHT)
        elif motion == 'clockwise':
            label.append(CLEFT2RIGHT)
        elif motion == 'rClockwise':
            label.append(CRIGHT2LEFT)
        
    print ("Found", err_cnt, "Errors!")
    print ("Label:", motion, " | value:", label[0])
    print ("data's shape:", data.shape)
    print ("label's len: ", len(label))

    return data, label

if __name__ == '__main__':
    data, label = make_data()

    #X_train, X_test, y_train, y_test = train_test_split(data, label, test_size=0.2, random_state=2990)
