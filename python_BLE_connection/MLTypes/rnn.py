import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
import csv
from sklearn.model_selection import train_test_split
import numpy as np

#Example database
#mnist = tf.keras.datasets.mnist  # mnist is a dataset of 28x28 images of handwritten digits and their labels
#(x_train, y_train),(x_test, y_test) = mnist.load_data()  # unpacks images to x_train/x_test and labels to y_train/y_test
#x_train = x_train/255.0
#x_test = x_test/255.0

SAMPLE_RATE = 25   #number of samples for one dynamic classification
NUM_VALUES = 6    #number of features

matrixSize = int(5000/SAMPLE_RATE)
class_names = ['Down', 'Middle', 'Up', 'Clap', 'Wave']
# For reading data in
y = []
X = []
count = 0
ystat = []
Xstat = []
with open('allData.csv', 'r') as cvsFile:
    reader = csv.reader(cvsFile)
    for row in reader:
        temp = []
        for i in range(0,NUM_VALUES):
            temp.append(float(row[i]))

        if count < 3000:
            Xstat.append(temp)
            count = count + 1
        X.append(temp)
    cvsFile.close()
count = 0
with open('allLabels.csv', 'r') as cvsFile:
    reader = csv.reader(cvsFile)
    for row in reader:
        if count < 3000:
            ystat.append(int(row[0]))
            count = count + 1
        y.append(int(row[0]))
    cvsFile.close()

# for dynamic classification
Xtemp = []
ytemp = []

for i in range(0,matrixSize):
    temp2 = []
    for j in range(0,SAMPLE_RATE):
        #print(str(i) + " and " + str(j))
        temp2.append(X[i*SAMPLE_RATE+j])
    Xtemp.append(temp2)
    ytemp.append(y[i*SAMPLE_RATE+j])


X_train, X_test, y_train, y_test = train_test_split(Xtemp, ytemp, random_state = 0)
X_train = np.array(X_train)
X_test = np.array(X_test)
y_train = np.array(y_train)
y_test = np.array(y_test)

# normalise data

for i in range(len(X_train)):
    X_train[i] = X_train[i]/X_train[i].max()

for i in range(len(X_test)):
    X_test[i] = X_test[i]/X_test[i].max()


#print(X_train.shape)
#print(X_train[0].shape)


model = Sequential()
model.add(LSTM(64, input_shape=(X_train.shape[1:]), activation='relu', return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(64, activation='relu'))
model.add(Dropout(0.1))

model.add(Dense(32, activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(5, activation='softmax'))


opt = tf.keras.optimizers.Adam(lr=0.001, decay=1e-6)

model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer=opt,
    metrics=['accuracy'],
)

model.fit(X_train,
          y_train,
          epochs=3,
          validation_data=(X_test, y_test))

def classifyDataRNN(testData):
    global model
    global class_names
    testData = np.array(testData)
    print("entered")
    pred = model.predict(np.array(testData))
    print(class_names[np.argmax(pred)])
    return class_names[np.argmax(pred)]


#testlist = []
#testing1 = [1,2,3,4,5,6]
#testing2 = [1,2,3,4,5,6]
#testing3 = [1,2,3,4,5,6]
#testing4 = [1,2,3,4,5,6]
#testing5 = [1,2,3,4,5,6]
#esting6 = [1,2,3,4,5,6]
#testing7 = [1,2,3,4,5,6]
#testing8 = [1,2,3,4,5,6]
#testing9 = [1,2,3,4,5,6]
#testing10 = [1,2,3,4,5,6]
#testlist.append(testing1)
#testlist.append(testing2)
#testlist.append(testing3)
#testlist.append(testing4)
#testlist.append(testing5)
#testlist.append(testing6)
#testlist.append(testing7)
#testlist.append(testing8)
#testlist.append(testing9)
#testlist.append(testing10)
#testDat = []
#testDat.append(testlist)
#3classifyDataRNN(testDat)
