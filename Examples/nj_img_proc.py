# import glob
# import cv2,os
# import numpy as np
# from PIL import ImageEnhance, ImageStat
# from PIL import Image as I
# from scipy.signal import convolve2d
#
#
# def loopForBlurring(sizeOfKernel, howManyTimes, givenIMG, sigmax):
#     for x in range(howManyTimes):
#         kernel = np.ones((3, 2), np.int32)
#         gaussian_1 = cv2.GaussianBlur(givenIMG, sizeOfKernel, sigmax)
#         # unsharp_image = cv2.addWeighted(img1, 1.5, gaussian_1, -0.5, 0, img1)
#         # dst = cv2.fastNlMeansDenoising(givenIMG, None, 12, 7, 21)
#         erode = cv2.erode(gaussian_1, kernel, iterations=1)
#         # img=cv2.fastNlMeansDenoising(givenIMG, None, 9, 13)
#
#     return erode
# # def estimate_noise(I):
# #
# #   _,H,W = I.shape
# #
# #   M = [[1, -2, 1],
# #        [-2, 4, -2],
# #        [1, -2, 1]]
# #
# #   sigma = np.sum(np.sum(np.absolute(convolve2d(I, M))))
# #   sigma = sigma * np.math.sqrt(0.5*np.math.pi)/ (6*(W - 2)*(H - 2))
# #
# #   return sigma
# def variance_of_laplacian(image):
#         # compute the Laplacian of the image and then return the focus
#         # measure, which is simply the variance of the Laplacian
#         return cv2.Laplacian(image, cv2.CV_64F).var()
#
# for IMAGENAME in glob.glob(r'C:\Users\ankitaa\Documents\Valid Driver Licenses\*.jpg'):
#     pImg = cv2.imread(IMAGENAME)
#     _,filename=os.path.split(IMAGENAME)
#
#     processedImage = cv2.fastNlMeansDenoising(pImg, None, 5, 5, 5)
#     # Gaussian blur
#     cv2.imwrite(r'C:\\Users\\ankitaa\\Desktop\\Process_Image\\'+filename + "_Final4.jpg",processedImage)
# #

import cv2
from pylab import array, plot, show, axis, arange, figure, uint8

# Image data
path=r"C:\Users\ankitaa\Desktop\NJ\NJ DL 3.JPG"
image = cv2.imread(path) # load as 1-channel 8bit grayscale
# image=cv2.fastNlMeansDenoising(img,5,5,5)
# cv2.imshow('image',image)
maxIntensity = 255.0 # depends on dtype of image data
x = arange(maxIntensity)

# Parameters for manipulating image data
phi = 1
theta = 1

# Increase intensity such that
# dark pixels become much brighter,
# bright pixels become slightly bright
newImage0 = (maxIntensity/phi)*(image/(maxIntensity/theta))**0.5
newImage0 = array(newImage0,dtype=uint8)

# cv2.imshow('newImage0',newImage0)


y = (maxIntensity/phi)*(x/(maxIntensity/theta))**0.5

# Decrease intensity such that
# dark pixels become much darker,
# bright pixels become slightly dark
newImage1 = (maxIntensity/phi)*(image/(maxIntensity/theta))**2
newImage1 = array(newImage1,dtype=uint8)

# cv2.imshow('newImage1',newImage1)
cv2.imwrite('newImage0.jpg',newImage1)
z = (maxIntensity/phi)*(x/(maxIntensity/theta))**2

# Plot the figures
# figure()
# plot(x,y,'r-') # Increased brightness
# plot(x,x,'k:') # Original image
# plot(x,z, 'b-') # Decreased brightness
# #axis('off')
# axis('tight')
# show()

# Close figure window and click on other window
# Then press any keyboard key to close all windows
# closeWindow = -1
# while closeWindow<0:
#     closeWindow = cv2.waitKey(1)
# cv2.destroyAllWindows()


import numpy as np
from PIL import Image

images_list2=r'C:\Users\ankitaa\PycharmProjects\iDocufy_OCR\Examples\newImage0.jpg'
img1=cv2.imread(path)
img2=cv2.imread(images_list2)

print([img1.shape])
# img_merge = np.vstack(imgs)
img_merge = np.vstack((img1,img2))
cv2.resize(img_merge,(1240,1240))
# img_merge.save( 'test.jpg' )
cv2.imshow('frame',img_merge)
cv2.imwrite('test.jpg',img_merge)
cv2.waitKey(0)


