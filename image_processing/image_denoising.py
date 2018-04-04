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
                img = Image.open(path).convert('L')
                img = np.array(img.copy())
                pImg=cv2.GaussianBlur(img,(3,3),0)

            cv2.imwrite("../images/static/" + filename, pImg)
            print("Done Image Proccessing")
            return "../images/static/" + filename
        except Exception as e:
            print(e)


# i=Denoising()
# val=i.image_conversion_smooth(r"C:\Users\ankitaa\Desktop\Valid Driver Licenses\157217830.jpg",'License')