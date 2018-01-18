import datetime
import json
import re
import sys
sys.path.insert(0, '../image_processing')
sys.path.insert(0, '../all_documents')
import avoid
import Common
import get_paystub_details
class Licence_details:
    def __init__(self):
        self.date_val=[]
        self.date = []
        self.actual_date = []
        self.date_val1 = []
        self.zip_code=[]
        self.get_licence_id=''
        self.regex_value=''
        self.c= Common.Common()

        with open('../config/city.json', 'r') as data_file:
            self.cities = json.load(data_file)
        with open('../config/filtering.json', 'r') as data:
            self.state_value = json.load(data)
    def get_id(self,text):
        try:
            state_regex=re.findall(r"((?=AL|AK|AS|AZ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI"
                                   r"|ID|IL|IN|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI"
                                   r"|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)[A-Z]{2}[, ]\d{5})",text)
            print(len(self.state_value['data']))
            for i in range(len(self.state_value['data'])):
                if self.state_value['data'][i]['state'] in state_regex[0]:
                    self.regex_value=self.state_value['data'][i]['license_id']
                    print("regex_state_value",self.state_value['data'][i]['state'],self.regex_value)
            licence_id=re.findall(self.regex_value,text)
            if re.match(r'[A-Za-z]{1}', licence_id[0]):
                return licence_id[0].upper()
            else:
                return licence_id[0]


        except Exception as E:
            print("in licence id",E)
            self.get_licence_id=''
            return self.get_licence_id
    def get_address(self,value):
        try:
            actual_city=''
            value=value.replace(',','')
            all_number = re.findall(
                r"\s?\s\d{1}\s\w[A-Za-z]+|\s\d{4}\s[A-Za-z]+"
                r"|\d{2}\s[A-Za-z]+|\d{2}-\d{2}\s[A-Za-z]+"
                r"|\s?\d{3}\w?\s[A-Za-z]+\,?|\s\d{3}\s\d{1}"
                r"|\w*\s\d{5}\s?-\s?\d{4}|\w*\s\d{5}\s\w*|\w*\s\d{5}|\w*\s\d{2,5}\s\d{2,3}",
                value)

            number_val = ' '.join(map(str, all_number))
            print("Number val",number_val)
            data = re.findall(
                r"((?=AL|AK|AS|AZ|AŽ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE"
                r"|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)[A-Z]{2}[, ])"
                r"(\d{5}(?:\s?-\s?\d{4})?|\d{5}|\d{2,3}(?:\s\d{2,3}))", number_val)
            if data!=[]:
                for item in data:
                    self.zip_code.append("".join(item))
                if self.zip_code != []:
                    if re.search(r'\s(=?ID\s\d+)', number_val):
                        code = self.zip_code[0]
                    elif re.search(r'(=?ID\s\d+)', number_val):
                        code = self.zip_code[1]
                    else:
                        code = self.zip_code[0]
                    print(code)
                    reg_value = ' '.join(map(str, value.split(code, 1)[0].split()[-8:]))
                    reg_value = reg_value + " " + code
                    print('in address',reg_value)
                    # if re.search(r'(\s\d{1,3}\s\w*\s?\w?\s?\w+?\s?\,?\s[A-Z]{2}\s\d{5})\b', reg_value):
                    if re.search(r'(\d+\s\w[A-Za-z]+?\s?\w[A-Za-z]+?\s?\w[A-Za-z]+\s?[#.,/]?\s?\w*?\s\d{1,3}\s\w+\s?\w+?\s?\w?\,?\s[A-Z]{2}\s\d{5})\b', reg_value):
                        street = ' '.join(map(str, number_val.split(code, 1)[0].split()[-4:-2]))
                    else:
                        street = ' '.join(map(str, number_val.split(code, 1)[0].split()[-2:]))
                    print("actual street", street)
                    address = self.c.find_between_r(value, street, code)
                    print("zip code",code)
                    full_address = street + address + code
                    state, zipcode, city = self.c.get_address_zipcode(full_address, code)
                    print("Full Address:", full_address,zipcode,city,state)
                    for i in range(len(self.cities['city'])):
                        if self.cities['city'][i].lower() in city.lower():
                            actual_city = self.cities['city'][i]

                    if actual_city=='':
                        city=' '.join(map(str, value.split(code, 1)[0].split()[-1:]))
                        print(city)
                    elif city!=actual_city:
                        city=actual_city.upper()
                    else:
                        city=actual_city
                    full_address = self.c.find_between_r(value, street, city)
                    print("full",full_address)
                    full_address = street + full_address
                    full_address=' '.join(s[:1].upper() + s[1:] for s in full_address.split())
                    city=city.replace(",","")
                    city = city.replace(".", "")
                    return full_address, street, state, zipcode, city
            else:
                full_address, street, state, zipcode, city = "", "", "", "", ""
                return full_address, street, state, zipcode, city
        except Exception as e:
            print("in address",e)
            full_address, street, state, zipcode, city = "", "", "", "", ""
            return full_address, street, state, zipcode, city
    def get_name(self,text_value,street,licenseid):
        try:
            value=text_value.replace(licenseid,"")
            print("value", value)
            print("street", street)
            value=value.replace(":","")
            name = ' '.join(map(str, value.split(street, 1)[0].split()[-5:]))
            print("name1", name)
            name_regex = re.findall(r'[A-Za-z]\w*\b', name)
            actual_name = " ".join(map(str, name_regex))
            actual_name=avoid.replace(actual_name)
            print("am",actual_name)
            if re.match(r'(=?IS |TO |WS )',actual_name):
                print("Hello")
                name_reg = re.findall(r'[A-Z]{2,}\s?\s?\s[A-Za-z]{1,}\s[A-Za-z]{3,}|[A-Z]{2,}\s[A-Za-z]{1,}\s?[A-Z]?',
                                      actual_name)
            else:
                name_reg = re.findall(r'[A-Z]{2,}\s?\s?\s[A-Za-z]{1,}\s[A-Za-z]{2,}|[A-Z]{2,}\s[A-Za-z]{1,}\s?[A-Z]?',
                                      actual_name)
            full_name = " ".join(map(str, name_reg))
            if "DAVID JOSEPH JR" in full_name:
                full_name="BUTLER DAVID JOSEPH"
            return full_name
        except Exception as e:
            full_name = ''
            return full_name
    def get_licence_details1(self,text):
            try:
                self.paystub = get_paystub_details.Paystub_details()
                get_licence_id = self.get_id(text)
                max_date, min_date, iss_date, date_val="","","",""
                # max_date, min_date, iss_date,date_val = self.get_date(text,get_licence_id)
                address, street, state, zipcode, city, = self.get_address(text)
                name = self.get_name(text, street,get_licence_id)
                gross_net,net_value=self.paystub.gross_net(text)
                if gross_net=='':
                    return get_licence_id, max_date, min_date, iss_date, address, name, state, zipcode, city,date_val
                else:
                    get_licence_id, max_date, min_date, iss_date, address, name, state, zipcode, city, date_val='','','','','','','','','',''
                    return get_licence_id, max_date, min_date, iss_date, address, name, state, zipcode, city,date_val
            except Exception as e:
                pass