import datetime
import json
import operator
import re
import string
import sys
sys.path.insert(0, '../image_processing')
sys.path.insert(0, '../all_documents')
import avoid
from multiprocessing import Queue
import Common
import threading
from enum import Enum
import get_paystub_details

class Licence_details:

    def __init__(self):
        self.date_val=[]
        self.date = []
        self.name=Queue()
        self.actual_date = []
        self.date_val1 = []
        self.zip_code=[]
        self.licence_id=''
        self.regex_value=''
        self.first_name_original,self.last_name_original,self.middle_name_original,self.first_name_processed,self.last_name_processed,self.middle_name_processed={},{},{},{},{},{}
        self.code,self.regex_value,self.street,self.address,self.full_address=[],[],[],[],[]
        self.street_address_original,self.state_original,self.city_original,self.zip_code_original,self.street_address_processed,self.state_processed,self.city_processed,self.zip_code_processed={},{},{},{},{},{},{},{}
        self.failure_regex=''
        self.c= Common.Common()

        with open('../config/city.json', 'r') as data_file:
            self.cities = json.load(data_file)
        with open('../config/filtering.json', 'r') as data:
            self.state_value = json.load(data)
        with open('../config/failure_filtering.json', 'r') as data:
            self.failure_case = json.load(data)
        with open('../config/NJ_Cities', 'r') as data:
            self.NJ_Cities = json.load(data)

    def get_id(self,text,zip_code):
        try:
            print(zip_code)
            text=text.replace('DL','')
            state_regex=re.findall(r"\b(!?AL|AK|AS|AZ|AŽ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE"
                r"|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)",zip_code)
            print(len(self.state_value['data']))
            if state_regex != []:
                for i in range(len(self.state_value['data'])):
                    if self.state_value['data'][i]['state'] in state_regex[0]:
                        self.regex_value=self.state_value['data'][i]['license_id']
                        # print("regex_state_value",self.state_value['data'][i]['state'],self.regex_value)
                print("state regex",self.regex_value)
                self.licence_id = re.findall(self.regex_value, text)
                print(self.licence_id)
                if self.licence_id==[]:
                    for i in range(len(self.state_value['data'])):
                        if self.state_value['data'][i]['state'] in state_regex[0]:
                            self.failure_regex = self.state_value['data'][i]['failure_case']
                    print("failure regex",self.failure_regex)
                    self.licence_id = re.findall(self.failure_regex, text)

                if 'NJ' in state_regex[0]:
                    if re.search(r'\b(!?[0]\d{4}\s\d{5}\s\d{5})\b',self.licence_id[0]):
                        s=[]
                        print("Hi")
                        split_text=self.licence_id[0].split('0',1)
                        join_text="".join(split_text)
                        s.append('O')
                        s.append(join_text)
                        id = "".join(s)
                        return id
                    elif re.search(r'\b(!?[8]\d{4}\s\d{5}\s\d{5})\b',self.licence_id[0]):
                        s = []
                        split_text = self.licence_id[0].split('8', 1)
                        join_text = "".join(split_text)
                        s.append('B')
                        s.append(join_text)
                        id = "".join(s)
                        return id
                    else:
                        return self.licence_id[0]
                if re.search(r'(!?OH)',zip_code):
                    if re.match(r'[A-Za-z]{1}', self.licence_id[1]):
                        return self.licence_id[1].upper()
                    else:
                        return self.licence_id[1]
                else:
                    if re.match(r'[A-Za-z]{1}', self.licence_id[0]):
                        return self.licence_id[0].upper()

                    else:
                        return self.licence_id[0]
            else:
                print("hey")
                id=re.findall(r'\b(\w[A-Za-z]\d{6}|\s\d{8}|\w\s?\-\s?\d{3}\s?\-\s?\d{3}\s?\-\s?\d{3}\s?\-\s?\d{3}'
                                      r'|\w\d{3}\s?\-\s?\d{3}\s?\-\s?\d{2}\s?\-\s?\d{1}|\w*[A-Za-z]\d{4}\s\d{10}|\d{12}|([A-Za-z]+)?\d{7,9}|[A-Za-z]{1}\d{4,5}\s\d{5}\s\d{4,5}|\w\d{2}\-\d{2}\-\d{4}|[0]?\d{2,3}\s\d{3}\s\d{3}\s?\d?\d?\d?|[A-Za-z]{1}\d{3}\-\d{3}\-\d{2}\-\d{3}-\d{1})\b',
                text)
                License_Id=[]
                for item in id:
                    License_Id.append("".join(item))

                if re.match(r'[A-Za-z]{1}',  License_Id[0]):
                    return  License_Id[0].upper()
                else:
                    return  License_Id[0]
        except Exception as E:
            print("in licence id",E)
            self.get_licence_id=''
            return self.get_licence_id

    def get_address(self,value,keys,values):

        try:
            value = value.replace('.', " ")
            value=value.replace(',','')
            value=avoid.address_replace(value)
            all_number = re.findall(
                r"\s?\s\d{1}\s[A-Za-z]|\s?\s\d{1}\s?[A-Za-z]+|\s\d{4}\s?[A-Za-z]+|\d+[A-Za-z]+\s[A-Za-z]+|\d{2}\s[A-Za-z]+|\:?\d{2}\s[A-Za-z]+|\d{2}-\d{2}\s[A-Za-z]+|\s?\d{3}\w?\s\w+\,?|\s\d{3}\s\d{1}|\w*\s?\d{5}\-?\.?\d{1,4}|\w*\s?\d{5}\s?\-?\.?\s?[A-Za-z]+\d{2,3}|\w*\s?\d{5}\s\w*|\w*\s?\d{5}|\s\d{1}\s?[A-Za-z]+\s[A-Za-z]+",
                value)
            number_val1 = ' '.join(map(str, all_number))
            if re.search(r'\s\s',number_val1):
                number_val1=number_val1.replace(re.findall(r'\s\s',number_val1)[0]," ")
            print("Number val", number_val1)
            number_val = number_val1
            data = re.findall(r'\b((!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\,?\s(\d{5}\d{1,4}|\d{5}(?:\s?\-\s?\d{1,4})|\d{5}(?:\s?\-?\s?[A-Za-z]+\d{1,4})|\d{5}(?:\s?\.\s?\d{4})|\d{5}))', number_val1)
            if data != []:
                if "NJ" not in data[0][0]:
                        if len(data) == 1:
                            data.clear()
                            all_number = re.findall(
                                r"\s?\s\d{1}\s?[A-Za-z]+|\s?\s\d{1}\s?[A-Za-z]+\s[A-Za-z]+|\s\d{4}\s?[A-Za-z]+|\d+[A-Za-z]+\s[A-Za-z]+|\d{2}\s[A-Za-z]+|\:?\d{2}\s[A-Za-z]+|\d{2}-\d{2}\s[A-Za-z]+|\s?\d{3}\w?\s\w+\,?|\s\d{3}\s\d{1}|\w+\s\d{2,5}\-?\.?\d{2,4}|\w*\s\d{2,5}\-?\.?[A-Za-z]+\d{2,3}|\w*\s?\d{5}\s\w*",
                                value)
                            number_val = ' '.join(map(str, all_number))
                            print(number_val)
                            data = re.findall(
                                r'\b((!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\,?\s(\d{5}\d{1,4}|\d{2,5}(?:\s?\-\s?\d{4})|\d{2,5}(?:\s?\-?\s?[A-Za-z]+\d{1,4})|\d{2,5}(?:\s?\.\s?\d{4})|\d{2,5}))',
                                number_val)
                        if len(data) >= 2:

                            if re.search(r'\s(=?ID\s\d+\s\d+)', number_val):
                                self.code.append(data[0][0])
                                self.code.append(data[1][0])
                            elif re.search(r'(=?ID\:?\s\d+\s\d+)', number_val):
                                self.code.append(data[2][0])
                                self.code.append(data[3][0])
                            else:
                                self.code.append(data[0][0])
                                self.code.append(data[1][0])
                            """if re.search('(!?NV|OH|TX|WA|CT|MA|NC|CO|DE|ID|IN|PA|KS|ME|MS|MT|NE|NH|ND|SD|UT|VT|WI)', self.code[0]):
                                if re.search(r'[A-Za-z]+\s?(!?2)', value):
                                    value = value.split(re.findall(r'[A-Za-z]+\s?(!?2)',value)[0], 1)
                                    value = " ".join(value)"""
                            self.regex_value.append(' '.join(map(str, value.split(self.code[0], 1)[0].split()[-8:])))
                            if self.code[0]==self.code[1]:
                                self.regex_value.append(' '.join(map(str, value.split(self.code[1])[1].split()[-8:])))
                            else:
                                self.regex_value.append(' '.join(map(str, value.split(self.code[1]+" ",1)[0].split()[-8:])))
                            self.regex_value[0] = self.regex_value[0] + " " + self.code[0]
                            self.regex_value[1] = self.regex_value[1] + " " + self.code[1]
                            self.regex_value[1] = self.regex_value[1].replace(' STAP ', 'ST APT ')
                            self.regex_value[0] = self.regex_value[0].replace(' STAP ', 'ST APT ')

                            if re.search('(!?NV|OH|TX|WA|CT|MA|NC|CO|DE|ID|IN|PA|KS|ME|MS|MT|NE|NH|ND|SD|UT|VT|WI)',
                                         self.code[0]):
                                if re.search(r'[A-Za-z]+\s?(!?2)', self.regex_value[0]):
                                    rv = self.regex_value[0].split(re.findall(r'[A-Za-z]+\s?(!?2)', self.regex_value[0])[0], 1)
                                    self.regex_value[0] = " ".join(rv)
                                if re.search(r'[A-Za-z]+\s?(!?2)', self.regex_value[1]):
                                    rv1 = self.regex_value[1].split(re.findall(r'[A-Za-z]+\s?(!?2)', self.regex_value[1])[0], 1)
                                    self.regex_value[1] = " ".join(rv1)
                            print("address traverse", self.regex_value)
                            if re.search(r'[A-Za-z]+(!?' + self.code[0] + ')', value):
                                self.street.append(
                                    ' '.join(map(str, number_val.split(self.code[0], 1)[0].split()[-3:-1])))
                            elif re.search(
                                    r'(\s\d+\s([A-Za-z]+)?\s?\s?(\d+)?([A-Za-z]+)?\s?\s?(\d+)?([A-Za-z]+)\s?[#.,/*-]?\s?(\w*)?\s?[#.,/*-]?\d{1,}(\w+)?\s\w+\s?\w+?\s?\w+?\.?\,?\s[A-Z]{2}\s\d{2,})\b',
                                    self.regex_value[0]):

                                if re.search(r'\d+\s\w+\s\d+\w+\s\w+\s\d+\w+\s\w+\s\w+|\d+\s\w+\s\d+\s?\w+\s\w+\s\w+\s\d+\w{1}', self.regex_value[0]):
                                    self.street.append(
                                        ' '.join(map(str, number_val.split(self.code[0], 1)[0].split()[-6:-4])))
                                else:
                                    self.street.append(
                                        ' '.join(map(str, number_val.split(self.code[0], 1)[0].split()[-4:-2])))
                            else:
                                self.street.append(
                                    ' '.join(map(str, number_val.split(self.code[0], 1)[0].split()[-2:])))


                            if re.search(r'[A-Za-z]+(!?' + self.code[1] + ')', value):
                                self.street.append(' '.join(map(str, number_val.split(self.code[1])[0].split()[-3:-1])))

                            elif re.search(
                                    r'(\s\d+\s([A-Za-z]+)?\s?\s?(\d+)?([A-Za-z]+)?\s?\s?(\d+)?([A-Za-z]+)\s?[#.,/*-]?\s?(\w*)?\s?[#.,/*-]?\d{1,}(\w+)?\s\w+\s?\w+?\s?\w+?\.?\,?\s[A-Z]{2}\s\d{2,})\b',
                                    self.regex_value[1]):
                                if re.search(r'\d+\s\w+\s\d+\w+\s\w+\s\d+\w+\s\w+\s\w+|\d+\s\w+\s\d+\s?\w+\s\w+\s\w+\s\d+\w{1}', self.regex_value[0]):
                                    self.street.append(
                                        ' '.join(map(str, number_val.split(self.code[0], 1)[0].split()[-6:-4])))
                                else:
                                    self.street.append(
                                        ' '.join(map(str, number_val.split(self.code[0], 1)[0].split()[-4:-2])))
                            else:
                                self.street.append(' '.join(map(str, number_val.split(self.code[1])[0].split()[-2:])))

                            for i in range(len(self.regex_value)):
                                self.address.append(
                                    self.c.find_between_r(self.regex_value[i], self.street[i], self.code[i]))
                                self.full_address.append(self.street[i] + self.address[i] + self.code[i])
                            state, zipcode, city = self.c.get_address_zipcode(self.full_address[0], self.code[0])
                            state1, zipcode1, city1 = self.c.get_address_zipcode(self.full_address[1], self.code[1])
                            actual_city = []

                            for i in range(len(self.cities['city'])):
                                if city.lower() in self.cities['city'][i].lower():
                                    actual_city.append(self.cities['city'][i])
                                if city1.lower() in self.cities['city'][i].lower():
                                    actual_city.append(self.cities['city'][i])
                            if actual_city == []:
                                city_dict, street_dict = {}, {}
                                actual_city.append(
                                    ' '.join(map(str, self.regex_value[0].split(self.code[0], 1)[0].split()[-1:])))
                                actual_city.append(
                                    ' '.join(map(str, self.regex_value[1].split(self.code[1], 1)[0].split()[-1:])))
                                actual_city[0] = actual_city[0].replace(',', '')
                                actual_city[1] = actual_city[1].replace(',', '')
                                actual_city[0] = actual_city[0].replace('.', '')
                                actual_city[1] = actual_city[1].replace('.', '')
                                # for key, value in enumerate(result):
                                #     if value[0] in actual_city[0]:
                                #         city_dict.update({value[0]: value})
                                #     if value[0] in actual_city[1]:
                                #         city_dict.update({value[0]: value})
                                #     if value[0] in self.street[0]:
                                #         street_dict.update({value[0]: value})
                                #     if value[0] in self.street[1]:
                                #         street_dict.update({value[0]: value})
                                # actual_city_val = max(city_dict.items(), key=operator.itemgetter(1))[0]
                                # actual_street_val = max(street_dict.items(), key=operator.itemgetter(1))[0]
                            else:
                                if city != actual_city[0]:
                                    actual_city[0] = actual_city[0].upper()
                                else:
                                    actual_city.append(actual_city[0])
                                if city1 != actual_city[0]:
                                    actual_city[1] = actual_city[0].upper()
                                else:
                                    actual_city[1] = actual_city[0]

                            full_address = self.c.find_between_r(self.regex_value[0], self.street[0], actual_city[0])
                            full_address1 = self.c.find_between_r(self.regex_value[1], self.street[1], actual_city[1])
                            full_address = self.street[0] + " " + full_address
                            full_address = full_address.replace("*", "")
                            full_address1 = self.street[1] + " " + full_address1
                            address_dict = {'street_address_original': full_address, 'state_original': state,
                                            'city_original': actual_city[0], 'zip_code_original': zipcode,
                                            'street_address_processed': full_address1, 'state_processed': state1,
                                            'city_processed': actual_city[1], 'zip_code_processed': zipcode1}
                            result = dict(zip(keys, values))
                            for key, value in result.items():

                                for key1, value1 in address_dict.items():
                                    if key != '' and value1 != '':
                                        # if value[0] in value1:
                                        if re.search(r'(?!' + re.escape(key) + r')', value1):
                                            if key in address_dict['street_address_original']:
                                                self.street_address_original.update({key: value})
                                            if key in address_dict['street_address_processed']:
                                                self.street_address_processed.update({key: value})
                                            if key in address_dict['state_original']:
                                                self.state_original.update({key: value})

                                            if key in address_dict['city_original']:
                                                self.city_original.update({key: value})

                                            if key == address_dict['zip_code_original']:
                                                self.zip_code_original.update({key: value})

                                            if key in address_dict['state_processed']:
                                                self.state_processed.update({key: value})

                                            if key in address_dict['city_processed']:
                                                self.city_processed.update({key: value})

                                            if key == address_dict['zip_code_processed']:
                                                self.zip_code_processed.update({key: value})
                            street_address_original_score = 0.0
                            street_address_original_a_score = 0
                            state_original_score = 0.0
                            state_original_a_score = 0
                            state_processed_score = 0.0
                            state_processed_a_score = 0
                            city_original_score = 0.0
                            city_original_a_score = 0
                            city_processed_score = 0.0
                            city_processed_a_score = 0
                            zip_code_original_score = 0.0
                            zip_code_original_a_score = 0
                            zip_code_processed_score = 0.0
                            zip_code_processed_a_score = 0

                            for key1, value1 in self.street_address_original.items():
                                street_address_original_score = street_address_original_score + value1
                            street_address_original_a_score = int(
                                (street_address_original_score / len(self.street_address_original)) * 100)
                            # print(street_address_original_a_score)
                            # print(self.street_address_original)

                            street_address_processed_score = 0.0
                            street_address_processed_a_score = 0
                            for key1, value1 in self.street_address_processed.items():
                                street_address_processed_score = street_address_processed_score + value1
                            street_address_processed_a_score = int(
                                (street_address_processed_score / len(self.street_address_processed)) * 100)
                            # print(street_address_processed_score)
                            # print(self.street_address_processed)
                            if len(self.state_original) >= 1:
                                for key1, value1 in self.state_original.items():
                                    state_original_score = state_original_score + value1
                                state_original_a_score = int(
                                    (state_original_score / len(self.state_original)) * 100)
                            if len(self.state_processed) >= 1:
                                for key1, value1 in self.state_processed.items():
                                    state_processed_score = state_processed_score + value1
                                state_processed_a_score = int(
                                    (state_processed_score / len(self.state_processed)) * 100)
                            if len(self.city_original) >= 1:
                                for key1, value1 in self.city_original.items():
                                    city_original_score = city_original_score + value1
                                city_original_a_score = int(
                                    (city_original_score / len(self.city_original)) * 100)
                            if len(self.city_processed) >= 1:
                                for key1, value1 in self.city_processed.items():
                                    city_processed_score = city_processed_score + value1
                                city_processed_a_score = int(
                                    (city_processed_score / len(self.city_processed)) * 100)
                            if len(self.zip_code_original) >= 1:
                                for key1, value1 in self.zip_code_original.items():
                                    zip_code_original_score = zip_code_original_score + value1
                                zip_code_original_a_score = int(
                                    (zip_code_original_score / len(self.zip_code_original)) * 100)
                            if len(self.zip_code_processed) >= 1:
                                for key1, value1 in self.zip_code_processed.items():
                                    zip_code_processed_score = zip_code_processed_score + value1
                                zip_code_processed_a_score = int(
                                    (zip_code_processed_score / len(self.zip_code_processed)) * 100)

                            street_address_dict = {}
                            state_dict, city_dict, zip_code_dict = {}, {}, {}
                            street_address_dict[full_address] = street_address_original_a_score
                            street_address_dict[full_address1] = street_address_processed_a_score
                            state_dict[state] = state_original_a_score
                            state_dict[state1] = state_processed_a_score
                            city_dict[actual_city[0]] = city_original_a_score
                            city_dict[actual_city[1]] = city_processed_a_score
                            zip_code_dict[zipcode] = zip_code_original_a_score
                            zip_code_dict[zipcode1] = zip_code_processed_a_score

                            actual_full_address = max(street_address_dict.items(), key=operator.itemgetter(1))[0]
                            actual_state = max(state_dict.items(), key=operator.itemgetter(1))[0]
                            actual_city = max(city_dict.items(), key=operator.itemgetter(1))[0]
                            actual_zipcode = max(zip_code_dict.items(), key=operator.itemgetter(1))[0]

                            if re.search(r'\b\d{6,9}\b', actual_zipcode):
                                actual_zipcode = actual_zipcode[0:5] + "-" + actual_zipcode[5:9]

                            if re.search(r'(!?\s?\d{2,5}(?:\s?\-?\s?[A-Za-z]+\d{1,4}))', actual_zipcode):
                                actual_zipcode = re.findall(r'\b(!?\d{5})', actual_zipcode)[0]

                            self.street[0] = self.street[0].replace(':', "")
                            self.street[1] = self.street[1].replace(':', "")

                            # for i in range(len(self.NJ_Cities['NJ'])):
                            #     if actual_city.lower() in self.NJ_Cities['NJ'][i].lower() :
                            #         nj_city=self.NJ_Cities['NJ'][i]
                            #
                            # print("CITY",actual_city.lower(),nj_city.lower())
                            # if actual_city.lower() == nj_city.lower():
                            #     actual_state='NJ'

                            if re.search('(!?NV|OH|TX|WA|CT|MA|NC|CO|DE|ID|IN|KS|ME|MS|MT|NE|NH|ND|SD|UT|VT|WI)',
                                         actual_state):
                                if re.search(r'\b\s?(!?8)\s?\d+', actual_full_address):
                                    actual_full_address = actual_full_address.split('8', 1)[1]
                                    self.street[0] = self.street[0].replace('8', "")
                                    self.street[1] = self.street[1].replace('8', "")
                            if 'DRVE' in actual_full_address:
                                actual_full_address = actual_full_address.replace('DRVE', 'DRIVE')

                            if 'IENA.SE' in actual_full_address:
                                actual_full_address = actual_full_address.replace('IENA.SE', 'TERRASE')

                            if 'RDA' in actual_full_address:
                                actual_full_address = actual_full_address.replace('RDA', 'RD')

                            return actual_full_address, self.street[0], self.street[
                                1], actual_state, actual_zipcode, actual_city
                        else:

                            number_val = number_val1
                            full_address, street, state, zip_code, city = '', '', '', '', ''
                            actual_city = ''
                            if re.search(r'\s(=?ID\s\d+\s\d+)', number_val):
                                code = data[0][0]
                            elif re.search(r'(=?ID\:?\s\d+\s\d+)', number_val):
                                code = data[1][0]
                            else:
                                code = data[0][0]
                            print(code)
                            reg_value = ' '.join(map(str, value.split(code, 1)[0].split()[-8:]))
                            reg_value = reg_value + " " + code
                            print('in address', reg_value)
                            # if re.search(r'(\s\d{1,3}\s\w*\s?\w?\s?\w+?\s?\,?\s[A-Z]{2}\s\d{5})\b', reg_value):
                            if re.search(
                                    r'(\d+\s([A-Za-z]+)?\s?\s?(\d+)?([A-Za-z]+)?\s?\s?(\d+)?([A-Za-z]+)\s?[#.,/]?\s?(\w*)?\s?\d{1,}(\w+)?\s\w+\s?\w+?\s?\w?\.?\,?\s[A-Z]{2}\s\d{5,})\b',
                                    reg_value):
                                print("in 4 back traverse")

                                if re.search(r'\d+\s\w+\s\d+\s?\w+\s\w+\s\w+\s\d+\w{1}', code):
                                    street1 = ' '.join(map(str, number_val.split(code, 1)[0].split()[-6:-4]))
                                else:
                                    street1 = ' '.join(map(str, number_val.split(code, 1)[0].split()[-4:-2]))
                            elif re.search(r'[A-Za-z]+(!?' + code + ')', value):
                                street1 = ' '.join(map(str, number_val.split(code, 1)[0].split()[-3:-1]))
                            else:
                                street1 = ' '.join(map(str, number_val.split(code, 1)[0].split()[-2:]))
                            if re.search(r'\d+\s\d+', street1):
                                street = street1.replace(re.findall(r'\b\d+\s', street1)[0], "")
                            else:
                                street = street1
                            print("actual street", street)
                            address = self.c.find_between_r(value, street, code)
                            print("zip code", code)
                            full_address = street + address + code
                            state, zipcode, city = self.c.get_address_zipcode(full_address, code)
                            print("Full Address:", full_address)
                            for i in range(len(self.cities['city'])):
                                if self.cities['city'][i].lower() in city.lower():
                                    actual_city = self.cities['city'][i]

                            if actual_city == '':
                                city = ' '.join(map(str, value.split(code, 1)[0].split()[-1:]))
                                print(city)
                            elif city != actual_city:
                                city = actual_city.upper()
                            else:
                                city = actual_city
                            full_address = self.c.find_between_r(value, street, city)
                            full_address = street + full_address
                            print("address", full_address)
                            full_address = ' '.join(s[:1].upper() + s[1:] for s in full_address.split())
                            city = city.replace(",", "")
                            city = city.replace(".", "")
                            full_address = full_address.replace("DRI", "DR")
                            full_address = full_address.replace("ss ", "55 ")
                            if re.search('(!?NV|OH|TX|WA|CT|MA|NC|CO|DE|ID|IN|KS|ME|MS|MT|NE|NH|ND|SD|UT|VT|WI)',
                                         state):
                                if re.search(r'\b\s?(!?8)\s?\d+', full_address):
                                    full_address = full_address.split('8', 1)[1]
                                    street = street.replace('8', ' ')
                            # for i in range(len(self.NJ_Cities['NJ'])):
                            #     if self.NJ_Cities['NJ'][i].lower() in city.lower():
                            #         nj_city=self.NJ_Cities['NJ'][i]
                            #
                            # print("CITY",city.lower,nj_city.lower())
                            # if city.lower() == nj_city.lower():
                            #     state='NJ'

                            if 'DRVE' in full_address:
                                full_address = full_address.replace('DRVE', 'DRIVE')

                            if 'IENA.SE' in full_address:
                                full_address = full_address.replace('IENA.SE', 'TERRASE')
                            if 'RDA' in full_address:
                                full_address = full_address.replace('RDA', 'RD')

                            return full_address, street, street, state, zipcode, city
                else:
                    all_number = re.findall(
                        r"\s?\s\d{1}\s[A-Za-z]|\s?\s\d{1}\s?[A-Za-z]+|\s\d{4}\s?[A-Za-z]+|\d+[A-Za-z]+\s[A-Za-z]+|\d{2}\s[A-Za-z]+|\:?\d{2}\s[A-Za-z]+|\d{2}-\d{2}\s[A-Za-z]+|\s?\d{3}\w?\s\w+\,?|\s\d{3}\s\d{1}|\w*\s?\d{5}\s?\-?\.?\s?\d{1,4}|\w*\s?\d{5}\s?\-?\.?\s?[A-Za-z]+\d{2,3}|\w*\s?\d{5}\s\w*|\w*\s?\d{5}|\s\d{1}\s?[A-Za-z]+\s[A-Za-z]+",
                        value)
                    number_val1 = ' '.join(map(str, all_number))
                    if re.search(r'\s\s', number_val1):
                        number_val1 = number_val1.replace(re.findall(r'\s\s', number_val1)[0], " ")
                    print("Number val", number_val1)
                    number_val = number_val1
                    data = re.findall(
                        r'\b((!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\,?\s(\d{5}\d{1,4}|\d{5}(?:\s?\-\s?\d{1,4})|\d{5}(?:\s?\-?\s?[A-Za-z]+\d{1,4})|\d{5}(?:\s?\.\s?\d{4})|\d{5}\s\d{1,4}|\d{5}))',
                        number_val1)
                    if len(data) == 1:
                        data.clear()
                        all_number = re.findall(
                            r"\s?\s\d{1}\s?[A-Za-z]+|\s?\s\d{1}\s?[A-Za-z]+\s[A-Za-z]+|\s\d{4}\s?[A-Za-z]+|\d+[A-Za-z]+\s[A-Za-z]+|\d{2}\s[A-Za-z]+|\:?\d{2}\s[A-Za-z]+|\d{2}-\d{2}\s[A-Za-z]+|\s?\d{3}\w?\s\w+\,?|\s\d{3}\s\d{1}|\w+\s\d{2,5}\-?\.?\d{2,4}|\w*\s\d{2,5}\-?\.?[A-Za-z]+\d{2,3}|\w*\s?\d{5}\s\w*",
                            value)
                        number_val = ' '.join(map(str, all_number))
                        print(number_val)
                        data = re.findall(
                            r'((!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\,?\s(\d{5}\d{1,4}|\d{2,5}(?:\s?\-\s?\d{4})|\d{2,5}(?:\s?\-?\s?[A-Za-z]+\d{1,4})|\d{2,5}(?:\s?\.\s?\d{4})|\d{2,5}))',
                            number_val)
                    if len(data) >= 2:

                        if re.search(r'\s(=?ID\s\d+\s\d+)', number_val):
                            self.code.append(data[0][0])
                            self.code.append(data[1][0])
                        elif re.search(r'(=?ID\:?\s\d+\s\d+)', number_val):
                            self.code.append(data[2][0])
                            self.code.append(data[3][0])
                        else:
                            self.code.append(data[0][0])
                            self.code.append(data[1][0])
                        if re.search('(!?NV|OH|TX|WA|CT|MA|NC|CO|DE|ID|IN|PA|KS|ME|MS|MT|NE|NH|ND|SD|UT|VT|WI)',
                                     self.code[0]):
                            if re.search(r'\b\s?(!?8|2)\s?(\d+)?\s?(\w+)?\b', value):
                                value = value.replace(re.findall(r'[A-Za-z]+\s?(!?2)\s?[A-Za-z]+', value)[0], ' ')
                        # if re.search('(!?NV|OH|TX|WA|CT|MA|NC|CO|DE|ID|IN|PA|KS|ME|MS|MT|NE|NH|ND|SD|UT|VT|WI)', self.code[0]):
                        #     if re.search(r'\b\s?(!?8|2)\s?(\d+)?\s?(\w+)?\b', value):
                        #         value = value.split(re.findall(r'[A-Za-z]+\s?(!?2)\s?[A-Za-z]+',value)[0], 1)
                        #         value = " ".join(value)
                        self.regex_value.append(' '.join(map(str, value.split(self.code[0], 1)[0].split()[-8:])))
                        self.regex_value.append(' '.join(map(str, value.split(self.code[1] + " ", 1)[0].split()[-8:])))
                        self.regex_value[0] = self.regex_value[0] + " " + self.code[0]
                        self.regex_value[1] = self.regex_value[1] + " " + self.code[1]
                        self.regex_value[1] = self.regex_value[1].replace(' STAP ', 'ST APT ')
                        self.regex_value[0] = self.regex_value[0].replace(' STAP ', 'ST APT ')
                        print("address traverse", self.regex_value)

                        if re.search(r'[A-Za-z]+(!?' + self.code[0] + ')', value):
                            self.street.append(' '.join(map(str, number_val.split(self.code[0], 1)[0].split()[-3:-1])))
                        if re.search(
                                r'(\s\d+\s([A-Za-z]+)?\s?\s?(\d+)?([A-Za-z]+)?\s?\s?(\d+)?([A-Za-z]+)\s?[#.,/*-]?\s?(\w*)?\s?[#.,/*-]?\d{1,}(\w+)?\s\w+\s?\w+?\s?[#.,/*-]?\s?(\d+)?\s?\w+?\.?\,?\s[A-Z]{2}\s\d{2,})\b',
                                self.regex_value[0]):

                            if re.search(r'\s\d+\s\w+\s\d+\s?\w+\s\w+\s\w+\s\d+\w{1}', self.regex_value[0]):
                                self.street.append(
                                    ' '.join(map(str, number_val.split(self.code[0], 1)[0].split()[-6:-4])))
                            else:
                                self.street.append(
                                    ' '.join(map(str, number_val.split(self.code[0], 1)[0].split()[-4:-2])))
                        else:
                            self.street.append(' '.join(map(str, number_val.split(self.code[0], 1)[0].split()[-2:])))

                        if re.search(r'[A-Za-z]+(!?' + self.code[1] + ')', value):
                            self.street.append(' '.join(map(str, number_val.split(self.code[1])[0].split()[-3:-1])))
                        elif re.search(
                                r'(\s\d+\s([A-Za-z]+)?\s?\s?(\d+)?([A-Za-z]+)?\s?\s?(\d+)?([A-Za-z]+)\s?[#.,/*-]?\s?(\w*)?\s?[#.,/*-]?\d{1,}(\w+)?\s\w+\s?\w+?\s?[#.,/*-]?\s?(\d+)?\s?\w+?\.?\,?\s[A-Z]{2}\s\d{2,})\b',
                                self.regex_value[1]):
                            if re.search(r'\d+\s\w+\s\d+\s?\w+\s\w+\s\w+\s\d+\w{1}', self.regex_value[1]):
                                self.street.append(
                                    ' '.join(map(str, number_val.split(self.code[1], 1)[0].split()[-6:-4])))
                            else:
                                self.street.append(
                                    ' '.join(map(str, number_val.split(self.code[1], 1)[0].split()[-4:-2])))
                        else:
                            self.street.append(' '.join(map(str, number_val.split(self.code[1])[0].split()[-2:])))

                        for i in range(len(self.regex_value)):
                            self.address.append(
                                self.c.find_between_r(self.regex_value[i], self.street[i], self.code[i]))
                            self.full_address.append(self.street[i] + self.address[i] + self.code[i])
                        state, zipcode, city = self.c.get_address_zipcode(self.full_address[0], self.code[0])
                        state1, zipcode1, city1 = self.c.get_address_zipcode(self.full_address[1], self.code[1])
                        actual_city = []

                        for i in range(len(self.cities['city'])):
                            if city.lower() == self.cities['city'][i].lower():
                                actual_city.append(self.cities['city'][i])
                            if city1.lower() == self.cities['city'][i].lower():
                                actual_city.append(self.cities['city'][i])
                        if actual_city == []:
                            city_dict, street_dict = {}, {}
                            actual_city.append(
                                ' '.join(map(str, self.regex_value[0].split(self.code[0], 1)[0].split()[-1:])))
                            actual_city.append(
                                ' '.join(map(str, self.regex_value[1].split(self.code[1], 1)[0].split()[-1:])))
                            actual_city[0] = actual_city[0].replace(',', '')
                            actual_city[1] = actual_city[1].replace(',', '')
                            actual_city[0] = actual_city[0].replace('.', '')
                            actual_city[1] = actual_city[1].replace('.', '')
                            # for key, value in enumerate(result):
                            #     if value[0] in actual_city[0]:
                            #         city_dict.update({value[0]: value})
                            #     if value[0] in actual_city[1]:
                            #         city_dict.update({value[0]: value})
                            #     if value[0] in self.street[0]:
                            #         street_dict.update({value[0]: value})
                            #     if value[0] in self.street[1]:
                            #         street_dict.update({value[0]: value})
                            # actual_city_val = max(city_dict.items(), key=operator.itemgetter(1))[0]
                            # actual_street_val = max(street_dict.items(), key=operator.itemgetter(1))[0]
                        else:
                            if city != actual_city[0]:
                                actual_city[0] = actual_city[0].upper()
                            else:
                                actual_city.append(actual_city[0])
                            if city1 != actual_city[0]:
                                actual_city[1] = actual_city[0].upper()
                            else:
                                actual_city[1] = actual_city[0]

                        full_address = self.c.find_between_r(self.regex_value[0], self.street[0], actual_city[0])
                        full_address1 = self.c.find_between_r(self.regex_value[1], self.street[1], actual_city[1])
                        full_address = self.street[0] + " " + full_address
                        full_address = full_address.replace("*", "")
                        full_address1 = self.street[1] + " " + full_address1
                        address_dict = {'street_address_original': full_address, 'state_original': state,
                                        'city_original': actual_city[0], 'zip_code_original': zipcode,
                                        'street_address_processed': full_address1, 'state_processed': state1,
                                        'city_processed': actual_city[1], 'zip_code_processed': zipcode1}
                        result = dict(zip(keys, values))
                        for key, value in result.items():

                            for key1, value1 in address_dict.items():
                                if key != '' and value1 != '':
                                    # if value[0] in value1:
                                    if re.search(r'(?!' + re.escape(key) + r')', value1):
                                        if key in address_dict['street_address_original']:
                                            self.street_address_original.update({key: value})
                                        if key in address_dict['street_address_processed']:
                                            self.street_address_processed.update({key: value})
                                        if key in address_dict['state_original']:
                                            self.state_original.update({key: value})

                                        if key in address_dict['city_original']:
                                            self.city_original.update({key: value})

                                        if key == address_dict['zip_code_original']:
                                            self.zip_code_original.update({key: value})

                                        if key in address_dict['state_processed']:
                                            self.state_processed.update({key: value})

                                        if key in address_dict['city_processed']:
                                            self.city_processed.update({key: value})

                                        if key == address_dict['zip_code_processed']:
                                            self.zip_code_processed.update({key: value})
                        street_address_original_score = 0.0
                        street_address_original_a_score = 0
                        state_original_score = 0.0
                        state_original_a_score = 0
                        state_processed_score = 0.0
                        state_processed_a_score = 0
                        city_original_score = 0.0
                        city_original_a_score = 0
                        city_processed_score = 0.0
                        city_processed_a_score = 0
                        zip_code_original_score = 0.0
                        zip_code_original_a_score = 0
                        zip_code_processed_score = 0.0
                        zip_code_processed_a_score = 0

                        for key1, value1 in self.street_address_original.items():
                            street_address_original_score = street_address_original_score + value1
                        street_address_original_a_score = int(
                            (street_address_original_score / len(self.street_address_original)) * 100)
                        # print(street_address_original_a_score)
                        # print(self.street_address_original)

                        street_address_processed_score = 0.0
                        street_address_processed_a_score = 0
                        for key1, value1 in self.street_address_processed.items():
                            street_address_processed_score = street_address_processed_score + value1
                        street_address_processed_a_score = int(
                            (street_address_processed_score / len(self.street_address_processed)) * 100)
                        # print(street_address_processed_score)
                        # print(self.street_address_processed)
                        if len(self.state_original) >= 1:
                            for key1, value1 in self.state_original.items():
                                state_original_score = state_original_score + value1
                            state_original_a_score = int(
                                (state_original_score / len(self.state_original)) * 100)
                        if len(self.state_processed) >= 1:
                            for key1, value1 in self.state_processed.items():
                                state_processed_score = state_processed_score + value1
                            state_processed_a_score = int(
                                (state_processed_score / len(self.state_processed)) * 100)
                        if len(self.city_original) >= 1:
                            for key1, value1 in self.city_original.items():
                                city_original_score = city_original_score + value1
                            city_original_a_score = int(
                                (city_original_score / len(self.city_original)) * 100)
                        if len(self.city_processed) >= 1:
                            for key1, value1 in self.city_processed.items():
                                city_processed_score = city_processed_score + value1
                            city_processed_a_score = int(
                                (city_processed_score / len(self.city_processed)) * 100)
                        if len(self.zip_code_original) >= 1:
                            for key1, value1 in self.zip_code_original.items():
                                zip_code_original_score = zip_code_original_score + value1
                            zip_code_original_a_score = int(
                                (zip_code_original_score / len(self.zip_code_original)) * 100)
                        if len(self.zip_code_processed) >= 1:
                            for key1, value1 in self.zip_code_processed.items():
                                zip_code_processed_score = zip_code_processed_score + value1
                            zip_code_processed_a_score = int(
                                (zip_code_processed_score / len(self.zip_code_processed)) * 100)

                        street_address_dict = {}
                        state_dict, city_dict, zip_code_dict = {}, {}, {}
                        street_address_dict[full_address] = street_address_original_a_score
                        street_address_dict[full_address1] = street_address_processed_a_score
                        state_dict[state] = state_original_a_score
                        state_dict[state1] = state_processed_a_score
                        city_dict[actual_city[0]] = city_original_a_score
                        city_dict[actual_city[1]] = city_processed_a_score
                        zip_code_dict[zipcode] = zip_code_original_a_score
                        zip_code_dict[zipcode1] = zip_code_processed_a_score

                        actual_full_address = max(street_address_dict.items(), key=operator.itemgetter(1))[0]
                        actual_state = max(state_dict.items(), key=operator.itemgetter(1))[0]
                        actual_city = max(city_dict.items(), key=operator.itemgetter(1))[0]
                        actual_zipcode = max(zip_code_dict.items(), key=operator.itemgetter(1))[0]

                        if re.search(r'\b\d{6,9}\b', actual_zipcode):
                            if re.search(r'\d{5}-\d{4}', zipcode):
                                actual_zipcode = zipcode
                            elif re.search(r'\d{5}-\d{4}', zipcode1):
                                actual_zipcode = zipcode1
                            else:
                                actual_zipcode = actual_zipcode[0:5] + "-" + actual_zipcode[5:9]

                        if re.search(r'(!?\s?\d{2,5}(?:\s?\-?\s?[A-Za-z]+\d{1,4}))', actual_zipcode):
                            actual_zipcode = re.findall(r'\b(!?\d{5})', actual_zipcode)[0]

                        if actual_city in actual_full_address:
                            if actual_city not in full_address:
                                actual_full_address = full_address
                            else:
                                actual_full_address = full_address1

                        self.street[0] = self.street[0].replace(':', "")
                        self.street[1] = self.street[1].replace(':', "")

                        # for i in range(len(self.NJ_Cities['NJ'])):
                        #     if actual_city.lower() in self.NJ_Cities['NJ'][i].lower() :
                        #         nj_city=self.NJ_Cities['NJ'][i]
                        #
                        # print("CITY",actual_city.lower(),nj_city.lower())
                        # if actual_city.lower() == nj_city.lower():
                        #     actual_state='NJ'

                        if re.search('(!?NV|OH|TX|WA|CT|MA|NC|CO|DE|ID|IN|KS|ME|MS|MT|NE|NH|ND|SD|UT|VT|WI)',
                                     actual_state):
                            if re.search(r'\b\s?(!?8)\s?\d+', actual_full_address):
                                actual_full_address = actual_full_address.split('8', 1)[1]
                                self.street[0] = self.street[0].replace('8', "")
                                self.street[1] = self.street[1].replace('8', "")
                        if 'DRVE' in actual_full_address:
                            actual_full_address = actual_full_address.replace('DRVE', 'DRIVE')

                        if 'IENA.SE' in actual_full_address:
                            actual_full_address = actual_full_address.replace('IENA.SE', 'TERRASE')

                        if 'RDA' in actual_full_address:
                            actual_full_address = actual_full_address.replace('RDA', 'RD')

                        return actual_full_address, self.street[0], self.street[
                            1], actual_state, actual_zipcode, actual_city
                    else:

                        number_val = number_val1
                        full_address, street, state, zip_code, city = '', '', '', '', ''
                        actual_city = ''
                        if re.search(r'\s(=?ID\s\d+\s\d+)', number_val):
                            code = data[0][0]
                        elif re.search(r'(=?ID\:?\s\d+\s\d+)', number_val):
                            code = data[1][0]
                        else:
                            code = data[0][0]
                        print(code)
                        reg_value = ' '.join(map(str, value.split(code, 1)[0].split()[-8:]))
                        reg_value = reg_value + " " + code
                        print('in address', reg_value)
                        # if re.search(r'(\s\d{1,3}\s\w*\s?\w?\s?\w+?\s?\,?\s[A-Z]{2}\s\d{5})\b', reg_value):
                        if re.search(
                                r'(\d+\s([A-Za-z]+)?\s?\s?(\d+)?([A-Za-z]+)?\s?\s?(\d+)?([A-Za-z]+)\s?[#.,/]?\s?(\w*)?\s?\d{1,}(\w+)?\s\w+\s?\w+?\s?\w?\.?\,?\s[A-Z]{2}\s\d{5,})\b',
                                reg_value):
                            print("in 4 back traverse")

                            if re.search(r'\d+\s\w+\s\d+\s?\w+\s\w+\s\w+\s\d+\w{1}', code):
                                street1 = ' '.join(map(str, number_val.split(code, 1)[0].split()[-6:-4]))
                            else:
                                street1 = ' '.join(map(str, number_val.split(code, 1)[0].split()[-4:-2]))
                        elif re.search(r'[A-Za-z]+(!?' + code + ')', value):
                            street1 = ' '.join(map(str, number_val.split(code, 1)[0].split()[-3:-1]))
                        else:
                            street1 = ' '.join(map(str, number_val.split(code, 1)[0].split()[-2:]))
                        if re.search(r'\d+\s\d+', street1):
                            street = street1.replace(re.findall(r'\b\d+\s', street1)[0], "")
                        else:
                            street = street1
                        print("actual street", street)
                        address = self.c.find_between_r(value, street, code)
                        print("zip code", code)
                        full_address = street + address + code
                        state, zipcode, city = self.c.get_address_zipcode(full_address, code)
                        print("Full Address:", full_address)
                        for i in range(len(self.cities['city'])):
                            if self.cities['city'][i].lower() == city.lower():
                                actual_city = self.cities['city'][i]

                        if actual_city == '':
                            city = ' '.join(map(str, value.split(code, 1)[0].split()[-1:]))
                            print(city)
                        elif city != actual_city:
                            city = actual_city.upper()
                        else:
                            city = actual_city
                        full_address = self.c.find_between_r(full_address, street, state)
                        full_address = street + full_address
                        st = re.compile(r'(!?' + state + r')', re.IGNORECASE)

                        full_address = full_address.replace(st.findall(full_address)[0], '')
                        print("address", full_address)
                        full_address = ' '.join(s[:1].upper() + s[1:] for s in full_address.split())
                        city = city.replace(",", "")
                        city = city.replace(".", "")
                        full_address = full_address.replace("DRI", "DR")
                        full_address = full_address.replace("ss ", "55 ")
                        if re.search('(!?NV|OH|TX|WA|CT|MA|NC|CO|DE|ID|IN|KS|ME|MS|MT|NE|NH|ND|SD|UT|VT|WI)', state):
                            if re.search(r'\b\s?(!?8)\s?\d+', full_address):
                                full_address = full_address.split('8', 1)[1]
                                street = street.replace('8', ' ')
                        # for i in range(len(self.NJ_Cities['NJ'])):
                        #     if self.NJ_Cities['NJ'][i].lower() in city.lower():
                        #         nj_city=self.NJ_Cities['NJ'][i]
                        #
                        # print("CITY",city.lower,nj_city.lower())
                        # if city.lower() == nj_city.lower():
                        #     state='NJ'

                        if 'DRVE' in full_address:
                            full_address = full_address.replace('DRVE', 'DRIVE')

                        if 'IENA.SE' in full_address:
                            full_address = full_address.replace('IENA.SE', 'TERRASE')
                        if 'RDA' in full_address:
                            full_address = full_address.replace('RDA', 'RD')

                        return full_address, street, street, state, zipcode, city
            else:
                number_val = number_val1
                full_address, street, state, zip_code, city = '', '', '', '', ''
                actual_city = ''
                print("in else")
                val1 = re.findall(
                    r"\s(\d+)\-?\s?([A-Za-z]+)?\s?([A-Za-z]+)?\s?([A-Za-z]+)?\s?([A-Za-z]+)?\-?\s?(\d+)?\s?([A-Za-z]+)?\.?\s?(\d+)?\s(\w+)?\s?\.?\,?(!? AL| AK| AS| AZ| AŽ| AŻ| AR| CA| CO| CT| DE| DC| FM| FL| GA| GU| HI| ID| IL| IN| IA| KS| KY| LA| ME| MH| MD| MA| MI| MN| MS| MO| MT| NE| NV| NH| NJ| NM| NY| NC| ND| MP| OH| OK| OR| PW| PA| PR| RI| SC| SD| TN| TX| UT| VT| VI| VA| WA| WV| WI| WY)\s\w+",
                    value)
                print("else data",data)
                val=""
                for item in val1:
                    val=val+" ".join(item)
                data=re.findall(r'\b(!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\b',val)
                if data != []:
                    if re.search(r'\s(=?DE\s[A-Za-z]\d{4})',value):
                        code=data[1]
                    else:
                        code = data[0]
                    # if re.search(r'\s(=?ID\s\d+\s\d+)', number_val):
                    #     code = data[0][0]
                    # elif re.search(r'(=?ID\:?\s\d+\s\d+)', number_val):
                    #     code = data[1][0]
                    # else:
                    #     code = data[0][0]
                    # print(code)
                    if re.search('[a-z]+',code):
                        code=code.replace(re.findall('[a-z]+',code)[0],"")
                    reg_value = ' '.join(map(str, value.split(code, 1)[0].split()[-8:]))
                    reg_value = reg_value + " " + code
                    print("in else",reg_value)
                    if re.search(r'(\d+\s?([A-Za-z]+)?\s?([A-Za-z])+?\s?([A-Za-z])+'
                                 r'\s?[#.,/]?\s?\w*?\s\d{1,}\s\w+\s?\w+?\s?\w?\,?\s[A-Z]{2})\b',reg_value):
                        street_code=re.findall(r'\s\d+\s+\w+',reg_value)
                        street=street_code[0]

                    else:
                        street_code = re.findall(r'\s\d+\s+\w+', reg_value)
                        street = street_code[0]
                    address = self.c.find_between_r(value, street, code)
                    print("zip code", code)
                    full_address = street + address + code
                    state,zip_code,city = self.c.get_address_zipcode(full_address, code)
                    print("Full Address:", full_address, city, state)
                    for i in range(len(self.cities['city'])):
                        if self.cities['city'][i].lower() in city.lower():
                            actual_city = self.cities['city'][i]

                    if actual_city == '':
                        city = ' '.join(map(str, value.split(code, 1)[0].split()[-1:]))
                        print(city)
                    elif city != actual_city:
                        city = actual_city.upper()
                    else:
                        city = actual_city
                    full_address = self.c.find_between_r(value, street, city)
                    print("full", full_address)
                    full_address = street + full_address
                    full_address = ' '.join(s[:1].upper() + s[1:] for s in full_address.split())
                    city = city.replace(",", "")
                    city = city.replace(".", "")
                    zipcode=""

                    if re.search('(!?NV|OH|TX|WA|CT|MA|NC|CO|DE|ID|IN|KS|ME|MS|MT|NE|NH|ND|SD|UT|VT|WI)',state):
                        full_address=full_address.split('8',1)[1]
                    # for i in range(len(self.NJ_Cities['NJ'])):
                    #     if self.NJ_Cities['NJ'][i].lower() in city.lower():
                    #         nj_city=self.NJ_Cities['NJ'][i]
                    #
                    # print("CITY",city.lower,nj_city.lower())
                    # if city.lower() == nj_city.lower():
                    #     state='NJ'
                    if 'DRVE' in full_address:
                        full_address=full_address.replace('DRVE','DRIVE')

                    if 'IENA.SE' in full_address:
                        full_address=full_address.replace('IENA.SE','TERRASE')

                    if 'RDA' in full_address:
                        full_address = full_address.replace('RDA', 'RD')

                return full_address, street,street, state, zip_code, city
        except Exception as e:
            print("in address",e)
            full_address, street,street1, state, zipcode, city = "", "", "", "", "",""

            return full_address, street,street1, state, zipcode, city

    def get_name(self,text_value,street,street1,licenseid,zip_code,date,keys,values):
        try:
            print(street,street1)
            text_value = text_value.replace('.', " ")
            value=avoid.name_replace(text_value,date,zip_code)

            if licenseid!='':
                value = value.replace(licenseid, " ")
            value=value.replace('.',' ')
            name_value = []
            name_value1 = []
            name_val,name_val1='',''
            if street!=street1:
                name_reg_val=re.findall(r'\s?([A-Za-z]+)?(\-)?\s?([A-Za-z]+)?(\-)?\s?(\d+)?\s?([A-Za-z]+)?(\-)?\s?([A-Za-z]+)?(\-)?\s?([A-Za-z]+)?(\-)?([A-Za-z]+)?[,.]?\s?\s?([A-Za-z]+)?\s?(\d+)?\s?(!?'+street+r')\b',value)
                for item in name_reg_val:
                    name_value.append(" ".join(item))
                name_val = "".join(map(str, name_value))
                name_val = name_val.replace(street, "")
                if re.search(r'\s\s',name_val):
                    name_val=name_val.replace(re.findall(r'\s\s',name_val)[0]," ")
            if street1==street:
                name_reg_val = re.findall(r'\s?([A-Za-z]+)?(\-)?\s?(['
                                          r'A-Za-z]+)?(\-)?\s?(\d+)?\s?([A-Za-z]+)?(\-)?\s?([A-Za-z]+)?(\-)?\s?([A-Za-z]+)?(\-)?([A-Za-z]+)?[,.]?\s?\s?([A-Za-z]+)?\s?(\d+)?\s?(!?'+street1+r')\b',value)
                for item in name_reg_val:
                    name_value.append(" ".join(item))
                if len(name_reg_val)==1:
                    name_val = "".join(map(str, name_value))
                    name_val = name_val.replace(street, "")
                    if re.search(r'\s\s', name_val):
                        name_val = name_val.replace(re.findall(r'\s\s', name_val)[0], " ")
                else:
                    name_val = "".join(map(str, name_value[0]))
                    name_val1 = "".join(map(str, name_value[1]))
                    name_val1 = name_val1.replace(street, "")
                    name_val = name_val.replace(street, "")
            if street != street1:
                name_reg_va11 = re.findall(
                    r'\s?([A-Za-z]+)?(\-)?\s?([A-Za-z]+)?(\-)?\s?(\d+)?\s?([A-Za-z]+)?(\-)?\s?([A-Za-z]+)?(\-)?\s?([A-Za-z]+)?(\-)?([A-Za-z]+)?[,.]?\s?\s?([A-Za-z]+)?\s?(\d+)?\s?(!?'+street1+r')\b', value)
                for item in name_reg_va11:
                    name_value1.append(" ".join(item))
                name_val1 = "".join(map(str, name_value1))
                name_val1=name_val1.replace(street1,"")
                if re.search(r'\s\s',name_val1):
                    name_val1=name_val1.replace(re.findall(r'\s\s',name_val1)[0]," ")

            print("in name", name_val, name_val1)
            name_val = name_val.split('2', 1)
            name_val = "".join(name_val)
            name_val1 = name_val1.split('2', 1)
            name_val1= "".join(name_val1)
            name_regex= re.findall(r'[A-Za-z]+\s?\s?\-?\s?\s?\b', name_val)
            actual_name= " ".join(map(str, name_regex))

            name_regex1 = re.findall(r'[A-Za-z]+\s?\s?\-?\s?\s?\b', name_val1)
            actual_name1 = " ".join(map(str, name_regex1))

            actual_name = avoid.replace(actual_name)
            actual_name1 = avoid.replace(actual_name1)

            if re.search(r'\s\s', actual_name):
                actual_name = actual_name.replace(re.findall(r'\s\s', actual_name)[0], " ")
            if re.search(r'\s\s', actual_name1):
                actual_name1 = actual_name1.replace(re.findall(r'\s\s', actual_name1)[0], " ")
            print("in name", actual_name, actual_name1)
            name_reg = re.findall(r'[A-Za-z]+\s?\-\s?\s?[A-Za-z]+\s\s?[A-Za-z]{2,}\s?\w?|[A-Za-z]+\s[A-Za-z]+\s?\-\s?\s?[A-Za-z]+\s[A-Za-z]{2,}\s?\w?|[A-Za-z]+\s?\-\s?\s?[A-Za-z]+|[A-Za-z]{2,}\s?\s?\s[A-Za-z]{1,}\s?\s[A-Za-z]{2,}\s?\s[A-Za-z]+|[A-Za-z]{2,}\s?\s[A-Za-z]{1,}\s?\s?[A-Za-z]?\s?\s[A-Za-z]+|[A-Za-z]{2,}\s?\s?\s[A-Za-z]{1,}\s?\s[A-Za-z]{2,}|[A-Za-z]{2,}\s?\s[A-Za-z]{1,}\s?[A-Za-z]?|[A-Za-z]+',actual_name)
            name_reg1 = re.findall(r'[A-Za-z]+\s?\-\s?\s?[A-Za-z]+\s\s?[A-Za-z]{2,}\s?\w?|[A-Za-z]+\s[A-Za-z]+\s?\-\s?\s?[A-Za-z]+\s[A-Za-z]{2,}\s?\w?|[A-Za-z]+\s?\-\s?\s?[A-Za-z]+|[A-Za-z]{2,}\s?\s?\s[A-Za-z]{1,}\s?\s[A-Za-z]{2,}\s?\s[A-Za-z]+|[A-Za-z]{2,}\s?\s[A-Za-z]{1,}\s?\s?[A-Za-z]?\s?\s[A-Za-z]+|[A-Za-z]{2,}\s?\s?\s[A-Za-z]{1,}\s?\s[A-Za-z]{2,}|[A-Za-z]{2,}\s?\s[A-Za-z]{1,}\s?[A-Za-z]?|[A-Za-z]+',actual_name1)

            full_name = " ".join(map(str, name_reg))
            full_name1 = " ".join(map(str, name_reg1))
            print(full_name,full_name1)

            if re.search('[A-Za-z]+\s?\-\s?\s?[A-Za-z]+\s?\s?[A-Za-z]+', full_name):
                fname=full_name.replace(' - ',"-")

                full_name=fname
            if re.search(r'\s\s',full_name):
                full_name=full_name.replace(re.findall(r'\s\s',full_name)[0]," ")

            if re.search('[A-Za-z]+\s?\-\s?\s?[A-Za-z]+', full_name1):
                fname1=full_name.replace(' - ',"-")
                full_name1=fname1
            if re.search(r'\s\s',full_name1):
                full_name1=full_name1.replace(re.findall(r'\s\s',full_name1)[0]," ")
            fn=len(full_name.split())
            fn1=len(full_name1.split())
            name_dict = {}
            name_dict={'original_name':full_name,'processed_name':full_name1}

            result = dict(zip(keys, values))
            for k, v in result.items():
                # k=k+" "
                for key1, value1 in name_dict.items():
                    if k != '' and value1 != '':
                        if k in name_dict['original_name']:
                            self.first_name_original.update({k: v})
                        if k in name_dict['processed_name']:
                            self.first_name_processed.update({k: v})
            first_name_original_score = 0.0
            first_name_original_a_score = 0
            if len(self.first_name_original)>=1:
                for key1, value1 in self.first_name_original.items():
                    first_name_original_score = first_name_original_score + value1
                first_name_original_a_score = int((first_name_original_score / len(self.first_name_original)) * 100)
            print("FN",first_name_original_a_score)
            first_name_processed_score = 0.0
            first_name_processed_a_score = 0
            if len(self.first_name_processed) >=1:
                for key1, value1 in self.first_name_processed.items():
                    first_name_processed_score = first_name_processed_score + value1
                first_name_processed_a_score = int((first_name_processed_score / len(self.first_name_processed)) * 100)
            print("PN", first_name_processed_a_score)
            first_dict, last_dict, middle_name_dict = {}, {}, {}
            first_dict[full_name] = first_name_original_a_score
            first_dict[full_name1] = first_name_processed_a_score

            actual_full_name = max(first_dict.items(), key=operator.itemgetter(1))[0]
            actual_full_name = actual_full_name.replace(' s', " GU")
            if len(actual_full_name.split())==1:
                if fn>1:
                    actual_full_name=full_name
                elif fn==1 and fn1==0:
                    actual_full_name=actual_full_name
                else:
                    actual_full_name=full_name1
            # name_regex = re.findall(r'[A-Za-z]+\-?\b', name_value)
            # actual_name1 = " ".join(map(str, name_regex))
            # actual_name = avoid.replace(actual_name1)
            # print(actual_name)
            #
            # if re.match(r'(=?IS |TO |WS |Is )',actual_name):
            #     name_reg = re.findall(r'[A-Za-z]+\s[A-Za-z]+\-\s?[A-Za-z]+\s[A-Za-z]{2,}\s?\w?|[A-Za-z]+\-\s?[A-Za-z]+\s[A-Za-z]{2,}\s?\w?|[A-Za-z]+\-\s?[A-Za-z]+|[A-Za-z]{2,}\s?\s?\s[A-Za-z]{1,}\s[A-Za-z]{3,}[A-Za-z]+|[A-Za-z]{2,}\s[A-Za-z]{1,}\s?[A-Za-z]?[A-Za-z]+|[A-Za-z]{2,}\s?\s?\s[A-Za-z]{1,}\s[A-Za-z]{3,}|[A-Za-z]{2,}\s[A-Za-z]{1,}\s?[A-Za-z]?|[A-Za-z]+',
            #                           actual_name)
            # else:
            #     name_reg = re.findall(r'[A-Za-z]+\s[A-Za-z]+\-\s?[A-Za-z]+\s[A-Za-z]{2,}\s?\w?|[A-Za-z]+\-\s?[A-Za-z]+\s[A-Za-z]{2,}\s?\w?|[A-Za-z]+\-\s?[A-Za-z]+|[A-Za-z]{2,}\s?\s?\s[A-Za-z]{1,}\s[A-Za-z]{2,}\s[A-Za-z]+|[A-Za-z]{2,}\s[A-Za-z]{1,}\s?[A-Za-z]?\s[A-Za-z]+|[A-Za-z]{2,}\s?\s?\s[A-Za-z]{1,}\s[A-Za-z]{2,}|[A-Za-z]{2,}\s[A-Za-z]{1,}\s?[A-Za-z]?|[A-Za-z]+',
            #                           actual_name)
            # print("name_value",name_reg)
            # full_name = " ".join(map(str, name_reg))
            # if re.search('[A-Za-z]+\-\s[A-Za-z]+', full_name):
            #     fname=full_name.replace('- ',"-")
            #     full_name=fname
            #     print("name",full_name)
            # if re.search(r'\s\s',full_name):
            #     full_name=full_name.replace(re.findall(r'\s\s',full_name)[0]," ")
            # if full_name=='':
            #     if name_val == 'License_Id':
            #         temp_name = ' '.join(map(str, text_value.split(licenseid, 1)[1].split()[:6]))
            #
            #         temp_name = temp_name.replace('DONOR', "")
            #         temp_name = avoid.replace(temp_name)
            #         print(temp_name)
            #         name_regex1 = re.findall(r'[A-Za-z]+\-?\b', temp_name)
            #         print(name_regex1)
            #         full_name = " ".join(map(str, name_regex1))
            #
            #         print(full_name)
            # if "DAVID JOSEPH JR" in full_name:
            #     full_name="BUTLER DAVID JOSEPH"
            # if "EARLENE MICHELLEPUIG" in full_name:
            #     full_name="SHAEARLENE MICHELLE PUIG"
            self.name.put(actual_full_name)
        except Exception as e:
            full_name=""
            return full_name

    def get_date(self,text,license_id):
        string_date=''
        actual_expiry_date, actual_dob_date, actual_issue_date, issue_date, data, string_date_value = '', '', '', '', '', ''
        try:
            # Todo:To get all date format from text
            expiry_date=''
            text = text.replace(license_id, '')
            # val = re.findall(
            #     r'\b(?:(1[0-2]|0?[1-9])[./-](3[01]|[12][0-9]|0?[1-9])|(3[01]|[12][0-9]|0?[1-9])[./-](1[0-2]|0?[1-9]))[./-]((19|20|21)(?:[0-9]{2})?[0-9]{2}|[0-9]{2})',
            #     text)
            val = re.findall(r'(((0[0-9]|1[0-2])\s?[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])\s?[./-](19|20|21|22)\d\d|((0[0-9]|1[0-2]))[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-]\d\d)|((0[0-9]|1[0-2])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-](19|20|21|22)\d\d)|(0[0-9]|1[0-9])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-](19|20|21|22)\d\d)', text)
            date_val1 = []
            for item in val:
                date_val1.append(" ".join(item))
            string_date = "".join(map(str, date_val1))
            if re.search(r'\b\s(!?G|O|8|9|6)',string_date):
                string_date=string_date.replace(re.findall(r'\b\s(!?G|O|8|9|6)',string_date)[0],'0')
            # Todo:To remove all white spaces and [,/.]
            if re.search(r'\d{2}[./-]?\d{2}[./-]?\d{4}',string_date):
                date_val = re.findall(r'\d{2}[./-]?\d{2}[./-]?\d{4}', string_date)
                string_date_value = ",".join(map(str, date_val))
            else:
                date_val = re.findall(r'\d{2}[./-]?\d{2}[./-]?\d{2}', string_date)
                string_date_value = ",".join(map(str, date_val))
            for dob in date_val:
                if 'o' in dob:
                    dob = dob.replace("o", "0")
                if ' ' in dob:
                    dob = dob.replace(" ", "")
                if "/" in dob:
                    dob = dob.replace(" ", "")
                    dob = dob.replace("/", "")
                if "-" in dob:
                    dob = dob.replace(" ", "")
                    dob = dob.replace("-", "")
                if "." in dob:
                    dob = dob.replace(" ", "")
                    dob = dob.replace(".", "")
                # Todo:Proper Date Format (mm/dd/yyyy)
                dob = dob[0:2] + '/' + dob[2:4] + '/' + dob[4:8]
                self.date.append(dob)
            # Todo:to change format to (yyyy/mm/dd)
            print(self.date)
            for value in self.date:
                if re.match(r'\b\d{2}[./-]\d{2}[./-]\d{2}\b', value):
                    self.actual_date.append(datetime.datetime.strptime(value, '%m/%d/%y').strftime('%y/%m/%d'))
                else:
                    self.actual_date.append(datetime.datetime.strptime(value, '%m/%d/%Y').strftime('%Y/%m/%d'))
            data = " ".join(map(str, self.actual_date))
            print("in date_val", data)
            # Todo:To get birth date,expire date and issue date value

            if re.match(r'\b\d{2}[./-]\d{2}[./-]\d{2}\b', data):
                dob = max(self.actual_date)
                issue_date = min(self.actual_date)
                if dob != "" and issue_date != "":
                    for date in self.actual_date:
                        if date > issue_date and date < dob:
                            expiry_date = date
                    actual_expiry_date = datetime.datetime.strptime(expiry_date, '%y/%m/%d').strftime('%m/%d/%y')
                    actual_dob_date = datetime.datetime.strptime(dob, '%y/%m/%d').strftime('%m/%d/%y')
                    actual_issue_date = datetime.datetime.strptime(issue_date, '%y/%m/%d').strftime('%m/%d/%y')
            else:
                expiry_date = max(self.actual_date)
                dob = min(self.actual_date)
                if expiry_date != "" and dob != "":
                    for date in self.actual_date:
                        if date > dob and date < expiry_date:
                            issue_date = date
                    actual_expiry_date = datetime.datetime.strptime(expiry_date, '%Y/%m/%d').strftime('%m/%d/%Y')
                    actual_dob_date = datetime.datetime.strptime(dob, '%Y/%m/%d').strftime('%m/%d/%Y')
                    actual_issue_date = datetime.datetime.strptime(issue_date, '%Y/%m/%d').strftime('%m/%d/%Y')

            print('string_val', string_date_value)
            print("date",actual_expiry_date, actual_dob_date, actual_issue_date)
            return actual_expiry_date, actual_dob_date, actual_issue_date, string_date_value
        except Exception as E:
            try:
                if re.search(r'\b\d{2}[./-]\d{2}[./-]\d{4}\b', text):
                    if re.search(r'(=?(Issued|iss|ISS|Iss|ISSUED|es|Isa|SS488|Is|REN)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{4})', text):
                        issue_date = ' '.join(
                            map(str, text.split(re.findall(r'(=?Issued|iss|ISS|Isa|Iss|SS|es|ISSUED|488|Is|REN)', text)[0], 1)[1].split()[0:3]))
                        if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', issue_date):
                            actual_issue_date = re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', issue_date)[0]
                        elif re.search(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', issue_date):
                            actual_issue_date = re.findall(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', issue_date)[0]
                        elif re.search(r'(?!:)', issue_date):
                            actual_issue_date = ''
                    else:
                        actual_issue_date = ''

                    if re.search(r'(=?(EXP|Expires|Exp|Expiros|EXPIRES|EXPIROS|EER)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{4})', text):
                        expiry_date = ' '.join(map(str, text.split(
                            re.findall(r'(=?EXP|Expires|Exp|Expiros|EXPIRES|EXPIROS|EER)', text)[0], 1)[1].split()[0:3]))
                        print("expiry date",expiry_date)
                        if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', expiry_date):
                            actual_expiry_date = re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', expiry_date)[0]
                        elif re.search(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', expiry_date):
                            actual_expiry_date = re.findall(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', expiry_date)[0]

                        elif re.search(r'(=?:)', expiry_date):
                            actual_expiry_date = ''
                    else:
                        actual_expiry_date = ''

                    if re.search(
                            r'(=?(DOB:dob|DOB|gos|DO|Sa|so|nos|BIRTHDATE|Doe|birthdate|cor|Cor|Birth|BIRTH|D.O.B.|Dos|dos|pos|POS|DoB|birth|Bo:|Dso|DOB.|dob.|-poe|poe)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{4})',
                            text):
                        dob = ' '.join(map(str, text.split(
                            re.findall(
                                r'(=?DOB:dob|gos|DO|Sa|DOB|nos|DOB.|so|Doe|BIRTHDATE|cor|Cor|birthdate|Birth|BIRTH|D.O.B.|Dos|dos|pos|POS|DoB|birth|Bo:|Dso|dob.|-poe|poe)',
                                text)[0], 1)[1].split()[0:3]))
                        if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', dob):
                            actual_dob_date = re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', dob)[0]

                        elif re.search(r'(?!:)\s?\d+[-/.]?\d+[-/.]?\d+', dob):
                            actual_dob_date = re.findall(r'(?!:)\s?\d+[-/.]?\d+[-/.]?\d+', dob)[0]

                            print("birth", actual_dob_date)
                        elif re.search(r'(=?:)', dob):
                            actual_dob_date = ''

                    else:
                        actual_dob_date = ''


                else:

                        if re.search(r'(=?(Issued|iss|ISS|Iss|ISSUED|Isa|es|488|Is)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{2})', text):
                            issue_date = ' '.join(
                                map(str,
                                    text.split(re.findall(r'(=?Issued|iss|Isa|es|ISS|Iss|ISSUED|488|Is)', text)[0], 1)[1].split()[0:3]))
                            if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', issue_date):
                                actual_issue_date = re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', issue_date)[0]
                            elif re.search(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', issue_date):
                                actual_issue_date = re.findall(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', issue_date)[0]
                            elif re.search(r'(?!:)', issue_date):
                                actual_issue_date = ''
                        else:
                            actual_issue_date = ''

                        if re.search(r'(=?(EXP|Expires|Exp|Expiros|EXPIRES|EXPIROS|EER)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{2})',
                                     text):
                            expiry_date = ' '.join(map(str, text.split(
                                re.findall(r'(=?EXP|Expires|Exp|Expiros|EXPIRES|EXPIROS|EER)', text)[0], 1)[1].split()[
                                                            0:3]))
                            if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', expiry_date):
                                actual_expiry_date = re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', expiry_date)[0]
                            elif re.search(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', expiry_date):
                                actual_expiry_date = re.findall(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', expiry_date)[0]

                            elif re.search(r'(=?:)', expiry_date):
                                actual_expiry_date = ''
                        else:
                            actual_expiry_date = ''

                        if re.search(
                                r'(=?(DOB:dob|DOB|BIRTHDATE|Sa|gos|DO|Doe|cor|Cor|nos|so|birthdate|Birth|BIRTH|D.O.B.|Dos|dos|pos|POS|DoB|birth|Bo:|Dso)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{2})',
                                text):
                            dob = ' '.join(map(str, text.split(
                                re.findall(r'(=?DOB:dob|DOB|Sa|gos|nos|Doe|cor|Cor|DO|so|BIRTHDATE|birthdate|Birth|BIRTH|D.O.B.|Dos|dos|pos|POS|DoB|birth|Bo:|Dso)', text)[0], 1)[
                                                        1].split()[0:3]))
                            if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', dob):
                                actual_dob_date = re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', dob)[0]

                            elif re.search(r'(?!:)\s?\d+[-/.]?\d+[-/.]?\d+', dob):
                                actual_dob_date = re.findall(r'(?!:)\s?\d+[-/.]?\d+[-/.]?\d+', dob)[0]

                                print("birth", actual_dob_date)
                            elif re.search(r'(=?:)', dob):
                                actual_dob_date = ''

                        else:
                            actual_dob_date = ''
                return actual_expiry_date, actual_dob_date, actual_issue_date, string_date_value
            except Exception as e:
                print(e)

    def get_licence_details1(self,text,keys,values):
            try:

                print(text)

                text=text.replace('SOS ',"505")
                text=text.replace("'","")
                if re.search('(!?AŽ|AŻ)',text):
                    text=text.replace(re.findall('(!?AŽ|AŻ)',text)[0],"AZ")

                address, street,street1, state, zipcode, city, = self.get_address(text,keys,values)
                get_licence_id = self.get_id(text,state)
                if get_licence_id!='':
                    expiry_date, dob, issue_date,date_val = self.get_date(text,get_licence_id)
                else:
                    get_licence_id=' '
                    expiry_date, dob, issue_date, date_val = self.get_date(text, get_licence_id)

                #name = self.get_name(text, street,street,get_licence_id,state,date_val,keys,values)
                thread=threading.Thread(target=self.get_name,args=(text, street,street,get_licence_id,state,date_val,
                                                                   keys,values,))
                thread.start()
                name=self.name.get()

                return get_licence_id, expiry_date, dob, issue_date, address, name, state, zipcode, city,date_val
            except Exception as e:
                pass


class NameSequence(Enum):
    FN_LN = 1
    FN_MN_LN = 2
    LN_FN_MN = 3
    LN_FN_MN_SUF = 4
    SUF_FN_MN_LN = 5