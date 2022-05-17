#-------------------------------------------------------------------------------
# Name:        Plotting absorbance curves
# Purpose:     Analysing experiments's results
# Author:      Alessandro Volpato
# Created:     25/07/2018
# Copyright:
# Licence:     CC BY-SA 4.0
#-------------------------------------------------------------------------------

import os
import matplotlib.image as img
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.widgets import Cursor

######## INSERT HERE THE FILE NAME ################
# NOTE: Check the format!! png or csv

imageDirectory = os.getcwd() + "/samples/20220517/1652816696.0/"

referenceFile = imageDirectory + "0019_cropped.png"

title = "Kalium"
plotColors = ["purple"]
patchLabels = ["Kalium"]

saveFilename = imageDirectory + "plot.png"
# Don't change them!!
###################################################

###### CALIBRATION HERE ###########################
###### INSERT HERE YOUR PIXEL CORRELATIONS ########
#pixel = [868, 949, 967]
#wavelength = [585.24, 603, 607.4]
pixel = [1411, 1781.8]
wavelength = [585.24, 640.22]
# https://commons.wikimedia.org/wiki/File:Fluorescent_lighting_spectrum_peaks_labelled.png
###################################################


#####################################################################
# This is a function. Each time we call getSpectrum_PNG
# for the filename in brackets, we will execute these operations
#
def getSpectrum_PNG(filename):
    '''From a PNG file taken with spectralworkbench
        extracts a spectrum. Each channel's spectrum
        is calculated as column mean for the whole picture'''

    # Reading the image
    print("Reading image")
    image = img.imread(filename)

    # Preparing the variables
    imageR = []
    imageG = []
    imageB = []
    imgWidth = len(image[0])
    imgHeight = len(image)

    # Preparing the RGB arrays
    for i in range(imgWidth):
        imageR.append(image[0][i][0])
        imageG.append(image[0][i][1])
        imageB.append(image[0][i][2])

    # Columns summatory
    for i in range(imgHeight):
        for j in range(imgWidth):
            imageR[j] = imageR[j] + image[i][j][0]
            imageG[j] = imageG[j] + image[i][j][1]
            imageB[j] = imageB[j] + image[i][j][2]

    # Calculating the mean for every RGB column
    for i in range(imgWidth):
        imageR[i] = imageR[i] / imgHeight
        imageG[i] = imageG[i] / imgHeight
        imageB[i] = imageB[i] / imgHeight

    # Merging the RGB channels by addition
    spectrum = []
    for i in range(imgWidth):
        spectrum.append((imageR[i] + imageG[i] + imageB[i]) / 3)

    # returning the results of the operation
    return spectrum


def getSpectrum_CSV(filename):
    '''From a CSV file containing the serie of measurements,
        splits the values and returns them as a list, the spectrum'''

    # Reading the file
    print("Reading csv file")
    inFile = open(filename, "r")
    CSVline = inFile.read()

    # Splitting the values
    spectrumSTR = CSVline.split(",")

    # Transforming the values from string to float type
    spectrum = []
    for i in range(len(spectrumSTR)):
        spectrum.append(float(spectrumSTR[i]))

    # Returning the results of the operation
    return spectrum


def normalise(spectrumIn):
    spectrumOut = []
    maxPoint = max(spectrumIn)

    for value in spectrumIn:
        spectrumOut.append(value / maxPoint)

    return spectrumOut

# Preparing the plot

# Initialize and load spectra
spectraToPlot = normalise(getSpectrum_PNG(referenceFile))

# Finding out the coefficients
params = np.polyfit(pixel, wavelength, 3)
#return p = np.poly1d(range)

# Solving the equation for every pixel
# (Assigning to every pixel a wavelength)
nmAxis = []
for i in range(len(spectraToPlot)):
    v1 = params[0] * float(i**3)
    v2 = params[1] * float(i**2)
    v3 = params[2] * float(i**1)
    v4 = params[3] * float(i**0)
    nmAxis.append(v1 + v2 + v3 + v4)

patches = []
for i in range(len(patchLabels)):
    patches.append(mpatches.Patch(color=plotColors[i], label=patchLabels[i]))

fig, ax1 = plt.subplots(nrows=1, sharex=True)
cursor = Cursor(ax1, useblit=True, color='r', lw=0.5)

ax1.plot(nmAxis, spectraToPlot, color='purple')

plt.title(title)
plt.legend(handles=patches)
plt.xlim(min(nmAxis), max(nmAxis))
plt.ylim(-0.25, 2)
plt.xlabel('Wavelegth (nm)')
plt.ylabel('Absorbance')

plt.savefig(saveFilename)
plt.show()
