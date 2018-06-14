import copy
import datetime
import difflib

import googlemaps
import json
import re
from multiprocessing import Queue
from enum import Enum
import avoid
from Common import Common
from dateutil.parser import parse

DEBUG = False


class Licence_details:

    def __init__(self):


        self.result = {}

        self.keys = []
        self.values = []
        self.description = []

        self.name = Queue()
        self.actual_date = []
        self.date_val1 = []
        self.zip_code = []
        self.licence_id = ''
        self.regex_value = []
        self.code = ''
        self.first_name_original, self.last_name_original, self.middle_name_original, self.first_name_processed, self.last_name_processed, self.middle_name_processed = {}, {}, {}, {}, {}, {}
        self.regex_value, self.street, self.address, self.full_address = [], [], [], []
        self.street_address_original, self.state_original, self.city_original, self.zip_code_original, self.street_address_processed, self.state_processed, self.city_processed, self.zip_code_processed = {}, {}, {}, {}, {}, {}, {}, {}
        self.failure_regex = ''
        self.c = Common()
        with open('../config/config.json') as data_file:
            self.config = json.load(data_file)
        with open('../config/name', 'r') as data_file:
            self.name_list = json.load(data_file)
        with open('../config/city.json', 'r',encoding='utf-8') as data_file:
            self.cities = json.load(data_file)
        with open('../config/filtering.json', 'r') as data:
            self.state_value = json.load(data)

        self.api_key = self.config["google_map_key"]
        self.date_val = []
        self.date = []
        self.gmaps = googlemaps.Client(key=self.api_key)
        self.regex_val = ''

    def custom_print(self, *arg):
        if DEBUG:
            print(arg)

    # todo:License id details
    def get_id(self, text, zip_code):
        try:
            text = text.replace('.', "")
            text = text.replace(',', "")
            if re.search(r'(!?IA)', zip_code):
                text = text.replace(re.findall(r'(=?DD\s\d\w+)', text)[0], " ")
            text = text.replace('DL', '')
            state_regex = re.findall(
                r"\b(!?AL|AB|AK|AS|AZ|AŽ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE"
                r"|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)",
                zip_code)
            if state_regex != []:
                for i in range(len(self.state_value['data'])):
                    if self.state_value['data'][i]['state'] in state_regex[0]:
                        self.regex_val = self.state_value['data'][i]['license_id']
                self.licence_id = re.findall(self.regex_val, text)
                self.custom_print("license_id", self.licence_id)
                if self.licence_id == []:
                    for i in range(len(self.state_value['data'])):
                        if self.state_value['data'][i]['state'] in state_regex[0]:
                            self.failure_regex = self.state_value['data'][i]['failure_case']
                    self.licence_id = re.findall(self.failure_regex, text)

                if 'NJ' in state_regex[0]:
                    if re.search(r'\b(!?[0]\d{4}\s\d{5}\s\d{5})\b', self.licence_id[0]):
                        s = []
                        split_text = self.licence_id[0].split('0', 1)
                        join_text = "".join(split_text)
                        s.append('O')
                        s.append(join_text)
                        id = "".join(s)
                        return id
                    elif re.search(r'\b(!?[2]\d{4}\s\d{5}\s\d{5})\b', self.licence_id[0]):
                        s = []
                        split_text = self.licence_id[0].split('2', 1)
                        join_text = "".join(split_text)
                        s.append('Z')
                        s.append(join_text)
                        id = "".join(s)
                        return id
                    elif re.search(r'\b(!?[8]\d{4}\s\d{5}\s\d{5})\b', self.licence_id[0]):
                        s = []
                        split_text = self.licence_id[0].split('8', 1)
                        join_text = "".join(split_text)
                        s.append('B')
                        s.append(join_text)
                        id = "".join(s)
                        return id
                    elif re.search(r'(!?o|O)\w?\s?', self.licence_id[0]):
                        self.licence_id[0] = self.licence_id[0].replace(
                            re.findall(r'(!?o|O)\w?\s?', self.licence_id[0])[0], "0")
                    else:
                        return self.licence_id[0]
                if re.search(r'(!?OH)', zip_code):
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
                license_id = ''
                return license_id
        except Exception as E:
            self.custom_print("license_id Exception", E)
            self.get_licence_id = ''
            return self.get_licence_id

    # todo:address,state,city and zipcode details
    def get_address(self, details):
        global address_details, address_val, street_address, google_zipcode, value_name
        try:

            name, actual_city = [], []
            if re.search('\s(!?NH)\s'," ".join(map(str,details[0]['address']))) and re.search(r'(!?3|8|6|9)\.'," ".join(map(str,details[0]['address']))):
                    address_details = details[0]['address']
                    street_address = address_details[1]
                    street_address=street_address.replace('3.','')
                    address_val = address_details[2]
                    address_val=address_val.replace('-','')
                    value_name = address_details[0]
            elif 'dob' in details[0]["address"][0].lower():
                address_details = details[0]['address']
                street_address = address_details[1]
                address_val = address_details[2]
                name = details[0]['name']
                value_name = ' '.join(map(str, name))
            elif len(details[0]["address"]) > 2:
                if re.search(r'(!?(\w+)?\s?(\d+)?\s?[A-Za-z]+)', details[0]["name"][0]):
                    if re.search(r'\b(!?([A-Za-z]+)?\s?[2]\s?[A-Za-z]+)', details[0]["address"][0]):
                        address_details = details[0]['address']
                        street_address = address_details[1]
                        address_val = address_details[2]
                        if len(details[0]['name']) >= 2:
                            name.append(details[0]['name'][1])
                            name.append(details[0]['address'][0])
                        else:
                            name.append(details[0]['name'][0])
                            name.append(details[0]['address'][0])
                        value_name = ' '.join(map(str, name))
                    else:
                        if re.search(r'\b(!?\d+\s[A-Za-z]+)', details[0]["address"][0]) or re.search(r'\b(!?[8]\s?\d+)',
                                                                                                     details[0][
                                                                                                         "address"][1]):
                            if re.search(r'\b(!?([A-Za-z])?\s?(\d+)?\s?([A-Za-z]+)?)',
                                         details[0]["address"][1]):
                                address_details = details[0]['address']
                                street_address = address_details[0] + " " + address_details[1]
                                address_val = address_details[2]
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
            else:
                address_details = details[0]['address']
                street_address = address_details[0]
                address_val = address_details[1]

                name = details[0]['name']
                value_name = ' '.join(map(str, name))
            if re.search('\s(!?NH)\s'," ".join(map(str,details[0]['address']))) and re.search(r'(!?3|8|6|9)\.'," ".join(map(str,details[0]['address']))):

                    address = street_address+" "+address_val
                    address = avoid.address_replace(address)

            else:
                address = " ".join(map(str, address_details))
                address = avoid.address_replace(address)

            address_val = avoid.address_replace(address_val)
            address_val = address_val.replace(',', '')
            address = address.replace(',', '')
            address = address.replace('.', '')
            address_val = address_val.replace('.', '')
            # todo:to remove words before street number
            asp = address_val.split()
            is_val=re.findall(r'(!?([A-Za-z]+)?\s?[A-Za-z]+\s\d+\s)[A-Za-z]+', street_address)
            if is_val:
                if re.search(r'\d+\s?([A-Za-z]+)?\s?([A-Za-z]+)?\s?' + is_val[0][0] + '+', street_address):
                    is_digit = re.findall(r'\b\d+\b', street_address)
                else:
                    is_digit = re.findall(r'\b\d+\b', is_val[0][0])
                print("is_digit", is_digit)
                address_sp = street_address.split(is_digit[0])
                print("address_sp", address_sp)
                if not re.search(r'\b[A-Za-z]+\b', address_sp[0]):
                    pass
                else:
                    street_address = "".join(map(str, address_sp[1:]))
                    street_address = is_digit[0] + street_address
                    print("remove of the ", address)
            else:
                is_val = re.findall(r'(!?([A-Za-z]+)?\s?\w+\s\d+\s)',street_address)
                if is_val:
                    is_digit = re.findall(r'\b\d+\b', is_val[0][0])
                    print("is_digit", is_digit)
                    address_sp = street_address.split(is_digit[0])
                    print("address_sp", address_sp)
                    if not re.search(r'\b[A-Za-z]+\b', address_sp[0]):
                        pass
                    else:
                        street_address = "".join(map(str, address_sp[1:]))
                        street_address = is_digit[0] + street_address
                        print("remove of the ", address)
            if re.search(r'\d+\s\d+\-?\s\d+\,?\d+', address_val):
                address_val = address_val.replace(re.findall(r'\d+\s\d+\-?\s\d+\,?\d+', address_val)[0], '')
            # todo:to find state,city,zipcode
            data = re.findall(
                r'\b((!?AL|AB|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\,?\s(\d{5}(?:\-\d{4})|\d{5}(?:\s?\.\s?\d{4})|\d{5}))',
                address)
            if data != []:
                if re.search(r'(!?[A-Za-z]{2}\s\d{5}\s\d{2,4}|[A-Za-z]{2}\s\d{5}\s?\-\s?\d{2,4})',
                             address_val):
                    address = address.replace(re.findall(
                        r'(!?[A-Za-z]{2}\s\d{5}\s\d{2,4}|[A-Za-z]{2}\s\d{5}\s?\-\s?\d{2,4})',
                        address)[0], data[0][0])
                    address_val = address_val.replace(re.findall(
                        r'(!?[A-Za-z]{2}\s\d{5}\s\d{2,4}|[A-Za-z]{2}\s\d{5}\s?\-\s?\d{2,4})',
                        address_val)[0], data[0][0])
                if len(asp) >= 2:
                    # state_zipcode=" ".join(address_val.split()[-2:])
                    state, zipcode, city = self.c.get_address_zipcode(address, data[0][0])
                else:
                    state, zipcode, city = self.c.get_address_zipcode(address, address_val.split()[-1])
            else:
                # if len(asp)>=2:
                if len(asp) > 2:
                    # state, zipcode, city = self.c.get_address_zipcode(address, address_val.split()[-3])
                    state, zipcode, city = self.c.get_address_zipcode(address_val, asp, extra=True)
                    if re.search(r'[A-Za-z]+',zipcode):
                        a=re.findall(r'[A-Za-z]+\s?\d+\-?\d+|[A-Za-z]+', " ".join(map(str,asp[-2:])))[0]
                        address_val=address_val.replace(a,'')

                        state=address_val.split()[-1]
                        city=" ".join(address_val.split()[0:2])
                        zipcode=''
                        # state, zipcode, city = self.c.get_address_zipcode(address_val, asp,extra=True)
                    if not re.search(
                            r'\b(!?AL|AB|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\b',
                            state):
                        state, zipcode, city = self.c.get_address_zipcode(address,
                                                                          address_val.split()[-1])
                else:
                    state, zipcode, city = self.c.get_address_zipcode(address, address_val.split()[-1])
            city = city.replace(',', '')
            address_val = address_val.replace(',', '')
            city = city.replace('.', '')
            address_val = address_val.replace('.', '')
            if re.search(r'(!?BIOWA)', city):
                city = city.replace('BIOWA', 'IOWA')
            city = city.rstrip()
            address_val = address_val.rstrip()
            if re.search(r'\b' + state + r'\b', city):
                city = city.replace(state, "")
            actual_city.clear()
            for i in range(len(self.cities['city'])):
                city = city.replace(',', '')
                if city.lower() in self.cities['city'][i].lower():
                    actual_city.append(self.cities['city'][i])
            x = difflib.get_close_matches(city.lower(), [vt.lower() for vt in actual_city],
                                          cutoff=0.90)
            if x:
                city=x[0]
            else:
                actual_city=[]
                actual_city.append(
                    ' '.join(map(str, address_val.split(state, 1)[0].split()[-1:])))

                actual_city[0] = actual_city[0].replace(',', '')
                actual_city[0] = actual_city[0].replace('.', '')
                city = actual_city[0]
            if city.lower() == 'BROOKLAMIN'.lower():
                city = "BROOKLAWN"
            full_address = ' '.join(s[:1].upper() + s[1:] for s in street_address.split())
            full_address = full_address.replace("DRI", "DR")
            full_address = full_address.replace("HTH", "11TH")
            full_address = full_address.replace("STAPTA", "ST APT")
            full_address = full_address.replace("STAPT", "ST APT ")
            full_address = full_address.replace("ss ", "55 ")
            full_address = full_address.replace("RDUTE  ", "ROUTE ")
            full_address = full_address.replace("AVENUF", "AVENUE")
            full_address = full_address.replace("CI", "CT")
            full_address = full_address.replace("CTE", "CT")
            full_address = full_address.replace("FI", "")
            full_address = full_address.replace(" EN ", "")
            full_address = full_address.replace("COUPTOR", "COURT")
            full_address = full_address.replace("•", "")
            full_address = full_address.replace(" -", "")
            full_address = full_address.replace(".", "")

            if re.search(r'[A-Za-z]+', zipcode) or zipcode == '' or len(zipcode.split('-')[0]) >= 6:

                json_val = self.gmaps.geocode(full_address + " " + city + " " + state+" USA")
                if json_val != []:
                    for i in range(len(json_val[0]['address_components'])):
                        # #print(json_val[0]['address_components'][i]['types'])
                        if json_val[0]['address_components'][i]['types'] == ['postal_code']:
                            zipcode = json_val[0]['address_components'][i]['long_name']
                else:
                    zipcode = ''
            else:
                google_zipcode=''
                json_val = self.gmaps.geocode(full_address + " " + city + " " + state)
                if json_val != []:
                    for i in range(len(json_val[0]['address_components'])):
                        # #print(json_val[0]['address_components'][i]['types'])
                        if json_val[0]['address_components'][i]['types'] == ['postal_code']:
                            google_zipcode = json_val[0]['address_components'][i]['long_name']
                    if google_zipcode!='':
                        if zipcode.split('-')[0] != google_zipcode:
                            if re.search(r'-',zipcode):
                                z=zipcode.split('-')
                                zipcode = google_zipcode
                                zipcode=zipcode+"-"+z[1]
                            else:
                                zipcode=google_zipcode
                        

            zipcode = zipcode.replace('...', '')
            zipcode = zipcode.replace('.', '')
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
            full_address = full_address.replace("STAPTI.", "ST APT 1")
            if re.search('(!?NV|OH|TX|WA|CT|MA|NC|CO|DE|ID|IN|KS|ME|MO|MS|MT|NE|NH|ND|SD|UT|VT|WI)', state):
                if re.search(r'\b(!?8)\s?(\d+)?\b', full_address):
                    full_address = full_address.replace('8', ' ', 1)

            if re.search('((!?(S|s))\d+)', full_address):
                full_address = full_address.replace(re.findall('(!?S|s\d+)', full_address)[0], "5",
                                                    1)
            if not re.search(r'[A-Za-z]+', full_address):
                full_address = ''

            # json_val = self.gmaps.geocode(full_address + " " + city + " " + state + " " + zipcode+" USA")
            # junk_words=["dr","apt","mission","st","ave","unit","rd","ln","lane","pl","grn","ct","circle","drive","avenue","street","terrase","terrace","road","court","route","av","blvd"]
            # x = difflib.get_close_matches(full_address.split()[-1].lower(), [vt.lower() for vt in junk_words],cutoff=0.90)
            # if not x:
            #     x = difflib.get_close_matches(full_address.split()[-2].lower(), [vt.lower() for vt in junk_words], cutoff=0.90)
            # print("x value",x)
            # if not x:
            #     if json_val != []:
            #         address = json_val[0]['formatted_address']
            #         if full_address != address.split(',')[0]:
            #             full_address = address.split(',')[0]

            if full_address.split()[-1].lower() in city.split()[0].lower():
                if len(city.split())>1:
                    full_address=full_address.replace(city.split()[0],'',1)
            if 'PG' and city:
                city=city.replace('PG','UPPER MARLBORO PG')

            return full_address.upper(), state.upper(), zipcode, city.upper(), value_name
        except Exception as e:
            address = state = zipcode = city = value_name = ''
            return address, state, zipcode, city, value_name

    # todo:first,middle and last name details
    def get_name(self, text_value, date, state, text, license_id):
        global x, actual_full_name
        try:
            text_value = text_value.lstrip()
            text_value = text_value.rstrip()
            state=state.replace('T9K','AB')

            val = date.split(" ")
            avoid_signature = ''

            print("state in name",state)
            if state=='AB':
                for i in val:
                    st = parse(i)
                    rep = st.strftime('%d %b %Y')
                    # val[i] = val[i].replace(rep.upper(), "")
                    text_value = text_value.replace(rep.upper(), "")
            t1 = text_value.split()
            avoid1 = ["LM","LR","No","Dups","EN", "FN", "LN", "IN", "LR", "LA",'Identification','Card','ID','#','card','ovaryland','LR.','UN']
            result=[]
            for i in t1:
                if not i in avoid1:
                    result.append(i)
            if result!=[]:
                t1=result
            text_value = " ".join(map(str, t1))
            text_value = text_value.replace(license_id, "")

            text_value = text_value.replace('Driver License', "")

            text_value = text_value.replace('LICENSE', "")
            text_value = text_value.replace(',', " ")
            text_value = text_value.replace('Address', "")
            text_value = text_value.replace("DRIVER'S", "")
            text_value = text_value.replace('DRIVER', "")
            text_value = text_value.replace('2', " ")
            text_value = text_value.replace('1', " ")
            text_value = text_value.lstrip()
            text_value = text_value.rstrip()
            if re.search(r'[A-Za-z]+\s\s[A-Za-z]+', text_value):
                text_value = text_value.replace(re.findall(r'\s\s', text_value)[0], re.findall(r'\s', text_value)[0], 1)
            if re.search('[A-Za-z]+\-\s[A-Za-z]+|[A-Za-z]+\s\-[A-Za-z]+', text_value):
                text_value = text_value.replace(re.findall(r'\s', text_value)[0], "",1 )
            # if re.search(r'\b[A-Za-z]+\s?\-\s?\s?[A-Za-z]+\b', text_value):
            #     text_value = text_value.replace(re.findall(r'\s', text_value)[0], "", 1)
            # else:
            #     text_value = text_value.replace('-', "",1)
            if re.search(r'\d+\-?\.?(\d+)?\s[A-Za-z]+', text_value):
                text_value = " ".join(map(str, re.findall(r'(!?[A-Za-z]+\-?)', text_value)))
            if re.search(r'\d{2,}\s?[A-Za-za-z]+', text_value):
                actual_full_name = ''
                return actual_full_name
            text_value = text_value.replace('.', " ")
            text_value = text_value.replace('Ž', "Z")
            text_value = text_value.replace('È', "")

            value, avoid_signature = avoid.name_replace(text_value, date, state, text)
            if avoid_signature in value:
                value = value.replace(avoid_signature, "")
            if 'iss' in value.lower():
                value = value.replace(re.findall(r'(!?iss|ISS|iSS|Iss)', value)[0], "")
            if 'FEED' in value:
                value=value.replace('FEED','')
            name_seq, first_name, middle_name, last_name = '', '', '', ''
            for i in range(len(self.state_value['data'])):
                if self.state_value['data'][i]['state'] in state:
                    name_seq = self.state_value['data'][i]['name_seq']
            x=[]
            if 'FN_MN_LN_SUF' == name_seq:
                x = difflib.get_close_matches(value.split()[0].lower(), [vt.lower() for vt in self.name_list['names']],
                                              cutoff=0.88)
            elif 'LN_FN_MN_SUF' == name_seq:
                if len(value.split())>1:
                    x = difflib.get_close_matches(value.split()[1].lower(), [vt.lower() for vt in self.name_list['names']],
                                                  cutoff=0.88)
            if x:
                value=" ".join(map(str, value.upper().rpartition(x[0].upper())))
                value=value.rstrip()
            name = value.split()
            if len(name) >= 2:
                for i in range(len(name)):
                    if len(name[0]) == 1:
                        name.pop(0)
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
                elif len(name) == 5:
                    if len(name[0]) >= 2:
                        first_name = name[0]
                    else:
                        name[0] = name[0].replace(name[0], " ")

                    if name[0] != ' ':
                        if len(name[1]) >= 1:
                            first_name = first_name + " " + name[1]
                        else:
                            name[1] = name[1].replace(name[1], " ")

                    if name[1] != ' ':
                        if len(name[2]) >= 1:
                            first_name = first_name + " " + name[2]
                        else:
                            name[2] = name[2].replace(name[2], " ")

                    if name[2] != ' ':
                        if len(name[3]) >= 1:
                            middle_name = name[3]
                    if name[3] != ' ':
                        if len(name[4]) >= 1:
                            last_name = name[4]

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
                elif len(name) == 5:
                    if len(name[0]) >= 2:
                        last_name = name[0]
                    else:
                        name[0] = name[0].replace(name[0], " ")

                    if name[0] != ' ':
                        if len(name[1]) >= 1:
                            last_name = last_name + " " + name[1]
                        else:
                            name[1] = name[1].replace(name[1], " ")

                    if name[1] != ' ':
                        if len(name[2]) >= 1:
                            last_name = last_name + " " + name[2]
                        else:
                            name[2] = name[2].replace(name[2], " ")

                    if name[2] != ' ':
                        if len(name[3]) >= 1:
                            first_name = name[3]
                    if name[3] != ' ':
                        if len(name[4]) >= 1:
                            middle_name = name[4]

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
                else:
                    first_name = [0]
                    last_name = ""
                    middle_name = ""
                actual_full_name = last_name + " " + first_name + " " + middle_name
            # actual_full_name=actual_full_name.replace('-','')
            actual_full_name = actual_full_name.replace('.', '')
            actual_full_name = actual_full_name.replace(',', '')
            actual_full_name = actual_full_name.upper()

            return actual_full_name
        except:
            actual_full_name = ''
            return actual_full_name

    # todo:DOB,issue date and expiry date details
    def get_date(self, text, license_id):
        string_date = ''

        actual_expiry_date, actual_dob_date, actual_issue_date, issue_date, data, string_date_value = '', '', '', '', '', ''
        try:
            # Todo:To get all date format from text
            expiry_date = ''
            text_val = text.replace(license_id, '')
            if re.search('(!?\d+[./-]?\d+[./-]?49\d+)', text_val):
                text = text_val.replace(re.findall('\d+[./-]?\d+[./-]?(!?49)\d+', text_val)[0],
                                        '19')

            val = re.findall(
                r'((0[0-9]|1[0-2])\s?[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])\s?[./-](19|20|21|22)\d\d'
                r'|(0[0-9]|1[0-2])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-]\d\d'
                r'|(0[0-9]|1[0-2])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-](19|20|21|22)\d\d'
                r'|(0[0-9]|1[0-9])\s?(0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-](19|20|21|22)\d\d'
                r'|(0[0-9]|1[0-9])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])\s?(19|20|21|22)\d\d'
                r'|(0[0-9]|1[0-2])\s?[./-]?(0[1-9]|1[0-9]|2[0-9]|3[0-1])\s?[./-]?(19|20|21|22)\d\d'
                r'|(0[0-9]|1[0-2])\s?[,:./-]?(0[1-9]|1[0-9]|2[0-9]|3[0-1])\s?[,:./-]?(19|20|21|22)\d\d'
                r'|(0\s?[0-9]|1\s?[0-2])\s?[,:./-]\s?(0\s?[1-9]|1\s?[0-9]|2\s?[0-9]|3\s?[0-1])\s?[,:./-]?(19|20|21|22)\d\d'
                r'|(0[1-9]|1[0-9]|2[0-9]|3[0-1])\s(JAN|FEB|MAR|APR|MAY|JUN|JULY|JUL|AUG|SEPT|SEP|OCT|NOV|DEC|Jan|Feb|Mar|Apr|May|Jun|July|Jul|Aug|Sept|Sep|Oct|Nov|Dec|january|february|march|april|may|june|july|august|september|october|november|december|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)\s(19|20|21|22)\d\d|(19|20|21|22)\d\d\s?\-(JAN|FEB|MAR|APR|MAY|JUN|JULY|JUL|AUG|SEPT|SEP|OCT|NOV|DEC|Jan|Feb|Mar|Apr|May|Jun|July|Jul|Aug|Sept|Sep|Oct|Nov|Dec|january|february|march|april|may|june|july|august|september|october|november|december|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)\-(0[1-9]|1[0-9]|2[0-9]|3[0-1]))',
                text)
            date_val = []
            date_val1 = []
            for i in range(len(val)):
                date_val.append(val[i][0])
            for i in range(len(date_val)):
                if re.search(r'\d{2}\s[A-Za-z]+\s\d{4}|\d{4}\-[A-Za-z]+\-\d{2}', date_val[i]):
                    st = parse(date_val[i])
                    date_val1.append(st.strftime('%m/%d/%Y'))
            if date_val1 != []:
                date_val = date_val1
            string_date_value = " ".join(map(str, date_val))
            if re.search(r'\b\s(!?G|O|8|9|6)', string_date):
                string_date_value = string_date.replace(
                    re.findall(r'\b\s(!?G|O|8|9|6)', string_date)[0], '0')

            for dob in date_val[:4]:
                if 'o' in dob:
                    dob = dob.replace("o", "0")
                if ' ' in dob:
                    dob = dob.replace(" ", "")
                if ":" in dob:
                    dob = dob.replace(" ", "")
                    dob = dob.replace(":", "")
                if "," in dob:
                    dob = dob.replace(" ", "")
                    dob = dob.replace(",", "")
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
            string_date_value = " ".join(map(str, self.date))
            # Todo:to change format to (yyyy/mm/dd)
            for value in self.date:
                if re.match(r'\b\d{2}[./-]\d{2}[./-]\d{2}\b', value):
                    self.actual_date.append(value)
                else:
                    self.actual_date.append(
                        datetime.datetime.strptime(value, '%m/%d/%Y').strftime('%Y/%m/%d'))
            data = " ".join(map(str, self.actual_date))
            datea, dates = [], []
            if re.match(
                    r'\b(19|20|21|22)\d\d\s?[./-]?\s?(0[0-9]|1[0-2])\s?[./-]?(0[1-9]|1[0-9]|2[0-9]|3[0-1])\b',
                    data):

                expiry_date = max(self.actual_date)
                dob = min(self.actual_date)
                if expiry_date != "" and dob != "":
                    for date in self.actual_date:
                        if date > dob and date < expiry_date:
                            issue_date = date
                    actual_expiry_date = datetime.datetime.strptime(expiry_date,
                                                                    '%Y/%m/%d').strftime('%m/%d/%Y')
                    actual_dob_date = datetime.datetime.strptime(dob, '%Y/%m/%d').strftime(
                        '%m/%d/%Y')
                    actual_issue_date = datetime.datetime.strptime(issue_date, '%Y/%m/%d').strftime(
                        '%m/%d/%Y')

                from datetime import date

                current_date = date.today()
                current_date = current_date.year - 15
                dob = parse(actual_dob_date)
                if dob.year < current_date:
                    actual_dob_date = actual_dob_date
                    # actual_dob_date = actual_dob_date.replace(str(parse(actual_dob_date).year),str(parse(actual_dob_date).year - 100))

                else:
                    actual_dob_date = ''
            else:
                for i in range(len(self.actual_date)):
                    datea.append(parse(self.actual_date[i]))
                for i in range(len(datea)):
                    dates.append(datea[i].strftime('%Y/%m/%d'))
                if dates[0] > str(datetime.datetime.now().year):
                    dates[0] = dates[0].replace(str(parse(dates[0]).year),
                                                str(parse(dates[0]).year - 100))
                expiry_date = max(dates)
                dob = min(dates)
                if dob != "" and expiry_date != "":
                    for date in dates:
                        if date > dob and date < expiry_date:
                            issue_date = date
                    actual_expiry_date = datetime.datetime.strptime(expiry_date,
                                                                    '%Y/%m/%d').strftime('%m/%d/%y')
                    actual_dob_date = datetime.datetime.strptime(dob, '%Y/%m/%d').strftime(
                        '%m/%d/%y')
                    actual_issue_date = datetime.datetime.strptime(issue_date, '%Y/%m/%d').strftime(
                        '%m/%d/%y')
            return actual_expiry_date, actual_dob_date, actual_issue_date, string_date_value

        except Exception as E:
            try:
                if re.search(r'\b\d{2}[./-]\d{2}[./-]\d{4}\b', text):
                    if re.search(
                            r'(=?(Issued|iss|ISS|Iss|ISSUED|es|Isa|SS488|Is|REN)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{4})',
                            text):
                        issue_date = ' '.join(
                            map(str, text.split(
                                re.findall(r'(=?Issued|iss|ISS|Isa|Iss|SS|es|ISSUED|488|Is|REN)',
                                           text)[0], 1)[1].split()[0:3]))
                        if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', issue_date):
                            actual_issue_date = \
                                re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', issue_date)[0]
                        elif re.search(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', issue_date):
                            actual_issue_date = \
                                re.findall(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', issue_date)[0]
                        elif re.search(r'(?!:)', issue_date):
                            actual_issue_date = ''
                    else:
                        actual_issue_date = ''

                    if re.search(
                            r'(=?(EXP|Expires|Exp|Expiros|EXPIRES|EXPIROS|EER)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{4})',
                            text):
                        expiry_date = ' '.join(map(str, text.split(
                            re.findall(r'(=?EXP|Expires|Exp|Expiros|EXPIRES|EXPIROS|EER)', text)[0],
                            1)[1].split()[0:3]))
                        if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', expiry_date):
                            actual_expiry_date = \
                                re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', expiry_date)[0]
                        elif re.search(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', expiry_date):
                            actual_expiry_date = \
                                re.findall(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', expiry_date)[0]

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
                            actual_dob_date = re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', dob)[
                                0]

                        elif re.search(r'(?!:)\s?\d+[-/.]?\d+[-/.]?\d+', dob):
                            actual_dob_date = re.findall(r'(?!:)\s?\d+[-/.]?\d+[-/.]?\d+', dob)[0]

                        elif re.search(r'(=?:)', dob):
                            actual_dob_date = ''

                    else:
                        actual_dob_date = ''


                else:

                    if re.search(
                            r'(=?(Issued|iss|ISS|Iss|ISSUED|Isa|es|488|Is)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{2})',
                            text):
                        issue_date = ' '.join(
                            map(str,
                                text.split(
                                    re.findall(r'(=?Issued|iss|Isa|es|ISS|Iss|ISSUED|488|Is)',
                                               text)[0], 1)[1].split()[0:3]))
                        if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', issue_date):
                            actual_issue_date = \
                                re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', issue_date)[0]
                        elif re.search(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', issue_date):
                            actual_issue_date = \
                                re.findall(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', issue_date)[0]
                        elif re.search(r'(?!:)', issue_date):
                            actual_issue_date = ''
                    else:
                        actual_issue_date = ''

                    if re.search(
                            r'(=?(EXP|Expires|Exp|Expiros|EXPIRES|EXPIROS|EER)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{2})',
                            text):
                        expiry_date = ' '.join(map(str, text.split(
                            re.findall(r'(=?EXP|Expires|Exp|Expiros|EXPIRES|EXPIROS|EER)', text)[0],
                            1)[1].split()[
                                                        0:3]))
                        if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', expiry_date):
                            actual_expiry_date = \
                                re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', expiry_date)[0]
                        elif re.search(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', expiry_date):
                            actual_expiry_date = \
                                re.findall(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', expiry_date)[0]

                        elif re.search(r'(=?:)', expiry_date):
                            actual_expiry_date = ''
                    else:
                        actual_expiry_date = ''

                    if re.search(
                            r'(=?(DOB:dob|DOB|BIRTHDATE|Sa|gos|DO|Doe|cor|Cor|nos|so|birthdate|Birth|BIRTH|D.O.B.|Dos|dos|pos|POS|DoB|birth|Bo:|Dso)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{2})',
                            text):
                        dob = ' '.join(map(str, text.split(
                            re.findall(
                                r'(=?DOB:dob|DOB|Sa|gos|nos|Doe|cor|Cor|DO|so|BIRTHDATE|birthdate|Birth|BIRTH|D.O.B.|Dos|dos|pos|POS|DoB|birth|Bo:|Dso)',
                                text)[0], 1)[
                                                    1].split()[0:3]))
                        if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', dob):
                            actual_dob_date = re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', dob)[
                                0]

                        elif re.search(r'(?!:)\s?\d+[-/.]?\d+[-/.]?\d+', dob):
                            actual_dob_date = re.findall(r'(?!:)\s?\d+[-/.]?\d+[-/.]?\d+', dob)[0]

                        elif re.search(r'(=?:)', dob):
                            actual_dob_date = ''

                    else:
                        actual_dob_date = ''
                return actual_expiry_date, actual_dob_date, actual_issue_date, string_date_value
            except Exception as e:
                self.custom_print("Date Exception", e)
                actual_expiry_date = actual_dob_date = actual_issue_date = string_date_value = ''
                return actual_expiry_date, actual_dob_date, actual_issue_date, string_date_value

    def get_licence_details1(self, text, details):
        try:
            print(details)
            address, state, zipcode, city, value_name = self.get_address(details)
            if state != '':
                get_licence_id = self.get_id(text, state)
            else:
                get_licence_id = ' '

            if get_licence_id != ' ':
                expiry_date, dob, issue_date, date_val = self.get_date(text, get_licence_id)
            else:
                get_licence_id = ' '
                expiry_date, dob, issue_date, date_val = self.get_date(text, get_licence_id)
            # name=''

            name = self.get_name(value_name, date_val, state, text, get_licence_id)

            # thread=threading.Thread(target=self.get_name,args=(text, street,street,get_licence_id,state,date_val,
            #                                                    keys,values,))
            # thread.start()
            # name=self.name.get()

            return get_licence_id, expiry_date, dob, issue_date, address, name, state, zipcode, city, date_val
        except Exception as e:
            get_licence_id = expiry_date = dob = issue_date = address = name = state = zipcode = city = date_val = ''
            return get_licence_id, expiry_date, dob, issue_date, address, name, state, zipcode, city, date_val




class NameSequence(Enum):
    FN_LN = 1
    FN_MN_LN = 2
    LN_FN_MN = 3
    LN_FN_MN_SUF = 4
    SUF_FN_MN_LN = 5
