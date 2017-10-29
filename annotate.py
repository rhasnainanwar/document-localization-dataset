'''Fixes problems with annotation to label corners in correct order'''
import os
import csv

'''IMPORTANT SETTINGS'''
dir = "./iphone24/" # folder name
width = 3264 # image size
height = 2448
if not os.path.isdir(dir+"annotations/"):
	os.mkdir(dir+"annotations/")
annotations = dir+"annotations/"

for gt in os.listdir(dir):
	if gt.endswith("csv"):
		current_file = dir+gt
		# change JPG to jpg or vice versa according to the image extension
		with open(annotations+gt[:-3]+"JPG.csv", "a") as csvfile, open(current_file, "r") as coming:
			print current_file
			for _ in range(4):
				#read
				data = coming.readline().split()
				x, y = float(data[0].strip()), float(data[1].strip())
				print x, y
				#write
				spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
				spamwriter.writerow([str(x/640*width), str(y/640*height)])
