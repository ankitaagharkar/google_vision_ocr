import cv2,os
from pylab import array, plot, show, axis, arange, figure, uint8
import numpy as np
from PIL import ImageStat, ImageEnhance, ExifTags, Image
from PIL import Image as I


class Denoising:

    def denoise(self,img, weight=0.1, eps=1e-3, num_iter_max=5):
        """Perform total-variation denoising on a grayscale image.

        Parameters
        ----------
        img : array
            2-D input data to be de-noised.
        weight : float, optional
            Denoising weight. The greater `weight`, the more de-noising (at
            the expense of fidelity to `img`).
        eps : float, optional
            Relative difference of the value of the cost function that determines
            the stop criterion. The algorithm stops when:
                (E_(n-1) - E_n) < eps * E_0
        num_iter_max : int, optional
            Maximal number of iterations used for the optimization.

        Returns
        -------
        out : array
            De-noised array of floats.

        Notes
        -----
        Rudin, Osher and Fatemi algorithm.
        """
        u = np.zeros_like(img)
        px = np.zeros_like(img)
        py = np.zeros_like(img)
        nm = np.prod(img.shape[:2])
        tau = 0.250
        i = 0
        while i < num_iter_max:
            u_old = u
            # x and y components of u's gradient
            ux = np.roll(u, -1, axis=1) - u
            uy = np.roll(u, -1, axis=0) - u
            # update the dual variable
            px_new = px + (tau / weight) * ux
            py_new = py + (tau / weight) * uy
            norm_new = np.maximum(1, np.sqrt(px_new ** 2 + py_new ** 2))
            px = px_new / norm_new
            py = py_new / norm_new
            # calculate divergence
            rx = np.roll(px, 1, axis=1)
            ry = np.roll(py, 1, axis=0)
            div_p = (px - rx) + (py - ry)
            # update image
            u = img + weight * div_p
            # calculate error
            error = np.linalg.norm(u - u_old) / np.sqrt(nm)

            if i == 0:
                err_init = error
                err_prev = error
            else:
                # break if error small enough
                if np.abs(err_prev - error) < eps * err_init:
                    break
                else:
                    e_prev = error
            # don't forget to update iterator
            i += 1
        return u
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
    def image_conversion_smooth(self,path,doc_type,flag):
        try:
            pImg = ''
            filename=os.path.basename(path)
            if 'License' in doc_type:
                # img1 = cv2.imread(path,0)
                  #
                  # load as 1-channel 8bit grayscale
                # img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img1=''
                if flag==False:
                    print(path)
                    img = Image.open(path)
                    img = np.array(img.copy())
                    # img1 = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                    img1 = cv2.GaussianBlur(img.copy(), (1, 1), 0)

                    # img1 = cv2.fastNlMeansDenoising(img1.copy(), None, 10, 7, 21)
                    # width, height = img.size
                    # img.save("../images/static/" + filename)
                elif flag==True:
                    img1 = Image.open(path)
                    img=np.array(img1.copy())
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                    image=cv2.GaussianBlur(img.copy(),(1,1),0)
                    # image = cv2.fastNlMeansDenoising(image.copy(), None, 10, 7, 21)
                    # image=cv2.dilate(image,(1,2),0)
                    # image=cv2.fastNlMeansDenoisingColored(img,None,15,21,9,25)
                    maxIntensity = 255.0  # depends on dtype of image data
                    x = arange(maxIntensity)
                    # Parameters for manipulating image data
                    phi = 1
                    theta = 1
                    # Increase intensity such that
                    img1 = (maxIntensity / phi) * (image / (maxIntensity / theta)) ** 1.5
                    # cv2.imwrite("../images/static/" + tail+'_processed', img1)
                    z = (maxIntensity / phi) * (x / (maxIntensity / theta)) ** 1
                cv2.imwrite("../images/static/" + filename,img1)
                #
                # pImg = np.hstack((img, img1))

            elif 'SSN' in doc_type:
                img = Image.open(path).convert('L')
                img = np.array(img.copy())
                # print("im method", path)

                pImg=cv2.GaussianBlur(img,(3,3),0)
                # pImg=cv2.fastNlMeansDenoisingColored(image,None,13,13,7,21)

                # img = I.open(path)
                # print(pImg)
                # imStat = ImageStat.Stat(img)
                # medi = list(map((lambda x: x / 25), imStat.mean))
                # print(max(medi))
                # if max(medi) < 3:
                #     brightness = ImageEnhance.Brightness(img)
                #     img = brightness.enhance(3 - max(medi))
                # img = img.convert('L')
                # # brightImg.save(imgPath[:-4] + '_Bright'+ str(max(medi)) + '.jpg')
                # sharpness = ImageEnhance.Sharpness(img)
                # cvImg = np.array(img)
                # blur = self.variance_of_laplacian(cvImg)
                # if blur < 500:
                #     print("blur", blur)
                #
                #     sharpImg = sharpness.enhance(2.5)
                #     cvImg = np.array(sharpImg)
                #     contrast = ImageEnhance.Contrast(sharpImg)
                #     img = contrast.enhance(1.47)
                # pImg = np.array(img)
                cv2.imwrite("../images/static/" + filename, pImg)
            print("Done Image Proccessing")
            return "../images/static/" + filename
        except Exception as e:
            print(e)


# i=Denoising()
# val=i.image_conversion_smooth(r"C:\Users\ankitaa\Desktop\Valid Driver Licenses\157217830.jpg",'License')