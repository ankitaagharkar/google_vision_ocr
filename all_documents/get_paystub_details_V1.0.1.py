import json
from datetime import datetime as dt
import datetime
import sys
import re
sys.path.insert(0, '../image_processing')
import Common
#sys.path.insert(0, '../all_documents')
import get_licence_details
import avoid
import paystub_block_values

class Paystub_details:
    def __init__(self):
        self.pay_frequency,self.gross_pay,self.net_pay = '','',''
        self.employment_Start_date=datetime
        self.date_val = []
        self.date = []
        self.gross_net, self.net='',''
        self.net_profit, self.netp = [], []
        self.actual_date = []
        self.date_val1 = []
        self.zip_code=[]
        self.data, self.data1,self.value2 = [], [],[]
        self.c = Common.Common()
        self.paystub_block = paystub_block_values.get_all_location()
        self.license_Address=get_licence_details.Licence_details()
        with open('../config/city.json', 'r') as data_file:
            self.cities = json.load(data_file)
    def employer_address(self,value):
        try:
            full_address, street, state, zipcode, city='','','','',''
            actual_city=''
            value=value.replace(',','')
            value = value.replace(' AJ ', ' NJ ')
            all_number = re.findall(
                r"\s?\s\d{1}\s\w[A-Za-z]+|\s\d{4}\s[A-Za-z]+"
                r"|\d{2}\s[A-Za-z]+|\d{2}-\d{2}\s[A-Za-z]+"
                r"|\s?\d{3}\w?\s[A-Za-z]+\,?|\s\d{3}\s\d{1}"
                r"|\w*\s\d{5}\s?-\s?\d{4}|\w*\s\d{5}\s\w*|\w*\s\d{5}|\w*\s\d{2,5}\s\d{2,3}",
                value)

            number_val = ' '.join(map(str, all_number))
            #print("Number val",number_val)
            data = re.findall(
                r"\b((?=AL|AK|AS|AZ|AŽ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE"
                r"|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)[A-Z]{2}[, ])"
                r"(\d{5}(?:\s?-\s?\d{4})?|\d{5}|\d{2,3}(?:\s\d{2,3}))", number_val)
            if data!=[]:

                for item in data:
                    self.zip_code.append("".join(item))
                if self.zip_code != []:
                    code=self.zip_code[0]
                    reg_value = ' '.join(map(str, value.split(code, 1)[0].split()[-8:]))
                    reg_value = reg_value + " " + code
                    #print('in address',reg_value)
                    # if re.search(r'(\s\d{1,3}\s\w*\s?\w?\s?\w+?\s?\,?\s[A-Z]{2}\s\d{5})\b', reg_value):
                    if re.search(r'(\d+\s([A-Za-z]+)?\s?([A-Za-z])+?\s?([A-Za-z])+\s?[#.,/]?\s?\w*?\s\d{1,}\s\w+\s?\w+?\s?\w?\,?\s[A-Z]{2}\s\d{5})\b', reg_value):
                        street = ' '.join(map(str, number_val.split(code, 1)[0].split()[-4:-2]))
                    else:
                        street = ' '.join(map(str, number_val.split(code, 1)[0].split()[-2:]))
                    #print("actual street", street)
                    address = self.c.find_between_r(value, street, code)
                    #print("zip code",code)
                    full_address = street + address + code
                    state, zipcode, city = self.c.get_address_zipcode(full_address, code)
                    #print("Full Address:", full_address,zipcode,city,state)
                    for i in range(len(self.cities['city'])):
                        if self.cities['city'][i].lower() in city.lower():
                            actual_city = self.cities['city'][i]

                    if actual_city=='':
                        city=' '.join(map(str, value.split(code, 1)[0].split()[-1:]))
                        #print(city)
                    elif city!=actual_city:
                        city=actual_city.upper()
                    else:
                        city=actual_city
                    full_address = self.c.find_between_r(value, street, city)
                    #print("full",full_address)
                    full_address = street + full_address
                    full_address=' '.join(s[:1].upper() + s[1:] for s in full_address.split())
                    city=city.replace(",","")
                    city = city.replace(".", "")
                    return full_address, street, state, zipcode, city
            else:
                data = re.findall(
                    r"[A-Za-z]+\s[A-Za-z]+\s[A-Za-z]+(!? AL | AK | AS | AZ | AŽ | AR | CA | CO | CT | DE | DC | FM | FL | GA | GU | HI | ID | IL | IN | IA | KS | KY | LA "
                    r"| ME | MH | MD | MA | MI | MN | MS | MO | MT | NE | NV | NH | NJ | NM | NY | NC | ND | MP "
                    r"| OH | OK | OR | PW | PA | PR | RI | SC | SD | TN | TX | UT | VT | VI | VA | WA | WV | WI | WY )",
                    value)
                for item in data:
                    self.zip_code.append("".join(item))
                if self.zip_code != []:
                    code=self.zip_code[0]
                    reg_value = ' '.join(map(str, value.split(code, 1)[0].split()[-8:]))
                    reg_value = reg_value + " " + code
                    #print(reg_value)
                    if re.search(r'(\d+\s([A-Za-z]+)?\s?([A-Za-z])+?\s?([A-Za-z])+'
                                 r'\s?[#.,/]?\s?\w*?\s\d{1,3}\s\w+\s?\w+?\s?\w?\,?'
                                 r'\s[A-Z]{2})\b',reg_value):
                        street_code=re.findall(r'\s\d+\s+\w+',reg_value)
                        street=street_code[0]
                    else:
                        street_code = re.findall(r'\s\d+\s+\w+', reg_value)
                        street = street_code[1]
                    address = self.c.find_between_r(value, street, code)
                    #print("zip code", code)
                    full_address = street + address + code
                    state,zip,city = self.c.get_address_zipcode(full_address, code)
                    #print("Full Address:", full_address, city, state)
                    for i in range(len(self.cities['city'])):
                        if self.cities['city'][i].lower() in city.lower():
                            actual_city = self.cities['city'][i]

                    if actual_city == '':
                        city = ' '.join(map(str, value.split(code, 1)[0].split()[-1:]))
                        #print(city)
                    elif city != actual_city:
                        city = actual_city.upper()
                    else:
                        city = actual_city
                    full_address = self.c.find_between_r(value, street, city)
                    #print("full", full_address)
                    full_address = street + full_address
                    full_address = ' '.join(s[:1].upper() + s[1:] for s in full_address.split())
                    city = city.replace(",", "")
                    city = city.replace(".", "")
                    zipcode=""

            return full_address, street, state, zipcode, city
        except Exception as e:
            full_address, street, state, zipcode, city = "", "", "", "", ""
            return full_address, street, state, zipcode, city
    def employee_address(self, value):
        try:
            full_address, street, state, zipcode, city = '', '', '', '', ''
            actual_city = ''
            value = value.replace(',', '')
            value = value.replace(' AJ ', ' NJ ')
            all_number = re.findall(
                r"\s?\s\d{1}\s\w[A-Za-z]+|\s\d{4}\s[A-Za-z]+"
                r"|\d{2}\s[A-Za-z]+|\d{2}-\d{2}\s[A-Za-z]+"
                r"|\s?\d{3}\w?\s[A-Za-z]+\,?|\s\d{3}\s\d{1}"
                r"|\w*\s\d{5}\s?-\s?\d{4}|\w*\s\d{5}\s\w*|\w*\s\d{5}|\w*\s\d{2,5}\s\d{2,3}",
                value)

            number_val = ' '.join(map(str, all_number))
            #print("Number val", number_val)
            data = re.findall(
                r"\b((?=AL|AK|AS|AZ|AŽ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE"
                r"|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)[A-Z]{2}[, ])"
                r"(\d{5}(?:\s?-\s?\d{4})?|\d{5}|\d{2,3}(?:\s\d{2,3}))", number_val)
            if data != []:

                for item in data:
                    self.zip_code.append("".join(item))
                if self.zip_code != []:
                    code = self.zip_code[1]
                    reg_value = ' '.join(map(str, value.split(code, 1)[0].split()[-8:]))
                    reg_value = reg_value + " " + code
                    #print('in address', reg_value)
                    # if re.search(r'(\s\d{1,3}\s\w*\s?\w?\s?\w+?\s?\,?\s[A-Z]{2}\s\d{5})\b', reg_value):
                    if re.search(
                            r'(\d+\s([A-Za-z]+)?\s?([A-Za-z])+?\s?([A-Za-z])+\s?[#.,/]?\s?\w*?\s\d{1,}\s\w+\s?\w+?\s?\w?\,?\s[A-Z]{2}\s\d{5})\b',
                            reg_value):
                        street = ' '.join(map(str, number_val.split(code, 1)[0].split()[-4:-2]))
                    else:
                        street = ' '.join(map(str, number_val.split(code, 1)[0].split()[-2:]))
                    #print("actual street", street)
                    address = self.c.find_between_r(value, street, code)
                    #print("zip code", code)
                    full_address = street + address + code
                    state, zipcode, city = self.c.get_address_zipcode(full_address, code)
                    #print("Full Address:", full_address, zipcode, city, state)
                    for i in range(len(self.cities['city'])):
                        if self.cities['city'][i].lower() in city.lower():
                            actual_city = self.cities['city'][i]

                    if actual_city == '':
                        city = ' '.join(map(str, value.split(code, 1)[0].split()[-1:]))
                        #print(city)
                    elif city != actual_city:
                        city = actual_city.upper()
                    else:
                        city = actual_city
                    full_address = self.c.find_between_r(value, street, city)
                    #print("full", full_address)
                    full_address = street + full_address
                    full_address = ' '.join(s[:1].upper() + s[1:] for s in full_address.split())
                    city = city.replace(",", "")
                    city = city.replace(".", "")
                    return full_address, street, state, zipcode, city
            else:
                data = re.findall(
                    r"[A-Za-z]+\s[A-Za-z]+\s[A-Za-z]+(!? AL | AK | AS | AZ | AŽ | AR | CA | CO | CT | DE | DC | FM | FL | GA | GU | HI | ID | IL | IN | IA | KS | KY | LA "
                    r"| ME | MH | MD | MA | MI | MN | MS | MO | MT | NE | NV | NH | NJ | NM | NY | NC | ND | MP "
                    r"| OH | OK | OR | PW | PA | PR | RI | SC | SD | TN | TX | UT | VT | VI | VA | WA | WV | WI | WY )",
                    value)
                for item in data:
                    self.zip_code.append("".join(item))
                if self.zip_code != []:
                    code = self.zip_code[1]
                    reg_value = ' '.join(map(str, value.split(code, 1)[0].split()[-8:]))
                    reg_value = reg_value + " " + code
                    #print(reg_value)
                    if re.search(r'(\d+\s([A-Za-z]+)?\s?([A-Za-z])+?\s?([A-Za-z])+'
                                 r'\s?[#.,/]?\s?\w*?\s\d{1,3}\s\w+\s?\w+?\s?\w?\,?'
                                 r'\s[A-Z]{2})\b', reg_value):
                        street_code = re.findall(r'\s\d+\s+\w+', reg_value)
                        street = street_code[0]
                    else:
                        street_code = re.findall(r'\s\d+\s+\w+', reg_value)
                        street = street_code[1]
                    address = self.c.find_between_r(value, street, code)
                    #print("zip code", code)
                    full_address = street + address + code
                    state, zip, city = self.c.get_address_zipcode(full_address, code)
                    #print("Full Address:", full_address, city, state)
                    for i in range(len(self.cities['city'])):
                        if self.cities['city'][i].lower() in city.lower():
                            actual_city = self.cities['city'][i]

                    if actual_city == '':
                        city = ' '.join(map(str, value.split(code, 1)[0].split()[-1:]))
                        #print(city)
                    elif city != actual_city:
                        city = actual_city.upper()
                    else:
                        city = actual_city
                    full_address = self.c.find_between_r(value, street, city)
                    #print("full", full_address)
                    full_address = street + full_address
                    full_address = ' '.join(s[:1].upper() + s[1:] for s in full_address.split())
                    city = city.replace(",", "")
                    city = city.replace(".", "")
                    zipcode = ""

            return full_address, street, state, zipcode, city
        except Exception as e:
            full_address, street, state, zipcode, city = "", "", "", "", ""
            return full_address, street, state, zipcode, city
    def employer_name(self,value,street):
        try:

            name = ' '.join(map(str, value.split(street, 1)[0].split()[-6:]))
            #print("name", name)
            name_regex = re.findall(r'([A-Za-z]+[,.&\s]*[A-Za-z]+)+', name)
            actual_name = " ".join(map(str, name_regex))
            actual_name = actual_name.replace("NY New York Cit","")
            actual_name=avoid.replace(actual_name)
            #print("full_name",actual_name)
            return actual_name
        except Exception as e:
            full_name = ''
            return full_name
    def employee_name(self, value, street):
        try:


            name = ' '.join(map(str, value.split(street, 1)[0].split()[-6:]))
            #print("name", name)
            name_regex = re.findall(r'([A-Za-z]+[,.&\s]*[A-Za-z]+)+', name)
            actual_name = " ".join(map(str, name_regex))
            actual_name = actual_name.replace("NY New York Cit","")
            actual_name = avoid.replace(actual_name)
            #print("full_name", actual_name)
            return actual_name
        except Exception as e:
            full_name = ''
            return full_name
    def get_paystub_date(self, text):
        try:
            #print(text)
            # text = text_value.replace(' ', '')
            start_date = ""
            val = re.findall(
                r'(([0-9]|0[0-9]|1[0-9])[./-]([0-9][0-9]|[0-9])[./-]\d\d)|(([0-9]'
                r'|0[0-9]|1[0-9])[./-]([0-9][0-9]|[0-9])[./-](19|20|21|22|23|24)\d\d)\b', text)
            for item in val:
                self.date_val1.append("".join(item))
            string_date = " ".join(map(str, self.date_val1))
            self.date_val = re.findall(r'\d{2}[./-]\d{2}[./-]\d{2,4}', string_date)
            string_date_value = " ".join(map(str, self.date_val))
            #print(string_date_value)
            for dob in self.date_val:
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
                dob = dob[0:2] + '/' + dob[2:4] + '/' + dob[4:8]
                self.date.append(dob)
            for value in self.date[:2]:
                if re.match(r'\b\d{2}[./-]\d{2}[./-]\d{2}\b', value):
                    self.actual_date.append(datetime.datetime.strptime(value, '%m/%d/%y').strftime('%y/%m/%d'))
                else:
                    self.actual_date.append(datetime.datetime.strptime(value, '%m/%d/%Y').strftime('%Y/%m/%d'))
            pay_end_date=self.actual_date[3]
            data = " ".join(map(str, self.actual_date))
            if re.match(r'\b\d{2}[./-]\d{2}[./-]\d{2}\b', data):
                ending_date = max(self.actual_date)
                starting_date = min(self.actual_date)
                if ending_date != "" and starting_date != "":
                    ending_date = datetime.datetime.strptime(ending_date, '%y/%m/%d').strftime('%m/%d/%y')
                    starting_date = datetime.datetime.strptime(starting_date, '%y/%m/%d').strftime('%m/%d/%y')
                    self.employment_Start_date = dt.strptime(ending_date, "%m/%d/%y")
                    self.pay_date = dt.strptime(starting_date, "%m/%d/%y")
                    start_date = self.pay_date.date().strftime('%m/%d/%Y')
            else:
                ending_date = max(self.actual_date)
                starting_date = min(self.actual_date)
                if ending_date != None and starting_date != None:
                    ending_date = datetime.datetime.strptime(ending_date, '%Y/%m/%d').strftime('%m/%d/%Y')
                    starting_date = datetime.datetime.strptime(starting_date, '%Y/%m/%d').strftime('%m/%d/%Y')
                    self.employment_Start_date = dt.strptime(ending_date, "%m/%d/%Y")
                    self.pay_date = dt.strptime(starting_date, "%m/%d/%Y")
                    start_date = self.pay_date.date().strftime('%m/%d/%Y')
                    end_date=self.employment_Start_date.date().strftime('%m/%d/%Y')
            frequency = abs((self.pay_date - self.employment_Start_date).days)
            if self.pay_date.date().day>=15:
                self.pay_frequency = 'Bi-Monthly'
            elif 7>=self.pay_date.date().day<=14:
                self.pay_frequency = 'Bi-Weekly'
            elif self.pay_date.date().day<=7:
                self.pay_frequency = 'Weekly'
            # if frequency == 14 or frequency == 13:
            #     self.pay_frequency = 'Bi-Weekly'
            # elif frequency == 7 or frequency == 6:
            #     self.pay_frequency = 'Weekly'
            elif frequency == 30 or frequency == 31:
                self.pay_frequency = 'Monthly'
            else:
                self.pay_frequency=''
            # start_date=dt.strptime(start_date, "%m/%d/%Y")
            # #print("staring date",start_date)
            # #print("pay_frequency",self.pay_frequency)
            return str(start_date), self.pay_frequency, string_date_value,end_date,pay_end_date
        except Exception as E:
            print(E)
            start_date, self.pay_frequency, string_date_value,pay_end_date = "", "", "",""
            return start_date, self.pay_frequency, string_date_value,self.employment_Start_date,pay_end_date
    def get_gross_net_pay(self,path,description,result):
        try:
            # self.paystub_block.get_text(path)
            # lines = self.paystub_block.rectify_data()
            # for line in lines:
            #     #print(line)
            blocks1 = self.paystub_block.all_location_details(path,description,result)
            print(blocks1)
            # blocks=self.paystub_block.all_location()
            gross_net_values=list(blocks1.values())
            for i in range(len(gross_net_values)):
                
                if 'Gross Pay' in gross_net_values[i]:
                    self.gross_pay=gross_net_values[i][1]
                    self.gross_pay=self.gross_pay.replace('S',"")
                    self.net_pay = self.net_pay.replace('s', "")
                elif 'Net Pay'in gross_net_values[i]:
                    self.net_pay=gross_net_values[i][1]
                    self.net_pay = self.net_pay.replace('S', "")
                    self.net_pay = self.net_pay.replace('s', "")
            if re.search('\d+\s\d+', self.gross_pay):
                gn = self.gross_pay.split(" ")
                self.gross_net = gn[1] + "." + gn[2]
            elif re.search('\d+\s\s\d+', self.gross_pay):
                gn = self.gross_pay.split(" ")
                self.gross_net = gn[1] + "." + gn[3]
            if re.search('\d+\s\d+', self.net_pay):
                nv = self.net_pay.split(" ")
                self.net = nv[1] + "." + nv[2]
            elif re.search('\d+\s\s\d+', self.net_pay):
                nv = self.net_pay.split(" ")
                self.net = nv[1] + "." + nv[3]
            return self.gross_pay,self.net_pay
        except Exception as e:
            print(e)
    def get_details(self,text,path,description,result):
        try:
            #print(text)
            gross_pay, net_pay = self.get_gross_net_pay(path,description,result)
            employer_full_address, employer_street, employer_state, employer_zipcode, employer_city=self.employer_address(text)
            employee_full_address, employee_street, employee_state, employee_zipcode, employee_city=self.employee_address(text)
            start_date,pay_frequency, string_date_value,employment_Start_date,end_date = self.get_paystub_date(text)
            employer_name=self.employer_name(text,employer_street)
            employee_name=self.employee_name(text,employee_street)
            return employer_full_address, employer_street, employer_state, employer_zipcode, employer_city,employee_full_address, employee_street, employee_state, employee_zipcode, employee_city,start_date,pay_frequency, string_date_value,employer_name,employee_name,gross_pay,net_pay,employment_Start_date,end_date
        except Exception as e:
            print(e)



