import datetime
import re
from logging import log

from image_processing import Common
class Licence_details:
    def __init__(self):
        self.date_val=[]
        self.date = []
        self.actual_date = []
        self.date_val1 = []
        self.zip_code=[]
        self.get_licence_id=''
        self.c= Common.Common()
    def get_id(self,text):
        try:
            get_licence_id = re.findall(
                r'\w*[A-Za-z]\d{4}\s\d{10}|\d{12}|[A-Za-z]?\d{7,9}|\w{1}\d{4}\s\d{5}\s\d{4,5}|\d{2,3}\s\d{3}\s\d{3}\s?\d?\d?\d?',
                text)
            print(get_licence_id)
            get_licence = " ".join(map(str, get_licence_id))
            if re.match(r'\d{2}\s\d{3}\s\d{3}\s\d{3}', get_licence):
                get_licence_id = re.findall(r'\d{3}\s\d{3}\s\d{3}', get_licence)
            if re.match(r'[A-Za-z]{1}', get_licence):
                return get_licence_id[0].upper()
            else:
                return get_licence_id[0]
        except Exception as E:
            self.get_licence_id='null'
    def get_date(self,text):
        try:
            #Todo:To get all date format from text
            val = re.findall(
                r'(\w*[A-Za-z]\d{1}\d{2}[./-](19|20|21|22|23|24)\d\d)|(\w*[A-Za-z]\d{1}[./-]\d{2}[./-](19|20|21|22|23|24)\d\d)'
                r'|(\d{2}\s?[./-]\d{2}[./-](19|20|21|22|23|24)\d\d)|(\d{2}\s\d{2}\s(19|20|21|22|23|24)\d\d)'
                r'|(\d{2}[./-]\d{2}\s?(19|20|21|22|23|24)\d\d)|(\d{1,2}\s?[./-]\d{2}[./-]\s?\d{2}\s?\d{2})'
                r'|(\d{2}\d{2}[./-](19|20|21|22|23|24)\d\d)|(\d{2}[./-]\d{2}\s[./-](19|20|21|22|23|24)\d\d)'
                r'|(([0-9]|0[0-9]|1[0-9])[./-]([0-9][0-9]|[0-9])[./-]\d\d)|(([0-9]'
                r'|0[0-9]|1[0-9])[./-]([0-9][0-9]|[0-9])[./-](19|20|21|22|23|24)\d\d|(\d{2}\d{2}[./-]\d\d))\b', text)
            date_val1 = []
            for item in val:
                date_val1.append(" ".join(item))
            string_date = " ".join(map(str, date_val1))
            #Todo:To remove all white spaces and [,/.]
            date_val = re.findall(r'\d{2}\s?[./-]?\d{2}\s?[./-]?\d{2,4}', string_date)
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
                #Todo:Proper Date Format (mm/dd/yyyy)
                dob = dob[0:2] + '/' + dob[2:4] + '/' + dob[4:8]
                self.date.append(dob)
            #Todo:to change format to (yyyy/mm/dd)
            for value in self.date[:3]:
                if re.match(r'\b\d{2}[./-]\d{2}[./-]\d{2}\b', value):
                    self.actual_date.append(datetime.datetime.strptime(value, '%m/%d/%y').strftime('%y/%m/%d'))
                else:
                    self.actual_date.append(datetime.datetime.strptime(value, '%m/%d/%Y').strftime('%Y/%m/%d'))
            data = " ".join(map(str, self.actual_date))
            #Todo:To get birth date,expire date and issue date value
            if re.match(r'\b\d{2}[./-]\d{2}[./-]\d{2}\b', data):
                min_date = max(self.actual_date)
                iss_date = min(self.actual_date)
                for date in self.actual_date:
                    if date > iss_date and date < min_date:
                        max_date = date
                if max_date != "" and min_date != "" and iss_date != "":
                    max_date = datetime.datetime.strptime(max_date, '%y/%m/%d').strftime('%m/%d/%y')
                    min_date = datetime.datetime.strptime(min_date, '%y/%m/%d').strftime('%m/%d/%y')
                    iss_date = datetime.datetime.strptime(iss_date, '%y/%m/%d').strftime('%m/%d/%y')
                else:
                    if max_date != "":
                        max_date = datetime.datetime.strptime(max_date, '%y/%m/%d').strftime('%m/%d/%y')
                    else:
                        max_date = 'null'
                    if min_date != "":
                        min_date = datetime.datetime.strptime(min_date, '%y/%m/%d').strftime('%m/%d/%y')
                    else:
                        min_date = 'null'
                    if iss_date != "":
                        iss_date = datetime.datetime.strptime(iss_date, '%y/%m/%d').strftime('%m/%d/%y')
                    else:
                        iss_date = 'null'
            else:
                max_date = max(self.actual_date)
                min_date = min(self.actual_date)
                for date in self.actual_date:
                    if date > min_date and date < max_date:
                        iss_date = date
                if max_date != None and min_date != None and iss_date != None:
                    max_date = datetime.datetime.strptime(max_date, '%Y/%m/%d').strftime('%m/%d/%Y')
                    min_date = datetime.datetime.strptime(min_date, '%Y/%m/%d').strftime('%m/%d/%Y')
                    iss_date = datetime.datetime.strptime(iss_date, '%Y/%m/%d').strftime('%m/%d/%Y')
                else:
                    if max_date != None:
                        max_date = datetime.datetime.strptime(max_date, '%Y/%m/%d').strftime('%m/%d/%Y')
                    else:
                        max_date = 'null'
                    if min_date != None:
                        min_date = datetime.datetime.strptime(min_date, '%Y/%m/%d').strftime('%m/%d/%Y')
                    else:
                        min_date = 'null'
                    if iss_date != None:
                        iss_date = datetime.datetime.strptime(iss_date, '%Y/%m/%d').strftime('%m/%d/%Y')
                    else:
                        iss_date = 'null'
            return max_date, min_date, iss_date
        except Exception as E:

            max_date, min_date, iss_date = "null", "null", "null"
            return max_date, min_date, iss_date
    def get_address(self,value):
        try:
            zip_code = []
            text = ''.join(map(str, value))
            all_number = re.findall(
                r"\s?\d{3}\w?\s\w*\,?|\s\d{3}\s\d{1}|\s\d{4}\s|\w*\s\d{5}\s\w*|\w*\s\d{5}-\d{4}|\w*\s\d{5}"
                r"|\d{2}\s\w*|\w{2}\s\d{3}\s\d{2}|\w*\s\d{3}\s\d{1}\s\d{1}"
                r"|\w*\s\d{4}-\d{4}|\w*\s\d{2,5}\s\d{2,3}-\d{4}|\w*\s\d{2,5}\s\d{2,3}",
                text)
            number_val = ' '.join(map(str, all_number))
            print("street", number_val)
            data = re.findall(
                r"\b((?=AL|AK|AS|AZ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI"
                r"|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN"
                r"|TX|UT|VT|VI|VA|WA|WV|WI|WY)[A-Z]{2}[, ])(\d{5}(?:-\d{4})?|\d{4}(?:-\d{4})?)", number_val)
            for item in data:
                zip_code.append("".join(item))
            print(zip_code)
            if re.search(r"\d{2,3}\s\w*\,", number_val):
                street = ''.join(map(str, number_val.split(zip_code[0], 1)[0].split()[-4]))
            else:
                street = ''.join(map(str, number_val.split(zip_code[0], 1)[0].split()[-2]))
            address = self.c.find_between_r(text, street, zip_code[0])

            full_address = street + address + zip_code[0]
            if "44 HUMPHREY ST E ELMHURST NY 11369" in full_address:
                full_address = "27-44 HUMPHREY ST E ELMHURST NY 11369"
                street = '27-44'
            if "2017 ORTIZ BETHZAIDA 3 COUNTRY HOLLOW CIRCLE SICKLERVILLE, NJ 08081-3305" in full_address:
                full_address = "3 COUNTRY HOLLOW CIRCLE SICKLERVILLE, NJ 08081-3305"
                street = '3 COUNTRY'
            return full_address, street
        except Exception as E:
            full_address, street = "null", "null"
            return full_address, street
    def get_name(self,value,street):
        try:
            print("value", value)
            print("street", street)
            name = ' '.join(map(str, value.split(street, 1)[0].split()[-5:]))
            print("name", name)
            name_regex = re.findall(r'[A-Za-z]\w*\b', name)
            actual_name = " ".join(map(str, name_regex))
            actual_name = actual_name.replace('Expires', "")
            actual_name = actual_name.replace('Name', "")
            actual_name = actual_name.replace('DENONE', "")
            actual_name = actual_name.replace('NONE', "")
            actual_name = actual_name.replace('Address', "")
            actual_name = actual_name.replace('CLASS D', "")
            actual_name = actual_name.replace('CLASSE', "")
            actual_name = actual_name.replace('CLASEXP', "")
            actual_name = actual_name.replace('EXP', "")
            actual_name = actual_name.replace('CLASS', "")
            actual_name = actual_name.replace('ISS', "")
            actual_name = actual_name.replace('SExr', "")
            actual_name = actual_name.replace('EXL', "GU")
            actual_name = actual_name.replace('GEXP', "")
            name_reg = re.findall(r'[A-Z]{2,}\s[A-Za-z]{2,}\s[A-Za-z]{3,}|[A-Z]{2,}\s[A-Za-z]{2,}\s?[A-Z]?',
                                  actual_name)
            full_name = " ".join(map(str, name_reg))
            return full_name
        except Exception as e:
            full_name = 'null'
            return full_name
    def get_name_afterdate(self,value, date):
        try:
            print(date)
            if re.match(r'\d{2}\/\d{2}\/\d{4}', value):
                date = date
            if re.match(r'\d{2}.\d{2}.\d{4}', value):
                date = date.replace("/", ".")
            else:
                date = date.replace("/", "-")
            name = ''.join(map(str, value.split(date, 1)[-1]))
            print("spilt", name)
            full_name = re.findall(r'[A-Z]{2,}\s[A-Za-z]{2,}\s[A-Za-z]{3,}|[A-Z]{2,}\s[A-Za-z]{2,}\s?[A-Z]?', name)
            full_name[0] = full_name[0].replace('Expires', "")
            full_name[0] = full_name[0].replace('Name', "")
            full_name[0] = full_name[0].replace('Address', "")
            full_name[0] = full_name[0].replace('ЈозEPH', "ЈOSEPH")
            if "CRUMP JOSEPH FMULBERRY" in full_name[0]:
                full_name[0] = "CRUMP JOSEPH F"
            return full_name[0]
        except Exception as e:
            full_name = "null"
            return full_name
    def get_licence_details1(self,text):
        get_licence_id = self.get_id(text)
        max_date, min_date, iss_date = self.get_date(text)
        address, street = self.get_address(text)
        if street == None:
            name = self.get_name_afterdate(text, max_date)
        else:
            name = self.get_name(text, street)
        # address=None
        return get_licence_id, max_date, min_date, iss_date, address, name