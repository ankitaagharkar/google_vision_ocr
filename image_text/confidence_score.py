import io
import re,json
from google.cloud import vision
from google.cloud import vision_v1p1beta1 as vision

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
        self.word,self.license_text,self.regex_value= '','',""
        with open('../config/filtering.json', 'r') as data:
            self.state_value = json.load(data)
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

                            elif value[0] in data['address']:
                                self.address_val.update({value[0]: value[1]})

                            elif any(char in data['license_id'] for char in value[0]):
                                self.license_id_dict.update({value[0]: value[1]})

                            else:
                                self.others.update({value[0]:value[1]})

            print("other",self.others)
            for key5, value5 in self.license_id_dict.items():
                self.license_confidence_score = self.license_confidence_score + value5
                self.val.append(value5)
            print(self.val)
            len_confidence_score=len(self.license_id_dict)
            print(text)
            text = text.replace(' AJ ', ' NJ ')
            state_regex = re.findall(
                r"\b((?=AL|AK|AS|AZ|AŽ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE"
                r"|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)[A-Z]{2}[, ])([A-Za-z]+)?\d+",
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
    def paystub_confidence(self,data):
        try:
            for key, value in enumerate(self.result):
                for key1, value1 in data.items():
                    if value[0] != '' and value1 != '':
                        if re.search(r'(?!' + re.escape(value[0]) + r')', value1):
                            self.paystub.update({value[0]: value[1]})
            for key4, value4 in self.paystub.items():
                self.paystub_confidence_score = self.paystub_confidence_score + value4
            paystub_length = len(self.paystub)
            self.paystub_score = int((self.paystub_confidence_score/paystub_length) * 100)
            return self.paystub_score
        except Exception as E:
            return self.paystub_score

