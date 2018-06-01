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

        with open('../config/city.json', 'r',encoding='utf-8') as data_file:
            self.cities = json.load(data_file)

        self.pay_begin = ["pay period start", "pay begin date", "pay period begin", "begin date", "period beginning","period. beginning",
                          "period beginning date", "period starting",'pay begin date',"period start",'period begin date',
                          'start date','period start date','period starting date','pay start date','check stub for','earns begin date','check stub for the period']

        self.pay_end = ["pay period end", "pay end date", "end date", "period ending",
                        "period ending date", "period ending",'period end date',"period end",'to','earns end date']

        self.pay_date = ["check date", "advice date", "pay date","payment date",'deposite date','with a pay date of','pay day']

        self.pay_all = ["pay period from","period beg/end", "pay period","payroll period","period date",'period','begin/end dates']

        self.pay_frequency = ["pay frequency"]
        self.id = ["employee no.","emplid","employee inforamtion","emp#","emp #","employee#","employee id","employee dd", "emp no", "employee #", 'employee id #', 'identification no.','empl num','employee number','employec id','ee id','personnel id']
        self.name = ["employee","employee name", "emp name",'name','employee full name']
        self.emp_name = ["employer","employer name", "name",'company','employer full name']
        self.position = ["position", "job title"]
        self.emp_Address = ['employer address', 'address']
        self.employee_Address = ['employee address', 'address']
        self.emp_start_date=['hire date']
        self.all_others = self.pay_begin + self.pay_end + self.pay_date + self.pay_all + self.pay_frequency + self.id + self.name + self.emp_name + self.position + self.emp_Address + self.employee_Address+self.emp_start_date

    def custom_print(self, *arg):
        if DEBUG:
            print(arg)

    def paystub_address(self, block, emp_id,employer_name,employee_name):
        global city2, address1, address2, temp_emp_address
        try:

            actual_city1 = ''
            actual_city2 = ''
            if len(block["addresses"]) == []:
                employer_address, employee_address, employee_street, employer_street, city, city1, state, state1, zipcode, zipcode1 = "", "", "", "", "", "", "", "", "", ""

            elif len(block["addresses"]) >= 2:

                if re.search(r'((0[0-9]|1[0-2])\s[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])\s[./-](19|20|21|22)\d\d|(0[0-9]|1[0-2])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-]\d\d|(0[0-9]|1[0-2])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-](19|20|21|22)\d\d|(0[0-9]|1[0-9])\s(0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-](19|20|21|22)\d\d|(0[0-9]|1[0-9])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])\s(19|20|21|22)\d\d|([1-9]|0[0-9]|1[0-2])\s[./-]?([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])\s?[./-]?(19|20|21|22)\d\d|(0[0-9]|1[0-2])\s?[,:./-]?(0[1-9]|1[0-9]|2[0-9]|3[0-1])\s?[,:./-]?(19|20|21|22)\d\d|(0\s?[0-9]|1\s?[0-2])\s?[,:./-]\s?(0\s?[1-9]|1\s?[0-9]|2\s?[0-9]|3\s?[0-1])\s?[,:./-]?(19|20|21|22)\d\d|(0[1-9]|1[0-9]|2[0-9]|3[0-1])[,:./-]?\s?(Jan|Feb|Mar|Apr|May|Jun|July|Jul|Aug|Sept|Sep|Oct|Nov|Dec|january|february|march|april|may|june|july|august|september|october|november|december)\,?\s?(19|20|21|22)\d\d|(Jan|Feb|Mar|Apr|May|Jun|July|Jul|Aug|Sept|Sep|Oct|Nov|Dec|january|february|march|april|may|june|july|august|september|october|november|december)\s?(0[1-9]|1[0-9]|2[0-9]|3[0-1])[,:./-]?\,?\s?(19|20|21|22)\d\d|(19|20|21|22)\d\d\s?[,:./-]?(Jan|Feb|Mar|Apr|May|Jun|July|Jul|Aug|Sept|Sep|Oct|Nov|Dec|january|february|march|april|may|june|july|august|september|october|november|december)[,:./-]?([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])|(0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-](Jan|Feb|Mar|Apr|May|Jun|July|Jul|Aug|Sept|Sep|Oct|Nov|Dec|january|february|march|april|may|june|july|august|september|october|november|december)[./-](19|20|21|22)\d\d|(Jan|Feb|Mar|Apr|May|Jun|July|Jul|Aug|Sept|Sep|Oct|Nov|Dec|january|february|march|april|may|june|july|august|september|october|november|december)[./-]\s(0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-]\,?\s(19|20|21|22)\d\d)', " ".join(map(str, block["addresses"][0]['address']))):
                    address1 = block["addresses"][1]['address']
                    address2 = block["addresses"][2]['address']
                else:
                    if len(block["addresses"][0]['address'])>1:
                        address1 = block["addresses"][0]['address']
                        if not re.search(r'(!?ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)',address1[0].split()[0],re.IGNORECASE) and not re.search('([A-Za-z]+)?|\d+',address1[0].split()[0],re.IGNORECASE):
                            address1 = block["addresses"][2]['address']
                        elif re.search(r'\d+\.\d+',address1[0].split()[0]):
                            address1 = block["addresses"][2]['address']
                    elif len(block["addresses"][0]['address'])==1:
                        address1=block["addresses"][0]['address']
                    elif len(block["addresses"][0]['address'])>1 and len(block["addresses"]) > 2:
                        address1 = block["addresses"][2]['address']
                    else:
                        address1=block["addresses"][0]['address']

                    if len(block["addresses"][1]['address']) > 1:
                        if 'Employee ID' in block["addresses"][1]['address'][0]:
                            address2 = block["addresses"][2]['address']
                        else:
                            address2 = block["addresses"][1]['address']
                    elif len(block["addresses"][1]['address'])==1:
                        address2=block["addresses"][1]['address']
                    elif len(block["addresses"][0]['address'])>1 and len(block["addresses"]) > 3:
                        address2 = block["addresses"][3]['address']
                    else:
                        address2=block["addresses"][1]['address']

                address1 = " ".join(map(str, address1))
                address2 = " ".join(map(str, address2))

                if address1==address2:
                    address2 = block["addresses"][2]['address']
                    address2 = " ".join(map(str, address2))
                address1 = address1.replace(emp_id, '')
                address2 = address2.replace(emp_id, '')
                address1 = address1.replace('.', ' ')
                address2 = address2.replace('.', ' ')
                with open("../config/states", "r") as all_state_val:
                    state_name = all_state_val.read().replace('\n', '')
                with open("../config/postal_code_regex", "r") as post_val:
                    post_code = post_val.read()

                data = re.findall(r'(\s|\,)\b(!?'+state_name+')(\s|\.|\,|\-)('+post_code+')',address1)

                data1 = re.findall(r'(\s|\,)\b(!?'+state_name+')(\s|\.|\,|\-)('+post_code+')',address2)
                if data!=[] and data!=[]:
                    code = " ".join(map(str,data[0]))
                    code1 = " ".join(map(str,data1[0]))
                else:
                    if data==[]:
                        data = re.findall(r'\b(!?' + state_name + ')\s?', address1)


                    if data1==[]:
                        data = re.findall(r'\b(!?' + state_name + ')\s?', address2)
                    code = data[0][0]
                    code1 = data1[0][0]
                code=code.replace('   ',' ').lstrip()
                code1=code1.replace('   ',' ').lstrip()
                code = code.replace('   ', ' ').rstrip()
                code1 = code1.replace('   ', ' ').rstrip()
                val1 = re.compile(
                    r'(!?(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)\-?\.?\w?(\w+)?\s?\&?\-?\s?(\w+)?\s?[A-Za-z]+|\d+\s?\.\s[A-Za-z]+|\d+\s?[A-Za-z]+\s?\.?|(\w+)?\s?(\d+)?\-?\.?\w+?|\s?\d+\s?\-?\s?\d+\s?[A-Za-z]+\s?([A-Za-z]+)?\s?([A-Za-z]+)?|\w+?\d+\s?\-?\s?(\d+)?\s?[A-Za-z]+|[A-Za-z]+\s[A-Za-z]+\s\d+|[A-Za-z]+\.?[A-Za-z]+\.?\s?[A-Za-z]+\s\d+|\d+\s\d+|[A-Za-z]+\s[A-Za-z]+)',
                    re.IGNORECASE)
                street = val1.findall(address1)[0][0]
                val=re.compile(r'(!?(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)\-?\.?\w?(\w+)?\s?\&?\-?\s?(\w+)?\s?[A-Za-z]+|\d+\s?\.\s[A-Za-z]+|\d+\s?[A-Za-z]+\s?\.?|(\w+)?\s?(\d+)?\-?\.?\w+?|\s?\d+\s?\-?\s?\d+\s?[A-Za-z]+\s?([A-Za-z]+)?\s?([A-Za-z]+)?|\w+?\d+\s?\-?\s?(\d+)?\s?[A-Za-z]+|[A-Za-z]+\s[A-Za-z]+\s\d+|[A-Za-z]+\.?[A-Za-z]+\.?\s?[A-Za-z]+\s\d+|\d+\s\d+|[A-Za-z]+\s[A-Za-z]+)',re.IGNORECASE)
                street1 = val.findall(address2)[0][0]
                addresses1 = self.c.find_between_r(address1, street, code)
                addresses2 = self.c.find_between_r(address2, street1, code1)
                full_address = street + addresses1 + code
                full_address1 = street1 + addresses2 + code1
                full_address = full_address.replace('.', '')
                full_address = full_address.replace(',', '')

                full_address1 = full_address1.replace('.', '')
                full_address1 = full_address1.replace(',', '')

                street = street.replace('.', '')
                street = street.replace(',', '')

                street1 = street1.replace('.', '')
                street1 = street1.replace(',', '')
                if re.search(r'\s[A-Za-z]{2}\s\d{5}|\s[A-Za-z]{2}\s?\-\s?\d{5}',full_address):
                    state, zipcode, city = self.c.get_address_zipcode(full_address, code)
                else:
                    state, zipcode, city = self.c.get_address_zipcode(full_address, code)
                    if not re.search(r'(!?NEW|New)\s?\w+', city) and re.search(r'(!?NEW|New)\s?', full_address.split()[-1]):
                        city = city.split()[0]
                        state=re.findall('(!?NEW|New)',full_address)[0]+" "+state

                if re.search(r'\s[A-Za-z]{2}\s\d{5}|\s[A-Za-z]{2}\s?\-\s?\d{5}',full_address):
                    state1, zipcode1, city1 = self.c.get_address_zipcode(full_address1, code1)
                else:
                    state1, zipcode1, city1 = self.c.get_address_zipcode(full_address1, code1)
                    if not re.search(r'(!?NEW|New)\s?\w+', city1) and re.search(r'(!?NEW|New)\s?', full_address.split()[-1]):
                        city1 = city1.split()[0]
                        state = re.findall('(!?NEW|New)', full_address)[0] + " " + state

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
                    if city.lower() in self.cities['city'][i].lower():
                        actual_city1 = self.cities['city'][i].lower()
                    if city1.lower() in self.cities['city'][i].lower():
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

                if full_address.lower().count(city1)>1:
                    street=street.lower()+city1
                if full_address1.lower().count(city2)>1:
                    street1 = street1.lower()+ city2
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
                                        z=zipcode
                                        z1=zipcode1
                                        empr_city = city1
                                        empl_city = city2
                                        employee_address = empr_address
                                        employer_address = empl_address
                                        employee_street = street
                                        employer_street = street1
                                        city1 = empl_city
                                        city2 = empr_city
                                        zipcode=z1
                                        zipcode1=z
                                        s=state
                                        s1=state1
                                        state=s1
                                        state1=s
                                elif x[0] in self.employee_Address:
                                    emp_add = j[1]
                                    if emp_add.split()[0].replace(',', '').upper() in employer_address:
                                        empl_address = employee_address
                                        empr_address = employer_address
                                        street = employer_street
                                        street1 = employee_street
                                        z = zipcode
                                        z1 = zipcode1
                                        empr_city = city1
                                        empl_city = city2
                                        employee_address = empr_address
                                        employer_address = empl_address
                                        employee_street = street
                                        employer_street = street1
                                        city1 = empl_city
                                        city2 = empr_city
                                        zipcode = z1
                                        zipcode1 = z
                                        s = state
                                        s1 = state1
                                        state = s1
                                        state1 = s
            else:
                address1 = block["addresses"][0]['address']
                address1 = " ".join(map(str, address1))
                with open("../config/states", "r") as all_state_val:
                    state_name = all_state_val.read().replace('\n', '')
                with open("../config/postal_code_regex", "r") as post_val:
                    post_code = post_val.read()

                data = re.findall(r'(\s|\,)\b(!?'+state_name+')(\s|\.|\,|\-)('+post_code+')',address1)
                code = " ".join(map(str, data[0]))
                code = code.replace('   ', ' ').lstrip()
                code = code.replace('   ', ' ').rstrip()

                street = re.findall(
                    r'(!?(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)\-?\.?\w?(\w+)?\s?\&?\-?\s?(\w+)?\s?[A-Za-z]+|\d+\s?\.\s[A-Za-z]+|\d+\s?[A-Za-z]+\s?\.?|(\w+)?\s?(\d+)?\-?\.?\w+?|\s?\d+\s?\-?\s?\d+\s?[A-Za-z]+\s?([A-Za-z]+)?\s?([A-Za-z]+)?|\w+?\d+\s?\-?\s?(\d+)?\s?[A-Za-z]+|[A-Za-z]+\s[A-Za-z]+\s\d+|[A-Za-z]+\.?[A-Za-z]+\.?\s?[A-Za-z]+\s\d+|\d+\s\d+|[A-Za-z]+\s[A-Za-z]+)',
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
            employer_address=employer_address.replace(',', '')
            employee_address=employee_address.replace(',', '')
            employer_street=employer_street.replace(',', '')
            employee_street=employee_street.replace(',', '')
            employer_street=employer_street.replace('Of', '')
            employee_street=employee_street.replace('Of', '')
            employer_street=employer_street.replace('OF', '')
            employee_street=employee_street.replace('OF', '')
            if city1!='':
                if city1.split()[0].lower() in employer_address.split()[-1].lower():
                    employer_address=employer_address.rstrip().rsplit(' ', 1)[0]
            if city2!='':
                if city2.split()[0].lower() in employee_address.split()[-1].lower():
                    employee_address=employee_address.rstrip().rsplit(' ', 1)[0]
            if re.search(r'\d{3}-\d{3}-\d{4}',employer_address):
                employer_address = employer_address.replace(re.findall(r'\d{3}-\d{3}-\d{4}',employer_address)[0],'')
                employer_address = employer_address.replace('PAYROLL ACCOUNT','')
                employer_address = employer_address.replace('/','')
            if re.search(r'\d{3}-\d{3}-\d{4}',employee_address):
                employee_address = employee_address.replace(re.findall(r'\d{3}-\d{3}-\d{4}', employee_address)[0], '')
                employee_address = employee_address.replace('PAYROLL ACCOUNT', '')
                employee_address = employee_address.replace('/', '')
            if 'NEW NEW' in state:
                state=state.replace('NEW','')
            if 'NEW NEW' in state1:
                state1=state1.replace('NEW','')
            if 'PG' and city1:
                city1=city1.replace('PG','UPPER MARLBORO PG')
            if 'PG' and city2:
                city2=city2.replace('PG','UPPER MARLBORO PG')
            if employee_name!='' and employer_name in employer_address:
                emp_add=re.findall(r'(!?'+employer_name.replace(' ','|')+')',employer_address)
                for i in emp_add:
                    if i in employer_address.split()[0]:
                        employer_address = employer_address.replace(i, '')
                        employer_address = employer_address.lstrip()
                        employer_address = employer_address.rstrip()
            if employee_name!='' and employee_name in employee_address:
                employee_add=re.findall(r'(!?'+employee_name.replace(' ','|')+')',employee_address)

                for i in employee_add:
                    if i in employee_address.split()[0]:
                        employee_address = employee_address.replace(i, '')
                        employee_address = employee_address.lstrip()
                        employee_address = employee_address.rstrip()
            if employer_address.lower() in employee_address.lower():
                for i in range(len(block["addresses"])):
                    if block["addresses"][i]['name'] != []:
                        if block["addresses"][i]['name'][0].lower()==employee_name:
                            temp_emp_address=block["addresses"][i]['address']
                            temp_emp_address = " ".join(map(str, temp_emp_address))


                            # address1 = address1.replace('.', '')
                            # address1 = address1.replace(',', '')
                            #
                            # address2 = address2.replace('.', '')
                            # address2 = address2.replace(',', '')

                            temp_emp_address = temp_emp_address.replace(emp_id, '')
                            temp_emp_address = temp_emp_address.replace('.', ' ')
                            with open("../config/states", "r") as all_state_val:
                                state_name = all_state_val.read().replace('\n', '')
                            with open("../config/postal_code_regex", "r") as post_val:
                                post_code = post_val.read()

                            data = re.findall(r'(\s|\,)\b(!?' + state_name + ')(\s|\.|\,|\-)(' + post_code + ')', temp_emp_address)


                            if data != []:
                                code = " ".join(map(str, data[0]))
                            else:
                                if data == []:
                                    data = re.findall(r'\b(!?' + state_name + ')\s?', temp_emp_address)

                                code = data[0][0]

                            code = code.replace('   ', ' ').lstrip()
                            code = code.replace('   ', ' ').rstrip()
                            val1 = re.compile(
                                r'(!?(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)\-?\.?\w?(\w+)?\s?\&?\-?\s?(\w+)?\s?[A-Za-z]+|\d+\s?\.\s[A-Za-z]+|\d+\s?[A-Za-z]+\s?\.?|(\w+)?\s?(\d+)?\-?\.?\w+?|\s?\d+\s?\-?\s?\d+\s?[A-Za-z]+\s?([A-Za-z]+)?\s?([A-Za-z]+)?|\w+?\d+\s?\-?\s?(\d+)?\s?[A-Za-z]+|[A-Za-z]+\s[A-Za-z]+\s\d+|[A-Za-z]+\.?[A-Za-z]+\.?\s?[A-Za-z]+\s\d+|\d+\s\d+|[A-Za-z]+\s[A-Za-z]+)',
                                re.IGNORECASE)
                            street = val1.findall(temp_emp_address)[0][0]

                            addresses1 = self.c.find_between_r(temp_emp_address, street, code)

                            full_address = street + addresses1 + code
                            full_address = full_address.replace(',', '')
                            full_address = full_address.replace(',', '')

                            street = street.replace('.', '')
                            street = street.replace(',', '')


                            if re.search(r'\s[A-Za-z]{2}\s\d{5}|\s[A-Za-z]{2}\s?\-\s?\d{5}', full_address):
                                state, zipcode, city = self.c.get_address_zipcode(full_address, code)
                            else:
                                state, zipcode, city = self.c.get_address_zipcode(full_address, code)
                                if not re.search(r'(!?NEW|New)\s?\w+', city) and re.search(r'(!?NEW|New)\s?',
                                                                                           full_address.split()[-1]):
                                    city = city.split()[0]
                                    state = re.findall('(!?NEW|New)', full_address)[0] + " " + state


                            print("zipcode", zipcode, zipcode1)
                            city = city.replace('.', '')
                            city = city.replace(',', '')

                            print("city", city)
                            if re.search(r'(!?lowa)', city):
                                city = city.replace('lowa', 'Iowa')
                                full_address = full_address.replace('lowa', 'Iowa')

                            for i in range(len(self.cities['city'])):
                                if city.lower() in self.cities['city'][i].lower():
                                    actual_city1 = self.cities['city'][i].lower()


                            if actual_city1 == '':
                                city = ' '.join(map(str, full_address.split(code, 1)[0].split()[-1:]))
                                city = city.lower()
                            else:
                                city = actual_city1


                            if full_address.lower().count(city) > 1:
                                street = street.lower() + city

                            actual_full_address = self.c.find_between_r(full_address.lower(), street.lower(), city)
                            actual_full_address = street.lower() + actual_full_address


                            employee_address = actual_full_address.upper()
                            employee_street = street.upper()

                            city1 = city.replace('.', '').upper()
                            city1 = city1.replace(',', '').upper()

            if employee_address.lower() in employer_address.lower():
                for i in range(len(block["addresses"])):
                    if block["addresses"][i]['name']!=[]:
                        if block["addresses"][i]['name'][0].lower()==employer_name:
                            temp_employer_address=block["addresses"][i]['address']
                            temp_employer_address = " ".join(map(str, temp_employer_address))

                            # address1 = address1.replace('.', '')
                            # address1 = address1.replace(',', '')
                            #
                            # address2 = address2.replace('.', '')
                            # address2 = address2.replace(',', '')

                            temp_employer_address = temp_employer_address.replace(emp_id, '')
                            temp_employer_address = temp_employer_address.replace('.', ' ')
                            with open("../config/states", "r") as all_state_val:
                                state_name = all_state_val.read().replace('\n', '')
                            with open("../config/postal_code_regex", "r") as post_val:
                                post_code = post_val.read()

                            data = re.findall(r'(\s|\,)\b(!?' + state_name + ')(\s|\.|\,|\-)(' + post_code + ')',
                                              temp_employer_address)

                            if data != []:
                                code1 = " ".join(map(str, data[0]))
                            else:
                                if data == []:
                                    data = re.findall(r'\b(!?' + state_name + ')\s?', temp_employer_address)

                                code1 = data[0][0]

                            code1 = code1.replace('   ', ' ').lstrip()
                            code1 = code1.replace('   ', ' ').rstrip()
                            val1 = re.compile(
                                r'(!?(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)\-?\.?\w?(\w+)?\s?\&?\-?\s?(\w+)?\s?[A-Za-z]+|\d+\s?\.\s[A-Za-z]+|\d+\s?[A-Za-z]+\s?\.?|(\w+)?\s?(\d+)?\-?\.?\w+?|\s?\d+\s?\-?\s?\d+\s?[A-Za-z]+\s?([A-Za-z]+)?\s?([A-Za-z]+)?|\w+?\d+\s?\-?\s?(\d+)?\s?[A-Za-z]+|[A-Za-z]+\s[A-Za-z]+\s\d+|[A-Za-z]+\.?[A-Za-z]+\.?\s?[A-Za-z]+\s\d+|\d+\s\d+|[A-Za-z]+\s[A-Za-z]+)',
                                re.IGNORECASE)
                            street1 = val1.findall(temp_employer_address)[0][0]

                            addresses2 = self.c.find_between_r(temp_emp_address, street1, code1)

                            full_address1 = street1 + addresses2 + code1
                            full_address1 = full_address1.replace(',', '')
                            full_address1 = full_address1.replace(',', '')

                            street1 = street1.replace('.', '')
                            street1 = street1.replace(',', '')

                            if re.search(r'\s[A-Za-z]{2}\s\d{5}|\s[A-Za-z]{2}\s?\-\s?\d{5}', full_address1):
                                state1, zipcode1, city1 = self.c.get_address_zipcode(full_address1, code1)
                            else:
                                state1, zipcode1, city1 = self.c.get_address_zipcode(full_address1, code1)
                                if not re.search(r'(!?NEW|New)\s?\w+', city) and re.search(r'(!?NEW|New)\s?',
                                                                                           full_address1.split()[-1]):
                                    city1 = city1.split()[0]
                                    state1 = re.findall('(!?NEW|New)', full_address1)[0] + " " + state1


                            city1 = city1.replace('.', '')
                            city1 = city1.replace(',', '')

                            print("city", city1)
                            if re.search(r'(!?lowa)', city1):
                                city = city.replace('lowa', 'Iowa')
                                full_address1 = full_address1.replace('lowa', 'Iowa')

                            for i in range(len(self.cities['city'])):
                                if city1.lower() in self.cities['city'][i].lower():
                                    actual_city2 = self.cities['city'][i].lower()

                            if actual_city2 == '':
                                city1 = ' '.join(map(str, full_address1.split(code1, 1)[0].split()[-1:]))
                                city1 = city1.lower()
                            else:
                                city1 = actual_city2

                            if full_address1.lower().count(city1) > 1:
                                street1 = street1.lower() + city1

                            actual_full_address1 = self.c.find_between_r(full_address1.lower(), street1.lower(), city1)
                            actual_full_address1 = street1.lower() + actual_full_address1

                            employer_address = actual_full_address1.upper()
                            employer_street = street1.upper()

                            city2 = city1.replace('.', '').upper()
                            city2 = city2.replace(',', '').upper()




            return employer_address, employee_address, employee_street, employer_street, city1, city2, state, state1, zipcode, zipcode1
        except Exception as e:
            employer_address, employee_address, employee_street, employer_street, city, city1, state, state1, zipcode, zipcode1 = "", "", "", "", "", "", "", "", "", ""
            return employer_address, employee_address, employee_street, employer_street, city, city1, state, state1, zipcode, zipcode1

    def paystub_name(self, block):
        global position, employer_name
        try:
            employer_name = ''
            position = ''
            employee_id = ''
            middle_name = ''
            employee_name = ''
            gross_net_values = list(block.values())
            pays_keys = list(block.keys())
            # if len(block["addresses"][0]['name']) == []:
            #     employer_name = ''
            #     employee_name = ''
            if block["addresses"]!=[] and len(block["addresses"]) >= 2:
                if len(block["addresses"]) >= 2 or block["addresses"][0]['name']!=[] or block["addresses"][1]['name']!=[]:
                    name = block["addresses"][0]['name']

                    name1 = block["addresses"][1]['name']
                    if name==[]:
                        if len(block["addresses"]) > 2:
                            name = block["addresses"][2]['name']
                    if name1==[]:
                        if len(block["addresses"]) > 2:
                            name1 = block["addresses"][2]['name']
                    if name != [] and name1 != []:
                        if name[0].lower() == name1[0].lower():
                            if len(block["addresses"]) > 2:
                                name1 = block["addresses"][2]['name']
                        name1 = name1[0]
                        if name[0].lower() == name1[0].lower() or name[0].lower() == name1.lower():
                            for i in range(len(gross_net_values)):
                                if 'Others' in pays_keys[i]:
                                    for j in block['Others']:
                                        x = difflib.get_close_matches(j[0].lower(), [vt.lower() for vt in self.all_others],
                                                                      cutoff=0.95)
                                        if x:
                                            if x[0] in self.name:
                                                name1 = j[1]

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

                            ename = name1.split()
                        else:
                            ename = name1.split()
                        employer_name = name[0]
                        if employer_name == 'Attn Payroll':
                            employer_name = block["addresses"][2]['name'][0]

                    else:
                        if name == []:
                            employer_name = ''
                        if name1 != []:
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

                                ename = name1.split()
                        else:
                            name1 = ''
                    if employer_name.lower() == name1.lower():
                        name1 = ''
                    if name1!='':
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
                        employee_name = ''
                else:
                    if block["addresses"][0]['name']!=[]:
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
                                    if x[0] in self.emp_name:
                                        employer_name = j[1]
            else:
                    if block["addresses"][0]['name']!=[]:
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
                                    if x[0] in self.emp_name:
                                        employer_name = j[1]

            for i in range(len(gross_net_values)):
                if 'Others' in pays_keys[i]:
                    for j in block['Others']:
                        x = difflib.get_close_matches(j[0].lower(),
                                                      [vt.lower() for vt in self.all_others],
                                                      cutoff=0.95)
                        if x:
                            if x[0] in self.position:
                                position = j[1]
                            if x[0] in self.id:
                                employee_id = j[1]
                            if x[0] in self.name:
                                if employee_name=='':
                                    employee_name = j[1]
                                continue
                            if x[0] in self.emp_name:
                                if employer_name == '' or employer_name.lower() == 'company':
                                    employer_name = j[1]
            if employer_name.lower()=='earnings statement':
                employer_name=block["addresses"][1]['name'][0]
                employee_name=block["addresses"][2]['name'][0]
            if employer_name.lower() == employee_name.lower():
                employer_name = ''
            employer_name=employer_name.replace('.', '')
            if re.search('(!?\s-\s[A-Za-z].*)', employer_name):
                employer_name = employer_name.replace(re.findall('(!?\s-\s[A-Za-z].*)', employer_name)[0], '')
            employee_name=employee_name.replace('.', '')
            if re.search('(!?\s-\s[A-Za-z].*)', employee_name):
                 employee_name = employee_name.replace(re.findall('(!?\s-\s[A-Za-z].*)', employee_name)[0], '')
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
            emp_start_date = ''
            start_date = ''
            end_date = ''
            pay_date = ''
            pay_frequency = ''
            Pay_date = Start_date = End_date = ''
            all_values = list(block.values())
            pays_keys = list(block.keys())
            for i in range(len(all_values)):
                if 'Others' in pays_keys[i]:
                    for j in block['Others']:
                        x = difflib.get_close_matches(j[0].lower(), [vt.lower() for vt in self.all_others], cutoff=0.95)
                        if x:
                            if x[0] in self.pay_frequency:
                                pay_freq = j[1]
                            elif x[0] in self.emp_start_date:
                                emp_start_date = j[1]
                            elif x[0] in self.pay_begin:
                                start_date = j[1]
                            elif x[0] in self.pay_end:
                                end_date = j[1]
                            elif x[0] in self.pay_date:
                                if pay_date=='':
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
                                elif re.search(r'\sto\s', paya,re.IGNORECASE):
                                    paya = paya.split(re.findall(r'\s(!?To|to|TO)\s', paya)[0])
                                elif re.search(r'to\s', paya,re.IGNORECASE):
                                    paya = paya.split(re.findall(r'(!?To|to|TO)\s', paya)[0])
                                elif re.search(r'\sto', paya,re.IGNORECASE):
                                    paya = paya.split(re.findall(r'\s(!?To|to|TO)', paya)[0])
                                elif re.search(r'to', paya,re.IGNORECASE):
                                    paya = paya.split(re.findall(r'(!?To|to|TO)',paya)[0])
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
                frequency = abs((End_date - Start_date).days)+1

                if pay_freq.lower() == 'semimonthly' or pay_freq.lower() == 'semi monthly' or pay_freq.lower() == 'semi-monthly':
                    pay_frequency = 'Bi-Monthly'

                elif pay_freq == 'Bi-weekly':
                    pay_frequency = 'Bi-Weekly'
                else:
                    if 15<=frequency<28:
                        pay_frequency = 'Bi-Monthly'
                    elif 8<=frequency<15:
                        pay_frequency = 'Bi-Weekly'
                    elif frequency <= 7:
                        pay_frequency = 'Weekly'
                    elif frequency >= 28:
                        pay_frequency = 'Monthly'
                    else:
                        pay_frequency = ""


                string_date = str(Start_date.date()) + " " + str(End_date.date()) + " " + str(Pay_date.date())
                return str(Start_date.date().strftime('%m/%d/%Y')), pay_frequency, string_date, str(End_date.date().strftime('%m/%d/%Y')), str(Pay_date.date().strftime('%m/%d/%Y')),str(emp_start_date)
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
                       elif frequency <= 7:
                           pay_frequency = 'Weekly'
                       elif frequency >= 28:
                           pay_frequency = 'Monthly'
                       else:
                           pay_frequency = ""
                   elif pay_freq.lower() == 'semimonthly' or pay_freq.lower() == 'semi monthly' or pay_freq.lower() == 'semi-monthly':
                       pay_frequency = 'Bi-Monthly'
                   else:
                       if pay_freq=='Bi-weekly':
                            pay_frequency = 'Bi-Weekly'
                return str(Start_date), pay_frequency, string_date, str(End_date), str(Pay_date),str(emp_start_date)
        except Exception as E:
            self.custom_print("Paystub Date Exception", E)
            start_date, self.pay_frequency, string_date_value, end_date, pay_end_date,emp_start_date = "", "", "", "", "",""
            return start_date, self.pay_frequency, string_date_value, end_date, pay_end_date,emp_start_date

    def get_gross_net_pay(self, path):
        try:
            import paystub_block_values
            paystub_block = paystub_block_values.paystub_gcv()
            _, filename = os.path.split(path)
            blocks1, text, result_output_data = paystub_block.paystub_details(path)
            print(blocks1)
            # blocks=self.paystub_block.all_location()
            gross_net_values = list(blocks1.values())
            pays_keys = list(blocks1.keys())
            for i in range(len(gross_net_values)):
                for item in gross_net_values[i]:
                    if 'Gross Pay' in pays_keys[i]:
                        if self.current_gross_pay=='':
                            self.current_gross_pay = item[1]
                            self.ytd_gross_pay = item[2]
                    elif 'Net Pay' in pays_keys[i]:
                        if self.current_net_pay=='':
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
            actual_city2=''
            actual_city1=''
            current_gross_pay, ytd_gross_pay, current_net_pay, ytd_net_pay, taxes, current_taxes, ytd_taxes, rate_taxes, \
            hrs_taxes, earnings, current_earnings, ytd_earnings, rate_regular, hrs_regular, pre_deduction, current_pre_deduction, ytd_pre_deduction, rate_pre_deduction, hrs_pre_deduction, post_deduction, current_post_deduction, ytd_post_deduction, rate_post_deduction, hrs_post_deduction, total_calculated_taxes, current_total_calculated_taxes, ytd_total_calculated_taxes, hrs_total_calculated_taxes, rate_total_calculated_taxes, total_calculated_regular, current_total_calculated_regular, ytd_total_calculated_regular, hrs_total_calculated_regular, rate_total_calculated_regular, total_calculated_pre, current_total_calculated_pre, ytd_total_calculated_pre, hrs_total_calculated_pre, rate_total_calculated_pre, total_calculated_post, current_total_calculated_post, ytd_total_calculated_post, hrs_total_calculated_post, rate_total_calculated_post, total_taxes, current_total_taxes, ytd_total_taxes, hrs_total_taxes, rate_total_taxes, total_regular, current_total_regular, ytd_total_regular, hrs_total_regular, rate_total_regular, total_pre, current_total_pre, ytd_total_pre, hrs_total_pre, rate_total_pre, total_post, current_total_post, ytd_total_post, hrs_total_post, rate_total_post, text_value, result_output_data, text = self.get_gross_net_pay(
                path)

            start_date, pay_frequency, string_date_value, employment_Start_date, pay_date,emp_start_date = self.get_paystub_date(
                text_value)

            employer_name, employee_name, position, employee_id = self.paystub_name(text_value)

            employer_address, employee_address, employee_street, employer_street, employer_city, employee_city, employer_state, employee_state, employer_zipcode, employee_zipcode = self.paystub_address(
                text_value, employee_id,employer_name,employee_name)
            if 1<len(employer_name.split())<=5 and employer_name!='':
                x = difflib.get_close_matches(employer_name.split()[0].lower(), [vt.lower() for vt in self.name_list['names']],
                                              cutoff=0.93)
                y= difflib.get_close_matches(employer_name.split()[1].lower(), [vt.lower() for vt in self.surname_list['surnames']],
                                              cutoff=0.93)
                if not y:
                    if len(employer_name.split())>2:

                        y = difflib.get_close_matches(employer_name.split()[2].lower(),
                                                      [vt.lower() for vt in self.surname_list['surnames']],
                                                      cutoff=0.93)
                if x:
                    if y:
                        en=employee_name
                        employee_name=employer_name
                        employer_name=en
                        for i in range(len(text_value["addresses"])):
                                if text_value["addresses"][i]['name'] != []:
                                    if text_value["addresses"][i]['name'][0].lower() == employee_name.lower():
                                        temp_emp_address = text_value["addresses"][i]['address']
                                        temp_emp_address = " ".join(map(str, temp_emp_address))

                                        # address1 = address1.replace('.', '')
                                        # address1 = address1.replace(',', '')
                                        #
                                        # address2 = address2.replace('.', '')
                                        # address2 = address2.replace(',', '')

                                        temp_emp_address = temp_emp_address.replace(employee_id, '')
                                        temp_emp_address = temp_emp_address.replace('.', ' ')
                                        with open("../config/states", "r") as all_state_val:
                                            state_name = all_state_val.read().replace('\n', '')
                                        with open("../config/postal_code_regex", "r") as post_val:
                                            post_code = post_val.read()

                                        data = re.findall(
                                            r'(\s|\,)\b(!?' + state_name + ')(\s|\.|\,|\-)(' + post_code + ')',
                                            temp_emp_address)

                                        if data != []:
                                            code = " ".join(map(str, data[0]))
                                        else:
                                            if data == []:
                                                data = re.findall(r'\b(!?' + state_name + ')\s?', temp_emp_address)

                                            code = data[0][0]

                                        code = code.replace('   ', ' ').lstrip()
                                        code = code.replace('   ', ' ').rstrip()
                                        val1 = re.compile(
                                            r'(!?(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)\-?\.?\w?(\w+)?\s?\&?\-?\s?(\w+)?\s?[A-Za-z]+|\d+\s?\.\s[A-Za-z]+|\d+\s?[A-Za-z]+\s?\.?|(\w+)?\s?(\d+)?\-?\.?\w+?|\s?\d+\s?\-?\s?\d+\s?[A-Za-z]+\s?([A-Za-z]+)?\s?([A-Za-z]+)?|\w+?\d+\s?\-?\s?(\d+)?\s?[A-Za-z]+|[A-Za-z]+\s[A-Za-z]+\s\d+|[A-Za-z]+\.?[A-Za-z]+\.?\s?[A-Za-z]+\s\d+|\d+\s\d+|[A-Za-z]+\s[A-Za-z]+)',
                                            re.IGNORECASE)
                                        street = val1.findall(temp_emp_address)[0][0]

                                        addresses1 = self.c.find_between_r(temp_emp_address, street, code)

                                        full_address = street + addresses1 + code
                                        full_address = full_address.replace(',', '')
                                        full_address = full_address.replace(',', '')

                                        street = street.replace('.', '')
                                        street = street.replace(',', '')

                                        if re.search(r'\s[A-Za-z]{2}\s\d{5}|\s[A-Za-z]{2}\s?\-\s?\d{5}', full_address):
                                            state, zipcode, city = self.c.get_address_zipcode(full_address, code)
                                        else:
                                            state, zipcode, city = self.c.get_address_zipcode(full_address, code)
                                            if not re.search(r'(!?NEW|New)\s?\w+', city) and re.search(r'(!?NEW|New)\s?',
                                                                                                       full_address.split()[
                                                                                                           -1]):
                                                city = city.split()[0]
                                                state = re.findall('(!?NEW|New)', full_address)[0] + " " + state


                                        city = city.replace('.', '')
                                        city = city.replace(',', '')

                                        print("city", city)
                                        if re.search(r'(!?lowa)', city):
                                            city = city.replace('lowa', 'Iowa')
                                            full_address = full_address.replace('lowa', 'Iowa')

                                        for i in range(len(self.cities['city'])):
                                            if city.lower() in self.cities['city'][i].lower():
                                                actual_city1 = self.cities['city'][i].lower()

                                        if actual_city1 == '':
                                            city = ' '.join(map(str, full_address.split(code, 1)[0].split()[-1:]))
                                            city = city.lower()
                                        else:
                                            city = actual_city1

                                        if full_address.lower().count(city) > 1:
                                            street = street.lower() + city

                                        actual_full_address = self.c.find_between_r(full_address.lower(), street.lower(),
                                                                                    city)
                                        actual_full_address = street.lower() + actual_full_address

                                        employee_address = actual_full_address.upper()
                                        employee_street = street.upper()
                                        employer_zipcode = zipcode
                                        employer_state = state
                                        city1 = city.replace('.', '').upper()
                                        employee_city = city1.replace(',', '').upper()
                        for i in range(len(text_value["addresses"])):
                                if text_value["addresses"][i]['name'] != []:
                                    if text_value["addresses"][i]['name'][0].lower() == employer_name.lower():
                                        temp_employer_address = text_value["addresses"][i]['address']
                                        temp_employer_address = " ".join(map(str, temp_employer_address))

                                        temp_employer_address = temp_employer_address.replace(employee_id, '')
                                        temp_employer_address = temp_employer_address.replace('.', ' ')
                                        with open("../config/states", "r") as all_state_val:
                                            state_name = all_state_val.read().replace('\n', '')
                                        with open("../config/postal_code_regex", "r") as post_val:
                                            post_code = post_val.read()

                                        data = re.findall(
                                            r'(\s|\,)\b(!?' + state_name + ')(\s|\.|\,|\-)(' + post_code + ')',
                                            temp_employer_address)

                                        if data != []:
                                            code1 = " ".join(map(str, data[0]))
                                        else:
                                            if data == []:
                                                data = re.findall(r'\b(!?' + state_name + ')\s?', temp_employer_address)

                                            code1 = data[0][0]

                                        code1 = code1.replace('   ', ' ').lstrip()
                                        code1 = code1.replace('   ', ' ').rstrip()
                                        val1 = re.compile(
                                            r'(!?(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)\-?\.?\w?(\w+)?\s?\&?\-?\s?(\w+)?\s?[A-Za-z]+|\d+\s?\.\s[A-Za-z]+|\d+\s?[A-Za-z]+\s?\.?|(\w+)?\s?(\d+)?\-?\.?\w+?|\s?\d+\s?\-?\s?\d+\s?[A-Za-z]+\s?([A-Za-z]+)?\s?([A-Za-z]+)?|\w+?\d+\s?\-?\s?(\d+)?\s?[A-Za-z]+|[A-Za-z]+\s[A-Za-z]+\s\d+|[A-Za-z]+\.?[A-Za-z]+\.?\s?[A-Za-z]+\s\d+|\d+\s\d+|[A-Za-z]+\s[A-Za-z]+)',
                                            re.IGNORECASE)
                                        street1 = val1.findall(temp_employer_address)[0][0]

                                        addresses2 = self.c.find_between_r(temp_employer_address, street1, code1)

                                        full_address1 = street1 + addresses2 + code1
                                        full_address1 = full_address1.replace(',', '')
                                        full_address1 = full_address1.replace(',', '')

                                        street1 = street1.replace('.', '')
                                        street1 = street1.replace(',', '')

                                        if re.search(r'\s[A-Za-z]{2}\s\d{5}|\s[A-Za-z]{2}\s?\-\s?\d{5}', full_address1):
                                            state1, zipcode1, city1 = self.c.get_address_zipcode(full_address1, code1)
                                        else:
                                            state1, zipcode1, city1 = self.c.get_address_zipcode(full_address1, code1)
                                            if not re.search(r'(!?NEW|New)\s?\w+', city1) and re.search(r'(!?NEW|New)\s?',
                                                                                                       full_address1.split()[
                                                                                                           -1]):
                                                city1 = city1.split()[0]
                                                state1 = re.findall('(!?NEW|New)', full_address1)[0] + " " + state1

                                        city1 = city1.replace('.', '')
                                        city1 = city1.replace(',', '')

                                        print("city", city1)
                                        if re.search(r'(!?lowa)', city1):
                                            city1 = city1.replace('lowa', 'Iowa')
                                            full_address1 = full_address1.replace('lowa', 'Iowa')

                                        for i in range(len(self.cities['city'])):
                                            if city1.lower() in self.cities['city'][i].lower():
                                                actual_city2 = self.cities['city'][i].lower()

                                        if actual_city2 == '':
                                            city1 = ' '.join(map(str, full_address1.split(code1, 1)[0].split()[-1:]))
                                            city1 = city1.lower()
                                        else:
                                            city1 = actual_city2

                                        if full_address1.lower().count(city1) > 1:
                                            street1 = street1.lower() + city1

                                        actual_full_address1 = self.c.find_between_r(full_address1.lower(), street1.lower(),
                                                                                     city1)
                                        actual_full_address1 = street1.lower() + actual_full_address1

                                        employer_address = actual_full_address1.upper()
                                        employer_street = street1.upper()
                                        employer_zipcode=zipcode1
                                        employer_state=state1

                                        city2 = city1.replace('.', '').upper()
                                        employer_city = city2.replace(',', '').upper()
            employee_address=employee_address.upper()
            employer_address=employer_address.upper()
            employer_address = employer_address.replace(employer_name, '')
            employer_address = employer_address.replace(employee_name, '')
            employee_address = employee_address.replace(employer_name, '')
            employee_address = employee_address.replace(employee_name, '')
            return employer_address, employer_street, employer_state.upper(), employer_zipcode, employer_city.upper(), employee_address, employee_street, employee_state.upper(), employee_zipcode, employee_city.upper(), start_date, pay_frequency, string_date_value, employer_name.upper(), employee_name.upper(), current_gross_pay, ytd_gross_pay, current_net_pay, ytd_net_pay, taxes, current_taxes, ytd_taxes, rate_taxes, hrs_taxes, earnings, current_earnings, ytd_earnings, rate_regular, hrs_regular, pre_deduction, current_pre_deduction, ytd_pre_deduction, rate_pre_deduction, hrs_pre_deduction, post_deduction, current_post_deduction, ytd_post_deduction, rate_post_deduction, hrs_post_deduction, total_calculated_taxes, current_total_calculated_taxes, ytd_total_calculated_taxes, hrs_total_calculated_taxes, rate_total_calculated_taxes, total_calculated_regular, current_total_calculated_regular, ytd_total_calculated_regular, hrs_total_calculated_regular, rate_total_calculated_regular, total_calculated_pre, current_total_calculated_pre, ytd_total_calculated_pre, hrs_total_calculated_pre, rate_total_calculated_pre, total_calculated_post, current_total_calculated_post, ytd_total_calculated_post, hrs_total_calculated_post, rate_total_calculated_post, total_taxes, current_total_taxes, ytd_total_taxes, hrs_total_taxes, rate_total_taxes, total_regular, current_total_regular, ytd_total_regular, hrs_total_regular, rate_total_regular, total_pre, current_total_pre, ytd_total_pre, hrs_total_pre, rate_total_pre, total_post, current_total_post, ytd_total_post, hrs_total_post, rate_total_post, employment_Start_date, pay_date, position, result_output_data, employee_id, text,emp_start_date
        except Exception as e:

            employer_address = employer_street = employer_state = employer_zipcode = employer_city = employee_address = employee_street = employee_state = employee_zipcode = employee_city = start_date = pay_frequency = string_date_value = employer_name = employee_name = current_gross_pay = ytd_gross_pay = current_net_pay = ytd_net_pay = taxes = current_taxes = ytd_taxes = rate_taxes = hrs_taxes = earnings = current_earnings = ytd_earnings = rate_regular = hrs_regular = pre_deduction = current_pre_deduction = ytd_pre_deduction = rate_pre_deduction = hrs_pre_deduction = post_deduction = current_post_deduction = ytd_post_deduction = rate_post_deduction = hrs_post_deduction = total_calculated_taxes = current_total_calculated_taxes = ytd_total_calculated_taxes = hrs_total_calculated_taxes = rate_total_calculated_taxes = total_calculated_regular = current_total_calculated_regular = ytd_total_calculated_regular = hrs_total_calculated_regular = rate_total_calculated_regular = total_calculated_pre = current_total_calculated_pre = ytd_total_calculated_pre = hrs_total_calculated_pre = rate_total_calculated_pre = total_calculated_post = current_total_calculated_post = ytd_total_calculated_post = hrs_total_calculated_post = rate_total_calculated_post = total_taxes = current_total_taxes = ytd_total_taxes = hrs_total_taxes = rate_total_taxes = total_regular = current_total_regular = ytd_total_regular = hrs_total_regular = rate_total_regular = total_pre = current_total_pre = ytd_total_pre = hrs_total_pre = rate_total_pre = total_post = current_total_post = ytd_total_post = hrs_total_post = rate_total_post = employment_Start_date = pay_date = position = result = employee_id = text_value=emp_start_date = ''

            return employer_address, employer_street, employer_state, employer_zipcode, employer_city, employee_address, employee_street, employee_state, employee_zipcode, employee_city, start_date, pay_frequency, string_date_value, employer_name, employee_name, current_gross_pay, ytd_gross_pay, current_net_pay, ytd_net_pay, taxes, current_taxes, ytd_taxes, rate_taxes, hrs_taxes, earnings, current_earnings, ytd_earnings, rate_regular, hrs_regular, pre_deduction, current_pre_deduction, ytd_pre_deduction, rate_pre_deduction, hrs_pre_deduction, post_deduction, current_post_deduction, ytd_post_deduction, rate_post_deduction, hrs_post_deduction, total_calculated_taxes, current_total_calculated_taxes, ytd_total_calculated_taxes, hrs_total_calculated_taxes, rate_total_calculated_taxes, total_calculated_regular, current_total_calculated_regular, ytd_total_calculated_regular, hrs_total_calculated_regular, rate_total_calculated_regular, total_calculated_pre, current_total_calculated_pre, ytd_total_calculated_pre, hrs_total_calculated_pre, rate_total_calculated_pre, total_calculated_post, current_total_calculated_post, ytd_total_calculated_post, hrs_total_calculated_post, rate_total_calculated_post, total_taxes, current_total_taxes, ytd_total_taxes, hrs_total_taxes, rate_total_taxes, total_regular, current_total_regular, ytd_total_regular, hrs_total_regular, rate_total_regular, total_pre, current_total_pre, ytd_total_pre, hrs_total_pre, rate_total_pre, total_post, current_total_post, ytd_total_post, hrs_total_post, rate_total_post, employment_Start_date, pay_date, position, result, employee_id, text_value,emp_start_date


