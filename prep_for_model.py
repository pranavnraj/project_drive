import os
import numpy as np
import cv2

filelist=os.listdir('./drive_py/color')
for fichier in filelist[:]:
	if (fichier.endswith(".png")):
		img = cv2.imread(fichier, 0);
		cv2.imwrite('./drive_py/greyscale/' + fichier, img)
