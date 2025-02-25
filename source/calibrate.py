import os
import matplotlib.image as img
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor

# ------ INSER HERE THE FILE NAMES ----------------

imageDirectory = os.getcwd() + "/samples/20220517/1652816696.0/"

calibFile = imageDirectory + "0001_cropped.png"
saveFilename = imageDirectory + "0001_cropped_plot.png"

# ----------- END ---------------------------------

# ----------- Function ----------------------------

def getSpectrumPNG(filename):
	'''From a PNG file taken with spectralworkbench
	extracts a spectrum. Each channel's spectrum
	is calculated as column mean for the whole picture'''

	image = img.imread(filename)

	imageR = []
	imageG = []
	imageB = []
	imgWidth = len(image[0])
	imgHeight = len(image)

	# Preparing arrays
	for i in range(imgWidth):
		imageR.append(image[0][i][0])
		imageG.append(image[0][i][1])
		imageB.append(image[0][i][2])

	# Columns summatory
	for i in range(imgHeight):
		for j in range(imgWidth):
			imageR[j]=imageR[j]+image[i][j][0]
			imageG[j]=imageG[j]+image[i][j][1]
			imageB[j]=imageB[j]+image[i][j][2]

	# Calculating the mean for every column
	for i in range(imgWidth):
		imageR[i]=imageR[i]/640
		imageG[i]=imageG[i]/640
		imageB[i]=imageB[i]/640

	# Merging the RGB channels by addition
	spectrum = []
	for i in range(imgWidth):
		spectrum.append((imageR[i]+imageG[i]+imageB[i])/3)

	return spectrum

# -------------- Execution ----------------------

# Initialize and load spectra
spectrum = getSpectrumPNG(calibFile)

fig, ax1 = plt.subplots(nrows=1, sharex=True)
cursor = Cursor(ax1, useblit=True, color='r', lw=0.5)
ax1.plot(spectrum)

#plt.ylim(0,1)
plt.xlabel('Pixel ID')
plt.ylabel('Light intensity')

plt.savefig(saveFilename)
plt.show()
