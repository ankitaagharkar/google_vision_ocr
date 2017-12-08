import cv2,os
import numpy as np

class Denoising:
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
            pImg=''
            head, tail = os.path.split(path)
            mean = self.mean_using_mb(img)
            if 'License' in doc_type:
                if mean==84.5215623913:
                    pImg=img
                if mean < 20:
                    pImg=self.process_image(img,10)
                elif 20 < mean <= 46:
                    pImg = self.process_image(img, 12)
                elif 47< mean <=64:
                    pImg = self.process_image(img, 10)
                elif mean <=86.0:
                    pImg = self.process_image(img, 25)
                elif mean >=87.0:
                    pImg = self.process_image(img, 5)
                else:
                    pass
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
            cv2.imwrite("images/static/" + tail, pImg)
            return "images/static/" + tail
        except Exception as e:
            print(e)