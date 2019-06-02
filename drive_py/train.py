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
	files = os.listdir(img_folder_path)
	np.random.shuffle(files)
	for img_name in files: 
		label = int(img_name[:-4].split('_')[-1])
		img_path = os.path.join(img_folder_path, img_name)
		img = cv2.imread(img_path,0)
		img = img / 255.0
		images.append(img)
		labels.append(label)
	images = np.asarray(images)
	labels = np.asarray(labels)
	return images,labels


def train():
	# Create the neural network
	model = keras.Sequential([
		keras.layers.Flatten(input_shape=(28,28)),
		keras.layers.Dense(128, activation=tf.nn.relu),
		keras.layers.Dense(3, activation=tf.nn.softmax)
	])

	model.compile(optimizer="adam",
		loss='sparse_categorical_crossentropy',
		metrics=['accuracy'])

	train_images, train_labels = load_data("processed_data")
	
	split = int(len(train_images) * 0.8)
	
	test_images, test_labels = (train_images[split:], train_labels[split:])
	train_images, train_labels = (train_images[:split], train_labels[:split])

	model.fit(train_images, train_labels, epochs=50)

	test_loss, test_acc = model.evaluate(test_images, test_labels);
	
	print("Test loss: {}%, Test accuracy: {}%".format(test_loss*100, test_acc*100))

	if test_acc >= 0.85:
		logging.info("Reached accuracy threshold")
	else:
		logging.warning("Below accuracy threshold!")

	model.save('pathtracker.h5')

def train_cnn():
	model = keras.Sequential([
		keras.layers.Conv2D(24, kernel_size=(5,5), strides=(2,2), activation=tf.nn.relu, input_shape=(28,28,1),padding='same'),
		keras.layers.Conv2D(32, kernel_size=(5,5), strides=(2,2), activation=tf.nn.relu),
		keras.layers.Conv2D(64, kernel_size=(3,3), strides=(1,1), activation=tf.nn.relu), 
		keras.layers.Flatten(),
		keras.layers.Dense(128, activation=tf.nn.relu),
		keras.layers.Dropout(0.1),
		keras.layers.Dense(64, activation=tf.nn.relu),
		keras.layers.Dropout(0.1),
		keras.layers.Dense(3, activation=tf.nn.softmax)
	])

	model.compile(optimizer="adam",
		loss='sparse_categorical_crossentropy',
		metrics=['accuracy'])

	train_images, train_labels = load_data("processed_data")
	train_images = train_images.reshape(len(train_images),28,28,1)
	
	split = int(len(train_images) * 0.8)
	
	test_images, test_labels = (train_images[split:], train_labels[split:])
	train_images, train_labels = (train_images[:split], train_labels[:split])

	model.fit(train_images, train_labels, validation_data=(test_images,test_labels), epochs=10)

	test_loss, test_acc = model.evaluate(test_images, test_labels);
	
	print("Test loss: {}, Test accuracy: {}%".format(round(test_loss,2), round(test_acc*100,2)))

	if test_acc >= 0.85:
		logging.info("Reached accuracy threshold")
	else:
		logging.warning("Below accuracy threshold!")

	model.save('pathtracker_cnn.h5')
		

# limit memory allocated to jetson
config = tf.ConfigProto()
config.gpu_options.allow_growth = True

session = tf.Session(config=config)

# Set up logger
logging.basicConfig(filename='train.log', level=logging.DEBUG);

train_cnn()




