from datetime import datetime
import argparse
import pickle
import os
import numpy as np
import pandas as pd
from time import sleep
from socket import *

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
    elif m_id == 5:
        motion = 'neutral'

    return motion

def isAllZero(line):
    for element in line:
        if float(element) != 0.0:
            return False

    return True
    
if __name__ == '__main__':
    bundle = []

    with open('./model/CNN.txt', 'rb') as f:
        model = pickle.load(f)

    print ("Do")
    print ()

    try:
        serverPort = 32990
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(('', serverPort))
        print ("Ready to Recive")

        total = 0
        while True:
            msg, clientAddr = serverSocket.recvfrom(2048)

            if not msg:
                print ("disconnected from client")
                break

            line = pickle.loads(msg)

            if line[0] == 'IO':
                print ("I/O Error! Check Again!")
                continue
            if isAllZero(line):
                print ("Line Error! Check Again!")
                continue

            bundle.append(line)

            if total > 16:
                bundle.pop(0)
                wrapper = []
                wrapper.append(bundle)

                np_bundle = np.asarray(wrapper)
                np_bundle = np_bundle.reshape(np_bundle.shape[0], 17, 6, 1)
                pred = model.predict_proba(np_bundle)

                if max(pred[0]) > 0.9:
                    motion = get_motion_name(np.argmax(pred[0]))
                    print ("Motion Detect: ", motion, " |", round(max(pred[0]), 4))
                    print ()
                    bundle.clear()
                    total = 0

            else:
                total += 1

    except Exception as e:
        print ("Error:", e)
