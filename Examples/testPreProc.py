from PIL import Image, ImageEnhance, ImageStat
import cv2,os
import numpy as np
import sys
import glob

def variance_of_laplacian(image):
        # compute the Laplacian of the image and then return the focus
        # measure, which is simply the variance of the Laplacian
        return cv2.Laplacian(image, cv2.CV_64F).var()

# IMAGENAME = sys.argv[1]
for IMAGENAME in glob.glob(r'C:\Users\ankitaa\Desktop\idocufy\Images\Valid Licence and SSN\*.jpg'):
    img = Image.open(IMAGENAME).convert('L')
    head,tail=os.path.split(IMAGENAME)
    # img.save(IMAGENAME[:-4] + '_bnw.jpg')
    imStat = ImageStat.Stat(img)
    medi = list(map((lambda x: x/25), imStat.mean))
    # print(medi)

    if max(medi) < 3:
        brightness = ImageEnhance.Brightness(img)
        img = brightness.enhance(3 - max(medi))
	# brightImg.save(imgPath[:-4] + '_Bright'+ str(max(medi)) + '.jpg')
    sharpness = ImageEnhance.Sharpness(img)
    cvImg = np.array(img)
    blur = variance_of_laplacian(cvImg)
    print(IMAGENAME, blur)
    if blur < 700:
        sharpImg = sharpness.enhance(2)
        cvImg = np.array(sharpImg)
        blurA = variance_of_laplacian(cvImg)
        # print(IMAGENAME[:-4] + '_sharp.jpg', blur)
        contrast = ImageEnhance.Contrast(sharpImg)
        img = contrast.enhance(1.5)
        # sharpImg.save(IMAGENAME[:-4] + '_sharp.jpg')
        # conImg.save(IMAGENAME[:-4] + '_contrast.jpg')
    img.save(r"C:\\Users\\ankitaa\Desktop\\idocufy\\Images\\Valid Licence and SSN\\" +tail + "_Final.jpg")
        
