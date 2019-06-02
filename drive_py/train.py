import tensorflow as tf 
from tensorflow import keras

import logging
import cv2
import numpy as np
import os

# Load images and labels
def load_data(folder_name):
	images = []
	labels = []
	current_path = os.getcwd()
	img_folder_path = os.path.join(current_path, folder_name)
	for img_name in os.listdir(img_folder_path):
		label = int(img_name[:-4].split('_')[-1])
		img_path = os.path.join(img_folder_path, img_name)
		img = cv2.imread(img_path, cv2.CV_8UC1)
		images.append(img)
		labels.append(label)
	images = np.asarray(images)
	images = images / 255.0
	labels = np.asarray(labels)
	return images,labels


def train():
	# Create the neural network
	model = keras.Sequential([
		keras.layers.Flatten(input_shape=(28,28)),
		keras.layers.Dense(128, activation=tf.nn.relu),
		keras.layers.Dense(3, activation=tf.nn.softmax)
	])

	model.compile(optimizer='adam',
		loss='sparse_categorical_crossentropy',
		metrics=['accuracy'])

	train_images, train_labels = load_data("processed_data")

	
	test_images, test_labels = (train_images[len(train_images)//5:], train_labels[len(train_labels//5):])
#	train_images, train_labels = (train_images[:len(train_images)//5], train_labels[:len(train_labels//5)])

	model.fit(train_images, train_labels, epochs=100)

	test_loss, test_acc = model.evaluate(test_images, test_labels);
	
	print("Test loss: {}%, Test accuracy: {}%".format(test_loss*100, test_acc*100)

	if( test_acc >= 0.85):
		logging.info("Reached accuracy threshold")
	else:
		logging.warning("Below accuracy threshold!")

	model.save('pathtracker.h5')

# limit memory allocated to jetson
config = tf.ConfigProto()
config.gpu_options.allow_growth = True

session = tf.Session(config=config)

# Set up logger
logging.basicConfig(filename='train.log', level=logging.DEBUG);

train()




