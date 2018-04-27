import json
from datetime import datetime as dt
import datetime
import sys
import re
import difflib

sys.path.insert(0, '../image_processing')
import Common
from dateparser import parse

sys.path.insert(0, '../all_documents')
import get_licence_details
import avoid
import os

DEBUG = False


class Paystub_details:
    def __init__(self):
        self.code, self.regex_value, self.street, self.address, self.full_address = [], [], [], [], []
        self.current_gross_pay, self.current_net_pay = '', ''
        self.ytd_gross_pay, self.ytd_net_pay = '', ''
        self.employment_Start_date = datetime

        self.earnings, self.taxes, self.current_earnings, self.ytd_earnings, self.current_taxes, \
        self.ytd_taxes, self.current_pre_deduction, self.current_post_deduction, self.ytd_pre_deduction, self.ytd_post_deduction, self.rate_pre_deduction, self.rate_post_deduction, self.hrs_regular, self.rate_regular, self.hrs_post_deduction, self.hrs_pre_deduction, self.rate_taxes, self.hrs_taxes = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

        self.date_val = []
        self.date = []
        self.pre_deduction = []
        self.post_deduction = []

        self.total_calculated_taxes, self.current_total_calculated_taxes, self.ytd_total_calculated_taxes, self.hrs_total_calculated_taxes, self.rate_total_calculated_taxes = [], [], [], [], []
        self.total_calculated_regular, self.current_total_calculated_regular, self.ytd_total_calculated_regular, self.hrs_total_calculated_regular, self.rate_total_calculated_regular = [], [], [], [], []
        self.total_calculated_pre, self.current_total_calculated_pre, self.ytd_total_calculated_pre, self.hrs_total_calculated_pre, self.rate_total_calculated_pre = [], [], [], [], []
        self.total_calculated_post, self.current_total_calculated_post, self.ytd_total_calculated_post, self.hrs_total_calculated_post, self.rate_total_calculated_post = [], [], [], [], []

        self.total_taxes, self.current_total_taxes, self.ytd_total_taxes, self.hrs_total_taxes, self.rate_total_taxes = [], [], [], [], []
        self.total_regular, self.current_total_regular, self.ytd_total_regular, self.hrs_total_regular, self.rate_total_regular = [], [], [], [], []
        self.total_pre, self.current_total_pre, self.ytd_total_pre, self.hrs_total_pre, self.rate_total_pre = [], [], [], [], []
        self.total_post, self.current_total_post, self.ytd_total_post, self.hrs_total_post, self.rate_total_post = [], [], [], [], []

        self.current_gross_net, self.current_net = '', ''
        self.actual_date = []
        self.date_val1 = []
        self.zip_code = []
        self.data, self.data1, self.value2 = [], [], []
        self.c = Common.Common()

        with open('../config/name', 'r') as data_file:
            self.name_list = json.load(data_file)

        with open('../config/surname', 'r') as data_file:
            self.surname_list = json.load(data_file)

        self.license_Address = get_licence_details.Licence_details()

        with open('../config/city.json', 'r') as data_file:
            self.cities = json.load(data_file)

        self.pay_begin = ["pay period start", "pay begin date", "pay period begin", "begin date", "period beginning","period. beginning",
                          "period beginning date", "period starting",'pay begin date',"period start",'period begin date',
                          'start date','period start date','period starting date','pay start date']

        self.pay_end = ["pay period end", "pay end date", "end date", "period ending",
                        "period ending date", "period ending",'period end date',"period end"]

        self.pay_date = ["check date", "advice date", "pay date","payment date"]

        self.pay_all = ["period beg/end", "pay period","payroll period","period date",'period']

        self.pay_frequency = ["pay frequency"]
        self.id = ["employee id", "emp no", "employee #", 'employee id #', 'identification no.']
        self.name = ["employee name", "emp name",'name']
        self.emp_name = ["employer name", "name"]
        self.position = ["position", "job title"]
        self.emp_Address = ['employer address', 'address']
        self.employee_Address = ['employee address', 'address']
        self.all_others = self.pay_begin + self.pay_end + self.pay_date + self.pay_all + self.pay_frequency + self.id + self.name + self.emp_name + self.position + self.emp_Address + self.employee_Address

    def custom_print(self, *arg):
        if DEBUG:
            print(arg)

    def paystub_address(self, block, emp_id):
        global city2
        try:

            actual_city1 = ''
            actual_city2 = ''
            if len(block["addresses"]) == []:
                employer_address, employee_address, employee_street, employer_street, city, city1, state, state1, zipcode, zipcode1 = "", "", "", "", "", "", "", "", "", ""
            elif len(block["addresses"]) >= 2:
                if len(block["addresses"][0]['address'])>1:
                    address1 = block["addresses"][0]['address']
                elif len(block["addresses"][0]['address'])>1 and len(block["addresses"]) > 2:
                    address1 = block["addresses"][2]['address']
                if len(block["addresses"][1]['address']) > 1:
                    address2 = block["addresses"][1]['address']
                elif len(block["addresses"][0]['address'])>1 and len(block["addresses"]) > 2:
                    address1 = block["addresses"][4]['address']
                address1 = " ".join(map(str, address1))
                address2 = " ".join(map(str, address2))
                if address1==address2:
                    address2 = block["addresses"][2]['address']
                    address2 = " ".join(map(str, address2))
                address1 = address1.replace(emp_id, '')
                address2 = address2.replace(emp_id, '')
                data = re.findall(
                    r'\b((!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY|York|YORK|JERSEY|Jersey)\s?\.?\,?\-?\s?(\d{5}(?:\s?\-\s?\d{1,4})|\d{5}(?:\s?\.\s?\d{4})|\d{5}))',
                    address1)
                data1 = re.findall(
                    r'\b((!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY|York|YORK|JERSEY|Jersey)\s?\.?\,?\-?\s?(\d{5}(?:\s?\-\s?\d{1,4})|\d{5}(?:\s?\.\s?\d{4})|\d{5}))',
                    address2)
                code = data[0][0]
                code1 = data1[0][0]
                street = re.findall(
                    r'(!?(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)\-?\.?\w?(\w+)?\s?\&?\-?\s?(\w+)?\s?[A-Za-z]+|\d+\-?\.?\w?\d+\s?\-?\s?\d+\s?[A-Za-z]+\s?([A-Za-z]+)?\s?([A-Za-z]+)?|(\w+)?\s?\d+\s?\-?\s?(\d+)?\s?[A-Za-z]+)',
                    address1)[0][0]
                street1 = re.findall(
                    r'(!?(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)\-?\.?\w?(\w+)?\s?\&?\-?\s?(\w+)?\s?[A-Za-z]+|\d+\-?\.?\w?\d+\s?\-?\s?\d+\s?[A-Za-z]+\s?([A-Za-z]+)?\s?([A-Za-z]+)?|(\w+)?\s?\d+\s?\-?\s?(\d+)?\s?[A-Za-z]+)',
                    address2)[0][0]
                addresses1 = self.c.find_between_r(address1, street, code)
                addresses2 = self.c.find_between_r(address2, street1, code1)
                full_address = street + addresses1 + code
                full_address1 = street1 + addresses2 + code1
                full_address = full_address.replace('.', '')
                full_address = full_address.replace(',', '')
                full_address1 = full_address1.replace('.', '')
                full_address1 = full_address1.replace(',', '')
                state, zipcode, city = self.c.get_address_zipcode(full_address, code)
                state1, zipcode1, city1 = self.c.get_address_zipcode(full_address1, code1)
                print("zipcode",zipcode,zipcode1)
                city = city.replace('.', '')
                city = city.replace(',', '')
                city1 = city1.replace('.', '')
                city1 = city1.replace(',', '')
                print("city",city)
                if re.search(r'(!?lowa)', city):
                    city = city.replace('lowa', 'Iowa')
                    full_address = full_address.replace('lowa', 'Iowa')
                if re.search(r'(!?lowa)', city1):
                    city1 = city1.replace('lowa', 'Iowa')
                    full_address1 = full_address1.replace('lowa', 'Iowa')
                for i in range(len(self.cities['city'])):
                    if self.cities['city'][i].lower() in city.lower():
                        actual_city1 = self.cities['city'][i].lower()
                    if self.cities['city'][i].lower() in city1.lower():
                        actual_city2 = self.cities['city'][i].lower()

                if actual_city1 == '':
                    city1 = ' '.join(map(str, full_address.split(code, 1)[0].split()[-1:]))
                    city1 = city1.lower()
                else:
                    city1 = actual_city1
                if actual_city2 == '':
                    city2 = ' '.join(map(str, full_address1.split(code1, 1)[0].split()[-1:]))
                    city2 = city2.lower()
                else:
                    city2 = actual_city2

                actual_full_address = self.c.find_between_r(full_address.lower(), street.lower(), city1)
                actual_full_address = street.lower() + actual_full_address
                actual_full_address1 = self.c.find_between_r(full_address1.lower(), street1.lower(), city2)
                actual_full_address1 = street1.lower() + actual_full_address1

                employer_address = actual_full_address.upper()
                employee_address = actual_full_address1.upper()
                employer_street = street.upper()
                employee_street = street1.upper()
                city1 = city1.replace('.', '').upper()
                city2 = city2.replace('.', '').upper()
                city1 = city1.replace(',', '').upper()
                city2 = city2.replace(',', '').upper()
                # employer_address = employer_address.replace(city1, '')
                # employee_address = employee_address.replace(city2, '')
                all_values = list(block.values())
                pays_keys = list(block.keys())

                for i in range(len(all_values)):
                    if 'Others' in pays_keys[i]:
                        for j in block['Others']:
                            x = difflib.get_close_matches(j[0].lower(),
                                                          [vt.lower() for vt in self.all_others],
                                                          cutoff=0.95)
                            if x:
                                if x[0] in self.emp_Address:
                                    emp_add = j[1]
                                    if emp_add.split()[0].replace(',', '').upper() in employee_address:
                                        empl_address = employee_address
                                        empr_address = employer_address
                                        street = employer_street
                                        street1 = employee_street
                                        empr_city = city1
                                        empl_city = city2
                                        employee_address = empr_address
                                        employer_address = empl_address
                                        employee_street = street
                                        employer_street = street1
                                        city1 = empl_city
                                        city2 = empr_city
                                elif x[0] in self.employee_Address:
                                    emp_add = j[1]
                                    if emp_add.split()[0].replace(',', '').upper() in employer_address:
                                        empl_address = employee_address
                                        empr_address = employer_address
                                        street = employer_street
                                        street1 = employee_street
                                        empr_city = city1
                                        empl_city = city2
                                        employee_address = empr_address
                                        employer_address = empl_address
                                        employee_street = street
                                        employer_street = street1
                                        city1 = empl_city
                                        city2 = empr_city

            else:
                address1 = block["addresses"][0]['address']
                address1 = " ".join(map(str, address1))
                data = re.findall(
                    r'\b((!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY|York|YORK|JERSEY|Jersey)\.?\,?\s?\-?\s?(\d{5}(?:\s?\-\s?\d{1,4})|\d{5}(?:\s?\.\s?\d{4})|\d{5}))',
                    address1)
                code = data[0][0]
                street = re.findall(
                    r'(!?(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)\-?\.?\w?(\w+)?\s?\&?\-?\s?(\w+)?\s?[A-Za-z]+|\d+\-?\.?\w?\d+\s?\-?\s?\d+\s?[A-Za-z]+\s?([A-Za-z]+)?\s?([A-Za-z]+)?|\w?\d+\s?\-?\s?(\d+)?\s?[A-Za-z]+)',
                    address1)[0][0]
                addresses1 = self.c.find_between_r(address1, street, code)
                full_address = street + addresses1 + code
                state, zipcode, city = self.c.get_address_zipcode(full_address, code)
                for i in range(len(self.cities['city'])):
                    if city.lower() == self.cities['city'][i].lower():
                        actual_city1 = self.cities['city'][i]

                if actual_city1 == '':
                    city1 = ' '.join(map(str, full_address.split(code, 1)[0].split()[-1:]))
                elif city != actual_city1:
                    city1 = actual_city1.upper()
                else:
                    city1 = actual_city1
                actual_full_address = self.c.find_between_r(full_address, street, city1)
                actual_full_address = street + " " + actual_full_address
                employer_address = actual_full_address
                # employer_address = employer_address.replace(city1, '')
                employee_address = ''
                employer_street = street
                employee_street = ''
                city1 = city1.replace('.', '')
                city1 = city1.replace(',', '')
                # employer_address = employer_address.replace(city1, '')
                city2 = ''
                state1 = ''
                zipcode1 = ''
            employer_address.replace(',', '')
            employee_address.replace(',', '')
            employer_street.replace(',', '')
            employee_street.replace(',', '')
            if city1!='':
                if city1.split()[0].lower() in employer_address.lower():
                    employer_address=employer_address.rsplit(' ', 1)[0]
            if city2!='':
                if city2.split()[0].lower() in employee_address.lower():
                    employee_address=employee_address.rsplit(' ', 1)[0]

            return employer_address, employee_address, employee_street, employer_street, city1, city2, state, state1, zipcode, zipcode1
        except Exception as e:
            employer_address, employee_address, employee_street, employer_street, city, city1, state, state1, zipcode, zipcode1 = "", "", "", "", "", "", "", "", "", ""
            return employer_address, employee_address, employee_street, employer_street, city, city1, state, state1, zipcode, zipcode1

    def paystub_name(self, block):
        global position, employer_name
        try:

            position = ''
            employee_id = ''
            middle_name = ''
            employee_name = ''
            gross_net_values = list(block.values())
            pays_keys = list(block.keys())
            if len(block["addresses"]) == []:
                employer_name = ''
                employee_name = ''
            if len(block["addresses"]) >= 2:
                name = block["addresses"][0]['name']

                name1 = block["addresses"][1]['name']
                if name==[]:
                    if len(block["addresses"]) > 2:
                        name = block["addresses"][2]['name']
                if name[0]==name1[0]:
                    name1 = block["addresses"][2]['name']
                if name != [] and name1 != []:

                    name1 = name1[0]

                    if re.search(r'(!?\d+\-?\b)', name[0]) or re.search(r'(!?\d+\-?\b)', name1):
                        for i in range(len(gross_net_values)):
                            if 'Others' in pays_keys[i]:
                                for j in block['Others']:
                                    x = difflib.get_close_matches(j[0].lower(), [vt.lower() for vt in self.all_others],
                                                                  cutoff=0.95)
                                    if x:
                                        if x[0] in self.name:
                                            name1 = j[1]
                                        elif x[0] in self.emp_name:
                                            name[0] = j[1]
                                        elif x[0] in self.position:
                                            position = j[1]
                                        elif x[0] in self.id:
                                            employee_id = j[1]
                        ename = name1.split()
                    else:
                        ename = name1.split()
                    employer_name = name[0]
                    if employer_name == 'Attn Payroll':
                        employer_name = block["addresses"][2]['name']

                else:
                    if name == []:
                        employer_name = ''
                    if name1 != '' or name1 != []:
                        name1 = name1[0]

                        if re.search(r'(!?\d+\-?\b)', name1):
                            for i in range(len(gross_net_values)):
                                if 'Others' in pays_keys[i]:
                                    for j in block['Others']:
                                        x = difflib.get_close_matches(j[0].lower(),
                                                                      [vt.lower() for vt in
                                                                       self.all_others],
                                                                      cutoff=0.95)
                                        if x:
                                            if x[0] in self.name:
                                                name1 = j[1]
                                            elif x[0] in self.emp_name:
                                                name[0] = j[1]
                                            elif x[0] in self.position:
                                                position = j[1]
                                            elif x[0] in self.id:
                                                employee_id = j[1]
                            ename = name1.split()
                        else:
                            for i in range(len(gross_net_values)):
                                if 'Others' in pays_keys[i]:
                                    for j in block['Others']:
                                        x = difflib.get_close_matches(j[0].lower(),
                                                                      [vt.lower() for vt in
                                                                       self.all_others],
                                                                      cutoff=0.95)
                                        if x:
                                            if x[0] in self.name:
                                                name1 = j[1]
                                            elif x[0] in self.emp_name:
                                                name[0] = j[1]
                                            elif x[0] in self.position:
                                                position = j[1]
                                            elif x[0] in self.id:
                                                employee_id = j[1]
                            ename = name1.split()
                    else:
                        employee_name = ''
                if name1 != [] or name1 != '':
                    if re.search(r'(!?\,)', name1):
                        if len(ename) == 1:
                            last_name = ename[0]
                            first_name = ""
                            middle_name = ""
                        elif len(ename) == 3:
                            last_name = ename[0]
                            first_name = ename[1]
                            middle_name = ename[2]
                        elif len(ename) > 3:
                            last_name = ename[0]
                            first_name = ename[1]
                            middle_name = ename[2] + " " + ename[3]
                        else:
                            last_name = ename[0]
                            first_name = ename[1]
                            middle_name = ""
                        employee_name = last_name + " " + first_name + " " + middle_name
                    else:
                        if len(ename) == 1:
                            last_name = ""
                            first_name = ename[0]
                            middle_name = ""
                        elif len(ename) == 3:
                            last_name = ename[2]
                            first_name = ename[0]
                            middle_name = ename[1]
                        elif len(ename) > 3:
                            last_name = ename[2] + " " + ename[3]
                            first_name = ename[0]
                            middle_name = ename[1]
                        else:
                            last_name = ename[1]
                            first_name = ename[0]
                        employee_name = first_name + " " + middle_name + " " + last_name

                else:
                    employer_name = ''
                    employee_name = ''
            else:
                if block["addresses"]!=[]:
                    employer_name = block["addresses"][0]['name'][0]
                for i in range(len(gross_net_values)):
                    if 'Others' in pays_keys[i]:
                        for j in block['Others']:
                            x = difflib.get_close_matches(j[0].lower(),
                                                          [vt.lower() for vt in self.all_others],
                                                          cutoff=0.95)
                            if x:
                                if x[0] in self.name:
                                    employee_name = j[1]

            employer_name=employer_name.replace('.', '')
            employee_name=employee_name.replace('.', '')
            employer_name=employer_name.replace(',', '')
            employee_name=employee_name.replace(',', '')
            return employer_name, employee_name, position, employee_id
        except Exception as e:
            employer_name = employee_name = position = employee_id = ''
            return employer_name, employee_name, position, employee_id

    def unique_list(self, l):
        ulist = []
        [ulist.append(x) for x in l if x not in ulist]
        return ulist

    def get_paystub_date(self, block):
        global Start_date, End_date, Pay_date
        try:
            Start_date1=End_date1=''
            pay_freq = ''
            start_date = ''
            end_date = ''
            pay_date = ''
            pay_frequency = ''
            Pay_date = Start_date = End_date = ''
            all_values = list(block.values())
            pays_keys = list(block.keys())
            c = 0
            d, e, f, g, h, i = 0, 0, 0, 0, 0, 0
            for i in range(len(all_values)):
                if 'Others' in pays_keys[i]:
                    for j in block['Others']:
                        x = difflib.get_close_matches(j[0].lower(), [vt.lower() for vt in self.all_others], cutoff=0.95)
                        if x:
                            if x[0] in self.pay_frequency:
                                pay_freq = j[1]
                            elif x[0] in self.pay_begin:
                                start_date = j[1]
                            elif x[0] in self.pay_end:
                                end_date = j[1]
                            elif x[0] in self.pay_date:
                                pay_date = j[1]
                            elif x[0] in self.pay_all:
                                paya = j[1]
                                if re.search(r'\s\-\s', paya):
                                    paya = paya.split(' - ')
                                elif re.search(r'\-\s', paya):
                                    paya = paya.split('- ')
                                elif re.search(r'\s\-', paya):
                                    paya = paya.split(' -')
                                elif re.search(r'\-', paya):
                                    paya = paya.split('-')
                                elif re.search(r'\sto\s', paya):
                                    paya = paya.split(' to ')
                                elif re.search(r'to\s', paya):
                                    paya = paya.split('to ')
                                elif re.search(r'\sto', paya):
                                    paya = paya.split(' to')
                                elif re.search(r'to', paya):
                                    paya = paya.split('to')
                                start_date = paya[0]
                                end_date = paya[1]

            string_date = start_date + " " + end_date + " " + pay_date
            from dateutil.parser import parse
            import datetime
            from datetime import datetime as dt
            datev = string_date.split()
            if len(datev) == 3:
                st = parse(start_date)
                st = st.strftime('%m/%d/%Y')
                et = parse(end_date)
                et = et.strftime('%m/%d/%Y')
                pd = parse(pay_date)
                pd = pd.strftime('%m/%d/%Y')

                starting_date = datetime.datetime.strptime(st, '%m/%d/%Y').strftime('%m/%d/%Y')
                ending_date = datetime.datetime.strptime(et, '%m/%d/%Y').strftime('%m/%d/%Y')
                paying_date = datetime.datetime.strptime(pd, '%m/%d/%Y').strftime('%m/%d/%Y')
                Start_date = dt.strptime(starting_date, "%m/%d/%Y")
                End_date = dt.strptime(ending_date, "%m/%d/%Y")
                Pay_date = dt.strptime(paying_date, "%m/%d/%Y")
                frequency = abs((End_date - Start_date).days)

                if pay_freq == '':
                    if frequency == 15 or frequency == 16:
                        pay_frequency = 'Bi-Monthly'
                    elif frequency == 14 or frequency == 13:
                        pay_frequency = 'Bi-Weekly'
                    elif frequency == 7 or frequency == 6:
                        pay_frequency = 'Weekly'
                    elif frequency >= 28:
                        pay_frequency = 'Monthly'
                    else:
                        pay_frequency = ""
                elif pay_freq.lower() == 'semimonthly' or pay_freq.lower() == 'semi monthly' or pay_freq.lower() == 'semi-monthly':
                    pay_frequency = 'Bi-Monthly'

                string_date = str(Start_date.date()) + " " + str(End_date.date()) + " " + str(Pay_date.date())
                return str(Start_date.date().strftime('%m/%d/%Y')), pay_frequency, string_date, str(
                    End_date.date().strftime('%m/%d/%Y')), str(Pay_date.date().strftime('%m/%d/%Y'))
            else:
                if end_date != '':
                    et = parse(end_date)
                    et = et.strftime('%m/%d/%Y')
                    ending_date = datetime.datetime.strptime(et, '%m/%d/%Y').strftime('%m/%d/%Y')
                    End_date = dt.strptime(ending_date, "%m/%d/%Y").date().strftime('%m/%d/%Y')
                    End_date1 = dt.strptime(ending_date, "%m/%d/%Y")
                if pay_date != '':
                    pd = parse(pay_date)
                    pd = pd.strftime('%m/%d/%Y')
                    paying_date = datetime.datetime.strptime(pd, '%m/%d/%Y').strftime('%m/%d/%Y')
                    Pay_date = dt.strptime(paying_date, "%m/%d/%Y").date().strftime('%m/%d/%Y')
                if start_date != '':
                    sd = parse(start_date)
                    sd = sd.strftime('%m/%d/%Y')
                    starting_date_date = datetime.datetime.strptime(sd, '%m/%d/%Y').strftime('%m/%d/%Y')
                    Start_date = dt.strptime(starting_date_date, "%m/%d/%Y").date().strftime('%m/%d/%Y')
                    Start_date1 = dt.strptime(Start_date, "%m/%d/%Y")

                if Start_date1!='' and End_date1!='':
                   frequency = abs((End_date1 - Start_date1).days)
                   if pay_freq == '':
                       if frequency == 15 or frequency == 16:
                           pay_frequency = 'Bi-Monthly'
                       elif frequency == 14 or frequency == 13:
                           pay_frequency = 'Bi-Weekly'
                       elif frequency == 7 or frequency == 6:
                           pay_frequency = 'Weekly'
                       elif frequency >= 28:
                           pay_frequency = 'Monthly'
                       else:
                           pay_frequency = ""
                   elif pay_freq.lower() == 'semimonthly' or pay_freq.lower() == 'semi monthly' or pay_freq.lower() == 'semi-monthly':
                       pay_frequency = 'Bi-Monthly'
                else:
                    pay_frequency = pay_freq
                return str(Start_date), pay_frequency, string_date, str(End_date), str(Pay_date)
        except Exception as E:
            self.custom_print("Paystub Date Exception", E)
            start_date, self.pay_frequency, string_date_value, end_date, pay_end_date = "", "", "", "", ""
            return start_date, self.pay_frequency, string_date_value, end_date, pay_end_date

    def get_gross_net_pay(self, path):
        try:
            import paystub_block_values
            paystub_block = paystub_block_values.paystub_gcv()
            _, filename = os.path.split(path)
            blocks1, text, result_output_data = paystub_block.paystub_details(path)

            # blocks=self.paystub_block.all_location()
            gross_net_values = list(blocks1.values())
            pays_keys = list(blocks1.keys())
            for i in range(len(gross_net_values)):
                for item in gross_net_values[i]:
                    if 'Gross Pay' in pays_keys[i]:
                        self.current_gross_pay = item[1]
                        self.ytd_gross_pay = item[2]
                    elif 'Net Pay' in pays_keys[i]:
                        self.current_net_pay = item[1]
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
            return self.current_gross_pay, self.ytd_gross_pay, self.current_net_pay, self.ytd_net_pay, self.taxes, self.current_taxes, self.ytd_taxes, self.rate_taxes, self.hrs_taxes, self.earnings, self.current_earnings, self.ytd_earnings, self.rate_regular, self.hrs_regular, self.pre_deduction, self.current_pre_deduction, self.ytd_pre_deduction, self.rate_pre_deduction, self.hrs_pre_deduction, self.post_deduction, self.current_post_deduction, self.ytd_post_deduction, self.rate_post_deduction, self.hrs_post_deduction, self.total_calculated_taxes, self.current_total_calculated_taxes, self.ytd_total_calculated_taxes, self.hrs_total_calculated_taxes, self.rate_total_calculated_taxes, self.total_calculated_regular, self.current_total_calculated_regular, self.ytd_total_calculated_regular, self.hrs_total_calculated_regular, self.rate_total_calculated_regular, self.total_calculated_pre, self.current_total_calculated_pre, self.ytd_total_calculated_pre, self.hrs_total_calculated_pre, self.rate_total_calculated_pre, self.total_calculated_post, self.current_total_calculated_post, self.ytd_total_calculated_post, self.hrs_total_calculated_post, self.rate_total_calculated_post, self.total_taxes, self.current_total_taxes, self.ytd_total_taxes, self.hrs_total_taxes, self.rate_total_taxes, self.total_regular, self.current_total_regular, self.ytd_total_regular, self.hrs_total_regular, self.rate_total_regular, self.total_pre, self.current_total_pre, self.ytd_total_pre, self.hrs_total_pre, self.rate_total_pre, self.total_post, self.current_total_post, self.ytd_total_post, self.hrs_total_post, self.rate_total_post, blocks1, result_output_data, text

        except Exception as e:
            print(e)

    def get_details(self, path):
        try:
            # print(text)
            current_gross_pay, ytd_gross_pay, current_net_pay, ytd_net_pay, taxes, current_taxes, ytd_taxes, rate_taxes, \
            hrs_taxes, earnings, current_earnings, ytd_earnings, rate_regular, hrs_regular, pre_deduction, current_pre_deduction, ytd_pre_deduction, rate_pre_deduction, hrs_pre_deduction, post_deduction, current_post_deduction, ytd_post_deduction, rate_post_deduction, hrs_post_deduction, total_calculated_taxes, current_total_calculated_taxes, ytd_total_calculated_taxes, hrs_total_calculated_taxes, rate_total_calculated_taxes, total_calculated_regular, current_total_calculated_regular, ytd_total_calculated_regular, hrs_total_calculated_regular, rate_total_calculated_regular, total_calculated_pre, current_total_calculated_pre, ytd_total_calculated_pre, hrs_total_calculated_pre, rate_total_calculated_pre, total_calculated_post, current_total_calculated_post, ytd_total_calculated_post, hrs_total_calculated_post, rate_total_calculated_post, total_taxes, current_total_taxes, ytd_total_taxes, hrs_total_taxes, rate_total_taxes, total_regular, current_total_regular, ytd_total_regular, hrs_total_regular, rate_total_regular, total_pre, current_total_pre, ytd_total_pre, hrs_total_pre, rate_total_pre, total_post, current_total_post, ytd_total_post, hrs_total_post, rate_total_post, text_value, result_output_data, text = self.get_gross_net_pay(
                path)

            employer_name, employee_name, position, employee_id = self.paystub_name(text_value)

            employer_address, employee_address, employee_street, employer_street, employer_city, employee_city, employer_state, employee_state, employer_zipcode, employee_zipcode = self.paystub_address(
                text_value, employee_id)
            if len(employer_name.split())<4 and employer_name!='':
                x = difflib.get_close_matches(employer_name.split()[0].lower(), [vt.lower() for vt in self.name_list['names']],
                                              cutoff=0.93)
                y= difflib.get_close_matches(employer_name.split()[1].lower(), [vt.lower() for vt in self.surname_list['surnames']],
                                              cutoff=0.93)
                if not y:
                    y = difflib.get_close_matches(employer_name.split()[2].lower(),
                                                  [vt.lower() for vt in self.surname_list['surnames']],
                                                  cutoff=0.93)
                if x:
                    if y:
                        employee_name=employer_name
                        employee_address=employer_address
                        employee_city=employer_city
                        employee_state=employer_state
                        employee_zipcode=employer_zipcode
                        employee_street=employer_street
                        employer_name=''
                        employer_address=''
                        employer_city=''
                        employer_state=''
                        employer_zipcode=''
                        employer_street=''

            start_date, pay_frequency, string_date_value, employment_Start_date, pay_date = self.get_paystub_date(
                text_value)

            return employer_address, employer_street, employer_state, employer_zipcode, employer_city, employee_address, employee_street, employee_state, employee_zipcode, employee_city, start_date, pay_frequency, string_date_value, employer_name, employee_name, current_gross_pay, ytd_gross_pay, current_net_pay, ytd_net_pay, taxes, current_taxes, ytd_taxes, rate_taxes, hrs_taxes, earnings, current_earnings, ytd_earnings, rate_regular, hrs_regular, pre_deduction, current_pre_deduction, ytd_pre_deduction, rate_pre_deduction, hrs_pre_deduction, post_deduction, current_post_deduction, ytd_post_deduction, rate_post_deduction, hrs_post_deduction, total_calculated_taxes, current_total_calculated_taxes, ytd_total_calculated_taxes, hrs_total_calculated_taxes, rate_total_calculated_taxes, total_calculated_regular, current_total_calculated_regular, ytd_total_calculated_regular, hrs_total_calculated_regular, rate_total_calculated_regular, total_calculated_pre, current_total_calculated_pre, ytd_total_calculated_pre, hrs_total_calculated_pre, rate_total_calculated_pre, total_calculated_post, current_total_calculated_post, ytd_total_calculated_post, hrs_total_calculated_post, rate_total_calculated_post, total_taxes, current_total_taxes, ytd_total_taxes, hrs_total_taxes, rate_total_taxes, total_regular, current_total_regular, ytd_total_regular, hrs_total_regular, rate_total_regular, total_pre, current_total_pre, ytd_total_pre, hrs_total_pre, rate_total_pre, total_post, current_total_post, ytd_total_post, hrs_total_post, rate_total_post, employment_Start_date, pay_date, position, result_output_data, employee_id, text
        except Exception as e:

            employer_address = employer_street = employer_state = employer_zipcode = employer_city = employee_address = employee_street = employee_state = employee_zipcode = employee_city = start_date = pay_frequency = string_date_value = employer_name = employee_name = current_gross_pay = ytd_gross_pay = current_net_pay = ytd_net_pay = taxes = current_taxes = ytd_taxes = rate_taxes = hrs_taxes = earnings = current_earnings = ytd_earnings = rate_regular = hrs_regular = pre_deduction = current_pre_deduction = ytd_pre_deduction = rate_pre_deduction = hrs_pre_deduction = post_deduction = current_post_deduction = ytd_post_deduction = rate_post_deduction = hrs_post_deduction = total_calculated_taxes = current_total_calculated_taxes = ytd_total_calculated_taxes = hrs_total_calculated_taxes = rate_total_calculated_taxes = total_calculated_regular = current_total_calculated_regular = ytd_total_calculated_regular = hrs_total_calculated_regular = rate_total_calculated_regular = total_calculated_pre = current_total_calculated_pre = ytd_total_calculated_pre = hrs_total_calculated_pre = rate_total_calculated_pre = total_calculated_post = current_total_calculated_post = ytd_total_calculated_post = hrs_total_calculated_post = rate_total_calculated_post = total_taxes = current_total_taxes = ytd_total_taxes = hrs_total_taxes = rate_total_taxes = total_regular = current_total_regular = ytd_total_regular = hrs_total_regular = rate_total_regular = total_pre = current_total_pre = ytd_total_pre = hrs_total_pre = rate_total_pre = total_post = current_total_post = ytd_total_post = hrs_total_post = rate_total_post = employment_Start_date = pay_date = position = result = employee_id = text_value = ''

            return employer_address, employer_street, employer_state, employer_zipcode, employer_city, employee_address, employee_street, employee_state, employee_zipcode, employee_city, start_date, pay_frequency, string_date_value, employer_name, employee_name, current_gross_pay, ytd_gross_pay, current_net_pay, ytd_net_pay, taxes, current_taxes, ytd_taxes, rate_taxes, hrs_taxes, earnings, current_earnings, ytd_earnings, rate_regular, hrs_regular, pre_deduction, current_pre_deduction, ytd_pre_deduction, rate_pre_deduction, hrs_pre_deduction, post_deduction, current_post_deduction, ytd_post_deduction, rate_post_deduction, hrs_post_deduction, total_calculated_taxes, current_total_calculated_taxes, ytd_total_calculated_taxes, hrs_total_calculated_taxes, rate_total_calculated_taxes, total_calculated_regular, current_total_calculated_regular, ytd_total_calculated_regular, hrs_total_calculated_regular, rate_total_calculated_regular, total_calculated_pre, current_total_calculated_pre, ytd_total_calculated_pre, hrs_total_calculated_pre, rate_total_calculated_pre, total_calculated_post, current_total_calculated_post, ytd_total_calculated_post, hrs_total_calculated_post, rate_total_calculated_post, total_taxes, current_total_taxes, ytd_total_taxes, hrs_total_taxes, rate_total_taxes, total_regular, current_total_regular, ytd_total_regular, hrs_total_regular, rate_total_regular, total_pre, current_total_pre, ytd_total_pre, hrs_total_pre, rate_total_pre, total_post, current_total_post, ytd_total_post, hrs_total_post, rate_total_post, employment_Start_date, pay_date, position, result, employee_id, text_value


