import serial
import pygame

FORWARD_CHAR = 'a'
BACKWARD_CHAR = 'H'
LEFT_CHAR = '}'
RIGHT_CHAR = ':'
NEUTRAL_CHAR = 'Z'


class Driver(object):

	def __init__(self,serial_port,baud_rate):
		self.ser = serial.Serial(serial_port,baud_rate)
		pygame.init()
		pygame.display.set_mode((250,250))
		self.command = [NEUTRAL_CHAR,NEUTRAL_CHAR,'\n']

	def send(self,command):
		command = [ ord(i) for i in command ]
		b = bytearray(command)
		self.ser.write(b)	

	def drive(self):
		print("Driving started.")
		while True:
			# prepare the command to send to the arduino
			changed = False
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						self.command[1] = FORWARD_CHAR
						changed = True
					if event.key == pygame.K_DOWN:
						self.command[1] = BACKWARD_CHAR
						changed = True
					if event.key == pygame.K_LEFT:
						self.command[0] = LEFT_CHAR
						changed = True
					if event.key == pygame.K_RIGHT:
						self.command[0] = RIGHT_CHAR
						changed = True
					if event.key == pygame.K_ESCAPE:
						return
				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
						self.command[1] = NEUTRAL_CHAR
						changed = True
					if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
						self.command[0] = NEUTRAL_CHAR
						changed = True
			if changed:
				self.send(self.command)


	def __del__(self):
		self.command = ['Z', 'Z', '\n']
		self.send(self.command)
		self.ser.close()

if __name__ == '__main__':
	serial_port = '/dev/ttyTHS2'
	baud_rate = 115200

	driver = Driver(serial_port,baud_rate)
	driver.drive()
	del driver

