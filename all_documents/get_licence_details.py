import datetime
import io

import googlemaps
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image
import sys
import difflib
import json
import re

from multiprocessing import Queue

from enum import Enum
sys.path.insert(0, '../image_processing')
sys.path.insert(0, '../all_documents')
import avoid
import Common
from dateparser import parse

class Licence_details:

    def __init__(self):
        self.api_key='AIzaSyC7SQ-1m0M6dN9L4E2aUhTM1ihAfTXIA0k '
        self.date_val=[]
        self.date = []
        self.regex_val=''

        self.result = {}
        self.text_val = []
        self.keys = []
        self.values = []
        self.description = []

        self.name=Queue()
        self.actual_date = []
        self.date_val1 = []
        self.zip_code=[]
        self.licence_id=''
        self.regex_value=[]
        self.code=''
        self.first_name_original,self.last_name_original,self.middle_name_original,self.first_name_processed,self.last_name_processed,self.middle_name_processed={},{},{},{},{},{}
        self.regex_value,self.street,self.address,self.full_address=[],[],[],[]
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
            text = text.replace('.', "")
            text = text.replace(',', "")
            if re.search(r'(!?IA)', zip_code):
                text = text.replace(re.findall(r'(=?DD\s\d\w+)', text)[0], " ")
            print(zip_code)
            text=text.replace('DL','')
            state_regex=re.findall(r"\b(!?AL|AK|AS|AZ|AŽ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE"
                r"|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)",zip_code)
            print(len(self.state_value['data']))
            if state_regex != []:
                for i in range(len(self.state_value['data'])):
                    if self.state_value['data'][i]['state'] in state_regex[0]:
                        self.regex_val=self.state_value['data'][i]['license_id']
                        # print("regex_state_value",self.state_value['data'][i]['state'],self.regex_value)
                print("state regex",self.regex_val)
                self.licence_id = re.findall(self.regex_val, text)
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
                    elif re.search(r'\b(!?[2]\d{4}\s\d{5}\s\d{5})\b',self.licence_id[0]):
                        s=[]
                        print("Hi")
                        split_text=self.licence_id[0].split('2',1)
                        join_text="".join(split_text)
                        s.append('Z')
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
                    elif re.search(r'(!?o|O)\w?\s?', self.licence_id[0]):
                        self.licence_id[0] = self.licence_id[0].replace(re.findall(r'(!?o|O)\w?\s?', self.licence_id[0])[0], "0")
                    else:
                        return self.licence_id[0]
                if re.search(r'(!?OH)',zip_code):
                    if re.match(r'[A-Za-z]{1}', self.licence_id[1]):
                        return self.licence_id[1].upper()
                    else:
                        return self.licence_id[1]
                if re.search(r'(!?o|O)\w?\s?', self.licence_id[0]):
                    self.licence_id[0] = self.licence_id[0].replace(
                        re.findall(r'(!?o|O)\w?\s?', self.licence_id[0])[0], "0")
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
                if re.search(r'(!?o|O)\w?\s?', License_Id[0]):
                    License_Id[0] = self.licence_id[0].replace(re.findall(r'(!?o|O)\w?\s?',License_Id[0])[0], "0")
        except Exception as E:
            print("in licence id",E)
            self.get_licence_id=''
            return self.get_licence_id

    def get_address(self,text_value,texts,path):
        try:
            final_output=[]
            date_val1=[]
            # value=text_value.replace('.','')
            text_value = text_value.replace('END', '')
            text_value = text_value.replace('End', '')
            text_value = text_value.replace('None/', '')
            text_value = text_value.replace('None', '')
            text_value = text_value.replace('NONE/', '')
            text_value = text_value.replace('NONE', '')
            if re.search(r'\s\s', text_value):
                text_value = text_value.replace(re.findall(r'\s\s', text_value)[0], "")
            value=avoid.address_replace(text_value)
            date_val1 = []
            all_number = re.findall(r"\s\d{1}\s?[A-Za-z]+\s[A-Za-z]+|\s?\s\d{1}\s[A-Za-z]+|\s?\s\d{1}\s?[A-Za-z]+|\s\d{4}\s?[A-Za-z]+|\s\d+[A-Za-z]+\s[A-Za-z]+|\d{2}\s[A-Za-z]+|\:?\d{2}\s[A-Za-z]+|\d{2}-\d{2}\s[A-Za-z]+|\s?\d{3}\w?\s\w+\,?|\s\d{3}\s\d{1}|\w*\s?\d{5}\-?\.?\d{1,4}|\w*\s?\d{5}\s?\-?\.?\s?[A-Za-z]+\d{2,3}|\w*\s?\d{5}\s\w*|\w*\s?\d{5}",value)
            number_val1 = ' '.join(map(str, all_number))
            if re.search(r'\s\s',number_val1):
                number_val1=number_val1.replace(re.findall(r'\s\s',number_val1)[0]," ")
            print("Number val", number_val1)
            number_val = number_val1
            if re.search('(!?00\sNJ)',number_val):
                number_val=number_val.replace('00',"")
            data = re.findall(r'\b((!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\,?\s(\d{5}\d{1,4}|\d{5}(?:\s?\-\s?\d{1,4})|\d{5}(?:\s?\-?\s?[A-Za-z]+\d{1,4})|\d{5}(?:\s?\.\s?\d{4})|\d{5}))', number_val)
            if data!=[]:
                self.code=data[0][0]
            else:

                all_number = re.findall(r"\s\d{1}\s?[A-Za-z]+\s[A-Za-z]+|\s?\s\d{1}\s[A-Za-z]+|\s?\s\d{1}\s?[A-Za-z]+|\s\d{4}\s?[A-Za-z]+|\s\d+[A-Za-z]+\s[A-Za-z]+|\d{2}\s[A-Za-z]+|\:?\d{2}\s[A-Za-z]+|\d{2}-\d{2}\s[A-Za-z]+|\s?\d{3}\w?\s\w+\,?|\s\d{3}\s\d{1}|\w*\s?\d{5}\-?\.?\d{1,4}|\w*\s?\d{5}\s?\-?\.?\s?[A-Za-z]+\d{2,3}|\w*\s?\d{5}\s\w*|\w*\s?\d{5}", value)
                number_val1 = ' '.join(map(str, all_number))
                if re.search(r'\s\s',number_val1):
                    number_val1=number_val1.replace(re.findall(r'\s\s',number_val1)[0]," ")
                print("Number val", number_val1)
                number_val = number_val1
                data = re.findall(
                    r'\b((!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH'
                    r'|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT'
                    r'|VT|VI|VA|WA|WV|WI|WY)\,?\s(\d{5}\d{1,4}|\d{5}(?:\s?\-\s?\d{1,4})|\d{5}(?:\s?\-?\s?['
                    r'A-Za-z]+\d{1,4})|\d{5}(?:\s?\.\s?\d{4})|\d{5}))', number_val)
                if data != []:
                    self.code = data[0][0]
                else:

                    val1 = re.findall(
                        r"\s(\d+)\-?\.?\s?([A-Za-z]+)?\.?\-?\s?(\w+)?\.?\-?\s?(\w+)?\s?([ŽA-Za-z]+)?\.?\-?\s?(\d+)?\s?([A-Za-z]+)?\-?\.?\s?(\d+)?\s?(\w+)?\s?\.?\,?\s?(!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\s\s?\w+",
                        value)

                    val = ""
                    for item in val1:
                        val = val + " ".join(item)
                    data = re.findall(
                        r'\b(!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\b',
                        val)
                    print("else data", data)
                    self.code=data[0]
            state_code=''
            state_code=self.code
            state_val=''
            ignore_val = re.findall(
                r'\b(\s\d+\s?([A-Za-z]+)?\s?([A-Za-z]+)?\s?\s?([A-Za-z]+)?\s?(\d+)?\s?([ŽA-Za-z]+)?\s?(\d+)?[#.,/]?\s?([ŽA-Za-z]+)\s?[#.,/]?\s?(\w*)?\.?\s?(!?AŻ|NU|\.?NL|N\.|NJI|SU|NA|Na|NW|NIIN|NI|AJ|NO)\s?\w+)',
                text_value)

                # r'\b(\s\d+\s([A-Za-z]+)?\s([A-Za-z]+)?\s?\s([A-Za-z]+)?\s?(\d+)?\s?([A-Za-z]+)?\s?(\d+)?\s?([A-Za-z]+)\s?[#.,/]?\s?(\w*)?\s?(!?AŻ|NU |\.?NL|N\.|NJI | SU | NA | Na | NW |NI|AJ| NO)\s?\w+)',
                # text_value)

            if ignore_val!=[]:
                if re.search(r'\b(!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\b',text_value):
                    state_val = re.findall(
                        r'\b(!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)',
                        self.code)
                    state_val = state_val[0]

                else:
                    if re.search(ignore_val[0][::-1][0], text_value):
                        state_val = ignore_val[0][::-1][0]
            else:
                state_val = re.findall(
                    r'\b(!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)',
                    self.code)
                state_val = state_val[0]

            status, points = self.get_state_coordinates(texts, state_val)
            if not status and not points:
                print('We could not find state in this image')
            elif not status:
                content = self.rotate_image(path,points[0])
                texts = self.get_texts_from_bytes(content)
                self.code=state_val
                status, points = self.get_state_coordinates(texts,state_val)
            if status:
                data_box, text_height = self.generate_data_box(points[0],points[1],points[2],points[3],state_val)
                final_output,line_data = self.generate_lines(data_box,text_height,state_val)

            final_output[1] = final_output[1].replace(".","")
            final_output[1]=avoid.address_replace(final_output[1])
            self.code=state_code
            street=re.findall(r'(!?\w?\d+\s?\-?\s?(\d+)?\s?[A-Za-z]+)',final_output[1])[0][0]
            data = re.findall(
                r'[A-Za-z]+\s?[.,]?\s\b(!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|AŻ|NU|\.?\s?NL|N\.|NJI|SU|NA|Na|NW|NI|AJ|NO|CO|CT|DE|DC|FM|FL|GA|GU'
                r'|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT'
                r'|VT|VI|VA|WA|WV|WI|WY)\,?\s?\b', final_output[1])
            address = self.c.find_between_r(final_output[1], street, data[0])
            print("zip code", self.code)
            full_address = street + address + self.code
            state, zipcode, city = self.c.get_address_zipcode(full_address, self.code)
            actual_city=''
            city = city.replace("1oWA", "IOWA")
            full_address = full_address.replace("1oWA", "IOWA")
            city = city.replace(",", "")
            city = city.replace(".", "")
            # full_address = full_address.replace(",", "")
            # full_address = full_address.replace(".", "")
            for i in range(len(self.cities['city'])):
                if city.lower()==self.cities['city'][i].lower():
                    actual_city = self.cities['city'][i]

            if actual_city == '':
                city = ' '.join(map(str, value.split(self.code, 1)[0].split()[-1:]))
                print(city)
            elif city != actual_city:
                city = actual_city.upper()
            else:
                city = actual_city
            city=city.replace('.','')
            # city = city.replace(",", "")
            city = city.replace(".", "")
            full_address = self.c.find_between_r(full_address, street, city)
            full_address = street + full_address
            if re.search('(!?' + state + r')', full_address):
                st = re.compile(r'(!?' + state + r')', re.IGNORECASE)
                full_address = full_address.replace(st.findall(full_address)[0], '')
            print("address", full_address)
            full_address = ' '.join(s[:1].upper() + s[1:] for s in full_address.split())


            full_address = full_address.replace("DRI", "DR")
            full_address = full_address.replace("STAPT ", "ST APT ")
            full_address = full_address.replace("ss ", "55 ")

                # for i in range(len(self.NJ_Cities['NJ'])):
                #     if self.NJ_Cities['NJ'][i].lower() in city.lower():
                #         nj_city=self.NJ_Cities['NJ'][i]
                #
                # print("CITY",city.lower,nj_city.lower())
                # if city.lower() == nj_city.lower():
                #     state='NJ'
            if zipcode=='':
                gmaps = googlemaps.Client(key=self.api_key)
                json_val = gmaps.geocode(full_address + " " + actual_city + " " + state)
                if json_val!=[]:
                    for i in range(len(json_val[0]['address_components'])):
                        # print(json_val[0]['address_components'][i]['types'])
                        if json_val[0]['address_components'][i]['types'] == ['postal_code']:
                            zipcode = json_val[0]['address_components'][i]['long_name']
                else:
                    zipcode=''
            city = city.replace(",", "")
            city = city.replace(".", "")
            if 'DRVE' in full_address:
                full_address = full_address.replace('DRVE', 'DRIVE')

            if 'IENA.SE' in full_address:
                full_address = full_address.replace('IENA.SE', 'TERRASE')
            if 'ŽENA.SE' in full_address:
                full_address = full_address.replace('IENA.SE', 'TERRASE')
            if 'RDA' in full_address:
                full_address = full_address.replace('RDA', 'RD')

            if re.search('(!?NV|OH|TX|WA|CT|MA|NC|CO|DE|ID|IN|KS|ME|MS|MT|NE|NH|ND|SD|UT|VT|WI)',state):
                if re.search(r'\b(!?8)\s?(\d+)?\b', full_address):
                    street=street.replace('8'," ",1)
                    full_address = full_address.replace('8', ' ',1)
                    final_output[1] = final_output[1].replace('8', " ",1)
                if re.search(r'\b\s?(!?2)\s?(\w+)?\b', final_output[0]):
                    final_output[0] = final_output[0].replace('2', " ")
            if re.search('((!?(S|s))\d+)',full_address):
                full_address=full_address.replace(re.findall('(!?S|s\d+)',full_address)[0],"5",1)
            value_name=' '.join(map(str,final_output))
            return full_address, street, state, zipcode, city,value_name,data[0]
        except Exception as e:
            address, street, state, zipcode, city, value_name, zip_val='','','','','','',''
            return address, street, state, zipcode, city,value_name,zip_val

    def get_name(self,text_value,street,date,state,text):

        actual_name=''
        text_value = text_value.replace('.', " ")
        text_value = text_value.replace('Ž', "Z")
        value,avoid_signature = avoid.name_replace(text_value,date,state,text)
        if avoid_signature in value:
            value=value.replace(avoid_signature,"")

        if re.search(r'\s\s', value):
            value = value.replace(re.findall(r'\s\s', value)[0], " ")
        name_value=[]
        val = re.compile(
            r'\s?([A-Za-z]+)?(\-)?\s?([A-Za-z]+)?(\-)?\s?([A-Za-z]+)?(\-)?\s?([A-Za-z]+)?(\-)?\s?(\d+)?\s?([A-Za-z]+)?(\-)?\s?([A-Za-z]+)?(\-)?\s?([A-Za-z]+)?(\-)?\s([A-Za-z]+)?\s?[,.]?\s?\s?([A-Za-z]+)?\s?(\d+)?\s?(!?' + street + r')\b',
            re.IGNORECASE)
        name_reg_val = val.findall(value)
        for item in name_reg_val:
            name_value.append(" ".join(item))
        name_val = "".join(map(str, name_value))
        name_val = name_val.replace(street, "")
        if re.search(r'\s\s', name_val):
            name_val = name_val.replace(re.findall(r'\s\s', name_val)[0], " ")
        name_val = name_val.split('2', 1)
        name_val = "".join(name_val)
        name_regex = re.findall(r'[A-Za-z]+\s?\s?\-?\s?\s?\b', name_val)
        actual_name = " ".join(map(str, name_regex))
        actual_name = avoid.replace(actual_name)
        if actual_name == '':
            actual_name = ' '
            return actual_name


        else:
            if re.search(r'\s\s', actual_name):
                actual_name = actual_name.replace(re.findall(r'\s\s', actual_name)[0], " ")
            checked = []
            name = actual_name.split()
            for e in name:
                if e not in checked:
                    checked.append(e)
            actual_name=" ".join(map(str,checked))
            print("in name", actual_name)
            name_reg = re.findall(
                r'[A-Za-z]+\s?\-\s?\s?[A-Za-z]+\s\s?[A-Za-z]{2,}\s?\w?|[A-Za-z]+\s[A-Za-z]+\s?\-\s?[A-Za-z]+|[A-Za-z]+\s[A-Za-z]+\s?\-\s?[A-Za-z]+\s[A-Za-z]{2,}\s?\w?|[A-Za-z]+\s?\-\s?\s?[A-Za-z]+|[A-Za-z]{2,}\s?\s?\s[A-Za-z]{1,}\s?\s[A-Za-z]{2,}\s?\s[A-Za-z]+|[A-Za-z]{2,}\s?\s[A-Za-z]{1,}\s?\s?[A-Za-z]?\s?\s[A-Za-z]+|[A-Za-z]{2,}\s?\s?\s[A-Za-z]{1,}\s?\s[A-Za-z]{2,}|[A-Za-z]{2,}\s?\s[A-Za-z]{1,}\s?[A-Za-z]?|[A-Za-z]+',
                actual_name)
            full_name = " ".join(map(str, name_reg))

            print(full_name)

            if re.search('[A-Za-z]+\s?\-\s?\s?[A-Za-z]+\s?\s?[A-Za-z]+', full_name):
                fname = full_name.replace(' - ', "-")
                full_name = fname
            if re.search(r'\s\s', full_name):
                full_name = full_name.replace(re.findall(r'\s\s', full_name)[0], " ")
            name = full_name.split()
            actual_full_name=''
            if name!=[]:
                name_seq, first_name, middle_name, last_name = '', '', '', ''
                for i in range(len(self.state_value['data'])):
                    if self.state_value['data'][i]['state'] == state:
                        name_seq = self.state_value['data'][i]['name_seq']

                if len(name) >= 2:
                    for i in range(len(name)):
                        if len(name[0]) == 1:
                            name.pop(0)
                print(name)
                if 'FN_MN_LN_SUF' == name_seq:
                    if len(name) == 1:
                        if len(name[0]) >= 2:
                            first_name = name[0]
                        last_name = ""
                        middle_name = ""
                    elif len(name) == 2:
                        if len(name[0]) >= 2:
                            first_name = name[0]
                        else:
                            name[0] = name[0].replace(name[0], " ")

                        if name[0] != ' ':
                            if len(name[1]) >= 1:
                                last_name = name[1]
                            else:
                                name[1] = name[1].replace(name[1], " ")
                        else:
                            last_name = name[1]
                    elif len(name) == 3:
                        if len(name[0]) >= 2:
                            first_name = name[0]
                        else:
                            name[0] = name[0].replace(name[0], " ")
                        if name[0] != ' ':
                            if len(name[1]) >= 1:
                                middle_name = name[1]
                            else:
                                name[1] = name[1].replace(name[1], " ")
                        else:
                            if len(name[1]) == 1:
                                middle_name = name[1]
                            else:
                                first_name = name[1]
                        if name[1] != ' ':
                            if len(name[2]) >= 1:
                                last_name = name[2]
                            else:
                                name[2] = name[2].replace(name[2], " ")
                        else:
                            last_name = name[2]
                    elif len(name) == 4:
                        if len(name[0]) >= 2:
                            first_name = name[0]
                        else:
                            name[0] = name[0].replace(name[0], " ")

                        if name[0] != ' ':
                            if len(name[1]) >= 1:
                                middle_name = name[1]
                            else:
                                name[1] = name[1].replace(name[1], " ")

                        if name[1] != ' ':
                            if len(name[2]) >= 1:
                                last_name = name[2]
                            else:
                                name[2] = name[2].replace(name[2], " ")

                        if name[2] != ' ':
                            if len(name[3]) >= 1:
                                last_name = last_name + " " + name[3]

                        if name[0] == ' ' or name[3] == ' ':
                            first_name = name[1]
                            middle_name = name[2]
                            last_name = name[3]
                        elif name[1] == ' ':
                            first_name = name[0]
                            last_name = name[2]
                            last_name = last_name + " " + name[3]

                        elif name[2] == ' ':
                            first_name = name[0]
                            middle_name = name[1]
                            last_name = name[3]

                    actual_full_name = first_name + " " + middle_name + " " + last_name

                elif 'LN_FN_MN_SUF' == name_seq:
                    if len(name) == 1:
                        if len(name[0]) >= 2:
                            last_name = name[0]
                        first_name = ""
                        middle_name = ""
                    elif len(name) == 2:
                        if len(name[0]) >= 2:
                            last_name = name[0]
                        else:
                            name[0] = name[0].replace(name[0], " ")

                        if name[0] != ' ':
                            if len(name[1]) >= 1:
                                first_name = name[1]
                            else:
                                name[1] = name[1].replace(name[1], " ")
                        else:
                            first_name = name[1]

                    elif len(name) == 3:
                        if len(name[0]) >= 2:
                            last_name = name[0]
                        else:
                            name[0] = name[0].replace(name[0], " ")
                        if name[0] != ' ':
                            if len(name[1]) >= 1:
                                first_name = name[1]
                            else:
                                name[1] = name[1].replace(name[1], " ")
                        if name[1] != ' ':
                            if len(name[2]) >= 1:
                                middle_name = name[2]
                            else:
                                name[2] = name[2].replace(name[2], " ")

                    elif len(name) == 4:
                        if len(name[0]) >= 2:
                            last_name = name[0]
                        else:
                            name[0] = name[0].replace(name[0], " ")
                        if name[0] != ' ':
                            if len(name[1]) >= 1:
                                first_name = name[1]
                            else:
                                name[1] = name[1].replace(name[1], " ")
                        if name[1] != ' ':
                            if len(name[2]) >= 1:
                                middle_name = name[2]
                            else:
                                name[2] = name[2].replace(name[2], " ")
                        if name[2] != ' ':
                            if len(name[3]) >= 1:
                                middle_name = middle_name + " " + name[3]

                        if name[0] == ' ' or name[3] == ' ':
                            last_name = name[1]
                            first_name = name[2]
                            middle_name = name[3]
                        elif name[1] == ' ':
                            last_name = name[0]
                            middle_name = name[2]
                            middle_name = middle_name + " " + name[3]

                        elif name[2] == ' ':
                            last_name = name[0]
                            first_name = name[1]
                            middle_name = name[3]
                    else:
                        first_name=[0]
                        last_name=""
                        middle_name=""
                    actual_full_name = last_name + " " + first_name + " " + middle_name
                # actual_full_name=actual_full_name.replace('-','')
                actual_full_name=actual_full_name.replace('.','')
                actual_full_name=actual_full_name.replace(',','')
            else:
                actual_full_name=''
            return actual_full_name

    def get_date(self,text,license_id):
            string_date=''

            actual_expiry_date, actual_dob_date, actual_issue_date, issue_date, data, string_date_value = '', '', '', '', '', ''
            try:
                # Todo:To get all date format from text
                expiry_date=''
                text_val = text.replace(license_id, '')
                if re.search('(!?\d+[./-]?\d+[./-]?49\d+)',text_val):
                    text=text_val.replace(re.findall('\d+[./-]?\d+[./-]?(!?49)\d+',text_val)[0],'19')
                # val = re.findall(
                #     r'\b(?:(1[0-2]|0?[1-9])[./-](3[01]|[12][0-9]|0?[1-9])|(3[01]|[12][0-9]|0?[1-9])[./-](1[0-2]|0?[1-9]))[./-]((19|20|21)(?:[0-9]{2})?[0-9]{2}|[0-9]{2})',
                #     text)
                val = re.findall(r'((0[0-9]|1[0-2])\s?[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])\s?[./-](19|20|21|22)\d\d|(0[0-9]|1[0-2])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-]\d\d|(0[0-9]|1[0-2])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-](19|20|21|22)\d\d|(0[0-9]|1[0-9])\s?(0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-](19|20|21|22)\d\d|(0[0-9]|1[0-9])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])\s?(19|20|21|22)\d\d)', text)
                date_val = []
                for i in range(len(val)):
                    date_val.append(val[i][0])
                string_date_value = "".join(map(str, date_val))
                if re.search(r'\b\s(!?G|O|8|9|6)',string_date):
                    string_date_value=string_date.replace(re.findall(r'\b\s(!?G|O|8|9|6)',string_date)[0],'0')
                # Todo:To remove all white spaces and [,/.]
                # if re.search(r'\d{2}[./-]?\d{2}[./-]?\d{4}',string_date):
                #     date_val = re.findall(r'\d{2}[./-]?\d{2}[./-]?\d{4}', string_date)
                #     string_date_value = ",".join(map(str, date_val))
                # else:
                #     date_val = re.findall(r'\d{2}[./-]?\d{2}[./-]?\d{2}', string_date)
                #     string_date_value = ",".join(map(str, date_val))
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
                        self.actual_date.append(value)
                    else:
                        self.actual_date.append(datetime.datetime.strptime(value, '%m/%d/%Y').strftime('%Y/%m/%d'))
                data = " ".join(map(str, self.actual_date))
                # print("in date_val", data)
                # Todo:To get birth date,expire date and issue date value
                datea,dates=[],[]
                if re.match(r'(0[0-9]|1[0-2])\s?[./-]?(0[1-9]|1[0-9]|2[0-9]|3[0-1])\s?[./-]?(19|20|21|22)\d\d', data):

                    for i in range(len(self.actual_date)):
                        datea.append(parse(self.actual_date[i]))
                    for i in range(len(datea)):
                        dates.append(datea[i].strftime('%Y/%m/%d'))

                    expiry_date = max(dates)
                    dob = min(dates)
                    if dob != "" and expiry_date != "":
                        for date in dates:
                            if date > dob and date < expiry_date:
                                issue_date = date
                        actual_expiry_date = datetime.datetime.strptime(expiry_date, '%Y/%m/%d').strftime('%m/%d/%y')
                        actual_dob_date = datetime.datetime.strptime(dob, '%Y/%m/%d').strftime('%m/%d/%y')
                        actual_issue_date = datetime.datetime.strptime(issue_date, '%Y/%m/%d').strftime('%m/%d/%y')
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

                # print('string_val', string_date_value)
                print("date",actual_expiry_date, actual_dob_date, actual_issue_date)
                from datetime import date

                current_date=date.today()
                current_date=current_date.year-15
                dob=parse(actual_dob_date)
                if dob.year<current_date:
                    actual_dob_date=actual_dob_date
                else:
                    actual_dob_date=''
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

    def get_data_in_box(self, bounding):
        bounding_x1, bounding_y1 = bounding[0]
        bounding_x2, bounding_y2 = bounding[1]

        min_overlap = 37
        output_values = []
        for key, values in enumerate(self.result):
            print(values)
            # Get bounding box by taking minimum of x and y, maximum of x and y.
            # this will solve problem of rotated texts as well.
            min_x = min(values[1], key=lambda x: x[0])[0]
            min_y = min(values[1], key=lambda x: x[1])[1]
            max_x = max(values[1], key=lambda x: x[0])[0]
            max_y = max(values[1], key=lambda x: x[1])[1]
            text_area = (max_x - min_x) * (max_y - min_y)
            x_overlap = max(0, min(bounding_x2, max_x) - max(bounding_x1, min_x))
            y_overlap = max(0, min(bounding_y2, max_y) - max(bounding_y1, min_y))
            overlapArea = x_overlap * y_overlap
            if overlapArea > 0 and (overlapArea / text_area) * 100 >= min_overlap:
                output_values.append([values[0], values[1]])
        return output_values

    def get_text_from_path(self, path):
        client = vision.ImageAnnotatorClient()
        with io.open(path, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        response = client.document_text_detection(image=image)
        texts = response.text_annotations
        print(texts[-1].description)
        return texts

    def get_texts_from_bytes(self, content):
        client = vision.ImageAnnotatorClient()
        image = types.Image(content=content)
        response = client.document_text_detection(image=image)
        texts = response.text_annotations
        return texts

    def get_state_coordinates(self, texts, state):
        self.description = texts[0]
        self.description.description=str(self.description.description).replace('END','')
        self.description.description=str(self.description.description).replace('End','')
        self.description.description = str(self.description.description).replace('NONE/', '')
        self.description.description = str(self.description.description).replace('None/', '')
        self.description.description=str(self.description.description).replace('None','')
        self.description.description=str(self.description.description).replace('NONE','')
        if re.search(r'\s\s', self.description.description):
            self.description.description = self.description.description.replace(re.findall(r'\s\s', self.description.description)[0], "")
        state_val = ''
        # state_name = re.findall(r'\b(!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\,?\s(\d{5}\d{1,4}|\d{5}(?:\s?\-\s?\d{1,4})|\d{5}(?:\s?\-?\s?[A-Za-z]+\d{1,4})|\d{5}(?:\s?\.\s?\d{4})|\d{5})', str(self.description.description))
        # print(state_name)

        ignore_val = re.findall(
            r'\b(\s?(\d+)?\s?([ŽA-Za-z]+)?\s?(\d+)?[#.,/]?\s?([ŽA-Za-z]+)\s?[#.,/]?\s?(\w*)?\.?\.?\s?(!?AŻ|NU|NL|N\.|NJI|SU|NA|Na|NW|NIIN|NI|AJ|NO)\s?\w+)',
            str(self.description.description))

        # r'\b(\s\d+\s([A-Za-z]+)?\s([A-Za-z]+)?\s?\s([A-Za-z]+)?\s?(\d+)?\s?([A-Za-z]+)?\s?(\d+)?\s?([A-Za-z]+)\s?[#.,/]?\s?(\w*)?\s?(!?AŻ|NU |\.?NL|N\.|NJI | SU | NA | Na | NW |NI|AJ| NO)\s?\w+)',
        # text_value)

        if ignore_val != []:
            if re.search(
                    r'\b(!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\b',
                    str(self.description.description)):
                state_val = re.findall(
                    r'\b(!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)',
                    state)
                if state_val!=[]:
                    state_val = state_val[0]
                else:
                    if re.search(ignore_val[0][::-1][0], str(self.description.description)):
                        state_val = ignore_val[0][::-1][0]
            else:
                if re.search(ignore_val[0][::-1][0], str(self.description.description)):
                    state_val = ignore_val[0][::-1][0]
            state = state_val

        for text in texts[1:]:
            self.text_val.append(text.description)
            vertices = [(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices]
            self.keys.append(text.description)
            self.values.append(vertices)
        self.result = zip(self.keys, self.values)

        for text in texts[1:]:
            if difflib.get_close_matches(text.description, [state], cutoff=0.90):
                print('we got state name', state)
                vertices = [(vertex.x, vertex.y)
                            for vertex in text.bounding_poly.vertices]
                print(vertices)
                first_point = vertices[0]
                second_point = vertices[1]
                third_point = vertices[2]
                last_point = vertices[3]

                rotated_image = False
                if first_point[1] > third_point[1]:
                    rotated_image = True
                    rotation_deg = -90
                elif second_point[1] > last_point[1]:
                    rotated_image = True
                    rotation_deg = 90
                if rotated_image:
                    return False, [rotation_deg]
                else:
                    return True, [first_point, second_point, third_point, last_point]
        return False, []

    def generate_data_box(self, first_point, second_point, third_point, last_point,state_val):

        text_height = (first_point[1] - third_point[1])
        height = round(text_height * 4.5)
        if re.search('(!?MD)',state_val):
            third_pt_y = third_point[1] + round((9 * (third_point[1] - last_point[1])))
            third_pt_x = third_point[0] + round((9 * (third_point[0] - last_point[0])))
            print('TP', third_pt_x, third_pt_y)
            last_pt_y = last_point[1] + round((10.5 * (last_point[1] - third_point[1])))
            last_pt_x = last_point[0] + round((10.5 * (last_point[0] - third_point[0])))
            print('LP', last_pt_x, last_pt_y)
            first_pt_y = first_point[1] + round((10.5 * (first_point[1] - second_point[1])))
            first_pt_x = first_point[0] + round((10.5 * (first_point[0] - second_point[0])))
            first_pt_y += height
            print('FP', first_pt_x, first_pt_y)
            second_pt_y = second_point[1] + round((9 * (second_point[1] - first_point[1])))
            second_pt_x = second_point[0] + round((9 * (second_point[0] - first_point[0])))
            second_pt_y += height
            print('TP', second_pt_x, second_pt_y)
            data_box = self.get_data_in_box([(first_pt_x, first_pt_y), (third_pt_x, third_pt_y)])
        else:
            third_pt_y = third_point[1] + round((9.5 * (third_point[1] - last_point[1])))
            third_pt_x = third_point[0] + round((9.5 * (third_point[0] - last_point[0])))
            print('TP', third_pt_x, third_pt_y)
            last_pt_y = last_point[1] + round((9.5 * (last_point[1] - third_point[1])))
            last_pt_x = last_point[0] + round((9.5 * (last_point[0] - third_point[0])))
            print('LP', last_pt_x, last_pt_y)
            first_pt_y = first_point[1] + round((9.5 * (first_point[1] - second_point[1])))
            first_pt_x = first_point[0] + round((9.5 * (first_point[0] - second_point[0])))
            first_pt_y += height
            print('FP', first_pt_x, first_pt_y)
            second_pt_y = second_point[1] + round((9.5 * (second_point[1] - first_point[1])))
            second_pt_x = second_point[0] + round((9.5 * (second_point[0] - first_point[0])))
            second_pt_y += height
            print('TP', second_pt_x, second_pt_y)
            data_box = self.get_data_in_box([(first_pt_x, first_pt_y), (third_pt_x, third_pt_y)])

        return data_box, abs(text_height)
        """
        if rotated_image:
            data_box = self.get_data_in_box([(second_pt_x,second_pt_y),(last_pt_x,last_pt_y)])
        else:

        print(data_box)
        self.generate_lines(data_box,rotated_image,abs(text_height))

        first_pt = last_point
        second_pt_x = last_point[0] + (2 * (third_point[0]-last_point[0]))
        second_pt_y = last_point[1] + (2 * (third_point[1]-last_point[1]))
        fourth_pt_x = last_point[0] + (3 * (last_point[0]-first_point[0]))
        fourth_pt_y = last_point[1] + (3 * (last_point[1]-first_point[1]))
        third_pt_x = fourth_pt_x + (2 * (third_point[0]-last_point[0]))
        third_pt_y = fourth_pt_y + (2 * (third_point[1]-last_point[1]))

        #end_x = vertices[0][0] + (2 * abs(vertices[1][0]-vertices[0][0]))
        #end_y = vertices[0][1] + (4 * abs(vertices[0][1]-vertices[3][1]))
        refPt = []
        image = cv2.imread(path)
        #cv2.imshow("image", image)
        #cv2.waitKey(0)
        refPt.append((first_pt_x,first_pt_y))
        cv2.circle(image,(first_pt_x,first_pt_y), 2, (255,0,0), -1)
        refPt.append((second_pt_x,second_pt_y))
        cv2.circle(image,(second_pt_x,second_pt_y), 2, (255,0,0), -1)
        refPt.append((third_pt_x,third_pt_y))
        cv2.circle(image,(third_pt_x,third_pt_y), 2, (255,0,0), -1)
        refPt.append((last_pt_x,last_pt_y))
        cv2.circle(image,(last_pt_x,last_pt_y),2, (255,0,0), -1)
        print(refPt)




        #refPt.append((end_x,end_y))
        pilImage = self.cvToPil(image)
        pilImage.show()

        #cv2.imshow("image", image)
        #cv2.waitKey(0)
        break
        else:
            continue
        """
        return

    def cvToPil(self, cvImage):
        """Converts opencv format image to PIL object
        Args: cvImage: {numpy.ndarray}
        -- OpenCV or ndarray Image Returns: Image converted to PIL Image """
        pilImage = Image.fromarray(cvImage)
        return pilImage

    def generate_lines(self, data_box, text_height,state_val):
        text_height = round(0.60 * text_height)
        prev_y_pt = 0
        if re.search('(!?MD|VA|WA)',state_val):
            address_line_length = 3
            name_line_length = 2
        else:
            address_line_length = 2
            name_line_length = 2
        line_data = [[], []]
        generated_lines = 0
        print(text_height)
        for data in reversed(data_box):
            print(data)
            if ((data[1][0][1] - data[1][1][1]) - (data[1][2][1] - data[1][3][1])) > round(
                    text_height):
                print('this word seems to be off', data)
                continue
            if abs(data[1][0][1] - prev_y_pt) < text_height or abs(
                    data[1][1][1] - prev_y_pt) < text_height:
                prev_y_pt = data[1][0][1]
                print(prev_y_pt)
                if generated_lines <= address_line_length:
                    line_data[1].append(data[0])
                else:
                    line_data[0].append(data[0])
            else:
                print('new_line')
                generated_lines += 1
                prev_y_pt = data[1][0][1]
                if generated_lines <= address_line_length:
                    line_data[1].append(data[0])
                elif generated_lines <= address_line_length + name_line_length:
                    line_data[0].append(data[0])
                else:
                    break

        final_output = ['', '']
        for val in reversed(line_data[0]):
            if val != ',':
                final_output[0] = final_output[0] + ' ' + val
            else:
                final_output[0] = final_output[0] + val
        for val in reversed(line_data[1]):
            if val != ',':
                final_output[1] = final_output[1] + ' ' + val
            else:
                final_output[1] = final_output[1] + val

        print(final_output, line_data)
        return final_output, line_data

    def rotate_image(self, path, rotation_deg):
        ext = path.split('.')[-1]
        print('Rotating image by degress', rotation_deg)
        image = Image.open(path)
        image = image.rotate(rotation_deg)
        # pilImage = self.cvToPil(img2)
        # image.show()
        b = io.BytesIO()
        if ext.lower() in ('png'):
            save_ext = 'PNG'
        elif ext.lower() in ('jpg', 'jpeg'):
            save_ext = 'JPEG'
        image.save(b, save_ext)
        content = b.getvalue()
        return content

    def get_licence_details1(self,text,keys,values,texts,path):
            try:

                print(text)

                text=text.replace('SOS ',"505")
                text=text.replace("'","")


                address, street, state, zipcode, city,value_name,zip_val = self.get_address(text,texts,path)
                if state!='':
                    get_licence_id = self.get_id(text,state)
                else:
                    get_licence_id=' '

                if get_licence_id!=' ':
                    expiry_date, dob, issue_date,date_val = self.get_date(text,get_licence_id)
                else:
                    get_licence_id=' '
                    expiry_date, dob, issue_date, date_val = self.get_date(text, get_licence_id)
                # name=''
                if street!='':
                    name = self.get_name(value_name,street,date_val,state,text)
                else:
                    name=''


                # thread=threading.Thread(target=self.get_name,args=(text, street,street,get_licence_id,state,date_val,
                #                                                    keys,values,))
                # thread.start()
                # name=self.name.get()

                return get_licence_id, expiry_date, dob, issue_date, address, name, state, zipcode, city,date_val
            except Exception as e:
                pass




class NameSequence(Enum):
    FN_LN = 1
    FN_MN_LN = 2
    LN_FN_MN = 3
    LN_FN_MN_SUF = 4
    SUF_FN_MN_LN = 5