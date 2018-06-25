import io

import cv2,os
from pylab import arange
import numpy as np,sys
from PIL import Image

sys.path.insert(0, '../image_processing')


class Denoising:

    def image_conversion_smooth(self,path,doc_type):
        try:
            pImg = ''
            filename=os.path.basename(path)
            if 'SSN' in doc_type:
                with io.open(path, 'rb') as image_file:
                    self.image_content = image_file.read()
                img=Image.open(io.BytesIO(self.image_content)).convert('L')
                img = np.array(img.copy())
                pImg = cv2.GaussianBlur(img, (3,3), 0)
                # pImg = cv2.fastNlMeansDenoising(img, None, 1,1)
            elif 'Passport' in doc_type:
                img = Image.open(path)
                img = np.array(img.copy())
                # b, g, r = cv2.split(img)  # get b,g,r
                # Denoising
                img = cv2.GaussianBlur(img, (1, 1), 0)
                pImg = cv2.fastNlMeansDenoising(img, None, 5, 5)
                # b, g, r = cv2.split(dst)  # get b,g,r
                # pImg = cv2.merge([r, g, b])

            cv2.imwrite("../images/static/" + filename, pImg)
            print("Done Image Proccessing")
            return "../images/static/" + filename
        except Exception as e:
            print(e)


# i=Denoising()
# val=i.image_conversion_smooth(r"C:\Users\ankitaa\Desktop\Valid Driver Licenses\157217830.jpg",'License')