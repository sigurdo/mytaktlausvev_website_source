from PyPDF2 import PdfFileReader
import cv2
import numpy as np
import pdf2image
import time
from imutils.object_detection import non_max_suppression
import pytesseract
from PIL import Image
import os

# print("Hello sheet music")

def generateImagesFromPdf(pdfPath, outputDir):
	print("Generating images from ", pdfPath, "...", sep="")
	print()
	images = pdf2image.convert_from_path(pdfPath, dpi=200)
	generatedImages = []
	for i in range(len(images)):
		path = f"{outputDir}/img_{i}.jpg"
		print("Generated image from pdf:", path)
		images[i].save(path)
		generatedImages.append(path)
	print()
	return generatedImages

def textDetector(imagePath):
	args = {
		"image": imagePath,
		"width": 512,
		"height": 512,
		"east": "sheetmusicUploader/frozen_east_text_detection.pb",
		"min_confidence": 0.99
	}
	# load the input image and grab the image dimensions
	image = cv2.imread(args["image"])
	orig = image.copy()
	(H, W) = image.shape[:2]
	# set the new width and height and then determine the ratio in change
	# for both the width and height
	(newW, newH) = (args["width"], args["height"])
	rW = W / float(newW)
	rH = H / float(newH)
	# resize the image and grab the new image dimensions
	image = cv2.resize(image, (newW, newH))
	(H, W) = image.shape[:2]

	# define the two output layer names for the EAST detector model that
	# we are interested -- the first is the output probabilities and the
	# second can be used to derive the bounding box coordinates of text
	layerNames = [
		"feature_fusion/Conv_7/Sigmoid",
		"feature_fusion/concat_3"]

	# load the pre-trained EAST text detector
	print("[INFO] loading EAST text detector...")
	net = cv2.dnn.readNet(args["east"])

	# construct a blob from the image and then perform a forward pass of
	# the model to obtain the two output layer sets
	blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
		(123.68, 116.78, 103.94), swapRB=True, crop=False)
	start = time.time()
	net.setInput(blob)
	(scores, geometry) = net.forward(layerNames)
	end = time.time()
	# show timing information on text prediction
	print("[INFO] text detection took {:.6f} seconds".format(end - start))

	# grab the number of rows and columns from the scores volume, then
	# initialize our set of bounding box rectangles and corresponding
	# confidence scores
	(numRows, numCols) = scores.shape[2:4]
	rects = []
	confidences = []
	# loop over the number of rows
	for y in range(0, numRows):
		# extract the scores (probabilities), followed by the geometrical
		# data used to derive potential bounding box coordinates that
		# surround text
		scoresData = scores[0, 0, y]
		xData0 = geometry[0, 0, y]
		xData1 = geometry[0, 1, y]
		xData2 = geometry[0, 2, y]
		xData3 = geometry[0, 3, y]
		anglesData = geometry[0, 4, y]

		# loop over the number of columns
		for x in range(0, numCols):
			# if our score does not have sufficient probability, ignore it
			if scoresData[x] < args["min_confidence"]:
				continue
			# compute the offset factor as our resulting feature maps will
			# be 4x smaller than the input image
			(offsetX, offsetY) = (x * 4.0, y * 4.0)
			# extract the rotation angle for the prediction and then
			# compute the sin and cosine
			angle = anglesData[x]
			cos = np.cos(angle)
			sin = np.sin(angle)
			# use the geometry volume to derive the width and height of
			# the bounding box
			h = xData0[x] + xData2[x]
			w = xData1[x] + xData3[x]
			# compute both the starting and ending (x, y)-coordinates for
			# the text prediction bounding box
			endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
			endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
			startX = int(endX - w)
			startY = int(endY - h)
			# add the bounding box coordinates and probability score to
			# our respective lists
			rects.append((startX, startY, endX, endY))
			confidences.append(scoresData[x])

	# apply non-maxima suppression to suppress weak, overlapping bounding
	# boxes
	boxes = non_max_suppression(np.array(rects), probs=confidences)
	resizedBoxes = []
	# loop over the bounding boxes
	for (startX, startY, endX, endY) in boxes:
		# scale the bounding box coordinates based on the respective
		# ratios
		startX = int(startX * rW)
		startY = int(startY * rH)
		endX = int(endX * rW)
		endY = int(endY * rH)
		resizedBoxes.append((startX, startY, endX, endY))
		# draw the bounding box on the image
		cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)
	# show the output image
	cv2.imshow("Text Detection", orig)
	cv2.waitKey(0)
	return resizedBoxes

