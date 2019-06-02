import cv2
import numpy as np
import os

current_path = os.getcwd()
img_folder_path = os.path.join(current_path, "train_data")
new_img_folder_path = os.path.join(current_path, "processed_data")
num_files = len(os.listdir(img_folder_path))
counter = 0
for img_name in os.listdir(img_folder_path):
	if img_name not in os.listdir(new_img_folder_path):
		img_path = os.path.join(img_folder_path, img_name)
		new_img_path = os.path.join(new_img_folder_path, img_name)
		img = cv2.imread(img_path,cv2.CV_8UC1)
		img = cv2.resize(img,(28,28))
		cv2.imwrite(new_img_path, img)
	counter += 1
	print("Progress: {}/{}".format(counter,num_files), end="\r")
