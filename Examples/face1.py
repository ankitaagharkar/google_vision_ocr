from PIL import Image, ExifTags
import cv2,os,numpy as np,imutils

path=r"C:\Users\ankitaa\Documents\Valid Driver Licenses\NJ DL 22.JPG"
img = Image.open(path).convert('L')
width, height = img.size
# print(width,height)
# import scipy.ndimage
# height, width, channels = scipy.ndimage.imread(path).shape
# print(height,width)
# img.thumbnail((height,width),Image.ANTIALIAS)

# img.save("../Examples/12.png")

# print(img._getexif().items())
# exif=dict((ExifTags.TAGS[k], v) for k, v in img._getexif().items() if k in ExifTags.TAGS)
# if not exif['Orientation'] or width<height:
# img=np.array(img)
#     img=imutils.rotate_bound(img,270)
    # img=img.rotate(270)
# img.thumbnail((width,height), Image.ANTIALIAS)
# img.resize((height,width+100))
# img.save("../Examples/121.jpg")

# cv2.imwrite("../Examples/1.jpg", img,[cv2.IMWRITE_JPEG_QUALITY,90])
pImg=''
filename=os.path.basename(path)
# print(filename)
# head, tail = os.path.split(path)

# img1 = cv2.imread(path,0)
  #
  # load as 1-channel 8bit grayscale
# img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
image1=np.array(img.copy())
# image1=imutils.rotate_bound(image1,90)
image=cv2.GaussianBlur(image1,(3,1),0)
# image=cv2.dilate(image,(1,2),0)
# image=cv2.fastNlMeansDenoisingColored(img,None,15,21,9,25)
maxIntensity = 255.0  # depends on dtype of image data
x = np.arange(maxIntensity)
# Parameters for manipulating image data
phi = 1
theta = 1
# Increase intensity such that
img1 = (maxIntensity / phi) * (image / (maxIntensity / theta)) ** 2
# cv2.imwrite("../images/static/" + tail+'_processed', img1)
z = (maxIntensity / phi) * (x / (maxIntensity / theta)) ** 1


pImg = np.hstack((image1, img1))
# pImg=cv2.resize(pImg,(width,height))
cv2.imwrite("../Examples/" +str(1)+filename, pImg)

