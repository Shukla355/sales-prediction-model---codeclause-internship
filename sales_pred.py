# -*- coding: utf-8 -*-
"""sales-pred.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JKkEIArdNRfRLMw86atmHl_tDeW8btjf
"""

import torch
from torch import nn
import matplotlib.pyplot as plt
torch.__version__

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print('A {} device was detected.' .format(device))
if device=='cuda' :
  print (torch.cuda.get_device_name(device=device))

import pandas as pd
url = 'https://raw.githubusercontent.com/LeakyAI/FirstNeuralNet/main/lemons.csv'
df = pd.read_csv(url)
df.head(10)

df.shape

priceMean = df['Price'].mean()
priceStd = df['Price'].std()
df['Price'] = df['Price']-priceMean/priceStd

numSoldMean = df['NumberSold'].mean()
numSoldStd = df['NumberSold'].std()
df['NumberSold'] = (df['NumberSold']-numSoldMean)/numSoldStd

df.head()

inputs = ['Weekend','Sunny','Warm','BigSign','Price']
x = torch.tensor(df[inputs].values, dtype=torch.float, device=device)

outputs = ['NumberSold']
y = torch.tensor(df[inputs].values, dtype=torch.float, device=device)

x[0:5]

y[0:5]

from torch.nn.modules.activation import ReLU
model = nn.Sequential(

                      nn.Linear(5,100),
                      nn.ReLU(),
                      nn.Linear(100,1)
)
model.to(device)

import torch.optim as optim
criterion = torch.nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

for epoch in range(5):
    totalLoss = 0
    for i in range(len(x)):
        ypred = model(x[i])

        loss = criterion(ypred, y[i])

        totalLoss+=loss.item()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print ("Total Loss: ", totalLoss)

@torch.no_grad()
def graphPredictions(model, x, y , minValue, maxValue):
    model.eval()

    predictions=[]
    actual=[]

    x.to(device)
    y.to(device)
    model.to(device)

    for i in range(len(x)):
        pred = model(x[i])

        pred = pred*numSoldStd+numSoldMean
        act = y[i]*numSoldStd+numSoldMean

        predictions.append(pred.tolist())
        actual.append(act.item())

    plt.scatter(actual, predictions)
    plt.xlabel('Actual Lemonades Sold')
    plt.ylabel('Predicted Lemonades Sold')
    plt.plot([minValue,maxValue], [minValue,maxValue])
    plt.xlim(minValue, maxValue)
    plt.ylim(minValue, maxValue)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()5

graphPredictions(0, 800)

def datasetGenerator(weekend, sunny, warm, bigsign, price):
    numlemonssold = 0
    if weekend:
        numlemonssold = (sunny*5  + int(500 / price))
        if bigsign:
            numlemonssold = 1.3 * numlemonssold
        if warm:
            numlemonssold = 2 * numlemonssold
        if sunny:
            numlemonssold = 1.25 * numlemonssold
    numlemonssold = int(numlemonssold)

    return numlemonssold

weekend = 1
sunny = 0
warm = 0
bigsign = 1
price = 5
actual = datasetGenerator(weekend, sunny, warm, bigsign, price)
model.to('cpu')
price = (price - priceMean) / priceStd
x1 = torch.tensor([weekend, sunny, warm, bigsign, price],dtype=float)
y1 = model(x1.float())
y1 = y1*numSoldStd+numSoldMean
print ("Neural Network Predicts: ", y1.item())
print ("Actual Result: ", actual)

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Step 1: Data Collection (Assuming you have a dataset of eye images)
# TODO: Load your dataset and labels here

# Step 2: Data Preprocessing
# TODO: Preprocess the images (resize, normalization, etc.)

# Step 3: Model Architecture
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, channels)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

# Step 4: Model Compilation
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Step 5: Data Augmentation and Model Training
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

batch_size = 32
epochs = 10

model.fit(datagen.flow(train_images, train_labels, batch_size=batch_size),
          steps_per_epoch=len(train_images) // batch_size,
          epochs=epochs,
          validation_data=(val_images, val_labels))

# Step 6: Model Evaluation
loss, accuracy = model.evaluate(test_images, test_labels)
print("Test Loss:", loss)
print("Test Accuracy:", accuracy)

# Step 7: Model Deployment and Testing
# You can use the trained model to make predictions on new eye images.
# Note: Make sure to have a separate test set for real-world testing.

# TODO: Code to make predictions using the trained model