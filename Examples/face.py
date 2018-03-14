from PIL import Image, ImageFile
import imutils
import cv2,numpy as np
__all__ = ['fix_orientation']

# PIL's Error "Suspension not allowed here" work around:
# s. http://mail.python.org/pipermail/image-sig/1999-August/000816.html
# ImageFile.MAXBLOCK = 1024*1024
#
# # The EXIF tag that holds orientation data.
EXIF_ORIENTATION_TAG = 0x0112

# Obviously the only ones to process are 3, 6 and 8.
# All are documented here for thoroughness.
ORIENTATIONS = {
    1: ("Normal", 0),
    2: ("Mirrored left-to-right", 0),
    3: ("Rotated 180 degrees", 180),
    4: ("Mirrored top-to-bottom", 0),
    5: ("Mirrored along top-left diagonal", 0),
    6: ("Rotated 90 degrees", -90),
    7: ("Mirrored along top-right diagonal", 0),
    8: ("Rotated 270 degrees", -270)
}

def fix_orientation(img, save_over=False):
    """
    `img` can be an Image instance or a path to an image file.
    `save_over` indicates if the original image file should be replaced by the new image.
    * Note: `save_over` is only valid if `img` is a file path.
    """
    path = img
    if not isinstance(img, Image.Image):
        path = img
        img = Image.open(path)
    elif save_over:
        raise ValueError("You can't use `save_over` when passing an Image instance.  Use a file path instead.")
    try:
        orientation = img._getexif()[EXIF_ORIENTATION_TAG]
        print(orientation)
    except (TypeError, AttributeError, KeyError):
        raise ValueError("Image file has no EXIF data.")
    if orientation in [3,6,8]:
        degrees = ORIENTATIONS[orientation][1]
        print(degrees)
        # img = img.rotate(degrees)
        #
        # if save_over and path is not None:
        #     try:
        #         img.save(path, quality=95, optimize=1)
        #
        #     except IOError:
        #         # Try again, without optimization (PIL can't optimize an image
        #         # larger than ImageFile.MAXBLOCK, which is 64k by default).
        #         # Setting ImageFile.MAXBLOCK should fix this....but who knows.
        #         img.save(path, quality=95)

        return (img, degrees)
    else:
        return (img, 0)

if __name__=='__main__':
    # img1=r"C:\Users\ankitaa\Documents\Valid Driver Licenses\CA DL 3.jpg"
    # img1=r"C:\Users\ankitaa\Documents\Valid Driver Licenses\CA DL 3.jpg"
    img2,angle=fix_orientation(r"C:\Users\ankitaa\Documents\Valid Driver Licenses\MD ID 2.jpg", save_over=False)

    angle=angle%90
    # print(angle)
    image = np.array(img2)
    # img = cv2.imread(img1)
    result=imutils.rotate_bound(image,angle)
    # image_center = tuple(np.array(image.shape[1::-1]) / 2)
    # rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    # result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    result=cv2.resize(result,(640,640))
    # num_rows, num_cols = img.shape[:2]
    #
    # rotation_matrix = cv2.getRotationMatrix2D((num_cols / 2, num_rows / 2), 30, 1)
    # img_rotation = cv2.warpAffine(img, rotation_matrix, (num_cols, num_rows))
    cv2.imshow('Rotation', result)
    cv2.waitKey()
#
# from PIL import Image
# image = Image.open(r"C:\Users\ankitaa\Documents\Valid Driver Licenses\AZ DL 1 - Copy.jpg")
# if hasattr(image, '_getexif'):
#     orientation = 0x0112
#     exif = image._getexif()
#     if exif is not None:
#         orientation = exif[orientation]
#         rotations = {
#             3: Image.ROTATE_180,
#             6: Image.ROTATE_270,
#             8: Image.ROTATE_90
#         }
#         if orientation in rotations:
#             image = image.transpose(rotations[orientation])
# image.save('test.jpeg')

# import cv2
# import numpy
#
# # loading the image into a numpy array
# img = cv2.imread('<image path>')
#
# # rotating the image
# rotated_90_clockwise = numpy.rot90(img)  # rotated 90 deg once
# rotated_180_clockwise = numpy.rot90(rotated_90_clockwise)
# rotated_270_clockwise = numpy.rot90(rotated_180_clockwise)
#
# # displaying all the images in different windows(optional)
# cv2.imshow('Original', img)
# cv2.imshow('90 deg', rotated_90_clockwise)
# cv2.imshow('Inverted', rotated_180_clockwise)
# cv2.imshow('270 deg', rotated_270_clockwise)
#
# k = cv2.waitKey(0)
# if (k == 27):  # closes all windows if ESC is pressed
#     cv2.destroyAllWindows()