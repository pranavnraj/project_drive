import serial
import pygame
import time
import pyrealsense2 as rs
import cv2
import numpy as np

class CollectTrainingData(object):

	def __init__(self,serial_port,baud_rate):
		self.ser = serial.Serial(serial_port,baud_rate)
		pygame.init()
		pygame.display.set_mode((250,250))
		self.command = ['Z','Z','\n']
		self.pipeline = rs.pipeline() 
		self.config = rs.config() 
		self.config.enable_stream(rs.stream.color,640,480,rs.format.bgr8,30)
		self.pipeline.start(self.config)

	def send(self,command):
		command = [ ord(i) for i in command ]
		b = bytearray(command)
		print("Sending: " + str(b))
		self.ser.write(b)
	
	def drive(self):
		print("Logging started.")
		while True:
			# get the image from the camera
			frames = self.pipeline.wait_for_frames()
			color_frame = frames.get_color_frame()
			color_image = np.asanyarray(color_frame.get_data())	

			# prepare the command to send to the arduino
			changed = False
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP: 
						self.command[1] = 'e'
						changed = True
					if event.key == pygame.K_DOWN:
						self.command[1] = 'P'
						changed = True
					if event.key == pygame.K_LEFT:
						self.command[0] = 'z'
						changed = True
					if event.key == pygame.K_RIGHT:
						self.command[0] = 'A'
						changed = True
					if event.key == pygame.K_ESCAPE:
						return 
				elif event.type == pygame.KEYUP: 
					if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
						self.command[1] = 'Z'
						changed = True
					if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
						self.command[0] = 'Z'
						changed = True
			if changed: self.send(self.command)

			# save the image
			name_str = "%d_%c_%c.png" % (time.time(), self.command[0], self.command[1])
			# TODO: save image, determine directory to save in
			cv2.imwrite("data/" + name_str, color_image)

	def __del__(self):
		self.ser.close()
		self.pipeline.stop()
		
if __name__ == '__main__':
	serial_port = '/dev/ttyTHS2'
	baud_rate = 115200	

	driver = CollectTrainingData(serial_port,baud_rate)
	driver.drive()
	del driver
	
