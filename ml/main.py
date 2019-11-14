import os
import random
import numpy as np
import pandas as pd
import pickle
import gc
import lightgbm as lgb
from sklearn.metrics import accuracy_score, confusion_matrix

with open('test.txt', 'rb') as f:
    test = pickle.load(f)

with open('./model/lightGBM.txt', 'rb') as f:
    models = pickle.load(f)

predicts = []
test = np.asarray(test)
test = test.flatten()
input_ = []
input_.append(test.tolist())

for model in models:
    predict = model.predict(input_, num_iteration=model.best_iteration)
    predicts.append(predict)

predicts = np.mean(predicts, axis=0)
predicts = np.argmax(predicts, axis=1)

print ("predict: ", predicts)
print ("Acc: {}".format(accuracy_score(predicts, [2])))
