'''Converts .tiff or .tif images to JPEG'''
import os
from PIL import Image

current_path = os.getcwd()
to_path = os.path.join(current_path, "brodatzjpeg") #relative path

if (not os.path.isdir(to_path)):
    os.mkdir(to_path)

for root, dirs, files in os.walk(current_path, topdown=False):
    for name in files:
        print(os.path.join(root, name))

        if os.path.splitext(os.path.join(root, name))[1].lower() == ".tiff":
        #if os.path.splitext(os.path.join(root, name))[1].lower() == ".tif":
		outputfile = os.path.join(to_path, name)[:-4] + "jpg"
		#outputfile = os.path.join(to_path, name)[:-3] + "jpg", if .tif
            	if os.path.isfile(outputfile):
                	print "A jpeg file already exists for %s" % name
            	# If a jpeg with the name does *NOT* exist, covert one from the tif.
	    	else:
	    	    try:
	    	        im = Image.open(os.path.join(root, name))
	    	        print "Converting jpeg for %s" % name
	    	        im.thumbnail(im.size)
	    	        im.save(outputfile, "JPEG", quality=100)
	    	    except Exception, e:
	    	        print e
