import tensorflow as tf
from tensorflow import keras

import cv2
import numpy as np
import os


# Load images and labels
train_images = np.array()
labels = np.array()
current_path = os.getcwd()
img_folder_path = os.path.join(current_path, "processed_data")


# Create the neural network
model = keras.Sequential([
	keras.layers.Flatten(input_shape=(28,28)),
	keras.layers.Dense(128, activation=tf.nn.relu),
	keras.layers.Dense(9, activation=tf.nn.softmax)
])

# TODO: Determine what settings work best for our data set
model.compile(optimizer='adam',
		loss='sparse_categorical_crossentropy',
		metrics=['accuracy'])

