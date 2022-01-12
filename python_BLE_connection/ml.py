# importing necessary libraries
import csv

from sklearn import datasets
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import model_from_json

import numpy as np
import matplotlib.pyplot as plt
import os
import csv


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Format of input CSV:
# gyro x y x, accel x y z
# Forearm then upper arm
# UP: 1 - 620    == 0        --> 1 - 1500
# DOWN: 621 - 1220    == 1   --> 1501 - 3000
# MIDDLE: 1221 - 1800   == 2 --> 3001 - 4500
# WAVE: 1801 - 3100    == 3  --> 4500 - 6000
# CLAP: 3101 - 5000  == 4    --> 6001 - 7900

# Constants
SAMPLE_RATE = 10
NUM_VALUES = 12
UP_DATA = 1500 # -- > 620
DOWN_DATA = 1500 # -- > 600
MIDDLE_DATA = 1500 # -- > 580
WAVE_DATA = 1500 # --> 1300
CLAP_DATA = 1900 # --> 1900
TOTAL_DATA = UP_DATA + DOWN_DATA + MIDDLE_DATA + WAVE_DATA + CLAP_DATA
#STAT_DATA = MIDDLE_DATA + UP_DATA + DOWN_DATA
STAT_DATA = TOTAL_DATA
class_names = ['UP', 'DOWN', 'MIDDLE', 'WAVE', 'CLAP']


# Input: list of sensor readings
# Output: list of max, min, mean and variance
def extract_feature(sensor_value):
    returnlist = []
    #print(sensor_value)
    maxval = max(sensor_value)
    minval = min(sensor_value)
    meanval = sum(sensor_value)/len(sensor_value)
    varianceval = sum((i - meanval) ** 2 for i in sensor_value) / len(sensor_value)

    returnlist.append(maxval)
    returnlist.append(minval)
    returnlist.append(meanval)
    returnlist.append(varianceval)

    return returnlist


# Feature extraction for a list
# [Max, min, mean, variances]
# Input: [[gx, gy, gz, ax, ay,az, gx2, gy2, gz2, ax2, ay2, az2],[...],...]
# Output:  [gxmax gxmin .... az2mmean az2variance]
def extract_features_for_list(sensor_values):
    #print(len(sensor_values)) = 10
    #print(len(sensor_values[0])) = 12
    global SAMPLE_RATE
    ax = []
    ay = []
    az = []
    gx = []
    gy = []
    gz = []
    ax2 = []
    ay2 = []
    az2 = []
    gx2 = []
    gy2 = []
    gz2 = []
    for i in sensor_values:
        gx.append(i[0])

    for i in sensor_values:
        gy.append(i[1])

    for i in sensor_values:
        gz.append(i[2])

    for i in sensor_values:
        ax.append(i[3])

    for i in sensor_values:
        ay.append(i[4])

    for i in sensor_values:
        az.append(i[5])

    for i in sensor_values:
        gx2.append(i[6])

    for i in sensor_values:
        gy2.append(i[7])

    for i in sensor_values:
        gz2.append(i[8])

    for i in sensor_values:
        ax2.append(i[9])

    for i in sensor_values:
        ay2.append(i[10])

    for i in sensor_values:
        az2.append(i[11])

    returnlist = []
    returnlist = returnlist + extract_feature(gx)
    returnlist = returnlist + extract_feature(gy)
    returnlist = returnlist + extract_feature(gz)
    returnlist = returnlist + extract_feature(ax)
    returnlist = returnlist + extract_feature(ay)
    returnlist = returnlist + extract_feature(az)
    returnlist = returnlist + extract_feature(gx2)
    returnlist = returnlist + extract_feature(gy2)
    returnlist = returnlist + extract_feature(gz2)
    returnlist = returnlist + extract_feature(ax2)
    returnlist = returnlist + extract_feature(ay2)
    returnlist = returnlist + extract_feature(az2)
    return returnlist

# extraction for list containing lists containing lists
# Input: [[[...],[...]...],[...],...] list containg a few matrices with SAMPLE_RATE
# amount of sensor data in each matrix
def extract_all_feature(sensor_matrix):
    returnlist = []
    #print(sensor_matrix)
    for values in sensor_matrix:
        returnlist.append(extract_features_for_list(values))
    return returnlist


