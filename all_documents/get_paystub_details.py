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
import os


class Paystub_details:
    def __init__(self):
        self.code, self.regex_value, self.street, self.address, self.full_address = [], [], [], [], []
        self.pay_frequency,self.current_gross_pay,self.current_net_pay = '','',''
        self.ytd_gross_pay,self.ytd_net_pay = '',''
        self.employment_Start_date=datetime

        self.earnings, self.taxes, self.current_earnings, self.ytd_earnings, self.current_taxes,\
        self.ytd_taxes, self.current_pre_deduction,self.current_post_deduction ,self.ytd_pre_deduction, self.ytd_post_deduction,self.rate_pre_deduction,self.rate_post_deduction, self.hrs_regular, self.rate_regular, self.hrs_post_deduction,self.hrs_pre_deduction,self.rate_taxes, self.hrs_taxes = [], [], [], [], [], [], [], [], [], [], [],[], [], [], [], [], [], []

        self.date_val = []
        self.date = []
        self.pre_deduction=[]
        self.post_deduction=[]

        self.total_calculated_taxes, self.current_total_calculated_taxes, self.ytd_total_calculated_taxes, self.hrs_total_calculated_taxes, self.rate_total_calculated_taxes = [], [], [], [], []
        self.total_calculated_regular, self.current_total_calculated_regular, self.ytd_total_calculated_regular, self.hrs_total_calculated_regular, self.rate_total_calculated_regular = [], [], [], [], []
        self.total_calculated_pre, self.current_total_calculated_pre, self.ytd_total_calculated_pre, self.hrs_total_calculated_pre, self.rate_total_calculated_pre = [], [], [], [], []
        self.total_calculated_post, self.current_total_calculated_post, self.ytd_total_calculated_post, self.hrs_total_calculated_post, self.rate_total_calculated_post = [], [], [], [], []

        self.total_taxes, self.current_total_taxes, self.ytd_total_taxes, self.hrs_total_taxes, self.rate_total_taxes = [], [], [], [], []
        self.total_regular, self.current_total_regular, self.ytd_total_regular, self.hrs_total_regular, self.rate_total_regular = [], [], [], [], []
        self.total_pre, self.current_total_pre, self.ytd_total_pre, self.hrs_total_pre, self.rate_total_pre = [], [], [], [], []
        self.total_post, self.current_total_post, self.ytd_total_post, self.hrs_total_post, self.rate_total_post = [], [], [], [], []

        self.current_gross_net, self.current_net='',''
        self.actual_date = []
        self.date_val1 = []
        self.zip_code=[]
        self.data, self.data1,self.value2 = [], [],[]
        self.c = Common.Common()

        self.license_Address=get_licence_details.Licence_details()

        with open('../config/city.json', 'r') as data_file:
            self.cities = json.load(data_file)

    def paystub_address(self,value):
        try:
            value = value.replace(',', '')
            all_number = re.findall(r"\s\d{1}\s?[A-Za-z]+\s[A-Za-z]+|\s?\s\d{1}\s[A-Za-z] |\s?\s\d{1}\s?[A-Za-z]+|\s\d{4}\s?[A-Za-z]+|\d+[A-Za-z]+\s[A-Za-z]+|\d{2}\s[A-Za-z]+|\:?\d{2}\s[A-Za-z]+|\d{2}-\d{2}\s[A-Za-z]+|\s?\d{3}\w?\s\w+\,?|\s\d{3}\s\d{1}|\w*\s?\d{5}\-?\.?\d{1,4}|\w*\s?\d{5}\s?\-?\.?\s?[A-Za-z]+\d{2,3}|\w*\s?\d{5}\s\w*|\w*\-?\s?\d{5}",value)
            number_val1 = ' '.join(map(str, all_number))
            if re.search(r'\s\s', number_val1):
                number_val1 = number_val1.replace(re.findall(r'\s\s', number_val1)[0], " ")
            print("Number val", number_val1)
            number_val = number_val1
            data = re.findall(r'\b((!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\,?\s?(\d{5}\d{1,4}|\d{5}(?:\s?\-\s?\d{1,4})|\d{5}(?:\s?\-?\s?[A-Za-z]+\d{1,4})|\d{5}(?:\s?\.\s?\d{4})|\-?\d{5}))',number_val)
            if len(data) == 1:
                data.clear()
                all_number = re.findall(r"\s?\s\d{1}\s?[A-Za-z]+|\s?\s\d{1}\s?[A-Za-z]+\s[A-Za-z]+|\s\d{4}\s?[A-Za-z]+|\d+[A-Za-z]+\s[A-Za-z]+|\d{2}\s[A-Za-z]+|\:?\d{2}\s[A-Za-z]+|\d{2}-\d{2}\s[A-Za-z]+|\s?\d{3}\w?\s\w+\,?|\s\d{3}\s\d{1}|\w+\s\d{2,5}\-?\.?\d{2,4}|\w*\s\d{2,5}\-?\.?[A-Za-z]+\d{2,3}|\w*\s?\d{5}\s\w*",value)
                number_val = ' '.join(map(str, all_number))
                print(number_val)
                data = re.findall(r'\b((!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\,?\s(\d{5}\d{1,4}|\d{2,5}(?:\s?\-\s?\d{4})|\d{2,5}(?:\s?\-?\s?[A-Za-z]+\d{1,4})|\d{2,5}(?:\s?\.\s?\d{4})|\d{2,5}))',number_val)
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
                number_val=number_val.split(self.code[0])
                self.regex_value.append(' '.join(map(str, value.split(self.code[0], 1)[0].split()[-15:])))
                if self.code[0] == self.code[1]:
                    self.regex_value.append(' '.join(map(str, value.split(self.code[1])[1].split()[-15:])))
                else:
                    self.regex_value.append(' '.join(map(str, value.split(self.code[1] + " ", 1)[0].split()[-15:])))

                self.regex_value[0] = self.regex_value[0] + " " + self.code[0]
                self.regex_value[1] = self.regex_value[1] + " " + self.code[1]
                self.regex_value[1] = self.regex_value[1].replace(' STAP ', 'ST APT ')
                self.regex_value[0] = self.regex_value[0].replace(' STAP ', 'ST APT ')
                # if re.search('(!?NV|OH|TX|WA|CT|MA|NC|CO|DE|ID|IN|PA|KS|ME|MS|MT|NE|NH|ND|SD|UT|VT|WI)',
                #              self.code[0]):
                #     if re.search(r'[A-Za-z]+\s?(!?2)', self.regex_value[0]):
                #         rv = self.regex_value[0].split(re.findall(r'[A-Za-z]+\s?(!?2)', self.regex_value[0])[0], 1)
                #         self.regex_value[0] = " ".join(rv)
                #     if re.search(r'[A-Za-z]+\s?(!?2)', self.regex_value[1]):
                #         rv1 = self.regex_value[1].split(re.findall(r'[A-Za-z]+\s?(!?2)', self.regex_value[1])[0], 1)
                #         self.regex_value[1] = " ".join(rv1)
                print("address traverse", self.regex_value)

                if re.search(r'[A-Za-z]+(!?' + self.code[0] + ')', value):
                    self.street.append(
                        ' '.join(map(str, number_val[0].split(self.code[0], 1)[0].split()[-3:-1])))
                elif re.search(r'(\s\d+\s([A-Za-z]+)?\s?\s?(\d+)?([A-Za-z]+)?\s?\s?(\d+)?([A-Za-z]+)\s?[#.,/*-]?\s?(\w*)?\s?[#.,/*-]?\d{1,}(\w+)?\s?(\w+)?\s?(\w+)?[./-]?(\w+)?\s?(\w+)?\s?(\w+)?\s?\w+\s?\w+?\s?\w+?\.?\,?\s[A-Z]{2}\-?\s?\d{2,})\b',self.regex_value[0]):
                    if re.search(
                            r'\d+\s\w+\s\d+\w+\s\w+\s\d+\w+\s\w+\s\w+|\d+\s\w+\s\d+\s?\w+\s\w+\s\w+\s\d+\w{1}',
                            self.regex_value[0]):
                        self.street.append(
                            ' '.join(map(str, number_val[0].split(self.code[0], 1)[0].split()[-6:-4])))
                    else:
                        self.street.append(
                            ' '.join(map(str, number_val[0].split(self.code[0], 1)[0].split()[-4:-2])))
                else:
                    self.street.append(
                        ' '.join(map(str, number_val[0].split(self.code[0], 1)[0].split()[-2:])))

                if re.search(r'[A-Za-z]+(!?' + self.code[1] + ')', value):
                    self.street.append(' '.join(map(str, number_val[1].split(self.code[1])[0].split()[-3:-1])))

                elif re.search(r'(\s\d+\s([A-Za-z]+)?\s?\s?(\d+)?([A-Za-z]+)?\s?\s?(\d+)?([A-Za-z]+)\s?[#.,/*-]?\s?(\w*)?\s?[#.,/*-]?\d{1,}(\w+)?\s?(\w+)?\s?(\w+)?[./-]?(\w+)?\s?(\w+)?\s?(\w+)?\s?\w+\s?\w+?\s?\w+?\.?\,?\s[A-Z]{2}\-?\s?\d{2,})\b',self.regex_value[1]):
                    if re.search(r'\d+\s\w+\s\d+\w+\s\w+\s\d+\w+\s\w+\s\w+|\d+\s\w+\s\d+\s?\w+\s\w+\s\w+\s\d+\w{1}',
                            self.regex_value[1]):
                        self.street.append(' '.join(map(str, number_val[1].split(self.code[1], 1)[0].split()[-6:-4])))
                    else:
                        self.street.append(' '.join(map(str, number_val[1].split(self.code[1], 1)[0].split()[-4:-2])))
                else:
                    self.street.append(' '.join(map(str, number_val[1].split(self.code[1])[0].split()[-2:])))

                for i in range(len(self.regex_value)):
                    self.address.append(
                        self.c.find_between_r(self.regex_value[i], self.street[i], self.code[i]))
                    self.full_address.append(self.street[i] + self.address[i] + self.code[i])
                state, zipcode, city = self.c.get_address_zipcode(self.full_address[0],self.code[0])
                state1, zipcode1, city1 = self.c.get_address_zipcode(self.full_address[1],
                                                                     self.code[1])
                actual_city = []

                for i in range(len(self.cities['city'])):
                    if city.lower() == self.cities['city'][i].lower():
                        actual_city.append(self.cities['city'][i])
                    if city1.lower() == self.cities['city'][i].lower():
                        actual_city.append(self.cities['city'][i])
                if actual_city == []:
                    city_dict, street_dict = {}, {}
                    actual_city.append(' '.join( map(str, self.regex_value[0].split(self.code[0], 1)[0].split()[-1:])))
                    actual_city.append(' '.join(map(str, self.regex_value[1].split(self.code[1], 1)[0].split()[-1:])))
                    actual_city[0] = actual_city[0].replace(',', '')
                    actual_city[1] = actual_city[1].replace(',', '')
                    actual_city[0] = actual_city[0].replace('.', '')
                    actual_city[1] = actual_city[1].replace('.', '')
                else:
                    if city != actual_city[0]:
                        actual_city[0] = actual_city[0].upper()
                    else:
                        actual_city.append(actual_city[0])
                    if len(actual_city)==1:
                        if city1 != actual_city[0]:
                            actual_city.append(actual_city[0].upper())
                        else:
                            actual_city.append(actual_city[0])
                    else:
                        if city1 != actual_city[0]:
                            actual_city[1] = actual_city[0].upper()
                        else:
                            actual_city[1] = actual_city[0]

                full_address = self.c.find_between_r(self.regex_value[0], self.street[0],actual_city[0])
                full_address = self.street[0] + " " + full_address
                employer_address = full_address.replace("*", "")

                full_address1 = self.c.find_between_r(self.regex_value[1], self.street[1],actual_city[1])
                full_address1 = self.street[1] + " " + full_address1
                employee_address = full_address1.replace("*", "")

                employer_street=self.street[0]
                employee_street=self.street[1]
                return employer_address,employee_address,employee_street,employer_street,actual_city[0],actual_city[1],state,state1,zipcode,zipcode1

            # full_address, street, state, zipcode, city='','','','',''
            # actual_city=''
            # value=value.replace(',','')
            # value = value.replace(' AJ ', ' NJ ')
            # all_number = re.findall(
            #     r"\s?\s\d{1}\s\w[A-Za-z]+|\s\d{4}\s[A-Za-z]+"
            #     r"|\d{2}\s[A-Za-z]+|\d{2}-\d{2}\s[A-Za-z]+"
            #     r"|\s?\d{3}\w?\s[A-Za-z]+\,?|\s\d{3}\s\d{1}"
            #     r"|\w*\s\d{5}\s?-\s?\d{4}|\w*\s\d{5}\s\w*|\w*\s\d{5}|\w*\s\d{2,5}\s\d{2,3}",
            #     value)
            #
            # number_val = ' '.join(map(str, all_number))
            # #print("Number val",number_val)
            # data = re.findall(
            #     r"\b((?=AL|AK|AS|AZ|AŽ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE"
            #     r"|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)[A-Z]{2}[, ])"
            #     r"(\d{5}(?:\s?-\s?\d{4})?|\d{5}|\d{2,3}(?:\s\d{2,3}))", number_val)
            # if data!=[]:
            #     print("employer_code", data)
            #     for item in data:
            #         self.zip_code.append("".join(item))
            #     if self.zip_code != []:
            #         code=self.zip_code[0]
            #         print("employer_code",code)
            #         reg_value = ' '.join(map(str, value.split(code, 1)[0].split()[-8:]))
            #         reg_value = reg_value + " " + code
            #         #print('in address',reg_value)
            #         # if re.search(r'(\s\d{1,3}\s\w*\s?\w?\s?\w+?\s?\,?\s[A-Z]{2}\s\d{5})\b', reg_value):
            #         if re.search(r'(\d+\s([A-Za-z]+)?\s?([A-Za-z])+?\s?([A-Za-z])+\s?[#.,/]?\s?\w*?\s\d{1,}\s\w+\s?\w+?\s?\w?\,?\s[A-Z]{2}\s\d{5})\b', reg_value):
            #             street = ' '.join(map(str, number_val.split(code, 1)[0].split()[-4:-2]))
            #         else:
            #             street = ' '.join(map(str, number_val.split(code, 1)[0].split()[-2:]))
            #         #print("actual street", street)
            #         address = self.c.find_between_r(value, street, code)
            #         #print("zip code",code)
            #         full_address = street + address + code
            #         state, zipcode, city = self.c.get_address_zipcode(full_address, code)
            #         #print("Full Address:", full_address,zipcode,city,state)
            #         for i in range(len(self.cities['city'])):
            #             if self.cities['city'][i].lower() in city.lower():
            #                 actual_city = self.cities['city'][i]
            #
            #         if actual_city=='':
            #             city=' '.join(map(str, value.split(code, 1)[0].split()[-1:]))
            #             #print(city)
            #         elif city!=actual_city:
            #             city=actual_city.upper()
            #         else:
            #             city=actual_city
            #         full_address = self.c.find_between_r(value, street, city)
            #         if full_address!="":
            #         #print("full",full_address)
            #             full_address = street + full_address
            #             full_address=' '.join(s[:1].upper() + s[1:] for s in full_address.split())
            #             city=city.replace(",","")
            #             city = city.replace(".", "")
            #         else:
            #             full_address=address
            #         return full_address, street, state, zipcode, city
            # else:
            #     data = re.findall(
            #         r"[A-Za-z]+\s[A-Za-z]+\s[A-Za-z]+(!? AL | AK | AS | AZ | AŽ | AR | CA | CO | CT | DE | DC | FM | FL | GA | GU | HI | ID | IL | IN | IA | KS | KY | LA "
            #         r"| ME | MH | MD | MA | MI | MN | MS | MO | MT | NE | NV | NH | NJ | NM | NY | NC | ND | MP "
            #         r"| OH | OK | OR | PW | PA | PR | RI | SC | SD | TN | TX | UT | VT | VI | VA | WA | WV | WI | WY )",
            #         value)
            #     for item in data:
            #         self.zip_code.append("".join(item))
            #     if self.zip_code != []:
            #         code=self.zip_code[0]
            #         reg_value = ' '.join(map(str, value.split(code, 1)[0].split()[-8:]))
            #         reg_value = reg_value + " " + code
            #         #print(reg_value)
            #         if re.search(r'(\d+\s([A-Za-z]+)?\s?([A-Za-z])+?\s?([A-Za-z])+'
            #                      r'\s?[#.,/]?\s?\w*?\s\d{1,3}\s\w+\s?\w+?\s?\w?\,?'
            #                      r'\s[A-Z]{2})\b',reg_value):
            #             street_code=re.findall(r'\s\d+\s+\w+',reg_value)
            #             street=street_code[0]
            #         else:
            #             street_code = re.findall(r'\s\d+\s+\w+', reg_value)
            #             street = street_code[1]
            #         address = self.c.find_between_r(value, street, code)
            #         #print("zip code", code)
            #         full_address = street + address + code
            #         state,zip,city = self.c.get_address_zipcode(full_address, code)
            #         #print("Full Address:", full_address, city, state)
            #         for i in range(len(self.cities['city'])):
            #             if self.cities['city'][i].lower() in city.lower():
            #                 actual_city = self.cities['city'][i]
            #
            #         if actual_city == '':
            #             city = ' '.join(map(str, value.split(code, 1)[0].split()[-1:]))
            #             #print(city)
            #         elif city != actual_city:
            #             city = actual_city.upper()
            #         else:
            #             city = actual_city
            #         full_address = self.c.find_between_r(value, street, city)
            #         #print("full", full_address)
            #         full_address = street + full_address
            #         full_address = ' '.join(s[:1].upper() + s[1:] for s in full_address.split())
            #         city = city.replace(",", "")
            #         city = city.replace(".", "")
            #         zipcode=""
            #
            # return full_address, street, state, zipcode, city
        except Exception as e:
            employer_address, employee_address, employee_street, employer_street, city, city1, state, state1,zipcode,zipcode1 = "", "", "", "", "","", "", "","",""
            return employer_address, employee_address, employee_street, employer_street, city, city1, state, state1,zipcode,zipcode1
    # def employee_address(self, value):
    #     try:
    #         self.zip_code.clear()
    #         full_address, street, state, zipcode, city = '', '', '', '', ''
    #         actual_city = ''
    #         value = value.replace(',', '')
    #         value = value.replace(' AJ ', ' NJ ')
    #         all_number = re.findall(
    #             r"\s?\s\d{1}\s\w[A-Za-z]+|\s\d{4}\s[A-Za-z]+"
    #             r"|\d{2}\s[A-Za-z]+|\d{2}-\d{2}\s[A-Za-z]+"
    #             r"|\s?\d{3}\w?\s[A-Za-z]+\,?|\s\d{3}\s\d{1}"
    #             r"|\w*\s\d{5}\s?-\s?\d{4}|\w*\s\d{5}\s\w*|\w*\s\d{5}|\w*\s\d{2,5}\s\d{2,3}",
    #             value)
    #
    #         number_val = ' '.join(map(str, all_number))
    #         #print("Number val", number_val)
    #         data = re.findall(
    #             r"\b((?=AL|AK|AS|AZ|AŽ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE"
    #             r"|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)[A-Z]{2}[, ])"
    #             r"(\d{5}(?:\s?-\s?\d{4})?|\d{5}|\d{2,3}(?:\s\d{2,3}))", number_val)
    #         if data != []:
    #             print("employee_code",data)
    #             for item in data:
    #                 self.zip_code.append("".join(item))
    #             if self.zip_code != []:
    #                 code = self.zip_code[1]
    #                 print("employee_code",code)
    #
    #                 reg_value = ' '.join(map(str, value.split(code, 1)[0].split()[-8:]))
    #                 reg_value = reg_value + " " + code
    #                 #print('in address', reg_value)
    #                 # if re.search(r'(\s\d{1,3}\s\w*\s?\w?\s?\w+?\s?\,?\s[A-Z]{2}\s\d{5})\b', reg_value):
    #                 if re.search(
    #                         r'(\d+\s([A-Za-z]+)?\s?([A-Za-z])+?\s?([A-Za-z])+\s?[#.,/]?\s?\w*?\s\d{1,}\s\w+\s?\w+?\s?\w?\,?\s[A-Z]{2}\s\d{5})\b',
    #                         reg_value):
    #                     street = ' '.join(map(str, number_val.split(code, 1)[0].split()[-4:-2]))
    #                 else:
    #                     street = ' '.join(map(str, number_val.split(code, 1)[0].split()[-2:]))
    #                 #print("actual street", street)
    #                 address = self.c.find_between_r(value, street, code)
    #                 #print("zip code", code)
    #                 full_address = street + address + code
    #                 state, zipcode, city = self.c.get_address_zipcode(full_address, code)
    #                 #print("Full Address:", full_address, zipcode, city, state)
    #                 for i in range(len(self.cities['city'])):
    #                     if self.cities['city'][i].lower() in city.lower():
    #                         actual_city = self.cities['city'][i]
    #
    #                 if actual_city == '':
    #                     city = ' '.join(map(str, value.split(code, 1)[0].split()[-1:]))
    #                     #print(city)
    #                 elif city != actual_city:
    #                     city = actual_city.upper()
    #                 else:
    #                     city = actual_city
    #                 full_address = self.c.find_between_r(value, street, city)
    #                 #print("full", full_address)
    #                 full_address = street + full_address
    #                 full_address = ' '.join(s[:1].upper() + s[1:] for s in full_address.split())
    #                 city = city.replace(",", "")
    #                 city = city.replace(".", "")
    #                 return full_address, street, state, zipcode, city
    #         else:
    #             data = re.findall(
    #                 r"[A-Za-z]+\s[A-Za-z]+\s[A-Za-z]+(!? AL | AK | AS | AZ | AŽ | AR | CA | CO | CT | DE | DC | FM | FL | GA | GU | HI | ID | IL | IN | IA | KS | KY | LA "
    #                 r"| ME | MH | MD | MA | MI | MN | MS | MO | MT | NE | NV | NH | NJ | NM | NY | NC | ND | MP "
    #                 r"| OH | OK | OR | PW | PA | PR | RI | SC | SD | TN | TX | UT | VT | VI | VA | WA | WV | WI | WY )",
    #                 value)
    #             for item in data:
    #                 self.zip_code.append("".join(item))
    #             if self.zip_code != []:
    #                 code = self.zip_code[1]
    #                 reg_value = ' '.join(map(str, value.split(code, 1)[0].split()[-8:]))
    #                 reg_value = reg_value + " " + code
    #                 #print(reg_value)
    #                 if re.search(r'(\d+\s([A-Za-z]+)?\s?([A-Za-z])+?\s?([A-Za-z])+'
    #                              r'\s?[#.,/]?\s?\w*?\s\d{1,3}\s\w+\s?\w+?\s?\w?\,?'
    #                              r'\s[A-Z]{2})\b', reg_value):
    #                     street_code = re.findall(r'\s\d+\s+\w+', reg_value)
    #                     street = street_code[0]
    #                 else:
    #                     street_code = re.findall(r'\s\d+\s+\w+', reg_value)
    #                     street = street_code[1]
    #                 address = self.c.find_between_r(value, street, code)
    #                 #print("zip code", code)
    #                 full_address = street + address + code
    #                 state, zip, city = self.c.get_address_zipcode(full_address, code)
    #                 #print("Full Address:", full_address, city, state)
    #                 for i in range(len(self.cities['city'])):
    #                     if self.cities['city'][i].lower() in city.lower():
    #                         actual_city = self.cities['city'][i]
    #
    #                 if actual_city == '':
    #                     city = ' '.join(map(str, value.split(code, 1)[0].split()[-1:]))
    #                     #print(city)
    #                 elif city != actual_city:
    #                     city = actual_city.upper()
    #                 else:
    #                     city = actual_city
    #                 full_address = self.c.find_between_r(value, street, city)
    #                 #print("full", full_address)
    #                 full_address = street + full_address
    #                 full_address = ' '.join(s[:1].upper() + s[1:] for s in full_address.split())
    #                 city = city.replace(",", "")
    #                 city = city.replace(".", "")
    #                 zipcode = ""
    #
    #         return full_address, street, state, zipcode, city
    #     except Exception as e:
    #         full_address, street, state, zipcode, city = "", "", "", "", ""
    #         return full_address, street, state, zipcode, city
    def paystub_name(self,value,street,street1):
        try:
            value=value.replace('.'," ")
            name_value = []
            name_value1 = []
            name_val, name_val1 = '', ''
            if street!=street1:
                val=re.compile(r'\s?([A-Za-z]+)?(\-)?\s?(\d+)?\s?([A-Za-z]+)?(\-)?\s?([A-Za-z]+)?(\-)?\s?([A-Za-z]+)?(\-)?\s([A-Za-z]+)?\s?[,.]?\s?\s?([A-Za-z]+)?\s?(\d+)?\s?(!?'+street+r')\b',re.IGNORECASE)
                name_reg_val=val.findall(value)
                for item in name_reg_val:
                    name_value.append(" ".join(item))
                name_val = "".join(map(str, name_value))
                name_val = name_val.replace(street, "")
                if re.search(r'\s\s',name_val):
                    name_val=name_val.replace(re.findall(r'\s\s',name_val)[0]," ")
            if street1==street:
                val = re.compile(
                    r'\s?([A-Za-z]+)?(\-)?\s?(\d+)?\s?([A-Za-z]+)?(\-)?\s?([A-Za-z]+)?(\-)?\s?(['
                    r'A-Za-z]+)?(\-)?\s([A-Za-z]+)?\s?[,.]?\s?\s?([A-Za-z]+)?\s?(\d+)?\s?(!?' + street1 + r')\b',
                    re.IGNORECASE)
                name_reg_val = val.findall(value)
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
                val = re.compile(
                    r'\s?([A-Za-z]+)?(\-)?\s?(\d+)?\s?([A-Za-z]+)?(\-)?\s?([A-Za-z]+)?(\-)?\s?(['
                    r'A-Za-z]+)?(\-)?\s([A-Za-z]+)?\s?[,.]?\s?\s?([A-Za-z]+)?\s?(\d+)?\s?(!?' + street1 + r')\b',
                    re.IGNORECASE)
                name_reg_val1 = val.findall(value)
                for item in name_reg_val1:
                    name_value1.append(" ".join(item))
                name_val1 = "".join(map(str, name_value1))
                name_val1=name_val1.replace(street1,"")
                if re.search(r'\s\s',name_val1):
                    name_val1=name_val1.replace(re.findall(r'\s\s',name_val1)[0]," ")

            print("in name", name_val, name_val1)
            if re.search(r'(!?'+street+'|'+street1+')',name_val):
                rv=re.compile(r'(!?'+street+'|'+street1+')',re.IGNORECASE)
                name_val=name_val.replace(rv.findall(name_val)[0],"")
            if re.search(r'(!?'+street+'|'+street1+')',name_val1):
                rv1 = re.compile(r'(!?' + street + '|' + street1 + ')', re.IGNORECASE)
                name_val1 = name_val1.replace(rv1.findall(name_val1)[0], "")

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

            actual_name = avoid.paystub_replace(actual_name)
            actual_name1 = avoid.paystub_replace(actual_name1)

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
                fname1=full_name1.replace(' - ',"-")
                full_name1=fname1
            if re.search(r'\s\s',full_name1):
                full_name1=full_name1.replace(re.findall(r'\s\s',full_name1)[0]," ")


            employer_name=full_name
            employee_name=full_name1
            employer_name = ' '.join(self.unique_list(employer_name.split()))
            employee_name = ' '.join(self.unique_list(employee_name.split()))
            # name = ' '.join(map(str, value.split(street, 1)[0].split()[-6:]))
            # #print("name", name)
            # name_regex = re.findall(r'([A-Za-z]+[,.&\s]*[A-Za-z]+)+', name)
            # actual_name = " ".join(map(str, name_regex))
            # actual_name = actual_name.replace("NY New York Cit","")
            # actual_name=avoid.replace(actual_name)
            # actual_name=avoid.paystub_replace(actual_name)
            #print("full_name",actual_name)
            return employer_name,employee_name
        except Exception as e:
            full_name = ''
            return full_name
    # def employee_name(self, value, street,zipcode):
    #     try:
    #
    #         name = ' '.join(map(str, value.split(street)[0].split()[-4:]))
    #         print("name in employee",name)
    #         name_regex = re.findall(r'([A-Za-z]+[,.&\s]*[A-Za-z]+)+', name)
    #         actual_name = " ".join(map(str, name_regex))
    #         actual_name = actual_name.replace("NY New York Cit","")
    #         actual_name.replace(" NJ ", "")
    #         actual_name.replace(" Table ", "")
    #         actual_name.replace(" A ", "")
    #         actual_name = avoid.replace(actual_name)
    #         actual_name = avoid.paystub_replace(actual_name)
    #
    #         print(actual_name)
    #         #print("full_name", actual_name)
    #         return actual_name
    #     except Exception as e:
    #         full_name = ''
    #         return full_name
    def unique_list(self,l):
        ulist = []
        [ulist.append(x) for x in l if x not in ulist]
        return ulist
    def get_paystub_date(self, text):
        try:
            #print(text)
            # text = text_value.replace(' ', '')
            advice_pay_date=""
            start_date,end_date,ending_date,advice_pay = "","","",""
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
            if len(self.actual_date)==3:
                starting_date =self.actual_date[0]
                advice_pay = self.actual_date[2]
                ending_date =self.actual_date[1]
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
                        print("end_date", end_date)
                    else:
                        ending_date = datetime.datetime.strptime(ending_date, '%Y/%m/%d').strftime('%m/%d/%Y')
                        starting_date = datetime.datetime.strptime(starting_date, '%Y/%m/%d').strftime('%m/%d/%Y')
                        print(start_date)
                        self.employment_Start_date = dt.strptime(ending_date, "%m/%d/%Y")
                        self.pay_date = dt.strptime(starting_date, "%m/%d/%Y")
                        print("date in paystub", self.pay_date)
                        start_date = self.pay_date.date().strftime('%m/%d/%Y')
                        end_date = self.employment_Start_date.date().strftime('%m/%d/%Y')
                        print("end_date", end_date)

                frequency = abs((self.pay_date - self.employment_Start_date).days)
                print("in paystub days", self.pay_date.date().day)
                if self.pay_date.date().day >= 15:
                    self.pay_frequency = 'Bi-Monthly'
                else:
                    if frequency == 14 or frequency == 13:
                        self.pay_frequency = 'Bi-Weekly'
                    elif frequency == 7 or frequency == 6:
                        self.pay_frequency = 'Weekly'
                    elif frequency == 30 or frequency == 31:
                        self.pay_frequency = 'Monthly'
                    else:
                        self.pay_frequency = ""
                print("in paystub date", str(start_date), end_date, advice_pay_date)
            elif len(self.actual_date)==2:
                advice_pay = self.actual_date[0]
                ending_date = self.actual_date[1]
                start_date=""
                if re.match(r'\d{2}[./-]\d{2}[./-]\d{2}', data):
                    ending_date = datetime.datetime.strptime(ending_date, '%y/%m/%d').strftime('%m/%d/%y')
                    self.employment_Start_date = dt.strptime(ending_date, "%m/%d/%y")
                    end_date = self.employment_Start_date.date().strftime('%m/%d/%y')
                else:
                    ending_date = datetime.datetime.strptime(ending_date, '%Y/%m/%d').strftime('%m/%d/%Y')
                    self.employment_Start_date = dt.strptime(ending_date, "%m/%d/%Y")
                    end_date = self.employment_Start_date.date().strftime('%m/%d/%Y')
            ap=parse(advice_pay)
            advice_pay_date=ap.strftime('%m/%d/%Y')

            return str(start_date), self.pay_frequency, string_date_value,end_date,advice_pay_date
        except Exception as E:
            print(E)
            start_date, self.pay_frequency, string_date_value,end_date,pay_end_date= "", "", "","",""
            return start_date, self.pay_frequency, string_date_value,end_date,pay_end_date
    def get_gross_net_pay(self,path):
        try:
            import paystub_block_values
            paystub_block = paystub_block_values.paystub_gcv()
            _,filename=os.path.split(path)
            blocks1,text = paystub_block.paystub_details(path)
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
                    elif 'Taxes' == pays_keys[i]:
                        if 'Total_Calculated' in item:
                            self.total_calculated_taxes.append(item[0])
                            self.current_total_calculated_taxes.append(item[1])
                            self.ytd_total_calculated_taxes.append(item[2])
                            self.rate_total_calculated_taxes.append(item[3])
                            self.hrs_total_calculated_taxes.append(item[4])
                        elif 'Total' in item:
                            self.total_taxes.append(item[0])
                            self.current_total_taxes.append(item[1])
                            self.ytd_total_taxes.append(item[2])
                            self.rate_total_taxes.append(item[3])
                            self.hrs_total_taxes.append(item[4])
                        else:
                            self.taxes.append(item[0])
                            self.current_taxes.append(item[1])
                            self.ytd_taxes.append(item[2])
                            self.rate_taxes.append(item[3])
                            self.hrs_taxes.append(item[4])
                    elif 'Earnings' == pays_keys[i]:
                        if 'Total_Calculated' in item:
                            self.total_calculated_regular.append(item[0])
                            self.current_total_calculated_regular.append(item[1])
                            self.ytd_total_calculated_regular.append(item[2])
                            self.rate_total_calculated_regular.append(item[3])
                            self.hrs_total_calculated_regular.append(item[4])
                        elif 'Total' in item:
                            self.total_regular.append(item[0])
                            self.current_total_regular.append(item[1])
                            self.ytd_total_regular.append(item[2])
                            self.rate_total_regular.append(item[3])
                            self.hrs_total_regular.append(item[4])
                        else:
                            self.earnings.append(item[0])
                            self.current_earnings.append(item[1])
                            self.ytd_earnings.append(item[2])
                            self.rate_regular.append(item[3])
                            self.hrs_regular.append(item[4])
                    elif 'Pre Tax Deductions' == pays_keys[i]:
                        if 'Total_Calculated' in item:
                            self.total_calculated_pre.append(item[0])
                            self.current_total_calculated_pre.append(item[1])
                            self.ytd_total_calculated_pre.append(item[2])
                            self.rate_total_calculated_pre.append(item[3])
                            self.hrs_total_calculated_pre.append(item[4])
                        elif 'Total' in item:
                            self.total_pre.append(item[0])
                            self.current_total_pre.append(item[1])
                            self.ytd_total_pre.append(item[2])
                            self.rate_total_pre.append(item[3])
                            self.hrs_total_pre.append(item[4])
                        else:
                            self.pre_deduction.append(item[0])
                            self.current_pre_deduction.append(item[1])
                            self.ytd_pre_deduction.append(item[2])
                            self.rate_pre_deduction.append(item[3])
                            self.hrs_pre_deduction.append(item[4])
                    elif 'Post Tax Deductions' == pays_keys[i]:
                        if 'Total_Calculated' in item:
                            self.total_calculated_post.append(item[0])
                            self.current_total_calculated_post.append(item[1])
                            self.ytd_total_calculated_post.append(item[2])
                            self.rate_total_calculated_post.append(item[3])
                            self.hrs_total_calculated_post.append(item[4])
                        elif 'Total' in item:
                            self.total_post.append(item[0])
                            self.current_total_post.append(item[1])
                            self.ytd_total_post.append(item[2])
                            self.rate_total_post.append(item[3])
                            self.hrs_total_post.append(item[4])
                        else:
                            self.post_deduction.append(item[0])
                            self.current_post_deduction.append(item[1])
                            self.ytd_post_deduction.append(item[2])
                            self.rate_post_deduction.append(item[3])
                            self.hrs_post_deduction.append(item[4])
            # print(self.current_gross_pay,self.ytd_gross_pay, self.current_net_pay,self.ytd_net_pay,self.taxes,self.current_taxes,self.ytd_taxes,self.rate_taxes,self.hrs_taxes,self.earnings,self.current_earnings,self.ytd_earnings,self.rate_regular,self.hrs_regular,self.pre_deduction,self.current_pre_deduction,self.ytd_pre_deduction,self.rate_pre_deduction,self.hrs_pre_deduction,self.post_deduction,self.current_post_deduction,self.ytd_post_deduction,self.rate_post_deduction,self.hrs_post_deduction,self.total_calculated_taxes,self.current_total_calculated_taxes,self.ytd_total_calculated_taxes,self.hrs_total_calculated_taxes,self.rate_total_calculated_taxes,self.total_calculated_regular,self.current_total_calculated_regular,self.ytd_total_calculated_regular,self.hrs_total_calculated_regular,self.rate_total_calculated_regular,self.total_calculated_pre,self.current_total_calculated_pre,self.ytd_total_calculated_pre,self.hrs_total_calculated_pre,self.rate_total_calculated_pre,self.total_calculated_post,self.current_total_calculated_post,self.ytd_total_calculated_post,self.hrs_total_calculated_post,self.rate_total_calculated_post,self.total_taxes,self.current_total_taxes,self.ytd_total_taxes,self.hrs_total_taxes,self.rate_total_taxes,self.total_regular,self.current_total_regular,self.ytd_total_regular,self.hrs_total_regular,self.rate_total_regular,self.total_pre,self.current_total_pre,self.ytd_total_pre,self.hrs_total_pre,self.rate_total_pre,self.total_post,self.current_total_post,self.ytd_total_post,self.hrs_total_post,self.rate_total_post)
            return self.current_gross_pay,self.ytd_gross_pay, self.current_net_pay,self.ytd_net_pay,self.taxes,self.current_taxes,self.ytd_taxes,self.rate_taxes,self.hrs_taxes,self.earnings,self.current_earnings,self.ytd_earnings,self.rate_regular,self.hrs_regular,self.pre_deduction,self.current_pre_deduction,self.ytd_pre_deduction,self.rate_pre_deduction,self.hrs_pre_deduction,self.post_deduction,self.current_post_deduction,self.ytd_post_deduction,self.rate_post_deduction,self.hrs_post_deduction,self.total_calculated_taxes,self.current_total_calculated_taxes,self.ytd_total_calculated_taxes,self.hrs_total_calculated_taxes,self.rate_total_calculated_taxes,self.total_calculated_regular,self.current_total_calculated_regular,self.ytd_total_calculated_regular,self.hrs_total_calculated_regular,self.rate_total_calculated_regular,self.total_calculated_pre,self.current_total_calculated_pre,self.ytd_total_calculated_pre,self.hrs_total_calculated_pre,self.rate_total_calculated_pre,self.total_calculated_post,self.current_total_calculated_post,self.ytd_total_calculated_post,self.hrs_total_calculated_post,self.rate_total_calculated_post,self.total_taxes,self.current_total_taxes,self.ytd_total_taxes,self.hrs_total_taxes,self.rate_total_taxes,self.total_regular,self.current_total_regular,self.ytd_total_regular,self.hrs_total_regular,self.rate_total_regular,self.total_pre,self.current_total_pre,self.ytd_total_pre,self.hrs_total_pre,self.rate_total_pre,self.total_post,self.current_total_post,self.ytd_total_post,self.hrs_total_post,self.rate_total_post,text

        except Exception as e:
            print(e)
    def get_details(self,path):
        try:
            #print(text)
            current_gross_pay,ytd_gross_pay, current_net_pay,ytd_net_pay,taxes,current_taxes,ytd_taxes,rate_taxes,\
            hrs_taxes,earnings,current_earnings,ytd_earnings,rate_regular,hrs_regular,pre_deduction,current_pre_deduction,ytd_pre_deduction,rate_pre_deduction,hrs_pre_deduction,post_deduction,current_post_deduction,ytd_post_deduction,rate_post_deduction,hrs_post_deduction,total_calculated_taxes,current_total_calculated_taxes,ytd_total_calculated_taxes,hrs_total_calculated_taxes,rate_total_calculated_taxes,total_calculated_regular,current_total_calculated_regular,ytd_total_calculated_regular,hrs_total_calculated_regular,rate_total_calculated_regular,total_calculated_pre,current_total_calculated_pre,ytd_total_calculated_pre,hrs_total_calculated_pre,rate_total_calculated_pre,total_calculated_post,current_total_calculated_post,ytd_total_calculated_post,hrs_total_calculated_post,rate_total_calculated_post,total_taxes,current_total_taxes,ytd_total_taxes,hrs_total_taxes,rate_total_taxes,total_regular,current_total_regular,ytd_total_regular,hrs_total_regular,rate_total_regular,total_pre,current_total_pre,ytd_total_pre,hrs_total_pre,rate_total_pre,total_post,current_total_post,ytd_total_post,hrs_total_post,rate_total_post,text_value= self.get_gross_net_pay(path)
            # employer_address, employee_address, employee_street, employer_street, employee_city, employer_city, employer_state, employee_state,employee_zipcode,employer_zipcode=self.paystub_address(text_value)
            # employee_full_address, employee_street, employee_state, employee_zipcode, employee_city=self.employee_address(text)
            start_date, pay_frequency, string_date_value, employment_Start_date, pay_date='','','','',''
            employer_address, employee_address, employee_street, employer_street, employee_city, employer_city, employer_state, employee_state, employee_zipcode, employer_zipcode='','','','','','','','','',''
            employer_name, employee_name='',''
            # start_date,pay_frequency, string_date_value,employment_Start_date,pay_date = self.get_paystub_date(text_value)
            # employer_name, employee_name=self.paystub_name(text_value,employer_street,employee_street)
            # employee_name=self.employee_name(text,employee_street,employee_zipcode)
            return employer_address, employer_street, employer_state, employer_zipcode, employer_city,employee_address, employee_street, employee_state, employee_zipcode, employee_city,start_date,pay_frequency, string_date_value,employer_name,employee_name,current_gross_pay,ytd_gross_pay, current_net_pay,ytd_net_pay,taxes,current_taxes,ytd_taxes,rate_taxes,hrs_taxes,earnings,current_earnings,ytd_earnings,rate_regular,hrs_regular,pre_deduction,current_pre_deduction,ytd_pre_deduction,rate_pre_deduction,hrs_pre_deduction,post_deduction,current_post_deduction,ytd_post_deduction,rate_post_deduction,hrs_post_deduction,total_calculated_taxes,current_total_calculated_taxes,ytd_total_calculated_taxes,hrs_total_calculated_taxes,rate_total_calculated_taxes,total_calculated_regular,current_total_calculated_regular,ytd_total_calculated_regular,hrs_total_calculated_regular,rate_total_calculated_regular,total_calculated_pre,current_total_calculated_pre,ytd_total_calculated_pre,hrs_total_calculated_pre,rate_total_calculated_pre,total_calculated_post,current_total_calculated_post,ytd_total_calculated_post,hrs_total_calculated_post,rate_total_calculated_post,total_taxes,current_total_taxes,ytd_total_taxes,hrs_total_taxes,rate_total_taxes,total_regular,current_total_regular,ytd_total_regular,hrs_total_regular,rate_total_regular,total_pre,current_total_pre,ytd_total_pre,hrs_total_pre,rate_total_pre,total_post,current_total_post,ytd_total_post,hrs_total_post,rate_total_post,employment_Start_date,pay_date
        except Exception as e:
            print(e)



