'''
Better Image Generator:
Pastes the document onto a background with texture and other color tweaks.
In progress...
'''
import numpy as np
import os
import csv
import cv2

from label import create
from utils import four_point_transform, fix_points, adjust_light, saltPepper, rotate
from random import randint, uniform
#required size
width = 3264
height = 2448

#places a croped image on new background
def merge(background, img, M):
	#random rotate
	angle = randint(0, 180)
	img = rotate(img, angle)

	height_f, width_f = img.shape[:2]
	#random resize
	factor = uniform(0.40, 0.80)
	width_f = int(width_f*factor)
	height_f = int(height_f*factor)

	#change sizes
	background = cv2.resize(background, dsize=(width, height), interpolation=cv2.INTER_CUBIC)
	img = cv2.resize(img, dsize=(width_f, height_f), interpolation=cv2.INTER_CUBIC)
	
	#random location
	x = randint(50, height - height_f - 50)
	y = randint(50, width - width_f - 50)
	
	#new gt
	points = np.array([[x, y], [x+width_f, y], [x+width_f, y+height_f], [x, y+height_f]], dtype=np.float32)
	
	'''#adding shadow
	mask = np.ones((height_f+10, width_f+10, 3), dtype=np.uint8)*200
	#left
#	mask[:,:5,:] = np.mean( background[y:y+height_f,:5,:] + img[:,:5,:])
	mask[:,:6,:] = np.mean( background[y:y+height_f,:6,:])
	#right
#	mask[:,-4:,:] = np.mean( background[y:y+height_f, x+width_f:x+width_f+4, :] + img[:,-4:,:])
	mask[:,-5:,:] = np.mean( background[y:y+height_f, x+width_f:x+width_f+5, :])
	#top
#	mask[:5,:,:] = np.mean( background[:5,x:x+width_f,:] + img[:5,:,:])
	mask[:6,:,:] = np.mean( background[:6,x:x+width_f,:])
	#bottom
#	mask[-4:,:,:] = np.mean( background[y+height_f:y+height_f+4, x:x+width_f, :] + img[-4:,:,:])
	mask[-5:,:,:] = np.mean( background[y+height_f:y+height_f+5, x:x+width_f, :])
	
	mask = saltPepper(mask)
	mask = cv2.medianBlur(mask, 11)
	#mask = cv2.GaussianBlur(mask, (9,9), 0)
	mask[5:5+height_f, 5:5+width_f] = img'''
	
	for xi in range(height_f):
		for yi in range(width_f):
			px = img[xi, yi]
			if px.all() > 0:
				background[xi+x, yi+y] = px
	#background = adjust_light(background)
	
	pts = np.empty((4,2), dtype=np.float32)
	for i in range(4):
			pts[i] = points[i] + randint(0, 150)
			
	M = cv2.getPerspectiveTransform(pts, points)
	background = cv2.warpPerspective(background, M, dsize=(background.shape[1] + 200, background.shape[0] + 200))
	
	return background, points
	
if __name__ == '__main__':
	#directories
	dir = "./test/"
	back_source = "/home/hasnain/datageneration/backgrounds/wooden/"
	to = dir+"generated/"
	if not os.path.isdir(to):
		os.mkdir(to)

	for back in os.listdir(back_source): #each background in source
		print "Background: "+back_source+back
		new = to+back[:-4]+"/"
		if not os.path.isdir(new):
			os.mkdir(new)
		for image in os.listdir(dir): #each image in dir
			if image.endswith("JPG"):
				print dir+image
				coordinates = np.zeros((4,2), dtype="float32")
				if os.path.isfile(new+image):
					continue
				if not os.path.isfile(dir+image+".csv"): #if no gt, make one
					create(dir+image)
				with open(dir+image+".csv", 'r') as csvfile:
					for i in range(4):
						line = csvfile.readline().split(" ")
						coordinates[i][0] = float(line[0].strip())
						coordinates[i][1] = float(line[1].strip())
						
				background = cv2.imread(back_source+back)
				img = cv2.imread(dir+image, cv2.IMREAD_UNCHANGED) #orientation correction
				#perspective correction in document
				warped, M = four_point_transform(img, coordinates)
				#array to image
				merged, points = merge(background, warped, M)
				cv2.imwrite(new+image, merged)
				
				#binary
				im = cv2.cvtColor(background, cv2.COLOR_RGB2GRAY)
				#(thresh, im) = cv2.threshold(im_gray, 10, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
				#max
				kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11,11), (-1,-1))

				maxed = cv2.dilate(im, kernel)
				comp = cv2.compare(im, maxed, cmpop=cv2.CMP_EQ)
				im = cv2.multiply(im, comp)
				
				cv2.imwrite(new+"max"+image, im)
				'''#order points
				points = fix_points(points)
				#new annotations
				for i in range(4):
					with open(new+image+".csv", 'a') as csvfile:
					    spamwriter = csv.writer(csvfile, delimiter=' ',
								    quotechar='|', quoting=csv.QUOTE_MINIMAL)
					    spamwriter.writerow([points[i][0], points[i][1]])'''
		print
