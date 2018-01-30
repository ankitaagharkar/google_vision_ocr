import io
import json
import re
import os
import datetime
import cv2
import numpy as np
import requests
from google.cloud import vision
from google.cloud.vision import types

class get_all_location:
    def __init__(self):
        self.result={}
        self.address_val={}
        self.licence_id={}
        self.ssn={}
        self.keys=[]
        self.values=[]
        self.dict = {}
        self.emp_name={}
        self.text_val=[]
        self.location_json=''

    def get_text(self,path,doc_type):
        try:
            client = vision.ImageAnnotatorClient()
            text = []
            with io.open(path, 'rb') as image_file:
                content = image_file.read()

            image = vision.types.Image(content=content)

            response = client.document_text_detection(image=image)
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

            actual_text = " ".join(map(str, text))
            print(actual_text)
            for text in response.text_annotations[1:]:

                print(text.description)
                vertices = [(vertex.x, vertex.y)
                            for vertex in text.bounding_poly.vertices]
                print(vertices)
                self.keys.append(text.description)
                self.values.append(vertices)
            self.result = zip(self.keys, self.values)
            return actual_text

        except Exception as E:
            print(E)
    def get_location(self,value_json,image,application_id,base_url):
        try:
            # value_json = {key: value for key, value in value_data.items() if value != ""}
            # empty_key_vals = list(k for k,v in data.items() if v)
            # for k in empty_key_vals:
            #     del [k]
            print(value_json)
            img=cv2.imread(image)
            _,filename= os.path.split(image)

            for key, value in enumerate(self.result):
                print(value[0], value[1])
                for key1, value1 in value_json.items():
                    if value[0]!='' and value1!='':
                        value=list(value)

                        values=value[0].replace(',','')
                        values=values.replace(' ','')
                        values=values.replace('No:','')
                        values=values.replace('Issued:','')
                        values=values.replace('Expiros::','')
                        values=values.replace('Expires','')
                        value[0]=values
                        if key1=='issue_date' or key1=='expiration_date' or value[0]=='dob':
                            value1=value1[0:2] + ' ' + value1[2:4] + ' ' + value1[4:8]
                        if key1=='date_val':
                            if len(value1)==32:
                                value1=value1[0:2]+" "+value1[2:3]+" "+value1[3:5]+" "+value1[5:6]+" "+value1[6:10]+" "+value1[11:13]+" "+value1[13:14]+" "+value1[14:16]+" "+value1[16:17]+" "+value1[17:21]+" "+value1[22:24]+" "+value1[24:25]+" "+value1[25:27]+" "+value1[27:28]+" "+value1[28:32]
                            elif len(value1)==21:
                                value1 = value1[0:2] + " " + value1[2:3] + " " + value1[3:5] + " " + value1[5:6] + " " + value1[6:10] + " " + value1[11:13] + " " + value1[13:14] + " " + value1[14:16] + " " + value1[16:17] + " " + value1[17:21]
                            elif len(value1)==10:
                                value1 = value1[0:2] + " " + value1[2:3] + " " + value1[3:5] + " " + value1[5:6] + " " + value1[6:10]
                            elif len(value1)==26:
                                value1=value1[0:2]+" "+value1[2:3]+" "+value1[3:5]+" "+value1[5:6]+" "+value1[6:8]+" "+value1[9:11]+" "+value1[11:12]+" "+value1[12:14]+" "+value1[14:15]+" "+value1[15:17]+" "+value1[18:20]+" "+value1[20:21]+" "+value1[21:23]+" "+value1[23:24]+" "+value1[24:26]
                            elif len(value1)==17:
                                value1 = value1[0:2] + " " + value1[2:3] + " " + value1[3:5] + " " + value1[5:6] + " " + value1[6:8] + " " + value1[9:11] + " " + value1[11:12] + " " + value1[12:14] + " " + value1[14:15]+" "+value1[15:17]
                            elif len(value1)==8:
                                value1 = value1[0:2] + " " + value1[2:3] + " " + value1[3:5] + " " + value1[5:6] + " " + value1[6:8]
                            else:
                                pass
                        if re.search(r'(?!' + re.escape(value[0]) + r')', value1):

                            if value[0] in value_json['date_val']:
                                print("in locations",value_json['date_val'])
                                vrx = np.array(value[1], np.int32)
                                vrx = vrx.reshape((-1, 1, 2))
                                img = cv2.polylines(img.copy(), [vrx], True, (0, 255, 255), 1)
                                # print(key,value)
                                print(value[0],value[1])
                                self.dict.update({value[0]: value[1]})
                            elif value[0] in value_json['address']:
                                vrx = np.array(value[1], np.int32)
                                vrx = vrx.reshape((-1, 1, 2))
                                img = cv2.polylines(img.copy(), [vrx], True, (255, 255, 0), 1)
                                self.address_val.update({value[0]: value[1]})
                            elif value[0] in value_json['license_id']:
                                vrx = np.array(value[1], np.int32)
                                vrx = vrx.reshape((-1, 1, 2))
                                img = cv2.polylines(img.copy(), [vrx], True, (0, 0, 255), 1)
                                self.licence_id.update({value[0]: value[1]})
                            else:
                                vrx = np.array(value[1], np.int32)
                                vrx = vrx.reshape((-1, 1, 2))
                                img = cv2.polylines(img, [vrx], True, (0, 255, 0), 1)
                                self.dict.update({value[0]: value[1]})
            dt = datetime.datetime.now()
            date_val=dt.strftime("%Y%j%H%M%S") + str(dt.microsecond)
            cv2.imwrite("../images/processed/"+date_val+".jpg", img)
            return self.address_val,self.licence_id,self.dict,"../images/processed/"+date_val+".jpg"
        except Exception as e:
            print(e)
    def ssn_get_location(self,value_json,image,application_id,base_url):
        img = cv2.imread(image)
        _, filename = os.path.split(image)
        for key, value in enumerate(self.result):
            print(value[0], value[1])
            for key1, value1 in value_json.items():
                if value[0] != '' and value1 != '':
                    value = list(value)
                    values = value[0].replace(',', '')
                    values = values.replace(' ', '')
                    values = values.replace('No:', '')
                    value[0] = values
                    if re.search(r'\b(=?' + re.escape(value[0]) + r')\b', value1):
                        if value[0] in value_json['ssn_number']:
                            vrx = np.array(value[1], np.int32)
                            vrx = vrx.reshape((-1, 1, 2))
                            img = cv2.polylines(img.copy(), [vrx], True, (255, 0, 0), 3)
                            self.ssn.update({value[0]: value[1]})

        dt = datetime.datetime.now()
        date_val = dt.strftime("%Y%j%H%M%S") + str(dt.microsecond)
        cv2.imwrite("../images/processed/" + date_val + ".jpg", img)
        return self.ssn,"../images/processed/" + date_val + ".jpg"
    def paystub_get_location(self,value_json,image,application_id,base_url):
        img = cv2.imread(image)
        _, filename = os.path.split(image)
        for key, value in enumerate(self.result):
            print(value[0], value[1])
            for key1, value1 in value_json.items():
                # if key1 == 'employment_start_date' or key1 == 'expiration_date' or key == 'dob':
                #     value1 = value1[0:2] + ' ' + value1[2:4] + ' ' + value1[4:8]
                # if key1 == 'date_val':
                #     if len(value1) == 32:
                #         value1 = value1[0:2] + " " + value1[2:3] + " " + value1[3:5] + " " + value1[5:6] + " " + value1[6:10] + " " + value1[11:13] + " " + value1[13:14] + " " + value1[14:16] + " " + value1[16:17] + " " + value1[17:21] + " " + value1[22:24] + " " + value1[24:25] + " " + value1[25:27] + " " + value1[27:28] + " " + value1[28:32]
                #     elif len(value1) == 21:
                #         value1 = value1[0:2] + " " + value1[2:3] + " " + value1[3:5] + " " + value1[5:6] + " " + value1[6:10] + " " + value1[11:13] + " " + value1[13:14] + " " + value1[14:16] + " " + value1[16:17] + " " + value1[17:21]
                #     elif len(value1) == 10:
                #         value1 = value1[0:2] + " " + value1[2:3] + " " + value1[3:5] + " " + value1[5:6] + " " + value1[6:10]
                #     elif len(value1) == 26:
                #         value1 = value1[0:2] + " " + value1[2:3] + " " + value1[3:5] + " " + value1[5:6] + " " + value1[6:8] + " " + value1[9:11] + " " + value1[11:12] + " " + value1[12:14] + " " + value1[14:15] + " " + value1[15:17] + " " + value1[18:20] + " " + value1[20:21] + " " + value1[21:23] + " " + value1[23:24] + " " + value1[24:26]
                #     elif len(value1) == 17:
                #         value1 = value1[0:2] + " " + value1[2:3] + " " + value1[3:5] + " " + value1[5:6] + " " + value1[6:8] + " " + value1[9:11] + " " + value1[11:12] + " " + value1[12:14] + " " + value1[14:15] + " " + value1[15:17]
                #     elif len(value1) == 8:
                #         value1 = value1[0:2] + " " + value1[2:3] + " " + value1[3:5] + " " + value1[5:6] + " " + value1[6:8]
                #     else:
                #         pass
                if value[0] != '' and value1 != '':
                    value = list(value)
                    values = value[0].replace(',', '')
                    # keyskey.replace(' ', '')
                    values = values.replace('No:', '')
                    values = values.replace('Issued:', '')
                    values = values.replace('Expiros::', '')
                    values = values.replace('Expires', '')
                    values = values.replace('-48','')
                    value[0] = values
                    if re.search(r'\b(=?' +re.escape(value[0])+ r')\b', value1):
                        if value[0] in value_json['date_val']:
                            print("in locations", value_json['date_val'])
                            vrx = np.array(value[1], np.int32)
                            vrx = vrx.reshape((-1, 1, 2))
                            img = cv2.polylines(img.copy(), [vrx], True, (0, 255, 255), 1)
                            # print(key,value)
                            print(value[0], value[1])
                            self.dict.update({value[0]: value[1]})
                        elif value[0] in value_json['employer_name']:
                            print("in locations", value_json['employer_name'])
                            vrx = np.array(value[1], np.int32)
                            vrx = vrx.reshape((-1, 1, 2))
                            img = cv2.polylines(img.copy(), [vrx], True, (0, 255, 255), 1)
                            # print(key,value)
                            print(value[0], value[1])
                            self.emp_name.update({value[0]: value[1]})

                        else:
                            vrx = np.array(value[1], np.int32)
                            vrx = vrx.reshape((-1, 1, 2))
                            img = cv2.polylines(img, [vrx], True, (0, 255, 0), 1)
                            self.dict.update({value[0]: value[1]})
        print('emp_name',self.emp_name,self.dict)
        dt = datetime.datetime.now()
        date_val = dt.strftime("%Y%j%H%M%S") + str(dt.microsecond)
        cv2.imwrite("../images/processed/" + date_val + ".jpg", img)
        return self.emp_name, self.dict, "../images/processed/" + date_val + ".jpg"



