import datetime
import os
import time
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


imageDirectory = os.getcwd() + "/samples/20220517/"
croppedDirectory = imageDirectory + "/" + str(time.mktime(datetime.datetime.today().timetuple()))
os.mkdir(croppedDirectory)


refImg = mpimg.imread(imageDirectory + "0001.png")
ax = plt.gca()
fig = plt.gcf()
implot = ax.imshow(refImg)

left = 0
top = 0
right = 0
bottom = 0

count = 0
def onclick(event):
	global count, top, left, right, bottom # FIXME: This is bullshit... find a better solution
	if event.xdata != None and event.ydata != None:
		count += 1
		if(count == 1):
			left = event.xdata
			top = event.ydata
		elif(count == 2):
			right = event.xdata
			bottom = event.ydata
			plt.close()
		else:
			print("ERROR")

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()

for file in os.listdir(imageDirectory):
	if file.endswith(".png"):
		img = Image.open(os.path.join(imageDirectory, file))
		img_res = img.crop((left, top, right, bottom))
		img_res.save(os.path.join(croppedDirectory, os.path.splitext(file)[0] + "_cropped.png"))
