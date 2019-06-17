# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:02:45 2019

@author: DELL
"""
import prep
import training
import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode', required = True, help = "train for training model, test for testing on holdout data")
parser.add_argument('-d', '--dir', help = "Place files in directory (Absolute Path)")
args = vars(parser.parse_args())

filespath = args['dir']
filespath = os.getcwd()

def train(directory):
    #load training data and aggregate from "time" series to regular data
    train = prep.create_featureframe(raw_path = filespath + "\\safety\\features",
                                     label_path = filespath + "\\safety\\labels",
                                     labels = True)
    
    #export created file to csv and 
    train.to_csv('fframe.csv')
    train = pd.DataFrame.from_csv('fframe.csv')
    
    #create and save model file(s)
    training.train_model(train)

def test(directory):
    #load holdout set and apply same transforms / engineering to holdout set
    holdout = prep.create_featureframe(raw_path = filespath + "\\safety\\holdout",
                                       label_path = filespath + "\\safety\\holdout\\labels",
                                       labels = True)
    
    #import 10th fold model and make predictions
    predictions = training.holdout_predictions(model_path = filespath + "\\models\\best_model_fold_10.hdf5",
                                               holdout_dataframe = holdout)
    print(predictions)

if args['mode'] == 'train':
    train(filespath)
elif args['mode'] == 'test':
    test(filespath)
else:
    print("Enter correct mode. Valid modes are train and test")