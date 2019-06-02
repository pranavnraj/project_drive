import serial
import pygame
import time
import pyrealsense2 as rs
import cv2
import numpy as np
from PIL import Image

FORWARD_CHAR = 'a'
LEFT_CHAR = 'z'
RIGHT_CHAR = '='
NEUTRAL_CHAR = 'Z'

class CollectTrainingData(object):

	def __init__(self,serial_port,baud_rate):
		self.ser = serial.Serial(serial_port,baud_rate)
		

	def __enter__(self):
		pygame.init()
		pygame.display.set_mode((250,250))
		self.command = [NEUTRAL_CHAR,FORWARD_CHAR,'\n']
		self.pipeline = rs.pipeline()
		self.config = rs.config()
		self.config.enable_stream(rs.stream.color,640,480,rs.format.bgr8,15)
		self.pipeline.start(self.config)
		return self

	def send(self,command):
		command = [ ord(i) for i in command ]
		b = bytearray(command)
		#print("Sending: " + str(b))
		self.ser.write(b)	

	def drive(self):
		print("Logging started.")
		last_time = int(time.time())
		index_at_time = 0
		while True:
			# get the image from the camera
			frames = self.pipeline.wait_for_frames()
			color_frame = frames.get_color_frame()
			color_image = np.asanyarray(color_frame.get_data())

			# prepare the command to send to the arduino
			changed = False
			cmd_id = 0
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						self.command[0] = LEFT_CHAR
						changed = True
					if event.key == pygame.K_RIGHT:
						self.command[0] = RIGHT_CHAR
						changed = True
					if event.key == pygame.K_ESCAPE:
						return
				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
						self.command[0] = NEUTRAL_CHAR
						changed = True
			if changed:
				self.send(self.command)

			# construct the command id
			if (self.command[0] == LEFT_CHAR): cmd_id = 1
			elif (self.command[0] == RIGHT_CHAR): cmd_id = 2
			else: cmd_id = 0

			# add 1 to counter for every frame in the same second
			if (int(time.time()) == last_time): 
				index_at_time += 1
			else: 
			 	index_at_time = 0
			 	last_time = int(time.time())

			# save the image in the data directory
			name_str = "%d_%d_%d.png" % (time.time(), index_at_time, cmd_id)
			
			# convert to grayscale and shrink for better storage & faster processing
			processed_img = cv2.cvtColor(color_image,cv2.COLOR_BGR2GRAY)
			processed_img = cv2.resize(processed_img, (28,28))

			cv2.imwrite("processed_data/"+ name_str, processed_img)

	def __exit__(self, type, value, traceback):
		# stop the car on program end
		self.command = [NEUTRAL_CHAR, NEUTRAL_CHAR, '\n']
		self.send(self.command)
		self.ser.close()
		self.pipeline.stop()

if __name__ == '__main__':
	serial_port = '/dev/ttyTHS2'
	baud_rate = 115200

	input("Press enter to start.")
	with CollectTrainingData(serial_port,baud_rate) as driver:
		driver.drive()

