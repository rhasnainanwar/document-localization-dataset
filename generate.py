'''
Simple Image Generator:
Pastes the image onto a background with random size and location.
'''
import numpy as np
import os
from PIL import Image, ImageDraw, ImageColor
from random import randint
    	
#takes an image and its corner coordinates; returns its mask as image
def create_mask(original, coordinates):
	width, height = original.size

	#creating a mask image
	img = Image.new('L', (width, height), 0)
	ImageDraw.Draw(img).polygon(coordinates, outline=255, fill=255)
	return img

#places a croped image on new background
def merge(background, img, mask):
	#random rotate
	degree = randint(0, 180)
	img = img.rotate(degree, expand=True)
	mask = mask.rotate(degree, expand=True)

	width_b, height_b = background.size
	width_f, height_f = img.size
	
	if width_b <= width_f or height_b <= height_f:
		width_f = randint(width_b//2, width_b)
		height_f = randint(height_b//2, height_b)
		img = img.resize( (width_f, height_f) )
		mask = mask.resize((width_f, height_f))
	
	#random location
	x = randint(0, width_b - width_f )
	y = randint(0, height_b - height_f)

	#paste at random location
	background.paste(img, (x, y), mask)
	return background
	
if __name__ == '__main__':	
	#directories
	dir = "./aqsa/"
	back_source = "/home/hasnain/datageneration/dtd/images/woven/"
	to = dir+"generated/"
	if not os.path.isdir(to):
		os.mkdir(to)

	for back in os.listdir(back_source):
		print "Background: "+back_source+back
		new = to+back[:-4]+"/"
		if not os.path.isdir(new):
			os.mkdir(new)
		for image in os.listdir(dir):
			if image.endswith("JPG"):
				print dir+image
				coordinates = []
				if os.path.isfile(new+image):
					continue
				if not os.path.isfile(dir+image[:-3]+"csv"):
					label(dir+image)
				with open(dir+image[:-3]+"csv", 'r') as csvfile:
					for _ in range(4):
						line = csvfile.readline().split(" ")
						coordinates.append( int(line[0].strip()) )
						coordinates.append( int(line[1].strip()) )
				background = Image.open(back_source+back)
				img = Image.open(dir+image)
				mask = create_mask(img, coordinates)
				merged = merge(background, img, mask)
				merged.save(new+image, "JPEG")
		print
