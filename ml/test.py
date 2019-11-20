from time import sleep          #import
from datetime import datetime
import argparse
import pickle
import os
import numpy as np
import lightgbm as lgb
import pandas as pd

def get_motion_name(m_id):

    if m_id == 0:
        motion = 'up2down'
    elif m_id == 1:
        motion = 'right2left'
    elif m_id == 2:
        motion = 'left2right'
    elif m_id == 3:
        motion = 'clockwise'
    elif m_id == 4:
        motion = 'cClockwise'

    return motion

def isAllZero(line):
    for element in line:
        if float(element) != 0.0:
            return False

    return True

def test_lightGBM(t, models):
    predictions = []

    print ("Start!")
    for model in models:
        prediction = model.predict(t, num_iteration=model.best_iteration)

        predictions.append(prediction)

    predictions = np.mean(predictions, axis=0)

    result = np.argmax(predictions, axis=1)

    print ("Motion Detect: ", result,  "\n", predictions)
    print ()

if __name__ == '__main__':
    bundle = []

    with open('./model/CNN.txt', 'rb') as f:
        model = pickle.load(f)

    print ("Do")
    print ()

    t = []

    with open('./test/up2down.txt', 'rb') as f:
            tmp = np.asarray(pickle.load(f)).flatten()
            t.append(tmp.tolist())
    with open('./test/right2left.txt', 'rb') as f:
            tmp = np.asarray(pickle.load(f)).flatten()
            t.append(tmp.tolist())
    with open('./test/left2right.txt', 'rb') as f:
            tmp = np.asarray(pickle.load(f)).flatten()
            t.append(tmp.tolist())
    with open('./test/clock.txt', 'rb') as f:
            tmp = np.asarray(pickle.load(f)).flatten()
            t.append(tmp.tolist())
    with open('./test/cClock.txt', 'rb') as f:
            tmp = np.asarray(pickle.load(f)).flatten()
            t.append(tmp.tolist())

    t = np.asarray(t)
    t = t.reshape(t.shape[0], 17, 6, 1)

    print (model.predict_classes(t))
