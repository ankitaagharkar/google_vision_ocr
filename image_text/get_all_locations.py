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
        self.dict = {}
        self.emp_name={}
        self.text_val=[]
        self.location_json=''

    def get_text(self,path):
        client = vision.ImageAnnotatorClient()
        with io.open(path, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        # response = client.document_text_detection(image=image)
        # texts = response.full_text_annotation
        response = client.text_detection(image=image)
        texts = response.text_annotations
        for text in texts[1:]:

            self.text_val.append(text.description)
            vertices = [(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices]
            self.result.setdefault(text.description, vertices)
        data = " ".join(map(str, self.text_val))
        #print(text)
        return data
    def get_location(self,value_json,image,application_id,base_url):
        img=cv2.imread(image)
        _,filename= os.path.split(image)
        self.location_json = json.dumps(self.result)
        load_location_json = json.loads(self.location_json)
        for key, value in load_location_json.items():
            print(key, value)
            for key1, value1 in value_json.items():
                if key!='' and value1!='':
                    key=key.replace(',','')
                    key=key.replace(' ','')
                    key=key.replace('No:','')
                    key=key.replace('Issued:','')
                    key=key.replace('Expiros::','')
                    key=key.replace('Expires','')

                    if re.search(r'\b(=?'+re.escape(key)+r')\b',value1):

                        if key in value_json['date_val']:
                            print("in locations",value_json['date_val'])
                            vrx = np.array(value, np.int32)
                            vrx = vrx.reshape((-1, 1, 2))
                            img = cv2.polylines(img.copy(), [vrx], True, (0, 255, 255), 1)
                            # print(key,value)
                            print(key,value)
                            self.dict.update({key: value})
                        elif key in value_json['address']:
                            vrx = np.array(value, np.int32)
                            vrx = vrx.reshape((-1, 1, 2))
                            img = cv2.polylines(img.copy(), [vrx], True, (255, 255, 0), 1)
                            self.address_val.update({key: value})
                        elif key in value_json['license_id']:
                            vrx = np.array(value, np.int32)
                            vrx = vrx.reshape((-1, 1, 2))
                            img = cv2.polylines(img.copy(), [vrx], True, (0, 0, 255), 1)
                            self.licence_id.update({key: value})
                        else:
                            vrx = np.array(value, np.int32)
                            vrx = vrx.reshape((-1, 1, 2))
                            img = cv2.polylines(img, [vrx], True, (0, 255, 0), 1)
                            self.dict.update({key: value})
        dt = datetime.datetime.now()
        date_val=dt.strftime("%Y%j%H%M%S") + str(dt.microsecond)
        cv2.imwrite("../images/processed/"+date_val+".jpg", img)
        return self.address_val,self.licence_id,self.dict,"../images/processed/"+date_val+".jpg"
            # dt = datetime.datetime.now()
            # date_val=dt.strftime("%Y%j%H%M%S") + str(dt.microsecond)
            # cv2.imwrite(base_url+"/uploads"+application_id+"/processed/"+date_val+filename,img)
            # return date_val+filename
        # for key, value in load_location_json.items():
        #     for key1, value1 in value_json.items():
        #         if key!='' and value1!='':
        #             key_value=key.replace(',','')
        #             key_value=key.replace(' ','')
        #
        #             if re.search(r'\b(=?'+re.escape(key_value)+r')\b',value1):
        #                 #print(value)
        #                 if key in value_json['date_val']:
        #                     print(key,value)
        #                     self.dict.update({key: value})
        #                 elif key in value_json['address']:
        #                     self.address_val.update({key: value})
        #                 elif key in value_json['license_id']:
        #                     self.licence_id.update({key: value})
        #                 else:
        #                     self.dict.update({key: value})
        # #print(self.address_val, self.licence_id, self.dict)
        # return self.address_val, self.licence_id, self.dict
    def ssn_get_location(self,value_json,image,application_id,base_url):
        img = cv2.imread(image)
        _, filename = os.path.split(image)
        self.location_json = json.dumps(self.result)
        load_location_json = json.loads(self.location_json)
        for key, value in load_location_json.items():
            print(key, value)
            for key1, value1 in value_json.items():
                if key != '' and value1 != '':
                    key = key.replace(',', '')
                    key = key.replace(' ', '')
                    key = key.replace('No:', '')
                    if re.search(r'\b(=?' + re.escape(key) + r')\b', value1):
                        if key in value_json['ssn_number']:
                            vrx = np.array(value, np.int32)
                            vrx = vrx.reshape((-1, 1, 2))
                            img = cv2.polylines(img.copy(), [vrx], True, (255, 0, 0), 3)
                            self.ssn.update({key: value})

        dt = datetime.datetime.now()
        date_val = dt.strftime("%Y%j%H%M%S") + str(dt.microsecond)
        cv2.imwrite("../images/processed/" + date_val + ".jpg", img)
        return self.ssn,"../images/processed/" + date_val + ".jpg"
    def paystub_get_location(self,value_json,image,application_id,base_url):
        img = cv2.imread(image)
        _, filename = os.path.split(image)
        self.location_json = json.dumps(self.result)
        load_location_json = json.loads(self.location_json)
        for key, value in load_location_json.items():
            print(key, value)
            for key1, value1 in value_json.items():
                if key != '' and value1 != '':
                    key = key.replace(',', '')
                    key = key.replace(' ', '')
                    key = key.replace('No:', '')
                    key = key.replace('Issued:', '')
                    key = key.replace('Expiros::', '')
                    key = key.replace('Expires', '')
                    key = key.replace('1,374-48','1,374')

                    if key in value_json['date_val']:
                        print("in locations", value_json['date_val'])
                        vrx = np.array(value, np.int32)
                        vrx = vrx.reshape((-1, 1, 2))
                        img = cv2.polylines(img.copy(), [vrx], True, (0, 255, 255), 1)
                        # print(key,value)
                        print(key, value)
                        self.dict.update({key: value})
                    elif re.search(r'\b(=?' + re.escape(key) + r')\b', value1):
                        if key in value_json['employer_name']:
                            print("in locations", value_json['employer_name'])
                            vrx = np.array(value, np.int32)
                            vrx = vrx.reshape((-1, 1, 2))
                            img = cv2.polylines(img.copy(), [vrx], True, (0, 255, 255), 2)
                            # print(key,value)
                            print(key, value)
                            self.emp_name.update({key: value})

                        else:
                            vrx = np.array(value, np.int32)
                            vrx = vrx.reshape((-1, 1, 2))
                            img = cv2.polylines(img, [vrx], True, (0, 255, 0), 2)
                            self.dict.update({key: value})
        print('emp_name',self.emp_name,self.dict)
        dt = datetime.datetime.now()
        date_val = dt.strftime("%Y%j%H%M%S") + str(dt.microsecond)
        cv2.imwrite("../images/processed/" + date_val + ".jpg", img)
        return self.emp_name, self.dict, "../images/processed/" + date_val + ".jpg"