def textRecognizer(imagePath):
	img = cv2.imread(imagePath)
	"""
	# Prøver å øke kontrast:
	alpha = 4
	beta = -700
	for y in range(img.shape[0]):
		for x in range(img.shape[1]):
			for c in range(img.shape[2]):
				img[y, x, c] = np.clip(alpha * img[y, x, c] + beta, 0, 255)
	"""
	imgWithBoxes = img.copy()
	res = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
	filtered = {}
	for key in res:
		filtered[key] = []
	for i in range(len(res["text"])):
		if int(res["conf"][i]) > 10 and res["text"][i].strip(" ") != "":
			for key in res:
				filtered[key].append(res[key][i])
			x1 = res["left"][i]
			y1 = res["top"][i]
			x2 = x1 + res["width"][i]
			y2 = y1 + res["height"][i]
			print(x1, y1, x2, y2)
			cv2.rectangle(imgWithBoxes, (x1, y1), (x2, y2), (0, 0, 255), thickness=2) # (, res["top"]), (res["left"] + , res["top"] + res["width"]), (0, 0, 255))
	for key in filtered:
		print("{:>10}".format(key), end=": ")
		for i in range(len(filtered[key])):
			print("{:>10}".format(filtered[key][i]), end=" ")
		print()
	print(pytesseract.image_to_string(img))
	cv2.imshow("Text recognition", imgWithBoxes)
	cv2.waitKey(0)

def getPdfPaths(directory):
	pdfPaths = []
	sheetNames = []
	for (dirpath, dirnames, filenames) in os.walk(directory):
		for filename in filenames:
			name, extension = os.path.splitext(filename)
			if (extension.lower() == ".pdf"):
				pdfPaths.append(os.path.join(dirpath, filename))
				sheetNames.append(name)
	return pdfPaths, sheetNames

def clearDir(directory):
	for (dirpath, dirnames, filenames) in os.walk(directory):
		for filename in filenames:
			os.remove(os.path.join(directory, filename))

def removeDetection(i, detectionData):
	for key in detectionData.keys():
		detectionData[key].pop(i)

def cropImage(img):
	# return img
	return img[0:len(img)//4, 0:len(img[0])//3]

def processDetectionData(detectionData, img):
	imgWithBoxes = img.copy()
	nicePrint  = "+------------------------------+------------+----------+----------+\n"
	nicePrint += "| text                         | confidence | pos_left | pos_top  |\n"
	nicePrint += "+------------------------------+------------+----------+----------+\n"
	for i in range(len(detectionData["text"])):
		if int(detectionData["conf"][i]) > 10 and detectionData["text"][i].strip(" ") != "":
			x1 = detectionData["left"][i]
			y1 = detectionData["top"][i]
			x2 = x1 + detectionData["width"][i]
			y2 = y1 + detectionData["height"][i]
			cv2.rectangle(imgWithBoxes, (x1, y1), (x2, y2), (0, 0, 255), thickness=2)
			nicePrint += "| {:28} | {:>10} | {:>8} | {:>8} |\n".format(detectionData["text"][i],
				detectionData["conf"][i], detectionData["left"][i], detectionData["top"][i])
	nicePrint += "+------------------------------+------------+----------+----------+\n"
	return imgWithBoxes, nicePrint

INPUT_PDF_DIR = "sheetmusicUploader/input_pdfs"
TMP_PATH = "sheetmusicUploader/tmp"
BOUNDING_BOX_PATH = "sheetmusicUploader/images_with_bounding_boxes"

if not os.path.exists(INPUT_PDF_DIR): os.mkdir(INPUT_PDF_DIR)
if not os.path.exists(TMP_PATH): os.mkdir(TMP_PATH)
if not os.path.exists(BOUNDING_BOX_PATH): os.mkdir(BOUNDING_BOX_PATH)

clearDir(TMP_PATH)
pdfPaths, sheetNames = getPdfPaths(INPUT_PDF_DIR)

for sheetName in sheetNames:
	if not os.path.exists(os.path.join(BOUNDING_BOX_PATH, sheetName)): os.mkdir(os.path.join(BOUNDING_BOX_PATH, sheetName))

for pdfPath in pdfPaths:
	imagePaths = generateImagesFromPdf(pdfPath, TMP_PATH)
	for i in range(len(imagePaths)):
		imagePath = imagePaths[i]
		print("Analyzing ", imagePath, " from ", sheetNames[pdfPaths.index(pdfPath)], ":", sep="")
		img = cropImage(cv2.imread(imagePath))
		detectionData = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config="--user-words sheetmusicUploader/instrumentsToLookFor.txt --psm 11 --dpi 96 -l eng")
		imgWithBoxes, nicePrint = processDetectionData(detectionData, img)
		print(nicePrint)
		cv2.imwrite(os.path.join(BOUNDING_BOX_PATH, sheetNames[pdfPaths.index(pdfPath)], f"boxes_{i}.jpg"), imgWithBoxes)
