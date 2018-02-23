import io,sys
import re,json
from google.cloud import vision
from google.cloud import vision_v1p1beta1 as vision
sys.path.insert(0, '../image_text')
import pay_other_confidence
class text_score:
    def __init__(self):
        self.keys,self.values=[],[]
        self.dict,self.address_val, self.others={},{},{}
        self.address_confidence = 0.0
        self.ssn_confidence_score=0.0
        self.date_confidence_score = 0.0
        self.license_confidence_score=0.0
        self.date_score, self.address_score, self.other_score,self.license_score, self.ssn_score,self.paystub_score=0,0,0,0,0,0
        self.full_address = ''
        self.result={}
        self.val=[]
        self.paystub={}
        self.license_id_dict={}
        self.paystub_confidence_score = 0.0
        self.other_confidence=0.0

        self.emp_name, self.employee_name = {}, {}
        self.emp_address, self.employee_address = {}, {}
        self.regular1, self.regular2, self.regular3, self.regular4, self.regular5, self.regular6, self.regular7, self.regular8, self.regular9, self.regular10 = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
        self.tax1, self.tax2, self.tax3, self.tax4, self.tax5, self.tax6, self.tax7, self.tax8, self.tax9, self.tax10 = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
        self.deduction1, self.deduction2, self.deduction3, self.deduction4, self.deduction5, self.deduction6, self.deduction7, self.deduction8, self.deduction9, self.deduction10,self.deduction11,self.deduction12,self.deduction13,self.deduction14,self.deduction15={},{},{},{},{},{},{},{},{},{},{},{},{},{},{}
        self.pay_start_date, self.pay_end_date, self.pay_date = {}, {}, {}
        self.word,self.license_text,self.regex_value= '','',""
        with open('../config/filtering.json', 'r') as data:
            self.state_value = json.load(data)
        self.pay_val=pay_other_confidence.Confidence_Calculation()
        self.client = vision.ImageAnnotatorClient()
    def get_confidence_score(self,path):
        with io.open(path, 'rb') as image_file:
            content = image_file.read()
        image = vision.types.Image(content=content)
        response = self.client.document_text_detection(image=image)
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                block_words = []
                for paragraph in block.paragraphs:
                    block_words.extend(paragraph.words)
                block_text = ''
                block_symbols = []
                for word in block_words:
                    block_symbols.extend(word.symbols)
                    word_text=''
                    for symbol in word.symbols:
                        word_text = word_text + symbol.text

                    # ##print(u'Word text: {} (confidence: {})\n'.format(
                    #     word_text, word.confidence))
                    self.keys.append(word_text)
                    self.values.append(word.confidence)
        self.result = zip(self.keys, self.values)
    def license_confidence(self,data,text):
        try:
            for key, value in enumerate(self.result):
                for key1, value1 in data.items():
                    if value[0] != '' and value1 != '':
                        # if value[0] in value1:
                        if re.search(r'(?!' + re.escape(value[0]) + r')', value1):
                            if value[0] in data['date_val']:
                                    self.dict.update({value[0]: value[1]})

                            elif any(char in data['first_name'] for char in value[0]):
                                self.others.update({value[0]: value[1]})

                            elif any(char in data['last_name'] for char in value[0]):
                                self.others.update({value[0]: value[1]})

                            elif any(char in data['middle_name'] for char in value[0]):
                                self.others.update({value[0]: value[1]})

                            elif any(char in data['address'] for char in value[0]):
                                self.address_val.update({value[0]: value[1]})

                            elif any(char in data['license_id'] for char in value[0]):
                                self.license_id_dict.update({value[0]: value[1]})

                            else:
                                self.others.update({value[0]:value[1]})
            for key5, value5 in self.license_id_dict.items():
                self.license_confidence_score = self.license_confidence_score + value5
                self.val.append(value5)
            print(self.val)
            len_confidence_score=len(self.license_id_dict)
            text = text.replace(' AJ ', ' NJ ')
            state_regex = re.findall(
                r"\b((?=AL|AK|AS|AZ|AŽ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE"
                r"|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|and|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)[A-Z]{2}[, ])([A-Za-z]+)?\d+",
                text)
            print(len(self.state_value['data']))
            if state_regex != []:
                for i in range(len(self.state_value['data'])):
                    if self.state_value['data'][i]['state'] in state_regex[0][0]:
                        self.regex_value = self.state_value['data'][i]['license_id']
                        print("regex_state_value", self.state_value['data'][i]['state'], self.regex_value)
                print("state regex", self.regex_value)
            licence_id = re.findall(self.regex_value,text)
            if licence_id!=[]:
                self.license_score = int((self.license_confidence_score/len_confidence_score) * 100)
                if self.license_score>100:
                    self.license_score=85
            else:
                self.license_score=(min(self.val)*100)

            if len(self.address_val) > 1:
                for key3, value3 in self.address_val.items():
                    self.address_confidence = self.address_confidence + value3
                self.address_score = int((self.address_confidence / len(self.address_val)) * 100)
                # if self.address_score > 100:
                #     self.address_score = 97
            for key2, value2 in self.dict.items():
                self.date_confidence_score = self.date_confidence_score + value2
            for key4, value4 in self.others.items():
                self.other_confidence = self.other_confidence + value4
            ##print("total score",self.date_confidence_score,self.other_confidence)
            dict_length=len(self.dict)
            other_length=len(self.others)
            ##print("length",dict_length,other_length)
            if other_length>1:
                self.date_score = int((self.date_confidence_score / dict_length) * 100)
                self.other_score = int((self.other_confidence / other_length) * 100)
            return self.dict,self.date_score,self.address_score,self.license_score,self.other_score
        except Exception as e:
            return self.dict, self.date_score, self.address_score, self.license_score, self.other_score
    def ssn_confidence(self,data):
        try:
            for key, value in enumerate(self.result):
                for key1, value1 in data.items():
                    if value[0] != '' and value1 != '':
                        if re.search(r'\b(=?' + re.escape(value[0]) + r')\b', value1):
                            if value[0] in data['ssn_number']:
                                self.ssn_confidence_score = value[1]
            self.ssn_score = int((self.ssn_confidence_score * 100))
            return self.ssn_score
        except Exception as E:
            return self.ssn_score
    def paystub_confidence(self,data_val):
        data={}
        try:
            a = 0
            b = 0
            c = 0

            for key, value in data_val.items():
                if "field_value_original" in data_val[key]:
                    if value['field_value_original'] != "":
                        data.update({key:value})
                else:
                        data.update({key: value})

            # print("in None Data",data)
            for key, value in enumerate(self.result):
                a = a + 1
                b = b + 1
                c = c + 1
                for key1, value1 in data.items():
                    if key1 != '' and value1 != '':
                        if value[0] != '':
                            if "field_value_original" in data[key1]:
                                if value[0] in value1['field_value_original']:
                                    if "regular" in value1['alias']:

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
                                    if value[0] in data['pay_period_end_date']:
                                        self.pay_end_date.update({str(value[0]): value[1]})

                                    elif value[0] in data['pay_period_start_date']:
                                        self.pay_start_date.update({str(value[0]): value[1]})

                                    elif value[0] in data['pay_date']:
                                        self.pay_date.update({str(value[0]): value[1]})

                                    elif value[0] in data['employee_address'] :
                                        self.employee_address.update({str(value[0]): value[1]})

                                    elif value[0] in data['employer_address']:
                                        self.emp_address.update({str(value[0]): value[1]})

                                    elif value[0] in data['employee_name'] :
                                        self.employee_name.update({str(value[0]): value[1]})

                                    elif value[0] in data['employer_name']:

                                        self.emp_name.update({str(value[0]): value[1]})
                                    else:

                                        self.dict.update({str(value[0]): value[1]})

            regular1_scrore,regular2_scrore,regular3_scrore,regular4_scrore,regular5_scrore,regular6_scrore,regular7_scrore,\
            regular8_scrore,regular9_scrore,regular10_scrore,tax1_scrore,tax2_scrore,tax3_scrore,tax4_scrore,tax5_scrore,\
            tax6_scrore,tax7_scrore,tax8_scrore,tax9_scrore,tax10_scrore,deduction1_scrore,deduction2_scrore,deduction3_scrore,\
            deduction4_scrore,deduction5_scrore,deduction6_scrore,deduction7_scrore,deduction8_scrore,deduction9_scrore,deduction10,deduction11_scrore,deduction12_scrore,deduction13_scrore,deduction14_scrore,deduction15_scrore,\
            pay_end_date_scrore,pay_start_date_scrore,pay_date_scrore,employee_address_scrore,employee_name_scrore,\
            employer_address_scrore,employer_name_scrore,other_scrore = self.pay_val.all_confidence_scrore(self.regular1,
            self.regular2, self.regular3, self.regular4, self.regular5, self.regular6, self.regular7, self.regular8, self.regular9,
            self.regular10,self.tax1, self.tax2, self.tax3, self.tax4, self.tax5, self.tax6, self.tax7, self.tax8, self.tax9,
            self.tax10,self.deduction1, self.deduction2, self.deduction3,self.deduction4, self.deduction5, self.deduction6,
            self.deduction7, self.deduction8, self.deduction9, self.deduction10,self.deduction11,self.deduction12,self.deduction13,self.deduction14,self.deduction15,self.pay_start_date, self.pay_end_date,
            self.pay_date,self.employee_address,self.emp_address,self.employee_name,self.emp_name,self.dict)

            return regular1_scrore,regular2_scrore,regular3_scrore,regular4_scrore,regular5_scrore,regular6_scrore,regular7_scrore,\
            regular8_scrore,regular9_scrore,regular10_scrore,tax1_scrore,tax2_scrore,tax3_scrore,tax4_scrore,tax5_scrore,\
            tax6_scrore,tax7_scrore,tax8_scrore,tax9_scrore,tax10_scrore,deduction1_scrore,deduction2_scrore,deduction3_scrore,\
            deduction4_scrore,deduction5_scrore,deduction6_scrore,deduction7_scrore,deduction8_scrore,deduction9_scrore,deduction10,deduction11_scrore,deduction12_scrore,deduction13_scrore,deduction14_scrore,deduction15_scrore,\
            pay_end_date_scrore,pay_start_date_scrore,pay_date_scrore,employee_address_scrore,employee_name_scrore,\
            employer_address_scrore,employer_name_scrore,other_scrore

        except Exception as E:
            pass

