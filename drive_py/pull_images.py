import pygame
import time
import pyrealsense2 as rs
import cv2
import numpy as np
import serial


class Predictor(object)


        def __init__(self, serial_port, baud_rate):
		self.ser = serial.Serial(serial_port,baud_rate)
		self.pipeline = rs.pipeline()
		self.config = rs.config()
		self.config.enable_stream(rs.stream,.color,640,480,rs.format.bgr8,6)
		self.pipeline.start(self.config)
		self.command = ['Z','Z','\n']

	def get_images(self):
		frames = self.pipeline.wait_for_frames()
		color_frame = frames.get_color_frame()
		color_image = np.asanyarray(color_frame.get_data())
		img = Image.fromarray(color_image, 'RGB')
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		img = cv2.resize(img,(28,28)

		return img

	def make_prediction(self, img, model)
	
		single_img_arr = np.array([img])		
		predictions = model.predict(single_img_arr)

		label = np.argmax(predictions[0])			
		return label	

if __name__ == '__main__':
        serial_port = '/dev/ttyTHS2'
        baud_rate = 115200

	predictor = Predictor(serial_port, baud_rate)
	current_model = keras.models.load_model('pathtracker.h5')

	while True:
		img = predictor.get_image()
		label = predictor.make_prediction(img, current_model)

		# prepare the command to send to the arduino
                changed = False
                cmd_id = 0
	
		# TODO Kyle, you're gonna have to complete this part because I don't remember exactly how the labels marked to direction lol
		# TODO Also, make sure the send to serial part is correct cuz you know that stuff	
		switch(label) {
			case 0:
				changed = True
				break;
			case 1:
				changed = True
				break;
			case 2:
				changed = True
				break;
			case 3:
				changed = True
				break;
			case 4:
				changed = True
				break;
			case 5:
				changed = True
				break;
			case 6:
				changed = True
				break;
			case 7:
				changed = True
				break;
			case 8:	
				changed = True
				break;		
		}

		if changed:
			self.send(self.command)


