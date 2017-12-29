import cv2,os
import numpy as np
from PIL import ImageStat, ImageEnhance, Image


class Denoising:
    def variance_of_laplacian(self,image):
        # compute the Laplacian of the image and then return the focus
        # measure, which is simply the variance of the Laplacian
        return cv2.Laplacian(image, cv2.CV_64F).var()
    def mean_using_mb(self,image):
        median = cv2.medianBlur(image.copy(), 3)
        res = abs(image - median)
        res_mean = np.mean(res)
        return res_mean
    def process_image(self,image, val):
        img = cv2.GaussianBlur(image.copy(), (3, 3),0)
        dst = cv2.fastNlMeansDenoising(img.copy(), None, val, 7, 21)
        kernel = np.ones((3, 2), np.int32)
        erode = cv2.erode(dst, kernel, iterations=0)
        return erode
    def image_conversion_smooth(self,path,doc_type):
        try:
            img = cv2.imread(path)
            height, width, _ = img.shape
            print(height,width)
            pImg=''
            head, tail = os.path.split(path)
            mean = self.mean_using_mb(img)
            if 'License' in doc_type:

                pImg=Image.open(path)
                imStat = ImageStat.Stat(pImg)
                medi = list(map((lambda x: x / 25), imStat.mean))
                print(max(medi))
                if max(medi) < 3:
                    brightness = ImageEnhance.Brightness(pImg)
                    pImg = brightness.enhance(3 - max(medi))
                pImg=pImg.convert('L')
                # brightImg.save(imgPath[:-4] + '_Bright'+ str(max(medi)) + '.jpg')
                sharpness = ImageEnhance.Sharpness(pImg)
                cvImg = np.array(pImg)
                blur = self.variance_of_laplacian(cvImg)
                if blur < 700:
                    print("blur",blur)
                    sharpImg = sharpness.enhance(2)
                    cvImg = np.array(sharpImg)
                    blurA = self.variance_of_laplacian(cvImg)
                    contrast = ImageEnhance.Contrast(sharpImg)
                    pImg = contrast.enhance(1.45)
                pImg = np.array(pImg)
                # else:
                #     img = cv2.imread(path)
                #     if mean==84.5215623913:
                #         pImg=img
                #     if mean < 20:
                #         pImg=self.process_image(img,10)
                #     elif 20 < mean <= 46:
                #         pImg = self.process_image(img, 12)
                #     elif 47< mean <=64:
                #         pImg = self.process_image(img, 10)
                #     elif mean <=86.0:
                #         pImg = self.process_image(img, 25)
                #     elif mean >=87.0:
                #         pImg = self.process_image(img, 5)
                #     else:
                #         pass
            elif 'SSN' in doc_type:
                img = cv2.imread(path)
                head, tail = os.path.split(path)
                mean = self.mean_using_mb(img)
                print(mean)
                pImg = self.process_image(img, 30)
                for i in list(range(5)):  # to Iterate again
                    mean = self.mean_using_mb(pImg)
                    if (mean > 65.0):
                        pImg = self.process_image(pImg, 20)
                    else:
                        break
            elif 'PayStub' in doc_type:
                img = cv2.imread(path)
                head, tail = os.path.split(path)
                mean = self.mean_using_mb(img)
                print(mean)
                pImg = self.process_image(img, 10)
                for i in list(range(5)):  # to Iterate again
                    mean = self.mean_using_mb(pImg)
                    if (mean > 65.0):
                        pImg = self.process_image(pImg, 20)
                    else:
                        break
            cv2.imwrite("../images/static/" + tail, pImg)
            return "../images/static/" + tail
        except Exception as e:
            print(e)


# i=Denoising()
# val=i.image_conversion_smooth(r"C:\Users\ankitaa\Desktop\Valid Driver Licenses\157217830.jpg",'License')