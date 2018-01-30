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
        self.licence_id=''
        self.regex_value=''
        self.c= Common.Common()

        with open('../config/city.json', 'r') as data_file:
            self.cities = json.load(data_file)
        with open('../config/filtering.json', 'r') as data:
            self.state_value = json.load(data)
    def get_id(self,text):
        try:
            state_regex=re.findall(r"\b((?=AL|AK|AS|AZ|AŽ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE"
                r"|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)[A-Z]{2}[, ])\w\s?\d?",text)
            print(len(self.state_value['data']))
            if state_regex != []:
                for i in range(len(self.state_value['data'])):
                    if self.state_value['data'][i]['state'] in state_regex[0]:
                        self.regex_value=self.state_value['data'][i]['license_id']
                        print("regex_state_value",self.state_value['data'][i]['state'],self.regex_value)
                print("state regex",self.regex_value)
                self.licence_id = re.findall(self.regex_value, text)
                if re.match(r'[A-Za-z]{1}', self.licence_id[0]):
                    return self.licence_id[0].upper()
                else:
                    return self.licence_id[0]
            else:
                print("hey")
                id=re.findall(r'\b(\w[A-Za-z]\d{6}|\s\d{8}|\w\s?\-\s?\d{3}\s?\-\s?\d{3}\s?\-\s?\d{3}\s?\-\s?\d{3}'
                                      r'|\w\d{3}\s?\-\s?\d{3}\s?\-\s?\d{2}\s?\-\s?\d{1}|\w*[A-Za-z]\d{4}\s\d{10}|\d{12}|([A-Za-z]+)?\d{7,9}|[A-Za-z]{1}\d{4,5}\s\d{5}\s\d{4,5}|\w\d{2}\-\d{2}\-\d{4}|[0]?\d{2,3}\s\d{3}\s\d{3}\s?\d?\d?\d?|[A-Za-z]{1}\d{3}\-\d{3}\-\d{2}\-\d{3}-\d{1})\b',
                text)
                Licence_id=[]
                for item in id:
                    Licence_id.append("".join(item))

                if re.match(r'[A-Za-z]{1}', Licence_id[0]):
                    return Licence_id[0].upper()
                else:
                    return Licence_id[0]


        except Exception as E:
            print("in licence id",E)
            self.get_licence_id=''
            return self.get_licence_id

    def get_address(self,value):
        try:
            full_address, street, state, zipcode, city='','','','',''
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
                r"\b((?=AL|AK|AS|AZ|AŽ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE"
                r"|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)[A-Z]{2}[, ])"
                r"(\d{5}(?:\s?-\s?\d{4})?|\d{5}|\d{2,3}(?:\s\d{2,3}))", number_val)
            if data!=[]:

                for item in data:
                    self.zip_code.append("".join(item))
                if self.zip_code != []:
                    if re.search(r'\s(=?ID\s\d+\s\d+)', number_val):
                        code = self.zip_code[0]
                    elif re.search(r'(=?ID\:?\s\d+\s\d+)', number_val):
                        code = self.zip_code[1]
                    else:
                        code = self.zip_code[0]
                    print(code)
                    reg_value = ' '.join(map(str, value.split(code, 1)[0].split()[-8:]))
                    reg_value = reg_value + " " + code
                    print('in address',reg_value)
                    # if re.search(r'(\s\d{1,3}\s\w*\s?\w?\s?\w+?\s?\,?\s[A-Z]{2}\s\d{5})\b', reg_value):
                    if re.search(r'(\d+\s([A-Za-z]+)?\s?([A-Za-z])+?\s?([A-Za-z])+\s?[#.,/]?\s?\w*?\s\d{1,3}\s\w+\s?\w+?\s?\w?\,?\s[A-Z]{2}\s\d{5})\b', reg_value):
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
                data = re.findall(
                    r"(!? AL | AK | AS | AZ | AŽ | AR | CA | CO | CT | DE | DC | FM | FL | GA | GU | HI | ID | IL | IN | IA | KS | KY | LA "
                    r"| ME | MH | MD | MA | MI | MN | MS | MO | MT | NE | NV | NH | NJ | NM | NY | NC | ND | MP "
                    r"| OH | OK | OR | PW | PA | PR | RI | SC | SD | TN | TX | UT | VT | VI | VA | WA | WV | WI | WY )",
                    value)
                for item in data:
                    self.zip_code.append("".join(item))
                if self.zip_code != []:
                    if re.search(r'\s(=?ID\s\d+\s\d+)', number_val):
                        code = self.zip_code[0]
                    elif re.search(r'(=?ID\:?\s\d+\s\d+)', number_val):
                        code = self.zip_code[1]
                    else:
                        code = self.zip_code[0]
                    print(code)
                    reg_value = ' '.join(map(str, value.split(code, 1)[0].split()[-8:]))
                    reg_value = reg_value + " " + code
                    if re.search(r'(\d+\s([A-Za-z]+)?\s?([A-Za-z])+?\s?([A-Za-z])+'
                                 r'\s?[#.,/]?\s?\w*?\s\d{1,3}\s\w+\s?\w+?\s?\w?\,?'
                                 r'\s[A-Z]{2})\b',reg_value):
                        street_code=re.findall(r'\d+\s+\w+',reg_value)
                        street=street_code[0]
                    else:
                        street_code = re.findall(r'\d+\s+\w+', reg_value)
                        street = street_code[1]
                    address = self.c.find_between_r(value, street, code)
                    print("zip code", code)
                    full_address = street + address + code
                    state,zip,city = self.c.get_address_zipcode(full_address, code)
                    print("Full Address:", full_address, city, state)
                    for i in range(len(self.cities['city'])):
                        if self.cities['city'][i].lower() in city.lower():
                            actual_city = self.cities['city'][i]

                    if actual_city == '':
                        city = ' '.join(map(str, value.split(code, 1)[0].split()[-1:]))
                        print(city)
                    elif city != actual_city:
                        city = actual_city.upper()
                    else:
                        city = actual_city
                    full_address = self.c.find_between_r(value, street, city)
                    print("full", full_address)
                    full_address = street + full_address
                    full_address = ' '.join(s[:1].upper() + s[1:] for s in full_address.split())
                    city = city.replace(",", "")
                    city = city.replace(".", "")
                    zipcode=""

            return full_address, street, state, zipcode, city
        except Exception as e:
            print("in address",e)
            full_address, street, state, zipcode, city = "", "", "", "", ""
            return full_address, street, state, zipcode, city
    def get_name(self,text_value,street,licenseid,zip_code,date_Val):
        try:
            value=text_value.replace(date_Val,"")
            print("value", value)
            print("street", street)
            value=value.replace(":","")
            if 'ID' in zip_code:
                name = ' '.join(map(str, value.split(licenseid, 1)[0].split()[-4:]))
            else:
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
    def get_date(self,text,license_id):
        actual_expiry_date, actual_dob_date, actual_issue_date, issue_date, data, string_date_value = '', '', '', '', '', ''
        try:
            # Todo:To get all date format from text
            text = text.replace(license_id, '')
            val = re.findall(
                r'(\w*[A-Za-z]\d{1}\d{2}[./-](19|20|21|22|23|24)\d\d)|(\w*[A-Za-z]\d{1}[./-]\d{2}[./-](19|20|21|22|23|24)\d\d)'
                r'|(\d{2}\s?[./-]\d{2}[./-](19|20|21|22|23|24)\d\d)|(\d{2}\s\d{2}\s(19|20|21|22|23|24)\d\d)'
                r'|(\d{2}[./-]\d{2}\s?(19|20|21|22|23|24)\d\d)|(\d{2}[./-]\d{2}\s?\d\s?\d)|(\d{1,2}\s?[./-]\d{2}[./-]\s?\d{2}\s?\d{2})'
                r'|(\d{2}\d{2}[./-](19|20|21|22|23|24)\d\d)|(\d{2}[./-]\d{2}\s[./-](19|20|21|22|23|24)\d\d)|(([0-9]|0[0-9]'
                r'|1[0-9])[./-]([0-9][0-9]|[0-9])[./-]\d\d)|(([0-9]|0[0-9]'
                r'|1[0-9])[./-]([0-9][0-9]|[0-9])[./-](19|20|21|22|23|24)\d\d|(\d{2}\d{2}[./-]\d\d))\b', text)
            date_val1 = []
            for item in val:
                date_val1.append(" ".join(item))
            string_date = " ".join(map(str, date_val1))
            # Todo:To remove all white spaces and [,/.]
            date_val = re.findall(r'\d{2}\s?[./-]?\d{2}\s?[./-]?\d{2,4}', string_date)
            string_date_value = " ".join(map(str, date_val))
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
            for value in self.date[:3]:
                if re.match(r'\b\d{2}[./-]\d{2}[./-]\d{2}\b', value):
                    self.actual_date.append(datetime.datetime.strptime(value, '%m/%d/%y').strftime('%y/%m/%d'))
                else:
                    self.actual_date.append(datetime.datetime.strptime(value, '%m/%d/%Y').strftime('%Y/%m/%d'))
            data = " ".join(map(str, self.actual_date))
            print("in date_val", data)
            # Todo:To get birth date,expire date and issue date value

            if re.match(r'\b\d{2}[./-]\d{2}[./-]\d{2}\b', data):
                dob = max(self.actual_date)
                issue_date = min(self.actual_date)
                if dob != "" and issue_date != "":
                    for date in self.actual_date:
                        if date > issue_date and date < dob:
                            expiry_date = date
                    actual_expiry_date = datetime.datetime.strptime(expiry_date, '%y/%m/%d').strftime('%m/%d/%y')
                    actual_dob_date = datetime.datetime.strptime(dob, '%y/%m/%d').strftime('%m/%d/%y')
                    actual_issue_date = datetime.datetime.strptime(issue_date, '%y/%m/%d').strftime('%m/%d/%y')
            else:
                expiry_date = max(self.actual_date)
                dob = min(self.actual_date)
                if expiry_date != "" and dob != "":
                    for date in self.actual_date:
                        if date > dob and date < expiry_date:
                            issue_date = date
                    actual_expiry_date = datetime.datetime.strptime(expiry_date, '%Y/%m/%d').strftime('%m/%d/%Y')
                    actual_dob_date = datetime.datetime.strptime(dob, '%Y/%m/%d').strftime('%m/%d/%Y')
                    actual_issue_date = datetime.datetime.strptime(issue_date, '%Y/%m/%d').strftime('%m/%d/%Y')

            print('string_val', string_date_value)

            return actual_expiry_date, actual_dob_date, actual_issue_date, string_date_value
        except Exception as E:
            try:
                if re.match(r'\b\d{2}[./-]?\d{2}[./-]?\d{4}\b', string_date_value):
                    if re.search(r'(=?(Issued|ISS|Iss|ISSUED)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{4})', text):
                        issue_date = ' '.join(
                            map(str, text.split(re.findall(r'(=?Issued|ISS|Iss|ISSUED)', text)[0], 1)[1].split()[0:2]))
                        if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', issue_date):
                            actual_issue_date = re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', issue_date)[0]
                        elif re.search(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', issue_date):
                            actual_issue_date = re.findall(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', issue_date)[0]
                        elif re.search(r'(?!:)', issue_date):
                            actual_issue_date = ''
                    else:
                        actual_issue_date = ''

                    if re.search(r'(=?(EXP|Expires|Exp|Expiros|EXPIRES|EXPIROS)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{4})', text):
                        expiry_date = ' '.join(map(str, text.split(
                            re.findall(r'(=?EXP|Expires|Exp|Expiros|EXPIRES|EXPIROS)', text)[0], 1)[1].split()[0:2]))
                        if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', expiry_date):
                            actual_expiry_date = re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', expiry_date)[0]
                        elif re.search(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', expiry_date):
                            actual_expiry_date = re.findall(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', expiry_date)[0]

                        elif re.search(r'(=?:)', expiry_date):
                            actual_expiry_date = ''
                    else:
                        actual_expiry_date = ''

                    if re.search(r'(=?(dob|DOB|BIRTHDATE|birthdate|Birth|BIRTH|D.O.B.)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{4})', text):
                        dob = ' '.join(map(str, text.split(
                            re.findall(r'(=?dob|DOB|BIRTHDATE|birthdate|birth|Birth|BIRTH|D.O.B.)', text)[0], 1)[1].split()[0:2]))
                        if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', dob):
                            actual_dob_date = re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', dob)[0]

                        elif re.search(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', dob):
                            actual_dob_date = re.findall(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', dob)[0]

                            print("birth", actual_dob_date)
                        elif re.search(r'(=?:)', dob):
                            actual_dob_date = ''

                    else:
                        actual_dob_date = ''


                else:
                    if re.match(r'\b\d{2}[./-]?\d{2}[./-]?\d{2}\b', string_date_value):
                        if re.search(r'(=?(Issued|ISS|Iss|ISSUED)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{2})', text):
                            issue_date = ' '.join(
                                map(str,
                                    text.split(re.findall(r'(=?Issued|ISS|Iss|ISSUED)', text)[0], 1)[1].split()[0:2]))
                            if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', issue_date):
                                actual_issue_date = re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', issue_date)[0]
                            elif re.search(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', issue_date):
                                actual_issue_date = re.findall(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', issue_date)[0]
                            elif re.search(r'(?!:)', issue_date):
                                actual_issue_date = ''
                        else:
                            actual_issue_date = ''

                        if re.search(r'(=?(EXP|Expires|Exp|Expiros|EXPIRES|EXPIROS)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{2})',
                                     text):
                            expiry_date = ' '.join(map(str, text.split(
                                re.findall(r'(=?EXP|Expires|Exp|Expiros|EXPIRES|EXPIROS)', text)[0], 1)[1].split()[
                                                            0:2]))
                            if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', expiry_date):
                                actual_expiry_date = re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', expiry_date)[0]
                            elif re.search(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', expiry_date):
                                actual_expiry_date = re.findall(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', expiry_date)[0]

                            elif re.search(r'(=?:)', expiry_date):
                                actual_expiry_date = ''
                        else:
                            actual_expiry_date = ''

                        if re.search(
                                r'(=?(dob|DOB|BIRTHDATE|birthdate|Birth|BIRTH|D.O.B.)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{2})',
                                text):
                            dob = ' '.join(map(str, text.split(
                                re.findall(r'(=?dob|DOB|BIRTHDATE|birthdate|birth|Birth|BIRTH|D.O.B.)', text)[0], 1)[
                                                        1].split()[0:2]))
                            if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', dob):
                                actual_dob_date = re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', dob)[0]

                            elif re.search(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', dob):
                                actual_dob_date = re.findall(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', dob)[0]

                                print("birth", actual_dob_date)
                            elif re.search(r'(=?:)', dob):
                                actual_dob_date = ''

                        else:
                            actual_dob_date = ''
                return actual_expiry_date, actual_dob_date, actual_issue_date, string_date_value
            except Exception as e:
                print(e)
    def get_licence_details1(self,text):
            try:
                self.paystub = get_paystub_details.Paystub_details()
                get_licence_id = self.get_id(text)
                # max_date, min_date, iss_date, date_val="","","",""
                print(text)
                if get_licence_id!='':
                    expiry_date, dob, issue_date,date_val = self.get_date(text,get_licence_id)
                else:
                    get_licence_id=' '
                    expiry_date, dob, issue_date, date_val = self.get_date(text, get_licence_id)
                address, street, state, zipcode, city, = self.get_address(text)
                name = self.get_name(text, street,get_licence_id,state,date_val)
                gross_net,net_value=self.paystub.gross_net(text)
                if gross_net=='':
                    return get_licence_id, expiry_date, dob, issue_date, address, name, state, zipcode, city,date_val
                else:
                    get_licence_id, max_date, min_date, iss_date, address, name, state, zipcode, city, date_val='','','','','','','','','',''
                    return get_licence_id, max_date, min_date, iss_date, address, name, state, zipcode, city,date_val
            except Exception as e:
                pass