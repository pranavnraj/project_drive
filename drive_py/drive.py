import serial
import pygame
import array
import time

class CollectTrainingData(object):

	def __init__(self,serial_port,baud_rate):
		self.ser = serial.Serial(serial_port,baud_rate)
		pygame.init()
		pygame.display.set_mode((250,250))
		self.command = ['Z','Z','\n']

	def send(self,command):
		command = [ ord(i) for i in command ]
		b = bytearray(command)
		print("Sending: " + str(b))
		self.ser.write(b)
	
	def drive(self):
		while True:
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
			time.sleep(.05)
	def __del__(self):
		self.ser.close()
		
if __name__ == '__main__':
	serial_port = '/dev/ttyTHS2'
	baud_rate = 115200	

	driver = CollectTrainingData(serial_port,baud_rate)
	driver.drive()
	del driver
	
