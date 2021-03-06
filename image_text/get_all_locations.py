from google.cloud import vision_v1p1beta1 as vision
import io
import re
import os
import datetime
import threading
import cv2
import numpy as np
from PIL import Image
from multiprocessing import Queue


class get_all_location:
    def __init__(self,result):
        self.client = vision.ImageAnnotatorClient()
        self.result = {}
        self.address_val = {}
        self.licence_id = {}
        self.result = result
        self.ssn = {}
        self.name = {}
        self.date = {}
        self.pay_Val = Queue()
        self.keys = []
        self.values = []
        self.dict = {}

        self.date = {}
        self.conf_keys, self.conf_values = [], []
        self.conf_result = {}
        self.emp_name, self.employee_name = {}, {}
        self.emp_address, self.employee_address = {}, {}
        self.description = []
        self.text_val = []
        self.location_json = ''
        self.regular1, self.regular2, self.regular3, self.regular4, self.regular5, self.regular6, self.regular7, self.regular8, self.regular9, self.regular10 = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
        self.tax1, self.tax2, self.tax3, self.tax4, self.tax5, self.tax6, self.tax7, self.tax8, self.tax9, self.tax10 = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
        self.deduction1, self.deduction2, self.deduction3, self.deduction4, self.deduction5, self.deduction6, self.deduction7, self.deduction8, self.deduction9, self.deduction10, self.deduction11, self.deduction12, self.deduction13, self.deduction14, self.deduction15 = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
        self.pay_start_date, self.pay_end_date, self.pay_date = {}, {}, {}

    def paystub_value(self, value_data, path):
        img = cv2.imread(path)
        value_json={}
        _, filename = os.path.split(path)

        a = 0
        b = 0
        c = 0
        print("value_json",value_data)
        for key, value in value_data.items():
            if "field_value_original" in value_data[key]:
                if value['field_value_original'] != "":
                    value_json.update({key: value})
            else:
                    value_json.update({key: value})
        value_json_keys=list(value_json.keys())
        print("value_json",value_json)
        # key_compare=['pay_period_start_date','pay_period_end_date','pay_date','employee_address','employer_address','employee_name','employer_name']
        for key, value in enumerate(self.result):
            a = a + 1
            b = b + 1
            c = c + 1
            for key1, value1 in value_json.items():
                if  key1!='' and value1 != '':
                    if value[0] != '':
                        value = list(value)
                        values = value[0].replace(',', '')
                        values = values.replace('No:', '')
                        values = values.replace('Issued:', '')
                        values = values.replace('Expiros::', '')
                        values = values.replace('Expires', '')
                        values = values.replace('-48', '')
                        value[0] = values
                        if "field_value_original" in value_json[key1]:
                                if value[0] in value1['field_value_original']:
                                    if "regular" in value1['alias']:
                                        vrx = np.array(value[1], np.int32)
                                        vrx = vrx.reshape((-1, 1, 2))
                                        img = cv2.polylines(img.copy(), [vrx], True, (0, 255, 255), 1)
                                        var_name = "regular" + str(a)
                                        if "1" in var_name:
                                            self.regular1.update({str(value[0]): value[1]})
                                        if "2" in var_name:
                                            self.regular2.update({str(value[0]): value[1]})
                                        if "3" in var_name:
                                            self.regular3.update({str(value[0]): value[1]})
                                        if "4" in var_name:
                                            self.regular4.update({str(value[0]): value[1]})
                                        if "5" in var_name:
                                            self.regular5.update({str(value[0]): value[1]})
                                        if "6" in var_name:
                                            self.regular6.update({str(value[0]): value[1]})
                                        if "7" in var_name:
                                            self.regular7.update({str(value[0]): value[1]})
                                        if "8" in var_name:
                                            self.regular8.update({str(value[0]): value[1]})
                                        if "9" in var_name:
                                            self.regular9.update({str(value[0]): value[1]})
                                        if "10" in var_name:
                                            self.regular10.update({str(value[0]): value[1]})

                                    elif "tax" in value1['alias']:
                                        vrx = np.array(value[1], np.int32)
                                        vrx = vrx.reshape((-1, 1, 2))
                                        img = cv2.polylines(img.copy(), [vrx], True, (0, 255, 255), 1)
                                        var_name = "tax" + str(b)
                                        if "1" in var_name:
                                            self.tax1.update({str(value[0]): value[1]})
                                        if "2" in var_name:
                                            self.tax2.update({str(value[0]): value[1]})
                                        if "3" in var_name:
                                            self.tax3.update({str(value[0]): value[1]})
                                        if "4" in var_name:
                                            self.tax4.update({str(value[0]): value[1]})
                                        if "5" in var_name:
                                            self.tax5.update({str(value[0]): value[1]})
                                        if "6" in var_name:
                                            self.tax6.update({str(value[0]): value[1]})
                                        if "7" in var_name:
                                            self.tax7.update({str(value[0]): value[1]})
                                        if "8" in var_name:
                                            self.tax8.update({str(value[0]): value[1]})
                                        if "9" in var_name:
                                            self.tax9.update({str(value[0]): value[1]})
                                        if "10" in value:
                                            self.tax10.update({str(value[0]): value[1]})

                                    elif "deduction" in value1['alias']:
                                        vrx = np.array(value[1], np.int32)
                                        vrx = vrx.reshape((-1, 1, 2))
                                        img = cv2.polylines(img.copy(), [vrx], True, (0, 255, 255), 1)
                                        var_name = "deduction" + str(c)
                                        if "1" in var_name:
                                            self.deduction1.update({str(value[0]): value[1]})
                                        if "2" in var_name:
                                            self.deduction2.update({str(value[0]): value[1]})
                                        if "3" in var_name:
                                            self.deduction3.update({str(value[0]): value[1]})
                                        if "4" in var_name:
                                            self.deduction4.update({str(value[0]): value[1]})
                                        if "5" in var_name:
                                            self.deduction5.update({str(value[0]): value[1]})
                                        if "6" in var_name:
                                            self.deduction6.update({str(value[0]): value[1]})
                                        if "7" in var_name:
                                            self.deduction7.update({str(value[0]): value[1]})
                                        if "8" in var_name:
                                            self.deduction8.update({str(value[0]): value[1]})
                                        if "9" in var_name:
                                            self.deduction9.update({str(value[0]): value[1]})
                                        if "10" in var_name:
                                            self.deduction10.update({str(value[0]): value[1]})
                                        if "11" in var_name:
                                            self.deduction11.update({str(value[0]): value[1]})
                                        if "12" in var_name:
                                            self.deduction12.update({str(value[0]): value[1]})
                                        if "13" in var_name:
                                            self.deduction13.update({str(value[0]): value[1]})
                                        if "14" in var_name:
                                            self.deduction14.update({str(value[0]): value[1]})
                                        if "15" in var_name:
                                            self.deduction15.update({str(value[0]): value[1]})
                        else:
                            if re.search(r'(?!' + re.escape(value[0]) + r')', value1):

                                if value[0] in value_json['pay_period_start_date'] :
                                    vrx = np.array(value[1], np.int32)
                                    vrx = vrx.reshape((-1, 1, 2))
                                    img = cv2.polylines(img.copy(), [vrx], True, (0, 255, 255), 1)

                                    self.pay_start_date.update({str(value[0]): value[1]})

                                elif value[0] in value_json['pay_period_end_date']  :
                                    vrx = np.array(value[1], np.int32)
                                    vrx = vrx.reshape((-1, 1, 2))
                                    img = cv2.polylines(img.copy(), [vrx], True, (0, 255, 255), 1)

                                    self.pay_end_date.update({str(value[0]): value[1]})


                                elif value[0] in value_json['pay_date'] :
                                    vrx = np.array(value[1], np.int32)
                                    vrx = vrx.reshape((-1, 1, 2))
                                    img = cv2.polylines(img.copy(), [vrx], True, (0, 255, 255), 1)
                                    # #print(key,value)
                                    self.pay_date.update({str(value[0]): value[1]})


                                elif value[0] in value_json['employee_address']:
                                    vrx = np.array(value[1], np.int32)
                                    vrx = vrx.reshape((-1, 1, 2))
                                    img = cv2.polylines(img.copy(), [vrx], True, (255, 255, 0), 1)
                                    self.employee_address.update({str(value[0]): value[1]})


                                elif value[0] in value_json['employer_address'] :
                                    vrx = np.array(value[1], np.int32)
                                    vrx = vrx.reshape((-1, 1, 2))
                                    img = cv2.polylines(img.copy(), [vrx], True, (255, 255, 0), 1)
                                    self.emp_address.update({str(value[0]): value[1]})


                                elif value[0] in value_json['employee_name']:
                                # print("in else",value[1])
                                    vrx = np.array(value[1], np.int32)
                                    vrx = vrx.reshape((-1, 1, 2))
                                    img = cv2.polylines(img.copy(), [vrx], True, (0, 255, 255), 1)
                                    self.employee_name.update({str(value[0]): value[1]})


                                elif value[0] in value_json['employer_name']:
                                        vrx = np.array(value[1], np.int32)
                                        vrx = vrx.reshape((-1, 1, 2))
                                        img = cv2.polylines(img.copy(), [vrx], True, (0, 255, 255), 1)
                                        self.emp_name.update({str(value[0]): value[1]})
                                else:
                                    vrx = np.array(value[1], np.int32)
                                    vrx = vrx.reshape((-1, 1, 2))
                                    img = cv2.polylines(img, [vrx], True, (0, 255, 0), 1)
                                    self.dict.update({str(value[0]): value[1]})
        dt = datetime.datetime.now()
        date_val = dt.strftime("%Y%j%H%M%S") + str(dt.microsecond)
        cv2.imwrite("../images/processed/" + date_val + ".jpg", img)
        self.pay_Val.put((self.emp_name, self.employee_name, self.emp_address, self.employee_address, self.regular1, self.regular2, self.regular3, self.regular4,self.regular5, self.regular6, self.regular7, self.regular8, self.regular9, self.regular10,self.tax1, self.tax2, self.tax3, self.tax4, self.tax5, self.tax6, self.tax7, self.tax8,self.tax9, self.tax10, self.deduction1, self.deduction2, self.deduction3, self.deduction4,self.deduction5, self.deduction6, self.deduction7, self.deduction8, self.deduction9,self.deduction10,self.deduction11,self.deduction12,self.deduction13,self.deduction14,self.deduction15, self.pay_start_date, self.pay_end_date, self.pay_date, self.dict,"../images/processed/" + date_val + ".jpg",value_json))

    def get_text(self,path):
        try:

            text = []
            with io.open(path, 'rb') as image_file:
                content = image_file.read()

            image = vision.types.Image(content=content)

            response = self.client.document_text_detection(image=image)
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
                        if str("NEW LINE").lower() in str(test).lower():
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
                            #print(u'Word text: {} (confidence: {})\n'.format(word_text1, word1.confidence))

                        self.conf_keys.append(word_text1)
                        self.conf_values.append(word1.confidence)
            self.conf_result = zip(self.conf_keys, self.conf_values)
            actual_text = " ".join(map(str, text))
            self.description=response.text_annotations[0]
            texts=response.text_annotations
            for text in response.text_annotations[1:]:

                #print(text.description)
                vertices = [(vertex.x, vertex.y)
                            for vertex in text.bounding_poly.vertices]
                #print(vertices)
                self.keys.append(text.description)
                self.values.append(vertices)
            self.result = zip(self.keys, self.values)
            return actual_text,self.description,self.result,self.conf_keys,self.conf_values,texts

        except Exception as E:
            print(E)

    def get_license_location(self,value_json,path):
        try:
            img=Image.open(path)
            img=np.array(img.copy())
            _,filename= os.path.split(path)
            for key, value in enumerate(self.result):
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
                        if re.search(r'\b(=?' + re.escape(value[0].lower()) + r')\b', value1.lower()):

                            if value[0] in value_json['date_val']:

                                vrx = np.array(value[1], np.int32)
                                vrx = vrx.reshape((-1, 1, 2))
                                img = cv2.polylines(img.copy(), [vrx], True, (0, 255, 255), 1)
                                self.dict.update({value[0]: value[1]})

                            if value[0].lower() in value_json['address'].lower():
                                vrx = np.array(value[1], np.int32)
                                vrx = vrx.reshape((-1, 1, 2))
                                img = cv2.polylines(img.copy(), [vrx], True, (255, 255, 0), 1)
                                self.address_val.update({value[0]: value[1]})

                            if any(char in value_json['license_id'].lower() for char in value[0].lower()):
                                vrx = np.array(value[1], np.int32)
                                vrx = vrx.reshape((-1, 1, 2))
                                img = cv2.polylines(img.copy(), [vrx], True, (0, 0, 255), 1)
                                self.licence_id.update({value[0]: value[1]})

                            if any(char in value_json['first_name'].lower() for char in value[0].lower()):
                                vrx = np.array(value[1], np.int32)
                                vrx = vrx.reshape((-1, 1, 2))
                                img = cv2.polylines(img, [vrx], True, (0, 255, 0), 1)
                                self.dict.update({value[0]: value[1]})

                            if any(char in value_json['last_name'].lower() for char in value[0].lower()):
                                vrx = np.array(value[1], np.int32)
                                vrx = vrx.reshape((-1, 1, 2))
                                img = cv2.polylines(img, [vrx], True, (0, 255, 0), 1)
                                self.dict.update({value[0]: value[1]})

                            if any(char in value_json['middle_name'].lower() for char in value[0].lower()):
                                vrx = np.array(value[1], np.int32)
                                vrx = vrx.reshape((-1, 1, 2))
                                img = cv2.polylines(img, [vrx], True, (0, 255, 0), 1)
                                self.dict.update({value[0]: value[1]})
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

    def ssn_get_location(self,value_json,image):
        img = cv2.imread(image)
        _, filename = os.path.split(image)
        for key, value in enumerate(self.result):
            #print(value[0], value[1])
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
                            img = cv2.polylines(img.copy(), [vrx], True, (255, 0, 0), 2)
                            self.ssn.update({value[0]: value[1]})
                        elif value[0] in value_json['ssn_date']:
                            vrx = np.array(value[1], np.int32)
                            vrx = vrx.reshape((-1, 1, 2))
                            img = cv2.polylines(img.copy(), [vrx], True, (255, 0, 0), 2)
                            self.date.update({value[0]: value[1]})
                        else:
                            vrx = np.array(value[1], np.int32)
                            vrx = vrx.reshape((-1, 1, 2))
                            img = cv2.polylines(img.copy(), [vrx], True, (255, 0, 0), 2)
                            self.name.update({value[0]: value[1]})
        dt = datetime.datetime.now()
        date_val = dt.strftime("%Y%j%H%M%S") + str(dt.microsecond)
        cv2.imwrite("../images/processed/" + date_val + ".jpg", img)
        return self.ssn,self.name,self.date,"../images/processed/" + date_val + ".jpg"
    # def paystub_get_location(self,data,image):
    #     value_data,value_json={},{}
    #     for i in range(len(data['fields'])):
    #         if data['fields'][i]['field_value_original']!='':
    #             if 'regular' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['alias']] = {"field_value_original": data['fields'][i]['field_value_original'], "alias": "regular"}
    #             elif 'tax' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['alias']] = {
    #                     "field_value_original": data['fields'][i]['field_value_original'], "alias": "tax"}
    #
    #                 # value_data[data['fields'][i]['alias']] = data['fields'][i]['field_value_original']
    #                 # value_data[data['fields'][i]['alias'] + "_ytd"] = data['fields'][i]['optional_value']
    #             elif 'other' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['alias']] = {
    #                     "field_value_original": data['fields'][i]['field_value_original'], "alias": "deduction"}
    #             elif 'gross_pay' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['name']] = data['fields'][i]['field_value_original']
    #                 value_data[data['fields'][i]['name'] + "_ytd"] = data['fields'][i]['optional_value']
    #             elif 'net_pay' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['name'] ] = data['fields'][i]['field_value_original']
    #                 value_data[data['fields'][i]['name'] + "_ytd"] = data['fields'][i]['optional_value']
    #             elif 'employee_name' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['name']] = data['fields'][i]['field_value_original']
    #             elif 'employee_number' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['name']] = data['fields'][i]['field_value_original']
    #             elif 'employer_address' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['name']] = data['fields'][i]['field_value_original']
    #             elif 'employer/company_code' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['name']] = data['fields'][i]['field_value_original']
    #             elif 'pay_period_end_date' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['name']] = data['fields'][i]['field_value_original']
    #             elif 'pay_period_start_date' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['name']] = data['fields'][i]['field_value_original']
    #             elif 'pay_date' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['name']] = data['fields'][i]['field_value_original']
    #             elif 'state_unemployment' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['name']] = data['fields'][i]['field_value_original']
    #             elif 'position' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['name']] = data['fields'][i]['field_value_original']
    #             elif 'mi' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['name']] = data['fields'][i]['field_value_original']
    #             elif 'employer_name' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['name']] = data['fields'][i]['field_value_original']
    #             elif 'employer_city' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['name']] = data['fields'][i]['field_value_original']
    #             elif 'employee_city' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['name']] = data['fields'][i]['field_value_original']
    #             elif 'employer_state' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['name']] = data['fields'][i]['field_value_original']
    #             elif 'employee_state' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['name']] = data['fields'][i]['field_value_original']
    #             elif 'employment_start_date' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['name']] = data['fields'][i]['field_value_original']
    #             elif 'employee_address' in data['fields'][i]['name']:
    #                 value_data[data['fields'][i]['name']] = data['fields'][i]['field_value_original']
    #         # elif 'pay_frequency' in data['fields'][i]['name']:
    #     # for key, value in value_data.items():
    #     #     if "field_value_original" in value_data[key]:
    #     #         if value['field_value_original'] != "":
    #     #             value_json.update({key: value})
    #     #     else:
    #     #         value_json.update({key:value})
    #     # value_json = {key: value for key, value in value_data.items() if value != ""}
    #     thread=threading.Thread(target=self.paystub_value,args=(value_data,image,))
    #     thread.start()
    #     (self.emp_name, self.employee_name, self.emp_address, self.employee_address, self.regular1, self.regular2,
    #      self.regular3, self.regular4, self.regular5, self.regular6, self.regular7, self.regular8, self.regular9,
    #      self.regular10, self.tax1, self.tax2, self.tax3, self.tax4, self.tax5, self.tax6, self.tax7, self.tax8,
    #      self.tax9, self.tax10, self.deduction1, self.deduction2, self.deduction3, self.deduction4, self.deduction5,
    #      self.deduction6, self.deduction7, self.deduction8, self.deduction9, self.deduction10,self.deduction11,self.deduction12,self.deduction13,self.deduction14,self.deduction15, self.pay_start_date,
    #      self.pay_end_date, self.pay_date, self.dict,path,value_json)=self.pay_Val.get()
    #     return self.emp_name, self.employee_name, self.emp_address, self.employee_address, self.regular1, self.regular2, self.regular3, self.regular4,self.regular5, self.regular6, self.regular7, self.regular8, self.regular9, self.regular10,self.tax1, self.tax2, self.tax3, self.tax4, self.tax5, self.tax6, self.tax7, self.tax8,self.tax9, self.tax10, self.deduction1, self.deduction2, self.deduction3, self.deduction4,self.deduction5, self.deduction6, self.deduction7, self.deduction8, self.deduction9,self.deduction10,self.deduction11,self.deduction12,self.deduction13,self.deduction14,self.deduction15, self.pay_start_date, self.pay_end_date, self.pay_date, self.dict,path,value_json




