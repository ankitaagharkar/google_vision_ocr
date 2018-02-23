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
import sys
import difflib


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
        self.keys=[]
        self.values=[]
        self.description = []
        self.pay_names = ['regular','salary','bonus','commission','regular earn',
                    'holiday','overtime','hol','wkd ot','hol wkd ot',
                    'birthday','wellness','deferral bonus',
                    'sick','vacation','pers hol payout','uniform','uniform allowance',
                    'medicare','withholding',
                    'federal railroad',
                    'federal income','federal','federal withholding','fed inc','fit',
                    'ssi withholding','social','ssi','soc sec','social security',
                    'state withholding','state income','state','state inc','sit',
                    'unemployment','sui','ui-ee',
                    'susdi','suidi',
                    'fli-ee',
                    'workforce','development','workforce development','work dev','uiwf-ee','wf-ee',
                    'disability','di','sdi','sdi-ee',
                    'net','total net',
                    'gross','total gross'
                    ]
        self.pay_types = {'regular':'Earnings',
                        'regular earn':'Earnings',
                        'holiday':'Earnings',
                        'overtime':'Earnings',
                        'hol':'Earnings',
                        'wkd ot':'Earnings',
                        'salary':'Earnings',
                        'bonus':'Earnings',
                        'commission':'Earnings',
                        'hol wkd ot':'Earnings',
                        'birthday':'Earnings',
                        'wellness':'Earnings',
                        'deferral bonus':'Earnings',
                        'sick':'Earnings',
                        'vacation':'Earnings',
                        'pers hol payout':'Earnings',
                        'uniform':'Earnings',
                        'uniform allowance':'Earnings',
                        'medicare':'Deductions',
                        'withholding':'Deductions',
                        'federal railroad':'Deductions',
                        'federal income':'Deductions',
                        'federal':'Deductions',
                        'federal withholding':'Deductions',
                        'fed inc':'Deductions',
                        'fit':'Deductions',
                        'ssi withholding':'Deductions',
                        'social':'Deductions',
                        'ssi':'Deductions',
                        'soc sec':'Deductions',
                        'social security':'Deductions',
                        'state income':'Deductions',
                        'state':'Deductions',
                        'state withholding':'Deductions',
                        'state inc':'Deductions',
                        'sit':'Deductions',
                        'unemployment':'Deductions',
                        'sui':'Deductions',
                        'ui-ee':'Deductions',
                        'fli-ee':'Deductions',
                        'workforce':'Deductions',
                        'development':'Deductions',
                        'workforce development':'Deductions',
                        'work dev':'Deductions',
                        'uiwf-ee':'Deductions',
                        'wf-ee':'Deductions',
                        'disability':'Deductions',
                        'di':'Deductions',
                        'sdi':'Deductions',
                        'sdi-ee':'Deductions',
                        'susdi':'Deductions',
                        'suidi':'Deductions',
                        'net':'Net Pay',
                        'total net':'Net Pay',
                        'gross':'Gross Pay',
                        'total gross':'Gross Pay'
                    }

    def get_data_in_box(self,bounding):
        bounding_x1, bounding_y1 = bounding[0]
        bounding_x2, bounding_y2 = bounding[1]
        min_overlap = 20
        output_values = []
        for key, values in self.result.items():
            #Get bounding box by taking minimum of x and y, maximum of x and y.
            #this will solve problem of rotated texts as well.
            min_x = min(values, key = lambda x: x[0])[0]
            min_y = min(values, key = lambda x: x[1])[1]
            max_x = max(values, key = lambda x: x[0])[0]
            max_y = max(values, key = lambda x: x[1])[1]
            text_area = (max_x - min_x) * (max_y - min_y)
            x_overlap = max(0, min(bounding_x2, max_x) - max(bounding_x1, min_x))
            y_overlap = max(0, min(bounding_y2, max_y) - max(bounding_y1, min_y))
            overlapArea = x_overlap * y_overlap
            if overlapArea > 0 and (overlapArea/text_area)*100 >= min_overlap:
                output_values.append([(min_x,min_y),(max_x,max_y)])
        return output_values

    def is_float(self,s):
        try:
            if s[-3] == ',':
                k = s.rfind(",")
                s = s[:k] + "." + s[k+1:]
        except:
            pass
        s = s.replace(',','')
        s = s.replace('$','')
        s = s.replace('-','')
        s = s.replace('*','')
        s = s.replace(' ','.')
        s = s.replace('.','',s.count('.')-1)
        try:
            int(s)
            return False
        except:
            try:
                float(s)
                return True
            except ValueError:
                return False

    def is_float_or_int(self,s):
        try:
            if s[-3] == ',':
                k = s.rfind(",")
                s = s[:k] + "." + s[k+1:]
        except:
            pass
        s = s.replace(',','')
        s = s.replace('$','')
        s = s.replace('S','')
        s = s.replace('s','')
        s = s.replace('-','')
        s = s.replace('*','')
        s = s.replace(' ','.')
        s = s.replace('.','',s.count('.')-1)
        try:
            int(s)
            return True
        except:
            try:
                float(s)
                return True
            except ValueError:
                return False
    
    #to get key for sorting list with element at second position
    def getKey(self,item):
        return item[1]

    def rectify_data(self):
        line_list = []
        line_heights = []
        desc = self.description.description
        print(desc)
        #sort all words as per y-axis of its first element
        res = sorted(self.result, key=lambda x: x[1][0][1])
        #initialise all values for reading first word of document
        prev_y_start = -100
        prev_y_end = -100
        prev_y_mid = -100
        mod_ht = abs(res[0][1][0][1] - res[0][1][2][1])
        """
        Algorithm to bring all words in one line if it belongs to same line
        It works best on documents which are not slanted.
        1. For each word check if word falls on a new line, 
            i.e. its start-y is at a distance more than 3/4th of current line's start-y
            1A: If YES, start a new line with new start point, end point and 3/4th point
            1B: If NO, add the word to current line
        """
        for key, values in enumerate(res):
            print(values)
            if values[1][0][1] < prev_y_mid and abs(prev_y_start-values[1][0][1]) <= mod_ht:
                line_list[-1].append([values[0],values[1]])
            else:
                line_list.append([[values[0],values[1]]])
                prev_y_start = values[1][0][1]
                prev_y_end = values[1][2][1]
                prev_y_mid = int(((prev_y_start + prev_y_end) / 2 + prev_y_end)/2)
                line_heights.append(abs(prev_y_start-prev_y_end))
                mod_ht = max(line_heights,key=line_heights.count)
        """
        ALgorithm to sort each line as per its x-axis co-ordinate and also to merge words as per document
        1. For each line do steps 2 to 6:
        2. Sort the line w.r.to start-x of each word on line
        3. For each word on line do steps 4 to 5:
        4. Check if word falls under specific word such as $,|,USD
            4A: If YES, add the word to pop-elements list and continue to next word. (To discard them later)
        5. Check if new word is very close to the previous word,
            i.e. distance between two words is less than height of word
            5A: If YES, check if both word are float or both are characters
                5AA: If No, then add new word as a seperate word
                5AB: If YES, then check if combined word with or without spaces 
                    is present in description given by Google API, and merge the word accordingly.
                5AC: If word doesn't fall in any of above category, add it as a separate word.
            5B: If NO, add the new word a separate word.
        6. For each element in pop-elements list traversed in reverse:
            Remove the element from line. 
            (These words are either merged with some other words or are specific words to be discarded)
        """
        for k,line in enumerate(line_list):
            line_list[k] = sorted(line, key=lambda x: x[1][0][0])
            line = line_list[k]
            pop_elements = []
            word_end = 0
            word_height = 0
            for w_index,word in enumerate(line):
                if word[0] in ('$','|','USD','(',')'):
                    pop_elements.append(w_index)
                    continue
                #if new word is very close to the previous word
                if abs(word_end - word[1][0][0]) <= word_height:  
                    #check word without space
                    d = word_val + word[0]
                    d1 = word_val + ' ' + word[0]
                    if self.is_float_or_int(word_val):
                        if not self.is_float_or_int(word[0]) and word[0] not in (',','.','/','-'):
                            line_list[k][w_index] = word
                            word_height = abs(word[1][0][1] - word[1][2][1]) * 1.5
                            word_end = word[1][2][0]
                            word_val = word[0]
                            prev_index = w_index
                            check_word = word
                            continue
                        if word_val[-1] == '.' and len(word[0]) == 2:
                            word_height = 0
                    if d in desc:
                        line_list[k][prev_index][0] = d
                        line_list[k][prev_index][1] = [check_word[1][0],word[1][1],word[1][2],check_word[1][3]]
                        #remove current word from line list
                        pop_elements.append(w_index)
                        word_val = d
                        word_end = word[1][2][0]
                        continue
                    if d1 in desc:
                        line_list[k][prev_index][0] = d1
                        line_list[k][prev_index][1] = [check_word[1][0],word[1][1],word[1][2],check_word[1][3]]
                        #remove current word from line list
                        pop_elements.append(w_index)
                        word_val = d1
                        word_end = word[1][2][0]
                        continue
                    line_list[k][w_index] = word
                    word_height = abs(word[1][0][1] - word[1][2][1]) * 1.5
                    word_end = word[1][2][0]
                    word_val = word[0]
                    prev_index = w_index
                    check_word = word
                else:
                    """
                    if re.search('\b{!?S|s\d+}',word[0]):
                        print('heree')
                        word[0] = word[0].replace('S','')
                        word[0] = word[0].replace('s','')
                    """
                    line_list[k][w_index] = word
                    word_height = abs(word[1][0][1] - word[1][2][1]) * 1.5
                    word_end = word[1][2][0]
                    word_val = word[0]
                    prev_index = w_index
                    check_word = word
            for i in reversed(pop_elements):
                line_list[k].pop(i)
        return line_list

    def create_blocks(self,blocks,block_id,word,value_type,value):
        original_word = word
        if not word in blocks:
            word = word.lower().replace('taxes','')
            word = word.replace('tax','')
            word = word.replace('pay','')
            word = word.replace('.','')
            try:
                if word[-1] == ' ':
                    word = word[:-1]
            except:
                pass
            x = difflib.get_close_matches(word,self.pay_names,cutoff=0.75)
            if x:
                p_type = self.pay_types[x[0]]
            else:
                p_type = 'Other'
            blocks[original_word] = [p_type,None,None,block_id]
        if value_type == 'current':
            blocks[original_word][1] = value
        else:
            blocks[original_word][2] = value
        return blocks

    #function to get amounts from payslips, it will return a json with following values:
    #Wage/tax Type, Name as on payslip, Current Period, YTD
    """

    """
    def get_payslip_amounts(self,lines):
        block_start_flags = ['earnings','summary','current']
        block_end_flags = ['net pay','total']
        pay_header_flags = ['current','this period','current month','current period','is period','this','ratecurrent',
                            'year to date','ytd','total to date','y-t-d',
                            'earnings','amount']
        blocks = {}
        current = []
        ytd = []
        current_flag = False
        space_width = 45
        line_height = 40
        for line in lines:
            prev_word = ''
            for w_index,word in enumerate(line):
                x = difflib.get_close_matches(word[0].lower(),pay_header_flags,cutoff=0.80)
                if x:
                    if x[0] in ['current','this period','current period','current month','is period','this','ratecurrent']:
                        #append mean value of x axis as a start of new block, i.e. current column
                        current_flag = True
                        current_mean = (word[1][0][0] + word[1][1][0]) / 2
                        current_start = word[1][0][0]
                        try:
                            current_end = line[w_index+1][1][0][0]
                        except:
                            current_end = 0
                    elif x[0] in ['year to date','ytd','total to date','y-t-d']:
                        #append mean value of YTD column
                        if current_flag:
                            current_flag = False
                            current.append([current_mean,current_end,current_start])
                            ytd_mean = (word[1][0][0] + word[1][1][0]) / 2
                            ytd_start = word[1][0][0]
                            try:
                                ytd_end = line[w_index+1][1][0][0]
                            except:
                                ytd_end = 0
                            ytd.append([ytd_mean,ytd_end,ytd_start])
                    elif x[0] in ['earnings','amount']:
                        if not current_flag:
                            current_flag = True
                            current_mean = (word[1][0][0] + word[1][1][0]) / 2
                            current_start = word[1][0][0]
                            try:
                                current_end = line[w_index+1][1][0][0]
                            except:
                                current_end = 0
                        else:
                            current_flag = False
                            current.append([current_mean,current_end,current_start])
                            ytd_mean = (word[1][0][0] + word[1][1][0]) / 2
                            ytd_start = word[1][0][0]
                            try:
                                ytd_end = line[w_index+1][1][0][0]
                            except:
                                ytd_end = 0
                            ytd.append([ytd_mean,ytd_end,ytd_start])
                    print(x,current,ytd)
                elif current:
                    if self.is_float_or_int(word[0]):
                        word_end = word[1][1][0]
                        pos_found = False                        
                        for k, cur in enumerate(current):
                            if word_end > cur[0] and word_end < cur[1]:
                                blocks = self.create_blocks(blocks,k,prev_word,'current',word[0])
                                pos_found = True
                                break
                        if pos_found:
                            continue
                        for k, yt in enumerate(ytd):
                            if word_end > yt[0] and word_end < yt[1]:
                                blocks = self.create_blocks(blocks,k,prev_word,'ytd',word[0])
                                break
                            elif word_end > yt[0] and yt[1] == 0:
                                try:
                                    if word_end < ytd[k+1][0]:
                                        blocks = self.create_blocks(blocks,k,prev_word,'ytd',word[0])
                                        break
                                except:                                    
                                    blocks = self.create_blocks(blocks,k,prev_word,'ytd',word[0])
                                    break
                    else:
                        prev_word = word[0]
            current_flag = False
        print(blocks)

    def get_text(self,path):
        client = vision.ImageAnnotatorClient()
        with io.open(path, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        #if 'Pay Stub' in doc_type:
        #response = client.text_detection(image=image)
        #else:
        response = client.document_text_detection(image=image)
        #texts = response.full_text_annotation
        # response = client.text_detection(image=image)
        texts = response.text_annotations
        self.description = texts[0]
        for text in texts[1:]:

            self.text_val.append(text.description)
            vertices = [(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices]
            self.keys.append(text.description)
            self.values.append(vertices)
        self.result=zip(self.keys, self.values)
        data = " ".join(map(str, self.text_val))
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
                    if key1=='issue_date' or key1=='expiration_date' or key=='dob':
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
                # if key1 == 'issue_date' or key1 == 'expiration_date' or key == 'dob':
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
                if key != '' and value1 != '':
                    key = key.replace(',', '')
                    # key = key.replace(' ', '')
                    key = key.replace('No:', '')
                    key = key.replace('Issued:', '')
                    key = key.replace('Expiros::', '')
                    key = key.replace('Expires', '')
                    key = key.replace('-48','')
                    if re.search(r'\b(=?' +re.escape(key)+ r')\b', value1):
                        if key in value_json['date_val']:
                            print("in locations", value_json['date_val'])
                            vrx = np.array(value, np.int32)
                            vrx = vrx.reshape((-1, 1, 2))
                            img = cv2.polylines(img.copy(), [vrx], True, (0, 255, 255), 1)
                            # print(key,value)
                            print(key, value)
                            self.dict.update({key: value})
                        elif key in value_json['employer_name']:
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
"""
# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False
 
def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping
 
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
 
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False
 
        # draw a rectangle around the region of interest
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", image)

image = cv2.imread(sys.argv[1])
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
 
# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF
 
    # if the 'r' key is pressed, reset the selection region
    if key == ord("r"):
        image = clone.copy()
 
    # if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
        break

if len(refPt) == 2:
    x = get_all_location()
    x.get_text(sys.argv[1])
    res = x.get_data_in_box(refPt)
    if not res:
        print('No Text in this region')
    else:
        for val in res:
            cv2.rectangle(image,val[0],val[1],(0,255,255),2)
        cv2.imshow("image", image)
        cv2.waitKey(0)
"""


x = get_all_location()
x.get_text(sys.argv[1])

lines = x.rectify_data()
for line in lines:
    print(line)
blocks = x.get_payslip_amounts(lines)
#lines = sorted(lines, key=getKey)

