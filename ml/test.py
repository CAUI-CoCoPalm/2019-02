# numpy ver...

import numpy as np
import os
import pickle
import argparse
import platform
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

UP2DOWN = 0
RIGHT2LEFT = 1
LEFT2RIGHT = 2
CLOCKWISE = 3
CCLOCKWISE = 4

def get_directory(dataset_dir):
    directory = list()

    for name in os.listdir(dataset_dir):
        if os.path.isdir(dataset_dir + name):
            directory.append(os.path.abspath(dataset_dir + name) + '/')

    return directory

def make_data(dataset_dir='./dataset/'):
    motions = get_directory(dataset_dir)
    data = []
    label = []

    print ()
    print (len(motions), "motions found!")
    print ()

    for motion in motions:
        motion_data, motion_label = load_data(motion)
        data.append(motion_data)
        label.append(motion_label)

    return data, label

def isNotValid(one_motion):
    if type(one_motion[0]) != list:
        return True

    if len(one_motion) == 17:
        if len(one_motion[0]) == 6:
            if type(one_motion[0][0]) == str:

                for record in one_motion:
                    zero_cnt = 0
                    for val in record:
                        if float(val) == 0.00:
                            zero_cnt += 1
                    if zero_cnt == 6:
                        return True
                return False
    else:
        return False


def load_data(path_dir):
    # For Windows, split by '\\', -1, remove /
    # For Linux, split by '/', -2
    if (platform.system() == 'Windows'):
        motion = path_dir.split('\\')[-1].replace('/', '')
    else:
        motion = path_dir.split('/')[-2]

    label = []
    data = []
    err_cnt = 0

    file_list = os.listdir(path_dir)

    print ("There're ", len(file_list), " files in '", motion, "'")

    for one_file in file_list:
        file_path = path_dir + one_file
        one_motion = list()

        with open(file_path, 'rb') as f:
            one_motion = pickle.load(f)

        if isNotValid(one_motion):
            err_cnt += 1
            print ("Shape Error:", one_file, ":", one_motion.shape)
            continue
        
        data.append(one_motion)
        
        if motion == 'up2down':
            label.append(UP2DOWN)
        elif motion == 'right2left':
            label.append(RIGHT2LEFT)
        elif motion == 'left2right':
            label.append(LEFT2RIGHT)
        elif motion == 'clockwise':
            label.append(CLOCKWISE)
        elif motion == 'cClockwise':
            label.append(CCLOCKWISE)
     
    print ("Found", err_cnt, "Errors!")
    print ("Label:", motion, " | value:", label[0])
    print ("data's len:", len(data))
    print ("label's len: ", len(label))
    print ("------------------------------------")
    print ()

    return data, label

if __name__ == '__main__':
    data, label = make_data()

    X_train, X_test, y_train, y_test = train_test_split(data, label, test_size=0.2, random_state=2990)
