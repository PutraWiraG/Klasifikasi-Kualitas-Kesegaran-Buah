# -*- coding: utf-8 -*-
"""Klasifikasi-Buah.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12-mpJbbwYK7GZU0cox2vMyEBwFqrQF3X

<h1>Persiapan Dataset</h1>
"""

!pip install -q kaggle

from google.colab import files
files.upload()

!mkdir ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d sriramr/fruits-fresh-and-rotten-for-classification

"""<h1>Ekstrak File Dataset</h1>"""

import zipfile,os

local_zip = '/content/fruits-fresh-and-rotten-for-classification.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/tmp')
zip_ref.close()

base_dir = '/tmp/dataset/dataset'

test_dir = '/tmp/dataset/dataset/test'
train_dir = '/tmp/dataset/dataset/train'

"""<h1>Melihat File Dataset</h1>"""

total_test = 0

for i in os.listdir(test_dir):
  total_test += len(os.listdir(test_dir+'/'+i))
  print('Total File ', i, ' = ', len(os.listdir(test_dir+'/'+i)))

print(total_test)

total_train = 0

for i in os.listdir(train_dir):
  total_train += len(os.listdir(train_dir+'/'+i))
  print('Total File ', i, ' = ', len(os.listdir(train_dir+'/'+i)))

print(total_train)

total = 0
total = total_test + total_train

print('Total Dataset = ', total)

os.listdir(test_dir)

os.listdir(train_dir)

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random

def view_random_image(target_dir, target_class):
  target_folder = target_dir + target_class
  random_image = random.sample(os.listdir(target_folder), 1)

  img = mpimg.imread(target_folder + '/' + random_image[0])
  plt.imshow(img)
  plt.title(target_class)
  plt.axis('off')

  print(f"Ukuran Gambar :{img.shape}")
  return img

img = view_random_image(train_dir, '/rottenapples')

img

def plot_loss_curves(history):
 loss = history.history['loss'] 
 val_loss = history.history['val_loss']

 accuracy = history.history['accuracy'] 
 val_accuracy = history.history['val_accuracy']

 epochs = range(len(history.history['loss']))

 plt.plot(epochs, loss, label='training_loss') 
 plt.plot(epochs, val_loss, label='val_loss')
 plt.title("Loss")
 plt.xlabel("epochs")
 plt.legend()

 plt.figure()

 plt.plot(epochs, accuracy, label='training_accuracy') 
 plt.plot(epochs, val_accuracy, label='val_accuracy')
 plt.title("accuracy")
 plt.xlabel("epochs")
 plt.legend()

"""<h1>Pembuatan Model</h1>"""

import tensorflow as tf

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPool2D, Activation
from tensorflow.keras import Sequential
from tensorflow.keras.callbacks import ModelCheckpoint

train_datagen = ImageDataGenerator(
    rescale=1./255
)
val_datagen = ImageDataGenerator(
    rescale=1./255
)

train_data_rf = train_datagen.flow_from_directory(
    train_dir,
    batch_size = 15,
    target_size = (200,200),
    class_mode = "categorical"
)
val_data_rf = val_datagen.flow_from_directory(
    test_dir,
    batch_size = 15,
    target_size = (200,200),
    class_mode = "categorical"
)

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(200, 200, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(6, activation='softmax')
])

model.summary()

model.compile(
    loss='categorical_crossentropy',
    optimizer='adamax',
    metrics=['accuracy']
)

hist = model.fit(
    train_data_rf,
    epochs=15,
    validation_data=val_data_rf
)

plot_loss_curves(hist)

# Commented out IPython magic to ensure Python compatibility.
import numpy as np

# predict image
# %matplotlib inline
uploaded = files.upload()

for fn in uploaded.keys():
  path = fn
  img = tf.keras.utils.load_img(path, target_size=(200, 200))
  imgplot = plt.imshow(img)
  x = tf.keras.utils.img_to_array(img)
  x = np.expand_dims(x, axis=0)

  images = np.vstack([x])
  arr = model.predict(images, batch_size=10)
  if arr[0][0]==1:
    labels='Fresh Apples'
  elif arr[0][1]==1:
    labels='Fresh Banana'
  elif arr[0][2]==1:
    labels='Fresh Oranges'
  elif arr[0][3]==1:
    labels='Rotten Apples'
  elif arr[0][4]==1:
    labels='Rotten Banana'
  elif arr[0][5]==1:
    labels='Rotten Oranges'
print('{} is a {}'.format(fn,labels))

model.save("model.h5")