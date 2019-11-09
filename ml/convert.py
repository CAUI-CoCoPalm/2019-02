import argparse
import pickle
import os
import numpy as np

def get_motion_name():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=int,help="0: up2down, 1: right2left, 2: left2right, 3: cright2left, 4: cleft2right", choices=[0,1,2,3,4], metavar='Motion_id', required=True) 
    
    args = parser.parse_args()

    m_id = args.i
    max_record = 34
    motion = ""

    if m_id == 0:
        max_recod = 17
        motion = 'up2down'
    elif m_id == 1:
        motion = 'right2left'
    elif m_id == 2:
        motion = 'left2right'
    elif m_id == 3:
        motion = 'cright2left'
    elif m_id == 4:
        motion = 'cleft2right'

    return motion, max_record

def isExistDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
if __name__ == '__main__':
    
    motion, max_record = get_motion_name()
    result_path = './dataset/' + motion + '/'
    isExistDir(result_path)
    isFileOpen = False

    files = os.listdir(result_path)
   
    print ("current data in", str(result_path), ": ", len(files))

    for f in files:

        if f.split('/')[-1][:2] == 'np_':
            nump_arr = np.load(result_path + f)
            arr = nump_arr.tolist()

            old_f = result_path + f

            new_f = old_f.replace('np_', '')

            with open(new_f, 'wb') as list_f:
                pickle.dump(arr, list_f)

            os.remove(old_f)
            print ('Convert', old_f.split('/')[-1], 'to', new_f.split('/')[-1])
