import tensorflow as tf
from tensorflow import keras

import cv2
import numpy as np
import os


# Load images and labels
def load_train_data():
	train_images = []
	train_labels = []
	current_path = os.getcwd()
	img_folder_path = os.path.join(current_path, "processed_data")
	for img_name in os.listdir(img_folder_path):
		label = int(img_name[:-4].split('_')[1])
		img_path = os.path.join(img_folder_path, img_name)
		img = cv2.imread(img_path, cv2.CV_8UC1)
		train_images.append(img)
		train_labels.append(label)
	train_images = np.asarray(train_images)
	train_images = train_images / 255.0
	train_labels = np.asarray(train_labels)
	return train_images,train_labels

	


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

