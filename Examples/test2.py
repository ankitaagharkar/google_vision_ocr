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
        self.pay_names = ['regular','salary','bonus','commission',
                    'holiday','overtime','hol','wkd ot',
                    'federal income','federal','federal withholding','fed inc','fit',
                    'ssi withholding','social','ssi','soc sec','social security',
                    'state income','state','state withholding','state inc','sit',
                    'unemployment','sui','ui-ee',
                    'fli-ee',
                    'workforce','development','workforce development','work dev','uiwf-ee','wf-ee',
                    'disability','di','sdi','sdi-ee',
                    'net',
                    'gross'
                    ]
        self.pay_types = {'regular':'Regular wages',
                        'holiday':'Overtime Wages',
                        'overtime':'Overtime Wages',
                        'hol':'Overtime Wages',
                        'wkd ot':'Overtime Wages',
                        'salary':'Salary Wages',
                        'bonus':'Commission wages',
                        'commission':'Commission Wages',
                        'federal income':'Federal Income Tax',
                        'federal':'Federal Income tax',
                        'federal withholding':'Federal Income tax',
                        'fed inc':'Federal Income tax',
                        'fit':'Federal Income tax',
                        'ssi withholding':'SSI Withholding',
                        'social':'SSI Withholding',
                        'ssi':'SSI Withholding',
                        'soc sec':'SSI Withholding',
                        'social security':'SSI Withholding',
                        'state income':'State Income Tax',
                        'state':'State Income Tax',
                        'state withholding':'State Income Tax',
                        'state inc':'State Income Tax',
                        'sit':'State Income Tax',
                        'unemployment':'State Unemployment (UI) Withholding',
                        'sui':'State Unemployment (UI) Withholding',
                        'ui-ee':'State Unemployment (UI) Withholding',
                        'fli-ee':'Family Leave (FL) Withholding',
                        'workforce':'Workforce Development',
                        'development':'Workforce Development',
                        'workforce development':'Workforce Development',
                        'work dev':'Workforce Development',
                        'uiwf-ee':'Workforce Development',
                        'wf-ee':'Workforce Development',
                        'disability':'Disability Insurance (DI) withholding',
                        'di':'Disability Insurance (DI) withholding',
                        'sdi':'Disability Insurance (DI) withholding',
                        'sdi-ee':'Disability Insurance (DI) withholding',
                        'net':'Net Pay',
                        'gross':'Gross Pay'
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
        left_values = []
        line_height = 9
        space_width = 26
        desc = self.description.description
        prev_y_start = -20
        prev_y_end = -20
        #sort all words as per y-axis of its first element
        res = sorted(self.result, key=lambda x: x[1][0][1])
        for key, values in enumerate(res):
            init_flag = False
            merge_word = False
            start_y = values[1][0][1] #y value of first vertex
            start_x = values[1][0][0] #x value of first vertex
            end_y = values[1][1][1] #y value of second vertex
            if abs(start_y - prev_y_start) < line_height or abs(start_y - prev_y_end) < line_height:
                #assume it belongs to prev line in line list
                line = line_list[-1]
                for k,word in enumerate(line):
                    if start_x < word[1][0][0]:
                        if k==0:
                            prev_y_start = start_y
                        break
                    if k == len(line)-1:
                        prev_y_end = end_y
                        k += 1
                try:
                    check_word = line[k]
                    if True:
                        d = values[0]+' '+check_word[0]
                        d1 = values[0]+check_word[0]
                        if abs(values[1][1][0] - check_word[1][0][0]) < space_width:
                            if d in desc:
                                line_list[-1][k][0] = d
                                line_list[-1][k][1] = [values[1][0],check_word[1][1],check_word[1][2],values[1][3]]
                                values = (d,line_list[-1][k][1])
                                merge_word = True
                            elif d1 in desc:
                                line_list[-1][k][0] = d1
                                line_list[-1][k][1] = [values[1][0],check_word[1][1],check_word[1][2],values[1][3]]
                                values = (d1,line_list[-1][k][1])
                                merge_word = True
                except:
                    pass
                try:
                    check_word = line[k-1]
                    if True:
                        d = check_word[0]+' '+values[0]
                        d1 = check_word[0]+values[0]
                        if abs(values[1][0][0] - check_word[1][1][0]) < space_width:
                            if d in desc:
                                line_list[-1][k-1][0] = d
                                line_list[-1][k-1][1] = [check_word[1][0],values[1][1],values[1][2],check_word[1][3]]
                                if merge_word:
                                    line_list[-1].pop(k)
                                continue
                            elif d1 in desc:
                                line_list[-1][k-1][0] = d1
                                line_list[-1][k-1][1] = [check_word[1][0],values[1][1],values[1][2],check_word[1][3]]
                                if merge_word:
                                    line_list[-1].pop(k)
                                continue
                except:
                    pass
                if not merge_word:
                    line_list[-1].insert(k,[values[0],values[1]])
            else:
                #word is on a new line
                new_line = []
                prev_y_start = start_y
                prev_y_end = end_y
                new_line.append([values[0],values[1]])
                line_list.append(new_line)
        return line_list

    def create_blocks(self,blocks,block_id,word,value_type,value):
        original_word = word
        if not word in blocks:
            word = word.lower().replace('taxes','')
            word = word.replace('tax','')
            word = word.replace('pay','')
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
        pay_header_flags = ['current','this period','current month','current period','is period','this',
                            'year to date','ytd','total to date','y-t-d',
                            'earnings','amount']
        blocks = {}
        current = []
        ytd = []
        current_flag = False
        space_width = 45
        for line in lines:
            prev_word = ''
            for w_index,word in enumerate(line):
                x = difflib.get_close_matches(word[0].lower(),pay_header_flags,cutoff=0.80)
                if x:
                    
                    if x[0] in ['current','this period','current period','current month','is period','this']:
                        #append mean value of x axis as a start of new block, i.e. current column
                        current_flag = True
                        current_mean = (word[1][0][0] + word[1][1][0]) / 2
                        try:
                            current_end = line[w_index+1][1][0][0]
                        except:
                            current_end = 0
                    elif x[0] in ['year to date','ytd','total to date','y-t-d']:
                        #append mean value of YTD column
                        if current_flag:
                            current_flag = False
                            current.append([current_mean,current_end])
                            ytd_mean = (word[1][0][0] + word[1][1][0]) / 2
                            try:
                                ytd_end = line[w_index+1][1][0][0]
                            except:
                                ytd_end = 0
                            ytd.append([ytd_mean,ytd_end])
                    elif x[0] in ['earnings','amount']:
                        #if earnings or amount comes under current or ytd (as per Case II)
                        #search for closest column of current/ytd and change its mean as of earning's mean
                        mc_index = False
                        my_index = False
                        earnings_start = word[1][0][0] #x-axis value of first co-ordinate
                        try:
                            word_mean = (word[1][0][0] + word[1][1][0]) / 2
                            word_end = line[w_index+1][1][0][0]
                        except:
                            word_end = 0
                        
                        try:
                            max_current = max(x for x in current if int(x[0]) <= earnings_start)
                            mc_index = current.index(max_current)
                        except:
                           pass
                        
                        try:
                            max_ytd = max(x for x in ytd if int(x[0]) <= earnings_start)
                            my_index = current.index(max_ytd)
                        except:
                           pass
                        
                        #search where this current is closest
                        if mc_index and my_index:
                            #if current is smaller than ytd, that means word is closer to ytd
                            if current[mc_index][0] < ytd[my_index][0]:
                                ytd.insert(my_index,[word_mean,word_end])
                            else:
                                current.insert(mc_index,[word_mean,word_end])
                        elif mc_index:
                            #if it is closer to 'Current' column, update mean at mc_index with that of this word
                            current.insert(mc_index,[word_mean,word_end])
                        elif my_index:
                            #if it is closer to 'YTD' column, update mean at my_index with that of this word
                            ytd.insert(my_index,[word_mean,word_end])
                    
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
                        word_mean = (word[1][0][0] + word[1][1][0])/2
                        mean_diff_c = min(enumerate(current), key=lambda x:abs(x[1][0] - word_mean))
                        mean_diff_y = min(enumerate(ytd), key=lambda x:abs(x[1][0] - word_mean))
                        if abs(mean_diff_c[1][0] - word_mean) < space_width:
                            
                            current[mean_diff_c[0]] = [9999,9999]
                            ytd[mean_diff_c[0]] = [9999,9999]
                        if abs(mean_diff_y[1][0] - word_mean) < space_width:
                            current[mean_diff_y[0]] = [9999,9999]
                            ytd[mean_diff_y[0]] = [9999,9999]
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
blocks = x.get_payslip_amounts(lines)
#lines = sorted(lines, key=getKey)

