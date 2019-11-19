import os
import random
import numpy as np
import pandas as pd
import pickle
import gc
import lightgbm as lgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, KFold
from sklearn.metrics import accuracy_score, confusion_matrix

def get_dataframes():
    df1 = pd.read_csv('./dataset/cClockwise.csv')
    df2 = pd.read_csv('./dataset/clockwise.csv')
    df3 = pd.read_csv('./dataset/left2right.csv')
    df4 = pd.read_csv('./dataset/right2left.csv')
    df5 = pd.read_csv('./dataset/up2down.csv')

    df1['target'] = 4 # 반시계
    df2['target'] = 3 # 시계
    df3['target'] = 2 # 왼오
    df4['target'] = 1 # 오왼
    df5['target'] = 0 # 업다운

    data_num = len(df1) + len(df2) + len(df3) + len(df4) + len(df5)

    df = pd.DataFrame(columns=range(102), index=range(data_num))
    df = pd.concat([df1, df2], axis=0)
    df = pd.concat([df, df3], axis=0)
    df = pd.concat([df, df4], axis=0)
    df = pd.concat([df, df5], axis=0)

    df.append(df1)
    df.append(df2)
    df.append(df3)
    df.append(df4)
    df.append(df5)

    return df

def train_test_split(df):
    df = df.sample(frac=1)
    
    train_num = int(len(df)*0.9)

    train_df = df[:train_num]
    test_df = df[train_num:]

    print ("Train Test Split Result: ")
    print ("Train_df shape:", train_df.shape, "  | Test_df shape:", test_df.shape)

    X_train = train_df.iloc[:, :-1]
    y_train = train_df['target']
    X_test = test_df.iloc[:, :-1]
    y_test = test_df['target']

    return X_train, y_train, X_test, y_test

def train_lightGBM(X, y):
    num_class = y.nunique()

    params = {
            "objective": "multiclass",
            "num_class": num_class,
            "num_leaves": 2**8,
            "max_depth": 5,
            "learning_rate": 0.01,
            "bagging_fraction" : 0.9,  # subsample
            "feature_fraction" : 0.9,  # colsample_bytree
            "bagging_freq" : 2,        # subsample_freq
            "verbosity" : -1
    }

    NFOLDS = 5
    folds = StratifiedKFold(n_splits=NFOLDS, shuffle=True, random_state=2990)
    models = []

    for fold_, (trn_idx, val_idx) in enumerate(folds.split(X, y)):
        print('Fold:',fold_)
        tr_x, tr_y = X.iloc[trn_idx,:], y.iloc[trn_idx]
        vl_x, vl_y = X.iloc[val_idx,:], y.iloc[val_idx]

        lgb_train, lgb_valid = lgb.Dataset(tr_x, tr_y), lgb.Dataset(vl_x, vl_y)
        model = lgb.train(params, lgb_train, 250, valid_sets=[lgb_train, lgb_valid], verbose_eval=100, early_stopping_rounds=20)
        models.append(model)
        print('\n')
        del model, tr_x, tr_y, vl_x, vl_y, lgb_train, lgb_valid
        gc.collect()

    return models

def saveModel(model):
    with open('./model/lightGBM.txt', 'wb') as f:
        pickle.dump(model, f)

def inference(X_test, y_test, models):
    predictions = []
    for model in models:
        prediction = model.predict(X_test, num_iteration=model.best_iteration)
        predictions.append(prediction)
    predictions = np.mean(predictions, axis=0)
    predictions = np.argmax(predictions, axis=1)

    print("Accuracy: {}".format(accuracy_score(predictions, y_test)))

if __name__ == '__main__':
    data = get_dataframes()
    X_train, y_train, X_test, y_test = train_test_split(data)
    lightGBM = train_lightGBM(X_train, y_train)
    saveModel(lightGBM)

    inference(X_test, y_test, lightGBM)
