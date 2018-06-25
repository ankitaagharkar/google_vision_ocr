import numpy as np
import cv2
import sys
from deskew import Deskew
from PIL import Image

class SkewRotation:

	def __init__(self,input_path):
		self.path = input_path

	def process_image(self):

		#convert to grayscale and find canny edges
		gray = cv2.imread(self.path)
		edges = cv2.Canny(gray,100,150,apertureSize = 3)

		#get Hough Lines Probabilistic
		minLineLength=100
		lines = cv2.HoughLinesP(image=edges,rho=1,theta=np.pi/180, threshold=120,lines=np.array([]), minLineLength=minLineLength,maxLineGap=100)
		if lines == []:
			return
		a, _, _ = lines.shape

		x_diff = 0
		y_diff = 0

		for i in range(a):
			x_diff += abs(lines[i][0][0]-lines[i][0][2])
			y_diff += abs(lines[i][0][1]-lines[i][0][3])
		x_diff = x_diff/len(lines)
		y_diff = y_diff/len(lines)
		print('x_diff: ',x_diff,'y_diff: ',y_diff)
		if x_diff > y_diff:
			ratio = x_diff/y_diff
			print('Image is Horizontal, ratio is:',x_diff/y_diff)
		else:
			ratio = y_diff/x_diff
			print('Image is Vertical, ratio is:',y_diff/x_diff)
			return
			#self.rotate_image()

		if ratio < 7.0:
			print('we need to deskew this image')
			deskew_obj = Deskew(self.path)
			deskew_obj.deskew()

	def rotate_image(self):
		img = Image.open(self.path)
		img = img.transpose(Image.ROTATE_90)
		img.save(self.path)

if __name__ == '__main__':
	x = SkewRotation(sys.argv[1])
	x.process_image()	