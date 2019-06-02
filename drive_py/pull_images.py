import tensorflow as tf
from tensorflow import keras
import pyrealsense2 as rs

import cv2
import numpy as np
import serial
from PIL import Image

from globals import *

class Predictor(object):
	def __init__(self, serial_port, baud_rate):
		self.ser = serial.Serial(serial_port,baud_rate)
		self.cmd_id = 0
		

	def __enter__(self):
		self.pipeline = rs.pipeline()
		self.config = rs.config()
		self.config.enable_stream(rs.stream.color,640,480,rs.format.bgr8,15)
		self.pipeline.start(self.config)

		# limit memory allocated to jetson
		config = tf.ConfigProto()
		config.gpu_options.allow_growth = True

		session = tf.Session(config=config)


		self.current_model = keras.models.load_model('pathtracker.h5')
		return self
		

	def send(self):
		command = [NEUTRAL_CHAR,FORWARD_CHAR,'\n']

		if self.cmd_id == 1:
		    command[0] = LEFT_CHAR
		elif self.cmd_id == 2:
		    command[0] = RIGHT_CHAR

		b = bytearray([ ord(i) for i in command ])
		self.ser.write(b)

	def get_image(self):
		frames = self.pipeline.wait_for_frames()
		color_frame = frames.get_color_frame()
		color_image = np.asanyarray(color_frame.get_data())
		img = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
		img = cv2.resize(img,(28,28))
		return img

	def make_prediction(self, img, model):
		single_img_arr = np.array([img])
		predictions = model.predict(single_img_arr)

		label = np.argmax(predictions[0])
		return label

	def drive(self):
		while True:
			img = self.get_image()
			old_cmd = self.cmd_id
			self.cmd_id = predictor.make_prediction(img, self.current_model)
			print("Command: %s" % (self.cmd_id))

			if old_cmd != self.cmd_id:
				self.send()

	def __exit__(self, type, value, traceback):
		self.cmd_id = 0
		self.send()	
		self.ser.close()
		self.pipeline.stop()

if __name__ == '__main__':
	serial_port = '/dev/ttyTHS2'
	baud_rate = 115200

	input("Press enter to begin.")
	with Predictor(serial_port, baud_rate) as predictor:
		predictor.drive()



