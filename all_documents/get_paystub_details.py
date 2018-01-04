import json
from datetime import datetime as dt
import datetime
import sys

import re
sys.path.insert(0, '../image_processing')
import Common
sys.path.insert(0, '../all_documents')
import get_licence_details
import avoid

class Paystub_details:
    def __init__(self):
        self.pay_frequency = ''
        self.employment_Start_date=datetime
        self.date_val = []
        self.date = []
        self.actual_date = []
        self.date_val1 = []
        self.zip_code=[]
        self.data, self.data1,self.value2 = [], [],[]
        self.c = Common.Common()
        self.license_Address=get_licence_details.Licence_details()
        with open('../config/city.json', 'r') as data_file:
            self.cities = json.load(data_file)

    def get_Paystub_address(self, value):
        try:
            actual_city = ''
            all_number = re.findall(
                r"\w+\s\d{4}\s\w[A-Za-z]+|\s?\s\d{1}\s\w*|\s?\d{3}\w?\s\w*\,?|\s\d{3}\s\d{1}|\w*\s\d{5}\s\w*|\w*\s\d{5}-\d{4}|\w*\s\d{5}"
                r"|\d{2}\s\w*|\w{2}\s\d{3}\s\d{2}|\w*\s\d{3}\s\d{1}\s\d{1}"
                r"|\w*\s\d{4}-\d{4}|\w*\s\d{2,5}\s\d{2,3}-\d{4}|\w*\s\d{2,5}\s\d{2,3}",
                value)
            number_val = ' '.join(map(str, all_number))
            print("Number val", number_val)
            data = re.findall(
                r"\b((?=AL|AK|AS|AZ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI"
                r"|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN"
                r"|TX|UT|VT|VI|VA|WA|WV|WI|WY)[A-Z]{2}[, ])(\d{5}(?:-\d{4})?|\d{4}(?:-\d{4})?)", number_val)
            if data != []:
                for item in data:
                    self.zip_code.append("".join(item))
                code = self.zip_code[0]

                # if re.search(r'(\s\d{2,3}\s\w*\s?\w?\s?\w+?\s?\,?\s\w+\s\d{5})\b', number_val):
                #     street = ' '.join(map(str, number_val.split(code, 1)[0].split()[-4:-2]))
                # else:
                street = ' '.join(map(str, number_val.split(code, 1)[0].split()[-2:]))
                # street = ' '.join(map(str, number_val.split(code, 1)[0].split()[-2:]))
                print("actual street", street)
                address = self.c.find_between_r(value, street, code)

                full_address = street + address + self.zip_code[0]

                state, zipcode, city = self.c.get_address_zipcode(full_address, self.zip_code[0])
                # city=city.replace('NE',"")
                print("city",city)
                print("Full Address:", full_address)
                for i in range(len(self.cities['city'])):
                    if self.cities['city'][i].lower() in city.lower():
                        actual_city = self.cities['city'][i]
                print("actual_city",actual_city)
                if actual_city == '':
                    city = ' '.join(map(str, value.split(code, 1)[0].split()[-1:]))
                    print(city)
                elif city == actual_city:
                    city = actual_city
                    print(city)
                else:
                    city = actual_city.upper()

                full_address = self.c.find_between_r(value, street, city)

                full_address = street + full_address

                return full_address, street, state, zipcode, city
            else:
                full_address, street, state, zipcode, city = "", "", "", "", ""
                return full_address, street, state, zipcode, city
        except Exception as e:
            print("in address", e)
            full_address, street, state, zipcode, city = "", "", "", "", ""
            return full_address, street, state, zipcode, city
    def get_paystub_name(self,text,street,date):
        try:
            print("in paystub",text)
            date_val=date.split()
            print(date)
            value=text.replace(date_val[0],"")

            name = ' '.join(map(str, value.split(street, 1)[0].split()[-6:]))
            print("name", name)
            name_regex = re.findall(r'([A-Za-z]+[,.&\s]*[A-Za-z]+)+', name)
            actual_name = " ".join(map(str, name_regex))
            actual_name=avoid.replace(actual_name)
            print("full_name",actual_name)
            return actual_name
        except Exception as e:
            full_name = ''
            return full_name
    def get_paystub_date(self,text):
        try:
            start_date=""
            val = re.findall(
                r'(\w*[A-Za-z]\d{1}\d{2}[./-](19|20|21|22|23|24)\d\d)|(\w*[A-Za-z]\d{1}[./-]\d{2}[./-](19|20|21|22|23|24)\d\d)'
                r'|(\d{2}\s?[./-]\d{2}[./-](19|20|21|22|23|24)\d\d)|(\d{2}\s\d{2}\s(19|20|21|22|23|24)\d\d)'
                r'|(\d{2}[./-]\d{2}\s?(19|20|21|22|23|24)\d\d)|(\d{1,2}\s?[./-]\d{2}[./-]\s?\d{2}\s?\d{2})'
                r'|(\d{2}\d{2}[./-](19|20|21|22|23|24)\d\d)|(\d{2}[./-]\d{2}\s[./-](19|20|21|22|23|24)\d\d)'
                r'|(([0-9]|0[0-9]|1[0-9])[./-]([0-9][0-9]|[0-9])[./-]\d\d)|(([0-9]'
                r'|0[0-9]|1[0-9])[./-]([0-9][0-9]|[0-9])[./-](19|20|21|22|23|24)\d\d|(\d{2}\d{2}[./-]\d\d))\b', text)
            for item in val:
                self.date_val1.append(" ".join(item))
            string_date = " ".join(map(str, self.date_val1))
            self.date_val = re.findall(r'\d{2}\s?[./-]?\d{2}\s?[./-]?\d{2,4}', string_date)
            string_date_value = " ".join(map(str, self.date_val))
            print(string_date_value)
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
            frequency = abs((self.pay_date - self.employment_Start_date).days)
            if frequency == 14 or frequency == 13:
                self.pay_frequency = 'Bi-Weekly'
            elif frequency == 7 or frequency == 6:
                self.pay_frequency = 'Weekly'
            elif frequency == 30 or frequency == 31:
                self.pay_frequency = 'Monthly'
            # start_date=dt.strptime(start_date, "%m/%d/%Y")
            # print("staring date",start_date)
            # print("pay_frequency",self.pay_frequency)
            return str(start_date), self.pay_frequency,string_date_value
        except Exception as E:
            print(E)
            start_date, self.pay_frequency,string_date_value = "", "",""
            return start_date, self.pay_frequency,string_date_value
    def gross_net(self,text):
        try:
            if re.search(r'(=?amount|Amount|account|Account)',text):
                value = re.findall(
                    r'((=?Gross Pay|Gross Pa|Brose Pay|amount|Amount|Gross Earnings|account|Account)|\s?\$?\d{1,3}\s?\,?\s?\d+\.?\-?\d+?)\b', text)
                for item in value:
                    self.data.append("".join(item))
                string_date = " ".join(map(str,self.data))

                if re.search('(\w+\s\w+\s?\s?\$\d{1,3}\s?\,?\s?\d+\s?\.?\-?(\d+)?)', string_date) is not None:
                    if re.search('(=?amount|Amount)', string_date):
                        get_value = re.findall(
                            r'(=?(Gross Pay|Gross Pa|Brose Pay|amount|Amount|Gross Earnings)|\s?\s?\$\d{1,3}\s?\,?\s?\d+\s?\s?\.?\-?\d+?)\b',
                            string_date)
                    else:
                        get_value = re.findall(
                            r'(=?(Gross Pay|Gross Pa|Brose Pay|account|Account|Gross Earnings)|\s?\s?\$\d{1,3}\s?\,?\s?\d+\s?\s?\.?\-?\d+?)\b',
                            string_date)

                else:
                    if re.search('(=?amount|Amount)', string_date):
                        get_value = re.findall(
                            r'(=?(Gross Pay|Gross Pa|Brose Pay|amount|Amount|Gross Earnings)\s?\s?\d{1,3}\s?\,?\s?\d+\s?\s?\.?\-?\d+?)\b',
                            string_date)
                    else:
                        get_value = re.findall(
                            r'(=?(Gross Pay|Gross Pa|Brose Pay|Gross Earnings|account|Account)\s?\s?\d{1,3}\s?\,?\s?\s?\d+\s?\.?\-?\d+?)\b',
                            string_date)

                for item in get_value:
                    self.data1.append("".join(item))
                get_gn_value = "".join(map(str, self.data1))
                gross_net_value = re.findall(
                    r'((=?Gross Pay|Gross Pa|Brose Pay|amount|Amount|Gross Earnings|account|Account)\s?\s?\$?\d{1,3}\s?\,?\s?\d+\s?\s?\.?\-?(\d+)?)',
                    get_gn_value)
                for item in gross_net_value:
                    self.value2.append("".join(item))
                string_date1 = " ".join(map(str, self.value2))

                gross_net_value = re.findall(r'(\s?\$?\d{1,3}\s?\,?\s?\d+\s?\s?\.?\-?(\d+)?)', string_date1)
                print(gross_net_value)
            else:
                value = re.findall(
                    r'((=?Gross Pay|Gross Pa|Brose Pay|amount|Amount|Gross Earnings|Net Pay|NET PAY|Net Pa)|\s?\$?\d{1,3}\s?\,?\s?\d+\.?\-?\d+?)\b',
                    text)
                for item in value:
                    self.data.append("".join(item))
                string_date = " ".join(map(str, self.data))

                if re.search('(\w+\s\w+\s?\s?\$\d{1,3}\s?\,?\s?\d+\.?\-?(\d+)?)', string_date) is not None:
                    get_value = re.findall(
                        r'(=?(Gross Pay|Gross Pa|Brose Pay|amount|Amount|Gross Earnings|Net Pay|NET PAY|Net Pa)|\s?\s?\$\d{1,3}\s?\,?\s?\d+\.?\-?\d+?)\b',
                        string_date)
                else:
                    get_value = re.findall(
                        r'(=?(Gross Pay|Gross Pa|Brose Pay|amount|Amount|Gross Earnings|Net Pay|NET PAY|Net Pa)\s?\s?\d{1,3}\s?\,?\s?\d+\.?\-?\d+?)\b',
                        string_date)

                for item in get_value:
                    self.data1.append("".join(item))
                get_gn_value = "".join(map(str, self.data1))
                gross_net_value = re.findall(
                    r'((=?Gross Pay|Gross Pa|Brose Pay|amount|Amount|Gross Earnings|Net Pay|NET PAY|Net Pa)\s?\s?\$?\d{1,3}\s?\,?\s?\d+\.?\-?(\d+)?)',
                    get_gn_value)
                for item in gross_net_value:
                    self.value2.append("".join(item))
                string_date1 = " ".join(map(str, self.value2))

                gross_net_value = re.findall(r'(\s?\$?\d{1,3}\s?\,?\s?\d+\.?\-?(\d+)?)', string_date1)
                print(gross_net_value)

            if re.search(r'\$?\d{2,3}\.?\d+',gross_net_value[1][0].replace(" ", "")):

                    gross_net= gross_net_value[0][0].replace("$", "")
                    gross_net = gross_net.replace('-','.')
                    net_value=gross_net_value[1][0].replace("$", "")
                    net_value = net_value.replace("-", ".")
                    if re.search('\d+\s\d+',gross_net):
                        gn=gross_net.split(" ")
                        gross_net=gn[1]+"."+gn[2]
                    elif re.search('\d+\s\s\d+',gross_net):
                        gn=gross_net.split(" ")
                        gross_net=gn[1]+"."+gn[3]
                    if re.search('\d+\s\d+',net_value):
                        nv = net_value.split(" ")
                        gross_net = nv[1] + "." + nv[2]
                    elif re.search('\d+\s\s\d+',net_value):
                        nv = net_value.split(" ")
                        gross_net = nv[1] + "." + nv[3]
                    return gross_net.replace(" ",''), net_value.replace(" ",'')
            else:
                gross_net = gross_net_value[0][0].replace("$", "")
                gross_net = gross_net.replace('-', '.')
                net_value = gross_net_value[2][0].replace("$", "")
                net_value = net_value.replace("-", ".")
                if re.search('\d+\s\d+', gross_net):
                    gn = gross_net.split(" ")
                    gross_net = gn[1] + "." + gn[2]
                elif re.search('\d+\s\s\d+', gross_net):
                    gn = gross_net.split(" ")
                    gross_net = gn[1] + "." + gn[3]
                if re.search('\d+\s\d+', net_value):
                    nv = net_value.split(" ")
                    gross_net = nv[1] + "." + nv[2]
                elif re.search('\d+\s\s\d+', net_value):
                    nv = net_value.split(" ")
                    gross_net = nv[1] + "." + nv[3]
                return gross_net.replace(" ",''), net_value.replace(" ",'')
        except Exception as e:
            gross_val,net_val="",""
            return gross_val,net_val
    def get_details(self,text):
        try:
            address, street, state, zipcode, city, = self.get_Paystub_address(text)
            starting_date,pay_freq,string_date_value=self.get_paystub_date(text)
            full_name = self.get_paystub_name(text, street, string_date_value)
            gross_pay,net_pay=self.gross_net(text)
            return state,city,full_name,starting_date,pay_freq,gross_pay,net_pay,string_date_value
        except Exception as e:
            state, city, full_name, starting_date, pay_freq, gross_pay, net_pay,string_date_value="","","","","","","",""
            return state, city, full_name, starting_date, pay_freq, gross_pay, net_pay,string_date_value

