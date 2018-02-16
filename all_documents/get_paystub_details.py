import json
from datetime import datetime as dt
import datetime
import sys
import re
sys.path.insert(0, '../image_processing')
import Common
from dateparser import parse
sys.path.insert(0, '../all_documents')
import get_licence_details
import avoid
import paystub_block_values

class Paystub_details:
    def __init__(self):
        self.pay_frequency,self.current_gross_pay,self.current_net_pay = '','',''
        self.ytd_gross_pay,self.ytd_net_pay = '',''
        self.employment_Start_date=datetime
        self.earnings, self.deduction, self.other, self.current_earnings, self.ytd_earnings, self.current_deduction,\
        self.ytd_deduction, self.current_other, self.ytd_other = [], [], [], [], [], [], [], [], []
        self.date_val = []
        self.date = []
        self.current_gross_net, self.current_net='',''
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
                    if full_address!="":
                    #print("full",full_address)
                        full_address = street + full_address
                        full_address=' '.join(s[:1].upper() + s[1:] for s in full_address.split())
                        city=city.replace(",","")
                        city = city.replace(".", "")
                    else:
                        full_address=address
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
            name = ' '.join(map(str, value.split(street, 1)[0].split()[-3:]))
            #print("name", name)
            name_regex = re.findall(r'([A-Za-z]+[,.&\s]*[A-Za-z]+)+', name)
            actual_name = " ".join(map(str, name_regex))
            actual_name = actual_name.replace("NY New York Cit","")
            actual_name.replace(" NJ ", "")
            actual_name.replace(" Table ", "")
            actual_name.replace(" A ", "")
            actual_name = avoid.replace(actual_name)

            print(actual_name)
            #print("full_name", actual_name)
            return actual_name
        except Exception as e:
            full_name = ''
            return full_name
    def get_paystub_date(self, text):
        try:
            #print(text)
            # text = text_value.replace(' ', '')
            advice_pay_date=""
            start_date,end_date,ending_date = "","",""
            val = re.findall(
                r'(\w*[A-Za-z]\d{1}\d{2}[./-](19|20|21|22|23|24)\d\d)|(\w*[A-Za-z]\d{1}[./-]\d{2}[./-](19|20|21|22|23|24)\d\d)'
                r'|(\d{2}\s?[./-]\d{2}[./-](19|20|21|22|23|24)\d\d)|(\d{2}\s\d{2}\s(19|20|21|22|23|24)\d\d)'
                r'|(\d{2}[./-]\d{2}\s?(19|20|21|22|23|24)\d\d)|(\d{2}[./-]\d{2}\s?\d\s?\d)|(\d{1,2}\s?[./-]\d{2}[./-]\s?\d{2}\s?\d{2})'
                r'|(\d{2}\d{2}[./-](19|20|21|22|23|24)\d\d)|(\d{2}[./-]\d{2}\s[./-](19|20|21|22|23|24)\d\d)|(([0-9]|0[0-9]'
                r'|1[0-9])[./-]([0-9][0-9]|[0-9])[./-]\d\d)|(([0-9]|0[0-9]'
                r'|1[0-9])[./-]([0-9][0-9]|[0-9])[./-](19|20|21|22|23|24)\d\d|(\d{2}\d{2}[./-]\d\d))\b', text)
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
            print("all date",self.date)
            for value in self.date[:3]:
                if re.match(r'\b\d{2}[./-]\d{2}[./-]\d{2}\b', value):
                    self.actual_date.append(datetime.datetime.strptime(value, '%m/%d/%y').strftime('%y/%m/%d'))
                else:
                    self.actual_date.append(datetime.datetime.strptime(value, '%m/%d/%Y').strftime('%Y/%m/%d'))
            print("all date format", self.actual_date)
            data = " ".join(map(str, self.actual_date))
            print(data)

            starting_date =self.actual_date[0]
            advice_pay = self.actual_date[2]
            ending_date =self.actual_date[1]
            ap=parse(advice_pay)
            advice_pay_date=ap.strftime('%m/%d/%Y')
            if advice_pay != "" and starting_date != "":
            #     for date in self.actual_date:
            #         if date > start_date and date < advice_pay:
                if re.match(r'\d{2}[./-]\d{2}[./-]\d{2}', data):
                    ending_date = datetime.datetime.strptime(ending_date, '%y/%m/%d').strftime('%m/%d/%y')
                    starting_date = datetime.datetime.strptime(starting_date, '%y/%m/%d').strftime('%m/%d/%y')
                    self.employment_Start_date = dt.strptime(ending_date, "%m/%d/%y")
                    self.pay_date = dt.strptime(starting_date, "%m/%d/%y")
                    print("date in paystub", self.pay_date)
                    start_date = self.pay_date.date().strftime('%m/%d/%y')
                    end_date = self.employment_Start_date.date().strftime('%m/%d/%y')
                    print("end_date",end_date)
                else:
                    ending_date = datetime.datetime.strptime(ending_date, '%Y/%m/%d').strftime('%m/%d/%Y')
                    starting_date = datetime.datetime.strptime(starting_date, '%Y/%m/%d').strftime('%m/%d/%Y')
                    print(start_date)
                    self.employment_Start_date = dt.strptime(ending_date, "%m/%d/%Y")
                    self.pay_date = dt.strptime(starting_date, "%m/%d/%Y")
                    print("date in paystub",self.pay_date)
                    start_date = self.pay_date.date().strftime('%m/%d/%Y')
                    end_date=self.employment_Start_date.date().strftime('%m/%d/%Y')
                    print("end_date",end_date)

            frequency = abs((self.pay_date - self.employment_Start_date).days)
            print("in paystub days", self.pay_date.date().day)
            if self.pay_date.date().day>=15:
                self.pay_frequency = 'Bi-Monthly'
            else:
                if frequency==14 or frequency==13:
                    self.pay_frequency = 'Bi-Weekly'
                elif frequency==7 or frequency==6:
                    self.pay_frequency = 'Weekly'
                elif frequency == 30 or frequency == 31:
                    self.pay_frequency = 'Monthly'
                else:
                    self.pay_frequency=""
    #     self.pay_frequency = 'Monthly'
            # elif 8<=self.pay_date.date().day<=14:
            #     self.pay_frequency = 'Bi-Weekly'
            # elif self.pay_date.date().day<=7:
            #     self.pay_frequency = 'Weekly'
            # elif frequency == 30 or frequency == 31:
            #     self.pay_frequency = 'Monthly'
            # else:
            #     self.pay_frequency=''
            # start_date=dt.strptime(start_date, "%m/%d/%Y")
            # #print("staring date",start_date)
            print("in paystub date",str(start_date),end_date,advice_pay_date)
            return str(start_date), self.pay_frequency, string_date_value,end_date,advice_pay_date
        except Exception as E:
            print(E)
            start_date, self.pay_frequency, string_date_value,end_date,pay_end_date= "", "", "","",""
            return start_date, self.pay_frequency, string_date_value,end_date,pay_end_date
    def get_gross_net_pay(self,path,description,result):
        try:
            # self.paystub_block.get_text(path)
            # lines = self.paystub_block.rectify_data()
            # for line in lines:
            #     #print(line)

            blocks1 = self.paystub_block.all_location_details(path,description,result)
            print("in paystub",blocks1)
            # blocks=self.paystub_block.all_location()
            gross_net_values=list(blocks1.values())
            pays_keys=list(blocks1.keys())
            for i in range(len(gross_net_values)):
                for item in gross_net_values[i]:
                    if 'Gross Pay' in pays_keys[i]:
                        self.current_gross_pay=item[1]
                        self.ytd_gross_pay = item[2]
                    elif 'Net Pay'in pays_keys[i]:
                        self.current_net_pay=item[1]
                        self.ytd_net_pay = item[2]

                    elif 'Earnings' in pays_keys[i]:
                        self.earnings.append(item[0])
                        self.current_earnings.append(item[1])
                        self.ytd_earnings.append(item[2])

                    elif 'Taxes' in pays_keys[i]:
                        self.deduction.append(item[0])
                        self.current_deduction.append(item[1])
                        self.ytd_deduction.append(item[2])

                    elif 'Deductions' in pays_keys[i]:
                        self.other.append(item[0])
                        self.current_other.append(item[1])
                        self.ytd_other.append(item[2])
            return self.earnings,self.current_earnings,self.ytd_earnings,self.deduction,self.current_deduction,self.ytd_deduction\
                ,self.other,self.current_other,self.ytd_other,self.current_gross_pay,self.current_net_pay,self.ytd_gross_pay,self.ytd_net_pay
        except Exception as e:
            print(e)
    def get_details(self,text,path,description,result):
        try:
            #print(text)
            earnings, current_earnings, ytd_earnings, deduction, current_deduction, ytd_deduction \
                , other, current_other,ytd_other, current_gross_net, current_net, ytd_gross_pay, ytd_net_pay= self.get_gross_net_pay(path,description,result)
            employer_full_address, employer_street, employer_state, employer_zipcode, employer_city=self.employer_address(text)
            employee_full_address, employee_street, employee_state, employee_zipcode, employee_city=self.employee_address(text)
            start_date,pay_frequency, string_date_value,employment_Start_date,pay_date = self.get_paystub_date(text)
            employer_name=self.employer_name(text,employer_street)
            employee_name=self.employee_name(text,employee_street)
            return employer_full_address, employer_street, employer_state, employer_zipcode, employer_city,employee_full_address, employee_street, employee_state, employee_zipcode, employee_city,start_date,pay_frequency, string_date_value,employer_name,employee_name,earnings, current_earnings, ytd_earnings, deduction, current_deduction, ytd_deduction \
                , other, current_other,ytd_other, current_gross_net, current_net, ytd_gross_pay, ytd_net_pay,employment_Start_date,pay_date
        except Exception as e:
            print(e)



