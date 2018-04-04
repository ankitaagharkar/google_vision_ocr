""" Deskews file after getting skew angle """
import optparse
import numpy as np
import matplotlib.pyplot as plt
import sys

from skew_detect import SkewDetect
from skimage import io
from skimage.transform import rotate
from PIL import Image


class Deskew:

    def __init__(self, input_file):

        self.input_file = input_file
        self.display_image = None
        self.output_file = input_file
        self.r_angle = 0
        self.skew_obj = SkewDetect(self.input_file)

    def deskew(self):

        img = io.imread(self.input_file)
        res = self.skew_obj.process_single_file()
        angle = res['Estimated Angle']
        print('Estimated Angle ',angle)

        if angle >= 0 and angle <= 90:
            rot_angle = angle - 90 + self.r_angle
        if angle >= -45 and angle < 0:
            rot_angle = angle + self.r_angle
        if angle >= -90 and angle < -45:
            rot_angle = 90 + angle + self.r_angle

        pilImage = Image.open(self.input_file)
        pilImage = pilImage.rotate(rot_angle,expand=True)
        pilImage.save(self.input_file)

        """
        rotated = rotate(img, rot_angle, resize=True)

        if self.display_image:
            self.display(rotated)

        if self.output_file:
            self.saveImage(rotated*255)
        """

    def saveImage(self, img):
        path = self.skew_obj.check_path(self.output_file)
        io.imsave(path, img.astype(np.uint8))

    def display(self, img):

        plt.imshow(img)
        plt.show()

    def run(self):

        if self.input_file:
            self.deskew()


if __name__ == '__main__':

    parser = optparse.OptionParser()

    parser.add_option(
        '-i',
        '--input',
        default=None,
        dest='input_file',
        help='Input file name')
    parser.add_option(
        '-d', '--display',
        default=None,
        dest='display_image',
        help="display the rotated image")
    parser.add_option(
        '-o', '--output',
        default=None,
        dest='output_file',
        help='Output file name')
    parser.add_option(
        '-r', '--rotate',
        default=0,
        dest='r_angle',
        help='Rotate the image to desired axis',
        type=int)
    options, args = parser.parse_args()
    deskew_obj = Deskew(
        sys.argv[1],
        options.display_image,
        'xx.jpeg',
        options.r_angle)

    deskew_obj.run()