'''
Ground Truth Generator:
Label corner points by double-clicking each corner, in correct order.
'''
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

def onclick(event):
	global current_file
	if event.dblclick:
		print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
			(event.button, event.x, event.y, event.xdata, event.ydata))
		import csv
		with open(current_file+".csv", 'a') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
			spamwriter.writerow([str(event.xdata), str(event.ydata)])
            
def create(image):
	global current_file
	fig = plt.figure()
	cid = fig.canvas.mpl_connect('button_press_event', onclick)
	current_file = image
	img=mpimg.imread(image)
	plt.imshow(img)
	plt.show()