# To make the models
def make_models():
# For reading data in
    y = []
    X = []
    count = 0
    ystat = []
    Xstat = [] # just vectors with raw values
    Xtemp = [] # just vectors with raw values
    ytemp = []

    with open('allLabels.csv', 'r') as cvsFile:
        reader = csv.reader(cvsFile)
        for row in reader:
            if count != 0:
                if count < STAT_DATA:
                    ystat.append(int(row[0]))
                    count = count + 1
                y.append(int(row[0]))
            else :
                count = count + 1
        cvsFile.close()
    count = 0
    with open('allData.csv', 'r') as cvsFile:
        reader = csv.reader(cvsFile)
        for row in reader:
            temp = []
            if count != 0:
                for i in range(0,NUM_VALUES):
                    temp.append(float(row[i]))
                if count < STAT_DATA:
                    Xstat.append(temp)
                    count = count + 1
                X.append(temp)
            else:
                count = count + 1
        cvsFile.close()

    # for dynamic classification
    for i in range(0,int(TOTAL_DATA/SAMPLE_RATE)):
        temp2 = []
        for j in range(0,SAMPLE_RATE):
            #print(str(i) + " and " + str(j))
            temp2.append(X[i*SAMPLE_RATE+j])
        Xtemp.append(temp2)
        ytemp.append(y[i*SAMPLE_RATE+j])

    # extract specific features: max, min, mean, variance
    Xfeature = extract_all_feature(Xtemp)

    # dividing X, y into train and test data
    X_train, X_test, y_train, y_test = train_test_split(Xfeature, ytemp, random_state = 0)
    train_static, test_static, train_static_labels, test_static_labels = train_test_split(Xfeature, ytemp, random_state = 0)
    train_dynamic, test_dynamic, train_dynamic_labels, test_dynamic_labels = train_test_split(Xfeature, ytemp, random_state = 0)


    # training a Naive Bayes classifier
    from sklearn.naive_bayes import GaussianNB
    gnb = GaussianNB().fit(X_train, y_train)
    gnb_predictions = gnb.predict(X_test)
    accuracygnb = gnb.score(X_test, y_test)
    print("NB: " + str(accuracygnb))
    cmgnb = confusion_matrix(y_test, gnb_predictions)
    print(cmgnb)

    # training a DescisionTreeClassifier
    from sklearn.tree import DecisionTreeClassifier
    dtree_model = DecisionTreeClassifier(max_depth = 2).fit(X_train, y_train)
    dtree_predictions = dtree_model.predict(X_test)
    cmdtree = confusion_matrix(y_test, dtree_predictions)
    accuracycmd = dtree_model.score(X_test, y_test)
    print("Decision Tree: " + str(accuracycmd))
    print(cmdtree)

    # training a linear SVM classifier
    from sklearn.svm import SVC
    svm_model_linear = SVC(kernel = 'linear', C = 1).fit(X_train, y_train)
    svm_predictions = svm_model_linear.predict(X_test)
    accuracysvm = svm_model_linear.score(X_test, y_test)
    cmsvm = confusion_matrix(y_test, svm_predictions)
    print("SVM: " + str(accuracysvm))
    print(cmsvm)

    # training a KNN classifier
    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier(n_neighbors = 6).fit(X_train, y_train)
    accuracyknn = knn.score(X_test, y_test)
    knn_predictions = knn.predict(X_test)
    cmknn = confusion_matrix(y_test, knn_predictions)
    print("KNN: " + str(accuracyknn))
    print(cmknn)



    ####DNN
    #convert list to numpy arrays
    train_static = np.array(train_static)
    test_static = np.array(test_static)
    train_static_labels = np.array(train_static_labels)
    test_static_labels = np.array(test_static_labels)

    train_dynamic = np.array(train_dynamic)
    test_dynamic = np.array(test_dynamic)
    train_dynamic_labels = np.array(train_dynamic_labels)
    test_dynamic_labels = np.array(test_dynamic_labels)


    #normalise datasets
    for i in range(len(train_static)):
        train_static[i] = train_static[i]/train_static[i].max()

    for i in range(len(test_static)):
        test_static[i] = test_static[i]/test_static[i].max()

    for i in range(len(train_dynamic)):
        train_dynamic[i] = train_dynamic[i]/train_dynamic[i].max()

    for i in range(len(test_dynamic)):
        test_dynamic[i] = test_dynamic[i]/test_dynamic[i].max()

    #print(test_dynamic)
    # building models
    staticModel = keras.Sequential([
        keras.layers.Flatten(),
        keras.layers.Dense(20, activation="relu"),
        keras.layers.Dense(5, activation="softmax")
    ])

    dynamicModel = keras.Sequential([
        keras.layers.Flatten(),
        #keras.layers.Reshape((3,2), input_shape=(150,25,6)),
        keras.layers.Dense(100, activation="relu"),
        keras.layers.Dense(50, activation="relu"),
        keras.layers.Dense(20, activation="relu"),
        keras.layers.Dense(10, activation="relu"),
        keras.layers.Dense(5, activation="softmax")
    ])

    staticModel.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    staticModel.fit(train_static, train_static_labels, epochs=4)
    static_test_loss, static_test_acc = staticModel.evaluate(test_static, test_static_labels)
    print("Static Tested Acc:", static_test_acc)

    dynamicModel.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    dynamicModel.fit(train_dynamic, train_dynamic_labels, epochs=14)
    dynamic_test_loss, dynamic_test_acc = dynamicModel.evaluate(test_dynamic, test_dynamic_labels)
    print("Dynamic Tested Acc:", dynamic_test_acc)

    model_json = dynamicModel.to_json()
    with open("Model.json","w") as json_file:
        json_file.write(model_json)
    dynamicModel.save_weights("Model.h5")




# To use the models
def classifyDataDNNStatic(testData):
    global staticModel
    pred = staticModel.predict(np.array(testData))
    return class_names[np.argmax(pred)]


def classifyDataDNNDynamic(testData):
    #global dynamicModel
    json_file = open('Model2TwoSensorsLargeClap.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("Model2TwoSensorsLargeClap.h5")
    templist = extract_all_feature(testData)
    pred = loaded_model.predict(np.array(templist))
    #pred = dynamicModel.predict(np.array(templist))
    return class_names[np.argmax(pred)]

def classifyDataNB(testData):
    global gnb
    global class_names
    templist = extract_all_feature(testData)
    #print(testData)
    return class_names[gnb.predict(templist)[0]]


def classifyDataDTC(testData):
    global dtree_model
    global class_names
    templist = extract_all_feature(testData)
    return class_names[dtree_model.predict(templist)[0]]


def classifyDataSVM(testData):
    global svm_model_linear
    global class_names
    templist = extract_all_feature(testData)
    return class_names[svm_model_linear.predict(templist)[0]]


def classifyDataKNN(testData):
    global knn
    global class_names
    testData = extract_all_feature(testData)
    return class_names[knn.predict(testData)[0]]


#make_models()
#testlist = []
#testing = [1,2,3,4,5,6,7,8,9]
#testlist.append(testing)
#print(classifyDataNB(testlist))
#print(classifyDataDTC(testlist))
#print(classifyDataSVM(testlist))
#print(classifyDataKNN(testlist))
