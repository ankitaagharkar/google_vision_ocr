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
                    'net pay',
                    'gross pay'
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
                        'net pay':'Net Pay',
                        'gross pay':'Gross Pay'
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
        s = s.replace(',','')
        s = s.replace('$','')
        try:
            int(s)
            return False
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
        y_axis = []
        left_values = []
        desc = self.description.description
        for key, values in enumerate(self.result):
            init_flag = False
            start_y = values[1][0][1] #y value of first vertex
            start_x = values[1][0][0] #x value of first vertex
            end_y = values[1][3][1] #y value of last vertex
            end_x = values[1][3][0] #x value of last vertex
            try:
                min_y_diff = min(enumerate(y_axis), key=lambda x: abs(x[1]-start_y))
            except:
                init_flag = True
            
            #if a new line is found, i.e difference in y-axis is greater than certain value
            if init_flag or abs(min_y_diff[1] - start_y) > 12:

                #check if new word is a float, if yes line cannot start with a float value
                if not self.is_float(values[0]):
                    new_line = []
                    new_line.append(start_x) #x value of first vertex which becomes start_x of line
                    new_line.append(start_y) #start_y of line
                    new_line.append([[values[0],values[1]]]) #word and its vertices 
                    new_line.append(values[1][1][0]) #x value of second vertex which becomes end_x of line
                    new_line.append(values[1][1][1]) #y value of second vertex which becomes end_y of line
                    y_axis.append(new_line[4])
                    line_list.append(new_line)
                else:
                    left_values.append([values[0],values[1]]) #add float value to left-out values, read it later
            else:
                #write code to enter value in the line found
                line = line_list[min_y_diff[0]]
                flag = False
                for k,val in enumerate(line[2]):
                    d = val[0]+' '+values[0]
                    #search if new word is a part of a complete word as given by Google
                    #if yes update word and its co-ordinates
                    if d in desc:
                        #check if word is really close to be considered as one word
                        #using this to ensure incorrect word by Google API doesn't get in it
                        if abs(val[1][1][0] - values[1][0][0]) < 45: 
                            val[0] = d
                            new_vertex = [val[1][0],values[1][1],values[1][2],val[1][3]]
                            val[1] = new_vertex
                            #update values in line list
                            line_list[min_y_diff[0]][2][k] = val
                            #if line_list[min_y_diff[0]][3] < values[1][1][0]:
                            line_list[min_y_diff[0]][3] = values[1][1][0]
                            #if line_list[min_y_diff[0]][4] < values[1][1][1]:
                            line_list[min_y_diff[0]][4] = values[1][1][1]
                            y_axis[min_y_diff[0]] = values[1][1][1]
                            flag = True
                            break
                        else:
                            #add this word as a new word in current line
                            flag = False
                            break
                #if a new word is found on same line and it is not a part of complete word
                if not flag:
                    #search proper position for this new word in line
                    prior_position = False
                    for k, val in enumerate(line[2]):
                        #if new word isn't at the end of line, get its position in 'k'
                        if val[1][0][0] > values[1][0][0]:
                            prior_position = True
                            break
                    #if word is at the end of line, update list
                    if not prior_position:
                        line_list[min_y_diff[0]][2].append([values[0],values[1]])
                    #else insert word at its proper position
                    else:
                        #check if word to be added is going at first position
                        if k==0:
                            #if value is a float, donot add it at first position, instead try it later
                            if self.is_float(values[0]):
                                left_values.append([values[0],values[1]]) #add float value to left-out values, read it later
                                continue #continue with next iteration
                            else:
                                #if word is inserted at the start of line, update start co-ordinates of line
                                line_list[min_y_diff[0]][0] = values[1][0][0]
                                line_list[min_y_diff[0]][1] = values[1][0][1]
                        line_list[min_y_diff[0]][2].insert(k,[values[0],values[1]])
                    if line_list[min_y_diff[0]][3] < values[1][1][0]:
                        line_list[min_y_diff[0]][3] = values[1][1][0]
                    if line_list[min_y_diff[0]][4] < values[1][1][1]:
                        line_list[min_y_diff[0]][4] = values[1][1][1]
                        y_axis[min_y_diff[0]] = values[1][1][1]
        lines = sorted(line_list, key=self.getKey)
        #for all the left out values finds its appropriate line using closest approximate method
        for key, values in enumerate(left_values):
            min_y_diff = min(enumerate(lines), key=lambda x: abs(x[1][1]-values[1][0][1]))
            word_position = 0
            min_y = 9999
            line_number = 0
            is_last = False
            #get closest words in three lines i.e. min_y line, its previous line and next line
            #after you get words from all three lines, find best suitable place for this word
            for l_index in range(min_y_diff[0]-1,min_y_diff[0]+2):
                try:
                    line = lines[l_index]
                    for w_index, word in enumerate(line[2]):
                        #if exit x value of word is less than entry x value of input word
                        if word[1][1][0] < values[1][0][0]:
                            if not w_index == len(line[2])-1:
                                continue
                            else:
                                if abs(word[1][1][1] - values[1][0][1]) < min_y:
                                    min_y = abs(word[1][1][1] - values[1][0][1]) 
                                    line_number = l_index
                                    word_position = w_index+1
                                    is_last = True
                        else:
                            if not w_index==0 and abs(word[1][1][1] - values[1][0][1]) < min_y:
                                min_y = abs(word[1][1][1] - values[1][0][1]) 
                                line_number = l_index
                                word_position = w_index
                                is_last = False
                            break
                except Exception as e: 
                    print(e)
            try:
                lines[line_number][2].insert(word_position,[values[0],values[1]])
                if is_last:
                    if lines[line_number][3] < values[1][1][0]:
                        lines[line_number][3] = values[1][1][0]
                    if lines[line_number][4] < values[1][1][1]:
                        lines[line_number][4] = values[1][1][1]
            except Exception as e: 
                print(e)
        #block code is not yet implemented
        #if implemented it will give even more better results on any type of document
        return lines

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
                            'year to date','ytd','total to date',
                            'earnings','amount']
        blocks = {}
        current = []
        ytd = []
        current_flag = False
        for line in lines:
            prev_word = ''
            for w_index,word in enumerate(line[2]):
                x = difflib.get_close_matches(word[0].lower(),pay_header_flags,cutoff=0.75)
                if x:
                    if x[0] in ['current','this period','current period','current month','is period','this']:
                        #append mean value of x axis as a start of new block, i.e. current column
                        current_flag = True
                        current_mean = (word[1][0][0] + word[1][1][0]) / 2
                        try:
                            current_end = line[2][w_index+1][1][0][0]
                        except:
                            current_end = 0
                    elif x[0] in ['year to date','ytd','total to date']:
                        #append mean value of YTD column
                        if current_flag:
                            current_flag = False
                            current.append([current_mean,current_end])
                            ytd_mean = (word[1][0][0] + word[1][1][0]) / 2
                            try:
                                ytd_end = line[2][w_index+1][1][0][0]
                            except:
                                ytd_end = 0
                            ytd.append([ytd_mean,ytd_end])
                    elif x[0] in ['earnings','amount']:
                        #if earnings or amount comes under current or ytd (as per Case II)
                        #search for closest column of current/ytd and change its mean as of earning's mean
                        try:
                            earnings_start = word[1][0][0] #x-axis value of first co-ordinate
                            max_current = max(x for x in current if int(x) <= earnings_start)
                            max_ytd = max(x for x in ytd if int(x) <= earnings_start)
                        except:
                            pass
                elif current:
                    if self.is_float(word[0]):
                        word_end = word[1][1][0]
                        pos_found = False                        
                        for k, cur in enumerate(current):
                            if word_end > cur[0] and word_end < cur[1]:
                                print(prev_word,'current',word[0])
                                pos_found = True
                                blocks = self.create_blocks(blocks,k,prev_word,'current',word[0])
                                break
                        for k, yt in enumerate(ytd):
                            if not pos_found and word_end > yt[0] and word_end < yt[1]:
                                print(prev_word,'ytd',word[0])
                                blocks = self.create_blocks(blocks,k,prev_word,'ytd',word[0])
                                break
                            elif not pos_found and word_end > yt[0] and yt[1] == 0:
                                try:
                                    if word_end < ytd[k+1][0]:
                                        print(prev_word,'ytd',word[0])
                                        blocks = self.create_blocks(blocks,k,prev_word,'ytd',word[0])
                                        break
                                except:
                                    print(prev_word,'ytd',word[0])
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
        response = client.text_detection(image=image)
        #else:
        #response = client.document_text_detection(image=image)
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
x.get_text(r"C:\Users\ankitaa\Desktop\idocufy\Images\Paystub\1.jpg")

lines = x.rectify_data()

for line in lines:
    print(line)

blocks = x.get_payslip_amounts(lines)
#lines = sorted(lines, key=getKey)

