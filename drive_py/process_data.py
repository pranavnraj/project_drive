import cv2
import numpy as np
import os

current_path = os.getcwd()
img_folder_path = os.path.join(current_path, "data")
new_img_folder_path = os.path.join(current_path, "processed_data")
for img_name in os.listdir(img_folder_path):
	img_path = os.path.join(img_folder_path, img_name)
	new_img_path = os.path.join(new_img_folder_path, img_name)
	img = cv2.imread(img_path,cv2.CV_8UC1)
	img = cv2.resize(img,(28,28))
	cv2.imwrite(new_img_path, img)
