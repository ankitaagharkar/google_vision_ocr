import copy
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
import avoid
from Common import Common
from dateparser import parse

class Licence_details:

    def __init__(self):
        self.api_key='AIzaSyC7SQ-1m0M6dN9L4E2aUhTM1ihAfTXIA0k '
        self.date_val=[]
        self.date = []
        self.regex_val=''

        self.result = {}

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
        self.c= Common()

        with open('../config/city.json', 'r') as data_file:
            self.cities = json.load(data_file)
        with open('../config/filtering.json', 'r') as data:
            self.state_value = json.load(data)
        
       
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
                    if re.match(r'[A-Za-z]{1}', self.licence_id[0]):
                        return self.licence_id[0].upper()
                    else:
                        return self.licence_id[0]
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

    def get_address(self,details):
        global address_details, address_val, street_address
        try:
            name,actual_city=[],[]
            if len(details[0]["address"])>2:
                if re.search(r'(!?(\w+)?\s?(\d+)?\s?[A-Za-z]+)',details[0]["name"][0]):
                        if re.search(r'\b(!?([A-Za-z]+)?\s?[2]\s?[A-Za-z]+)',details[0]["address"][0]):
                            address_details = details[0]['address']
                            street_address = address_details[1]
                            address_val = address_details[2]
                            if len(details[0]['name'])>=2:
                                name.append(details[0]['name'][1])
                                name.append(details[0]['address'][0])
                            else:
                                name.append(details[0]['name'][0])
                                name.append(details[0]['address'][0])
                            value_name = ' '.join(map(str, name))
                        else:
                            if re.search(r'\b(!?\d+\s[A-Za-z]+)', details[0]["address"][0]):
                                if re.search(r'\b(!?([A-Za-z])?\s?(\d+)?\s?([A-Za-z]+)?)',details[0]["address"][1]):
                                    address_details = details[0]['address']
                                    street_address = address_details[0]+" "+address_details[1]
                                    address_val = address_details[2]
                            else:
                                address_details=details[0]['address']
                                street_address=address_details[0]
                                address_val=address_details[1]

                            name=details[0]['name']
                            if re.search('\d+',name[0]):
                                name.pop(0)
                            value_name = ' '.join(map(str, name))
                else:
                    address_details = details[0]['address']
                    street_address = address_details[0]
                    address_val = address_details[1]

                    name = details[0]['name']
                    value_name = ' '.join(map(str, name))
            else:
                address_details = details[0]['address']
                street_address = address_details[0]
                address_val = address_details[1]

                name = details[0]['name']
                value_name = ' '.join(map(str, name))

            address=" ".join(map(str,address_details))
            address=avoid.address_replace(address)
            address_val=avoid.address_replace(address_val)
            asp=address_val.split()

            data = re.findall(r'\b((!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\,?\s(\d{5}(?:\s?\-\s?\d{4})|\d{5}(?:\s?\.\s?\d{4})|\d{5}))',
                address)
            if data!=[]:
                if re.search(r'(!?[A-Za-z]{2}\s\d{5}\s\d{2,4})',address):
                    address=address.replace(re.findall(r'(!?[A-Za-z]{2}\s\d{5}\s\d{2,4})',address)[0], data[0][0])
                if len(asp)>=2:
                    # state_zipcode=" ".join(address_val.split()[-2:])
                    state, zipcode, _ = self.c.get_address_zipcode(address," ".join(address_val.split()[-2:]))
                else:
                    state, zipcode, _ = self.c.get_address_zipcode(address, address_val.split()[-1])
            else:
                if len(asp)>=2:
                    state, zipcode, _ = self.c.get_address_zipcode(address, address_val.split()[-3])
                    if not re.search(r'\b(!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\b',state):
                        state, zipcode, _ = self.c.get_address_zipcode(address,address_val.split()[-2])
                else:
                    state, zipcode, _ = self.c.get_address_zipcode(address, address_val.split()[-1])
            if zipcode!='':
                city = address_val.split()[0:-2]
                city = " ".join(map(str, city))
            else:
                city = address_val.split()[0:-1]
                city = " ".join(map(str, city))
            city =city.replace(',', '')
            city = city.replace('.', '')
            city = city.replace(state, "")
            for i in range(len(self.cities['city'])):
                if city.lower() == self.cities['city'][i].lower():
                    actual_city.append(self.cities['city'][i])

            if actual_city == []:
                city_dict, street_dict = {}, {}
                actual_city.append(
                    ' '.join(map(str, address_val.split(state, 1)[0].split()[-1:])))

                actual_city[0] = actual_city[0].replace(',', '')
                actual_city[0] = actual_city[0].replace('.', '')

            else:
                if city != actual_city[0]:
                    actual_city[0] = actual_city[0].upper()
                else:
                    actual_city.append(actual_city[0])
            city=actual_city[0]
            if city.lower()=='BROOKLAMIN'.lower():
                city="BROOKLAWN"
            full_address = ' '.join(s[:1].upper() + s[1:] for s in street_address.split())
            full_address = full_address.replace("DRI", "DR")
            full_address = full_address.replace("STAPT ", "ST APT ")
            full_address = full_address.replace("ss ", "55 ")
            full_address = full_address.replace(" AD", " RD")
            full_address = full_address.replace(" RO", " RD")
            if zipcode=='':
                gmaps = googlemaps.Client(key=self.api_key)
                json_val = gmaps.geocode(full_address + " " + city + " " + state)
                if json_val!=[]:
                    for i in range(len(json_val[0]['address_components'])):
                        # print(json_val[0]['address_components'][i]['types'])
                        if json_val[0]['address_components'][i]['types'] == ['postal_code']:
                            zipcode = json_val[0]['address_components'][i]['long_name']
                else:
                    zipcode=''


            if 'DRVE' in full_address:
                full_address = full_address.replace('DRVE', 'DRIVE')

            if 'IENA.SE' in full_address:
                full_address = full_address.replace('IENA.SE', 'TERRASE')
            if 'ŽENA.SE' in full_address:
                full_address = full_address.replace('IENA.SE', 'TERRASE')
            if 'RDA' in full_address:
                full_address = full_address.replace('RDA', 'RD')
            if 'START' in full_address:
                full_address = full_address.replace('START', 'ST APT')

            if re.search('(!?NV|OH|TX|WA|CT|MA|NC|CO|DE|ID|IN|KS|ME|MS|MT|NE|NH|ND|SD|UT|VT|WI)',state):
                if re.search(r'\b(!?8)\s?(\d+)?\b', full_address):
                    full_address = full_address.replace('8', ' ',1)
            if re.search('((!?(S|s))\d+)',full_address):
                full_address=full_address.replace(re.findall('(!?S|s\d+)',full_address)[0],"5",1)

            return full_address, state, zipcode, city, value_name
        except Exception as e:
            address=state=zipcode=city=value_name=''
            return address, state, zipcode, city,value_name

    def get_name(self,text_value,date,state,text,license_id):
        try:
            if re.search(r'\d+\-?\.?\d+\s[A-Za-z]+',text_value):
                text_value=re.findall(r'(!?[A-Za-z]+\s[A-Za-z]+)',text_value)[0]
            text_value = text_value.replace('.', " ")
            text_value = text_value.replace(license_id, "")
            text_value = text_value.replace('Ž', "Z")
            value,avoid_signature = avoid.name_replace(text_value,date,state,text)
            if avoid_signature in value:
                value=value.replace(avoid_signature,"")
            name=value.split()
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
            actual_full_name=actual_full_name.upper()

            return actual_full_name
        except:
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
               
                val = re.findall(r'((0[0-9]|1[0-2])\s?[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])\s?[./-](19|20|21|22)\d\d|(0[0-9]|1[0-2])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-]\d\d|(0[0-9]|1[0-2])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-](19|20|21|22)\d\d|(0[0-9]|1[0-9])\s?(0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-](19|20|21|22)\d\d|(0[0-9]|1[0-9])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])\s?(19|20|21|22)\d\d)', text)
                date_val = []
                for i in range(len(val)):
                    date_val.append(val[i][0])
                string_date_value = " ".join(map(str, date_val))
                if re.search(r'\b\s(!?G|O|8|9|6)',string_date):
                    string_date_value=string_date.replace(re.findall(r'\b\s(!?G|O|8|9|6)',string_date)[0],'0')

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
                datea,dates=[],[]
                if re.match(r'\b(19|20|21|22)\d\d\s?[./-]?\s?(0[0-9]|1[0-2])\s?[./-]?(0[1-9]|1[0-9]|2[0-9]|3[0-1])\b', data):


                    expiry_date = max(self.actual_date)
                    dob = min(self.actual_date)
                    if expiry_date != "" and dob != "":
                        for date in self.actual_date:
                            if date > dob and date < expiry_date:
                                issue_date = date
                        actual_expiry_date = datetime.datetime.strptime(expiry_date, '%Y/%m/%d').strftime('%m/%d/%Y')
                        actual_dob_date = datetime.datetime.strptime(dob, '%Y/%m/%d').strftime('%m/%d/%Y')
                        actual_issue_date = datetime.datetime.strptime(issue_date, '%Y/%m/%d').strftime('%m/%d/%Y')

                    
                else:
                    for i in range(len(self.actual_date)):
                        datea.append(parse(self.actual_date[i]))
                    for i in range(len(datea)):
                        dates.append(datea[i].strftime('%Y/%m/%d'))
                    if dates[0]>datetime.datetime.now().year:
                        dates[0] = dates[0].replace(year=dates[0].year - 100)
                    expiry_date = max(dates)
                    dob = min(dates)
                    if dob != "" and expiry_date != "":
                        for date in dates:
                            if date > dob and date < expiry_date:
                                issue_date = date
                        actual_expiry_date = datetime.datetime.strptime(expiry_date, '%Y/%m/%d').strftime('%m/%d/%y')
                        actual_dob_date = datetime.datetime.strptime(dob, '%Y/%m/%d').strftime('%m/%d/%y')
                        actual_issue_date = datetime.datetime.strptime(issue_date, '%Y/%m/%d').strftime('%m/%d/%y')
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

    def get_licence_details1(self,text,details):
            try:

               

                address, state, zipcode, city,value_name = self.get_address(details)
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

                name = self.get_name(value_name,date_val,state,text,get_licence_id)



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