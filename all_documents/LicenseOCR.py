import io
import json
import re
import os
import datetime
import cv2
import numpy as np
import requests
from google.cloud import vision_v1p1beta1 as vision

from google.cloud.vision import types
from pylab import arange
from PIL import Image
import sys
import difflib
import copy
import subprocess
from SkewRotation import SkewRotation
from LicenseAddress import LicenseAddress
from get_licence_details import Licence_details

"""
Changelog


"""


class LicenseOCR:
    def __init__(self):
        self.result = {}
        self.text_val = []
        self.keys = []
        self.values = []
        self.description = []
        self.conf_keys = []
        self.conf_values = []

    def get_texts_from_bytes(self, content):
        client = vision.ImageAnnotatorClient()
        image = vision.types.Image(content=content)
        response = client.document_text_detection(image=image)
        texts = response.text_annotations
        return texts, response

    def get_word_coordinates(self, texts):
        self.__init__()
        self.description = texts[0]

        height_list = []
        slanted_list = []
        rotated_list = []

        for text in texts[1:]:
            if text.description in ['*']:
                continue
            self.text_val.append(text.description)
            vertices = [(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices]
            self.keys.append(text.description)
            self.values.append(vertices)
            vertices = [(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices]
            height_list.append(abs(vertices[0][1] - vertices[3][1]))
            slanted_list.append(abs(vertices[0][1] - vertices[1][1]))
            if vertices[0][1] > vertices[2][1] and vertices[1][1] > vertices[3][1]:
                rotated_list.append(180)
            elif vertices[0][1] > vertices[2][1]:
                rotated_list.append(270)
            elif vertices[1][1] > vertices[3][1]:
                rotated_list.append(90)
            else:
                rotated_list.append(0)
        self.result = zip(self.keys, self.values)
        return height_list, slanted_list, rotated_list

    def get_word_confidence(self, response):
        text = []
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                block_words = []
                for paragraph in block.paragraphs:
                    block_words.extend(paragraph.words)
                block_symbols = []
                for word in block_words:
                    block_symbols.extend(word.symbols)
                block_text = ''
                for symbol in block_symbols:
                    test = symbol.property.detected_break
                    if str("SPACE").lower() in str(test).lower():
                        symbol.text = symbol.text + ' '
                    block_text = block_text + symbol.text

                text.append(block_text)
        for page1 in response.full_text_annotation.pages:
            for block1 in page1.blocks:
                block_words1 = []
                for paragraph1 in block1.paragraphs:
                    block_words1.extend(paragraph1.words)
                block_text = ''
                block_symbols1 = []
                for word1 in block_words1:
                    block_symbols1.extend(word1.symbols)
                    word_text1 = ''
                    for symbol1 in word1.symbols:
                        word_text1 = word_text1 + symbol1.text
                        # print(u'Word text: {} (confidence: {})\n'.format(word_text1, word1.confidence))

                    self.conf_keys.append(word_text1)
                    self.conf_values.append(word1.confidence)
        self.conf_result = zip(self.conf_keys, self.conf_values)
        actual_text = " ".join(map(str, text))
        return actual_text, self.conf_result

    def get_state_coordinates(self):

        global state_name
        self.description.description = self.description.description.replace(" EN ", "")
        self.description.description = self.description.description.replace("END", "")
        self.description.description = self.description.description.replace("End", "")
        self.description.description = self.description.description.replace("NONE", "")
        self.description.description = self.description.description.replace("None", "")
        self.description.description = self.description.description.replace(" FN ", "")
        self.description.description = self.description.description.replace(" LN ", "")
        if re.search(r'(!?New|NEW|JERSEY|Jersey)', self.description.description):
            self.description.description = self.description.description.replace(' DE ', '', 1)
            self.description.description = self.description.description.replace(' NE ', '', 1)
            self.description.description = self.description.description.replace(' ID ', '', 1)
            self.description.description = self.description.description.replace(' IN ', '', 1)
        text_value=str(self.description.description)
        if re.search(r'(!?New|NEW|JERSEY|Jersey)', self.description.description):
            self.description.description= self.description.description.replace('DE','',1)
        if 'M. 088173441' in self.description.description:
            state_name='M'
        if 'NJQ8104-2010' in self.description.description:
            state_name='NJQ8104'
        else:
            val = re.findall(
                r'\b(!?AL|AB|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MJ|MN|MS|MO|MT|NE|NV|NH|NJ|NL|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\,?\s(\d{5}(?:\s?\-\s?\d{4})|\d{5}(?:\s?\.\s?\d{4})|\d{5})',
                self.description.description)
            if not val:
                val1 = re.findall(r'\s\b(!?AL|AB|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MJ|MN|MS|MO|MT|NE|NV|NH|NJ|NL|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\s',
                    self.description.description)
                val1_empty = True
                if val1!=[]:
                    val1_empty = False
                    print(val1)
                    if len(val1) >= 2:
                        poppedElements = []
                        for (index, i) in enumerate(val1):
                            val2 = ' '.join(map(str, self.description.description.split(i, 1)[0].split()[-1:]))
                            print(val2)
                            if re.search(r'\d+', val2) or 'DRIVER LICENSE'.lower()==val2.lower():
                                # val1.remove(i)
                                poppedElements.append(index)
                        for i in reversed(poppedElements):
                            val1.pop(i)
                        if len(val1) > 1:
                            val2 = ' '.join(map(str, self.description.description.split(val1[-1], 1)[0].split()[0:2]))
                            print(val2)
                            if not re.search(r'\d+\s?[A-Za-z]+\s[A-Za-z]+', val2):
                                val1.pop()
                                # val1.remove(i)
                                # poppedElements.append(val1.index(i))
                        elif len(val1) == 0:
                            val1_empty = True
                        else:
                            state_name=val1[0]
                    else:
                        state_name=val1[0]
                if val1_empty:
                # state_name = re.findall(
                #     r'\b(!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MJ|MN|MS|MO|MT|NE|NV|NH|NJ|NL|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\,?\s(\d{5}\d{1,4}|\d{5}(?:\s?\-\s?\d{1,4})|\d{5}(?:\s?\-?\s?[A-Za-z]+\d{1,4})|\d{5}(?:\s?\.\s?\d{4})|\d{5})',
                #     str(self.description.description))
                # if not state_name:
                #     state_name = re.findall(
                #         r'\b(!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|I|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MJ|MN|MS|MO|MT|NE|NV|NH|NJ|NL|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\,?\s',
                #         str(self.description.description))
                #     if not state_name:
                    ignore_val = re.findall(
                        r'\b(\s\d+\s?([A-Za-z]+)?\s?([A-Za-z]+)?\s?\s?([A-Za-z]+)?\s?(\d+)?\s?([ŽA-Za-z]+)?\s?(\d+)?[#.,/]?\s?([ŽA-Za-z]+)\s?[#.,/]?\s?(\w*)?\.?\s?(!?AŻ|NU|\.?NL|N\.|NJI|SU|NA|Na|NW|NIIN|NI|AJ|NO)\s?\s?\s?\w+)',
                        self.description.description)

                    if ignore_val != []:
                        if re.search(
                                r'[A-Za-z]+\s?\.?\s?(!?AL|AB|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\b',
                                self.description.description):
                            state_val = re.findall(
                                r'\b(!?AL|AB|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)',
                                text_value)
                            state_name = state_val[0]

                        else:
                            if re.search(ignore_val[0][::-1][0], text_value):
                                state_name = ignore_val[0][::-1][0]

                    else:
                        state_val = re.findall(
                            r'\b(!?AL|AB|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)',
                            text_value)
                        state_name = state_val[0]
            else:
                state_name = val[0][0]
        # else:
        #     state_name = [state_name[0][0]]

        # print('State name is ', state_name)
        state = state_name
        all_points = []
        if not state:
            return False, all_points

        result = copy.deepcopy(self.result)
        for key, values in enumerate(result):
            if difflib.get_close_matches(values[0], [state], cutoff=0.90):
                # print(values)
                all_points.append(values)


        if all_points:
            return True, all_points
        return False, all_points
    # def get_state_coordinates(self):
    #
    #     global state_val
    #     self.description.description = self.description.description.replace(" EN ", "")
    #     self.description.description = self.description.description.replace(" FN ", "")
    #     self.description.description = self.description.description.replace(" LN ", "")
    #     text_value = str(self.description.description)
    #     all_number = re.findall(
    #         r"\s?\s\d{1}\s\w[A-Za-z]+|\s\d{4}\s[A-Za-z]+"
    #         r"|\d{2}\s[A-Za-z]+|\d{2}-\d{2}\s[A-Za-z]+"
    #         r"|\s?\d{3}\w?\s[A-Za-z]+\,?|\s\d{3}\s\d{1}"
    #         r"|\w*\s\d{2,5}\s?-\s?\d{4}|\w*\s\d{5}\s\w*|\w*\s\d{2,5}|\w*\s\d{2,5}\s\d{2,3}",
    #         str(self.description.description))
    #
    #     number_val = ' '.join(map(str, all_number))
    #     state_name = re.findall(
    #         r'\b(!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MJ|MN|MS|MO|MT|NE|NV|NH|NJ|NL|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\,?\s(\d{5}\d{1,4}|\d{5}(?:\s?\-\s?\d{1,4})|\d{5}(?:\s?\-?\s?[A-Za-z]+\d{1,4})|\d{5}(?:\s?\.\s?\d{4})|\d{5})',
    #         str(self.description.description))
    #
    #     if not state_name:
    #         # state_name = re.findall(r'\b(!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|I|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MJ|MN|MS|MO|MT|NE|NV|NH|NJ|NL|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\,?\s', str(self.description.description))
    #         state_name = re.findall(
    #             r'\b(\s\d+\s?([A-Za-z]+)?\s?([A-Za-z]+)?\s?\s?([A-Za-z]+)?\s?(\d+)?\s?([ŽA-Za-z]+)?\s?(\d+)?[#.,/]?\s?([ŽA-Za-z]+)\s?[#.,/]?\s?(\w*)?\.?\s(AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|I|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MJ|MN|MS|MO|MT|NE|NV|NH|NJ|NL|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY))',
    #             str(self.description.description))
    #         if state_name!=[]:
    #             for item in state_name[0]:
    #                 state_val = "".join(item)
    #             state_name = re.findall(
    #                 r'\b(!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|I|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MJ|MN|MS|MO|MT|NE|NV|NH|NJ|NL|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)',
    #                 state_val)
    #
    #         if state_name==[]:
    #             ignore_val = re.findall(
    #                 r'\b(\s\d+\s?([A-Za-z]+)?\s?([A-Za-z]+)?\s?\s?([A-Za-z]+)?\s?(\d+)?\s?([ŽA-Za-z]+)?\s?(\d+)?[#.,/]?\s?([ŽA-Za-z]+)\s?[#.,/]?\s?(\w*)?\.?\s?(!?AŻ|NU|\.?NL|N\.|NJI|SU|NA|Na|NW|NIIN|NI|AJ|NO)\s?\w+)',
    #                 text_value)
    #
    #             # r'\b(\s\d+\s([A-Za-z]+)?\s([A-Za-z]+)?\s?\s([A-Za-z]+)?\s?(\d+)?\s?([A-Za-z]+)?\s?(\d+)?\s?([A-Za-z]+)\s?[#.,/]?\s?(\w*)?\s?(!?AŻ|NU |\.?NL|N\.|NJI | SU | NA | Na | NW |NI|AJ| NO)\s?\w+)',
    #             # text_value)
    #
    #             if ignore_val != []:
    #                 if re.search(
    #                         r'\b(\s\d+\s?([A-Za-z]+)?\s?([A-Za-z]+)?\s?\s?([A-Za-z]+)?\s?(\d+)?\s?([ŽA-Za-z]+)?\s?(\d+)?[#.,/]?\s?([ŽA-Za-z]+)\s?[#.,/]?\s?(\w*)?\.?\s(!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\b',
    #                         text_value):
    #                     state_val = re.findall(
    #                         r'\b(\s\d+\s?([A-Za-z]+)?\s?([A-Za-z]+)?\s?\s?([A-Za-z]+)?\s?(\d+)?\s?([ŽA-Za-z]+)?\s?(\d+)?[#.,/]?\s?([ŽA-Za-z]+)\s?[#.,/]?\s?(\w*)?\.?\s(!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)',
    #                         text_value)
    #                     state_name = state_val[0]
    #
    #                 else:
    #                     if re.search(ignore_val[0][::-1][0], text_value):
    #                         state_name = ignore_val[0][::-1][0]
    #             else:
    #                 state_val = re.findall(
    #                     r'\b(\s\d+\s?([A-Za-z]+)?\s?([A-Za-z]+)?\s?\s?([A-Za-z]+)?\s?(\d+)?\s?([ŽA-Za-z]+)?\s?(\d+)?[#.,/]?\s?([ŽA-Za-z]+)\s?[#.,/]?\s?(\w*)?\.?\s(!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)',
    #                     text_value)
    #                 state_name = state_val[0]
    #     else:
    #         state_name = [state_name[0][0]]
    #
    #     print('State name is ', state_name)
    #     state = state_name
    #     all_points = []
    #     if not state:
    #         return False, all_points
    #
    #     result = copy.deepcopy(self.result)
    #     for key, values in enumerate(result):
    #         if difflib.get_close_matches(values[0], [state[len(all_points)]], cutoff=0.90):
    #             print(values)
    #             all_points.append(values)
    #             if len(all_points) == len(state):
    #                 break
    #     if all_points:
    #         return True, all_points
    #     return False, all_points

    def cvToPil(self, cvImage):
        """Converts opencv format image to PIL object 
        Args: cvImage: {numpy.ndarray} 
        -- OpenCV or ndarray Image Returns: Image converted to PIL Image """
        pilImage = Image.fromarray(cvImage)
        return pilImage

    def rotate_image(self, ext, rotation_deg):
        # read image from bytes content and return bytes content
        image = Image.open(io.BytesIO(self.image_content))
        if rotation_deg == 90:
            image = image.transpose(Image.ROTATE_90)
        else:
            image = image.transpose(Image.ROTATE_270)

        b = io.BytesIO()
        if ext.lower() in ('png'):
            save_ext = 'PNG'
        elif ext.lower() in ('jpg', 'jpeg'):
            save_ext = 'JPEG'
        image.save(b, save_ext)

        return b.getvalue()

    def process_image(self, ext):
        # read image from bytes in PIL

        pilImage = Image.open(io.BytesIO(self.image_content))
        processedImage = cv2.GaussianBlur(np.array(pilImage), (1, 1), 0)

        # processedImage = cv2.boxFilter(np.array(pilImage), 0, (1, 1))
        # processedImage = cv2.GaussianBlur(np.array(pilImage), (3, 1), 0)
        # convert PIL image to cv2 and do processing
        # img=np.array(pilImage.copy())
        #
        # image=cv2.GaussianBlur(img.copy(),(1,1),0.6)
        # # # processedImage=cv2.GaussianBlur(img.copy(),(1,1),0.5)
        # # # processedImage = cv2.fastNlMeansDenoising(image.copy(), None, 10, 7, 21)
        # #
        # #
        # maxIntensity = 255.0 # depends on dtype of image data
        # x = arange(maxIntensity)
        # # Parameters for manipulating image data
        # phi = 1
        # theta = 1
        # # Increase intensity such that
        # processedImage = (maxIntensity / phi) * (image / (maxIntensity / theta)) * 1
        # #
        # #
        # # #convert cv2 image to PIL
        pilImage = Image.fromarray(processedImage)

        # convert PIL image to byte contents
        b = io.BytesIO()
        if ext.lower() in ('png'):
            save_ext = 'PNG'
        elif ext.lower() in ('jpg', 'jpeg'):
            save_ext = 'JPEG'
        elif ext.lower() in ('bmp'):
            save_ext = 'bmp'
        pilImage.save(b, save_ext)
        return b.getvalue()

    def process_after_image(self, ext):
        # read image from bytes in PIL
        pilImage = Image.open(io.BytesIO(self.image_content))

        img = cv2.boxFilter(np.array(pilImage), 0, (3, 3))
        processedImage = cv2.GaussianBlur(img.copy(), (1, 1), 0)
        # #
        # #
        # # #convert cv2 image to PIL
        pilImage = Image.fromarray(processedImage)

        # convert PIL image to byte contents
        b = io.BytesIO()
        if ext.lower() in ('png'):
            save_ext = 'PNG'
        elif ext.lower() in ('jpg', 'jpeg'):
            save_ext = 'JPEG'
        pilImage.save(b, save_ext)
        return b.getvalue()

    def remove_dotted_band(self, ext):
        # img = cv2.imread(sys.argv[1], 0)
        # read image from bytes in PIL
        img = Image.open(io.BytesIO(self.image_content))

        w, h = img.size
        if h + w > 5000:
            filter_size = 12
        else:
            filter_size = 5
        img = np.array(img)

        # if image is not black and white already, convert it to grayscale
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img

        gray = cv2.threshold(gray, 127, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        img = cv2.medianBlur(gray, 1)

        _, blackAndWhite = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

        nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(blackAndWhite, 4,
                                                                             cv2.CV_32S)
        sizes = stats[1:, -1]  # get CC_STAT_AREA component
        img2 = np.zeros((labels.shape), np.uint8)

        for i in range(0, nlabels - 1):
            if sizes[i] >= filter_size:  # filter small dotted regions
                img2[labels == i + 1] = 255
        res = cv2.bitwise_not(img2)
        pilImage = Image.fromarray(res)
        pilImage.show()

        return pilImage

    def pdf_to_image(self, image_path):
        split_path = os.path.split(os.path.abspath(image_path))
        filename = split_path[1].split('.')[0] + '.jpg'
        out_path = os.path.join(split_path[0], filename)
        image_path = image_path.replace(' ', '\ ')
        out_path = out_path.replace(' ', '\ ')
        process = subprocess.call(
            'convert -density 300 -trim ' + image_path + ' -quality 100 ' + out_path, shell=True)
        image_path = out_path.replace('\ ', ' ')
        return image_path, 'jpg'

    def change_coordinates(self, mode_rotate, points):
        image = Image.open(io.BytesIO(self.image_content))
        width, height = image.size
        text_result = copy.deepcopy(self.result)

        new_result = []
        new_points = []

        slanted_list = []
        height_list = []
        if mode_rotate == 90:
            for v in text_result:
                for i in range(4):
                    v[1][i] = (v[1][i][1], width - v[1][i][0])
                height_list.append(abs(v[1][0][1] - v[1][3][1]))
                slanted_list.append(abs(v[1][0][1] - v[1][1][1]))
                new_result.append(v)
            for p in points:
                for i in range(4):
                    p[1][i] = (p[1][i][1], width - p[1][i][0])
                new_points.append(p)
        elif mode_rotate == 270:
            for v in text_result:
                for i in range(4):
                    v[1][i] = (height - v[1][i][1], v[1][i][0])
                height_list.append(abs(v[1][0][1] - v[1][3][1]))
                slanted_list.append(abs(v[1][0][1] - v[1][1][1]))
                new_result.append(v)
            for p in points:
                for i in range(4):
                    p[1][i] = (height - p[1][i][1], p[1][i][0])
                new_points.append(p)
        elif mode_rotate == 180:
            for v in text_result:
                # print(v)
                for i in range(4):
                    v[1][i] = (width - v[1][i][0], height - v[1][i][1])
                # print(v)
                height_list.append(abs(v[1][0][1] - v[1][3][1]))
                slanted_list.append(abs(v[1][0][1] - v[1][1][1]))
                new_result.append(v)
            for p in points:
                for i in range(4):
                    p[1][i] = (width - p[1][i][0], height - p[1][i][1])
                new_points.append(p)
        self.result = new_result
        return height_list, slanted_list, points

    def run(self, image_path):

        global pdf_image_path
        pdf_image_path = ''
        ext = image_path.split('.')[-1]
        if ext == 'pdf':
            image_path, ext = self.pdf_to_image(image_path)
            pdf_image_path = image_path

        # read image contents from io, for all operations except deskew we shall use
        # this image_content.
        with io.open(image_path, 'rb') as image_file:
            self.image_content = image_file.read()

        image_updated = False  # flag to track changes in image contents

        self.image_content = self.process_image(ext)
        image = Image.open(io.BytesIO(self.image_content))
        image.save(image_path)

        texts, response = self.get_texts_from_bytes(self.image_content)
        hl, sl, rl = self.get_word_coordinates(texts)
        mode_slant = max(set(sl), key=sl.count)
        mode_rotate = max(set(rl), key=rl.count)
        # print('Mode Slant ', mode_slant)

        """
        Create an object of get details class, and retrieve dates and its confidence.
        To be done by Ankita
        """

        state_status, points = self.get_state_coordinates()

        if not state_status:
            #if state not found, go for image processing
            # print('Processing Image')
            self.image_content = self.process_after_image(ext)
            image_updated = True



        # if image is updated, save it to its filepath using byte content
        if image_updated:
            image = Image.open(io.BytesIO(self.image_content))
            image.save(image_path)

        if mode_slant > 1 and mode_rotate == 0:
            # deskew image iff it is horizontal and slant is present
            # read image from path, and finally pass the content by reading it from io
            sr = SkewRotation(image_path)
            sr.process_image()
            with io.open(image_path, 'rb') as image_file:
                self.image_content = image_file.read()
            image_updated = True

        # retry GCV and fetch other details if image is updated
        if image_updated:
            texts, response = self.get_texts_from_bytes(self.image_content)
            hl, sl, rl = self.get_word_coordinates(texts)
            mode_slant = max(set(sl), key=sl.count)

            state_status, points = self.get_state_coordinates()
            if not state_status:
                print('No details found in this image, OCR failed')
                return

        if mode_rotate != 0:
            # code for rotating image by given degrees.
            # print('Rotating image by ', mode_rotate, ' degrees')
            hl, sl, points = self.change_coordinates(mode_rotate, points)

        text_result = copy.deepcopy(self.result)
        mode_height = max(set(hl), key=hl.count)
        la_obj = LicenseAddress()
        lic_details = Licence_details()
        address_details = la_obj.fetch(mode_slant, mode_height, points, self)
        licence_id, expiry_date, dob, issue_date, address, name, state, zipcode, city, date_val = lic_details.get_licence_details1(
            str(self.description.description), address_details)
        return response, licence_id, expiry_date, dob, issue_date, address, name, state, zipcode, city, date_val, text_result, pdf_image_path

#
# def main():
#     lic = LicenseOCR()
#     lic.run(sys.argv[1])
#
# if __name__ == "__main__":
#     main()
