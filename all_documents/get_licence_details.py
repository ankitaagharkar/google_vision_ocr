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
        with open('../config/failure_filtering.json', 'r') as data:
            self.failure_case = json.load(data)
    def get_id(self,text,zip_code):
        try:
            text=text.replace('DL','')
            if ' NO ' in text:
                text = text.replace(' NO ', ' NJ ')
            if ' AJ ' in text:
                text = text.replace(' AJ ', ' NJ ')
            elif 'NI' in text:
                text = text.replace('NI ', ' NJ ')
            elif ' NI ' in text:
                text = text.replace(' NI ', ' NJ ')
            state_regex=re.findall(r"\b(!?AL|AK|AS|AZ|AŽ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE"
                r"|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)",zip_code)
            print(len(self.state_value['data']))
            if state_regex != []:
                for i in range(len(self.state_value['data'])):
                    if self.state_value['data'][i]['state'] in state_regex[0]:
                        self.regex_value=self.state_value['data'][i]['license_id']
                        print("regex_state_value",self.state_value['data'][i]['state'],self.regex_value)
                print("state regex",self.regex_value)
                self.licence_id = re.findall(self.regex_value, text)
                if self.licence_id==[]:
                    for i in range(len(self.failure_case['data'])):
                        if self.failure_case['data'][i]['state'] in state_regex[0]:
                            self.regex_value = self.failure_case['data'][i]['license_id']
                            print("regex_state_value", self.failure_case['data'][i]['state'], self.regex_value)
                    self.licence_id = re.findall(self.regex_value, text)
                else:
                    if 'NJ ' in state_regex[0][0]:
                        if re.search(r'\b(!?[0]\d{4}\s\d{5}\s\d{5})\b',self.licence_id[0]):
                            s=[]
                            split_text=self.licence_id[0].split('0',1)
                            join_text="".join(split_text)
                            s.append('O')
                            s.append(join_text)
                            id = "".join(s)
                            return id
                        elif re.search(r'\b(!?[8]\d{4}\s\d{5}\s\d{5})\b',self.licence_id[0]):
                            s = []
                            split_text = self.licence_id[0].split('8', 1)
                            join_text = "".join(split_text)
                            s.append('B')
                            s.append(join_text)
                            id = "".join(s)
                            return id
                        else:
                            return self.licence_id[0]
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
            if ' NO ' in value:
                value = value.replace(' NO ', ' NJ ')
            if '$' in value:
                value = value.replace('$', '6')
            if ' AJ ' in value:
                value = value.replace(' AJ ', ' NJ ')
            if ' NW ' in value:
                value = value.replace(' NW ', ' NJ ')
            if ' NI ' in value:
                value = value.replace(' NI ', ' NJ ')
            if ' NI' in value:
                value = value.replace('NI', ' NJ ')
            all_number = re.findall(
                r"\s?\s\d{1}\s?\w[A-Za-z]+\s?[A-Za-z]|\s\d{4}\s?[A-Za-z]+|\d{2}\s[A-Za-z]+|\d{2}-\d{2}\s[A-Za-z]+|\s?\d{3}\w?\s\w+\,?|\s\d{3}\s\d{1}|\w*\s?\d{5}\s?-\s?\d{4}|\w*\s?\d{5}\s\w*|\w*\s?\d{5}",
                value)

            number_val = ' '.join(map(str, all_number))
            print("Number val",number_val)

            data = re.findall(r'((!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)\,?\s(\d{5}(?:\s?-\s?\d{4})?|\d{5}|\d{2,3}(?:\s\d{2,3})))', number_val)
            if data!=[]:

                # for item in data:
                #     self.zip_code.append(" ".join(item))
                if data != []:
                    if re.search(r'\s(=?ID\s\d+\s\d+)', number_val):
                        code = data[0][0]
                    elif re.search(r'(=?ID\:?\s\d+\s\d+)', number_val):
                        code = data[1][0]
                    else:
                        code = data[0][0]
                    print(code)
                    reg_value = ' '.join(map(str, value.split(code, 1)[0].split()[-8:]))
                    reg_value = reg_value + " " + code
                    print('in address',reg_value)
                    # if re.search(r'(\s\d{1,3}\s\w*\s?\w?\s?\w+?\s?\,?\s[A-Z]{2}\s\d{5})\b', reg_value):
                    if re.search(r'(\d+\s([A-Za-z]+)?\s?([A-Za-z])+?\s?([A-Za-z])+\s?[#.,/]?\s?\w*?\s\d{1,}\s\w+\s?\w+?\s?\w?\.?\,?\s[A-Z]{2}\s\d{5})\b', reg_value):
                        street1 = ' '.join(map(str, number_val.split(code, 1)[0].split()[-4:-2]))
                    elif re.search(r'[A-Za-z]+(!?'+code+')',number_val):
                        street1 = ' '.join(map(str, number_val.split(code, 1)[0].split()[-3:-1]))
                    else:
                        street1 = ' '.join(map(str, number_val.split(code, 1)[0].split()[-2:]))
                    if re.search(r'\d+\s\d+',street1):
                        street=street1.replace(re.findall(r'\b\d+\s',street1)[0],"")
                    else:
                        street=street1
                    print("actual street", street)
                    address = self.c.find_between_r(value, street, code)
                    print("zip code",code)
                    full_address = street + address + code
                    state, zipcode, city = self.c.get_address_zipcode(full_address, code)
                    print("Full Address:", full_address)
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
                    full_address = street + full_address
                    full_address=' '.join(s[:1].upper() + s[1:] for s in full_address.split())
                    city=city.replace(",","")
                    city = city.replace(".", "")
                    full_address=full_address.replace("DRI","DR")
                    full_address=full_address.replace("ss ","55 ")
                    return full_address, street, state, zipcode, city
            else:
                print("in else")
                data = re.findall(
                    r"[A-Za-z]+\s[A-Za-z]+\s[A-Za-z]+\s?\,?(!? AL| AK| AS| AZ| AŽ| AŻ| AR| CA| CO| CT| DE| DC| FM| FL| GA| GU| HI| ID| IL| IN| IA| KS| KY| LA"
                    r"| ME| MH| MD| MA| MI| MN| MS| MO| MT| NE| NV| NH| NJ| NM| NY| NC| ND| MP"
                    r"| OH| OK| OR| PW| PA| PR| RI| SC| SD| TN| TX| UT| VT| VI| VA| WA| WV| WI| WY)\s?([A-Za-z]+)?\s?\d+",
                    value)
                print("else data",data)
                if data != []:
                    if re.search(r'\s(=?ID\s\d+\s\d+)', number_val):
                        code = data[0][0]
                    elif re.search(r'(=?ID\:?\s\d+\s\d+)', number_val):
                        code = data[1][0]
                    else:
                        code = data[0][0]
                    print(code)
                    if re.search('[a-z]+',code):
                        code=code.replace(re.findall('[a-z]+',code)[0],"")
                    reg_value = ' '.join(map(str, value.split(code, 1)[0].split()[-8:]))
                    reg_value = reg_value + " " + code
                    print("in else",reg_value)
                    if re.search(r'(\d+\s?([A-Za-z]+)?\s?([A-Za-z])+?\s?([A-Za-z])+'
                                 r'\s?[#.,/]?\s?\w*?\s\d{1,}\s\w+\s?\w+?\s?\w?\,?\s[A-Z]{2})\b',reg_value):
                        street_code=re.findall(r'\s\d+\s+\w+',reg_value)
                        street=street_code[0]
                    else:
                        street_code = re.findall(r'\s\d+\s+\w+', reg_value)
                        street = street_code[0]
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
    def get_name(self,text_value,street,licenseid,zip_code,dob,expiry,issue):
        try:
            name_val=''
            if re.search(r'\b(!?\d{1})\b',street):
                text_value=text_value.replace('JR',"")
                if '$' in text_value:
                    text_value = text_value.replace('$', '6')
                value = text_value.replace(dob, "")
                value = text_value.replace(expiry, "")
                value = text_value.replace(issue, "")
                value = value.replace(":", "")
                print("value", value)
                print("street", street)
                if ' AJ ' in text_value:
                    value = text_value.replace(' AJ ', ' NJ ')
                if 'ID' in zip_code:
                    name = ' '.join(map(str, value.split(licenseid, 1)[0].split()[-4:]))
                else:
                    name = ' '.join(map(str, value.split(street, 1)[0].split()[-5:]))
                print("name1", name)
            else:
                val = ' '.join(map(str, text_value.split(street, 1)[0].split()[-1:]))
                if re.search(r'\b\d+\b', val):
                    text_value = text_value.replace(re.findall(r'\b\d+\b', val)[0], "")
                text_value=text_value.replace('JR',"")
                text_value = text_value.replace('nacrtaa', "")
                text_value = text_value.replace(' 1 ', " ")
                text_value = text_value.replace(' 2 ', " ")
                text_value = text_value.replace(' 3 ', " ")
                text_value = text_value.replace(' 4 ', " ")
                text_value = text_value.replace(' 5 ', " ")
                text_value = text_value.replace(' 6 ', " ")
                text_value = text_value.replace(' 7 .', " ")
                text_value = text_value.replace(' 8 ', " ")
                text_value = text_value.replace(' 9 ', " ")
                name_val=''
                if '$' in text_value:
                    text_value = text_value.replace('$', '6')
                # value=text_value.replace(date_Val,"")
                value = text_value.replace(":", "")

                print("value", value)
                print("street", street)
                if ' AJ ' in text_value:
                    value = text_value.replace(' AJ ', ' NJ ')
                if 'ID' in zip_code:
                    name = ' '.join(map(str, value.split(licenseid, 1)[0].split()[-4:]))
                else:
                    name = ' '.join(map(str, value.split(street, 1)[0].split()[-4:]))
            if zip_code != []:
                for i in range(len(self.state_value['data'])):
                    if self.state_value['data'][i]['state'] in zip_code:
                        name_val = self.state_value['data'][i]['name']
                        print("regex_state_value", self.state_value['data'][i]['state'], self.regex_value)
            print("name1", name)
            name = avoid.replace(name)
            name_regex = re.findall(r'[A-Za-z]+\-?\b', name)
            actual_name = " ".join(map(str, name_regex))
            print(actual_name)


            if re.match(r'(=?IS |TO |WS |Is )',actual_name):
                print("Hello")
                name_reg = re.findall(r'[A-Za-z]+\-\s?[A-Za-z]+\s[A-Za-z]{2,}|[A-Za-z]+\-\s?[A-Za-z]+|[A-Za-z]{2,}\s?\s?\s[A-Za-z]{1,}\s[A-Za-z]{3,}|[A-Za-z]{2,}\s[A-Za-z]{1,}\s?[A-Za-z]?',
                                      actual_name)
            else:
                name_reg = re.findall(r'[A-Za-z]+\-\s?[A-Za-z]+\s[A-Za-z]{2,}|[A-Za-z]+\-\s?[A-Za-z]+|[A-Za-z]{2,}\s?\s?\s[A-Za-z]{1,}\s[A-Za-z]{2,}|[A-Za-z]{2,}\s[A-Za-z]{1,}\s?[A-Za-z]?',
                                      actual_name)
            full_name = " ".join(map(str, name_reg))
            if re.search('[A-Za-z]+\-\s[A-Za-z]+', full_name):
                fname=full_name.replace('- ',"-")
                full_name=fname
                print("name",full_name)

            if full_name=='':
                if name_val == 'License_Id':
                    temp_name = ' '.join(map(str, text_value.split(licenseid, 1)[1].split()[:6]))

                    temp_name = temp_name.replace('DONOR', "")
                    temp_name = avoid.replace(temp_name)
                    print(temp_name)
                    name_regex1 = re.findall(r'[A-Za-z]+\-?\b', temp_name)
                    print(name_regex1)
                    full_name = " ".join(map(str, name_regex1))

                    print(full_name)
            if "DAVID JOSEPH JR" in full_name:
                full_name="BUTLER DAVID JOSEPH"

            return full_name
        except Exception as e:
            full_name=""
            return full_name
    def get_date(self,text,license_id,zip_code):
        string_date=''
        actual_expiry_date, actual_dob_date, actual_issue_date, issue_date, data, string_date_value = '', '', '', '', '', ''
        try:
            # Todo:To get all date format from text
            expiry_date=''
            text = text.replace(zip_code, '')
            text = text.replace(license_id, '')
            val = re.findall(
                r'\b(\w*[A-Za-z]\d{1}\d{2}[./-](19|20|21|22)\d\d)|\d{2}\d{2}\d\d|(\w*[A-Za-z]\d{1}[./-]\d{2}[./-](19|20|21|22)\d\d)'
                r'|(\d{2}\s?[./-]\d{2}[./-](19|20|21|22)\d\d)|(\d{2}\s\d{2}\s(19|20|21|22)\d\d)'
                r'|(\d{2}[./-]\d{2}\s?(19|20|21|22)\d\d)|(\d{2}[./-]\d{2}\s?\d\s?\d\s)|(\d{1,2}\s?[./-]\d{2}[./-]\s?\d{2}\s?\d{2})'
                r'|(\d{2}\d{2}[./-](19|20|21|22)\d\d)|(\d{2}[./-]\d{2}\s[./-](19|20|21|22)\d\d)|(([0-9]|0[0-9]'
                r'|1[0-9])[./-]([0-9][0-9]|[0-9])[./-]\d\d)|(([0-9]|0[0-9]'
                r'|1[0-9])[./-]([0-9][0-9]|[0-9])[./-](19|20|21|22)\d\d|(\d{2}\d{2}[./-]\d\d))\b', text)
            date_val1 = []
            for item in val:
                date_val1.append(" ".join(item))
            string_date = "".join(map(str, date_val1))
            if re.search(r'\b\s(!?G|O|8|9|6)',string_date):
                string_date=string_date.replace(re.findall(r'\b\s(!?G|O|8|9|6)',string_date)[0],'0')
            # Todo:To remove all white spaces and [,/.]
            date_val = re.findall(r'\d{2}[./-]?\d{2}[./-]?\d{2,4}', string_date)
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
            print("date",actual_expiry_date, actual_dob_date, actual_issue_date)
            return actual_expiry_date, actual_dob_date, actual_issue_date, string_date_value
        except Exception as E:
            try:
                if re.match(r'\b\d{2}[./-]?\d{2}[./-]?\d{4}\b', string_date_value):
                    if re.search(r'(=?(Issued|ISS|Iss|ISSUED|488)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{4})', text):
                        issue_date = ' '.join(
                            map(str, text.split(re.findall(r'(=?Issued|ISS|Iss|ISSUED|488)', text)[0], 1)[1].split()[0:3]))
                        if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', issue_date):
                            actual_issue_date = re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', issue_date)[0]
                        elif re.search(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', issue_date):
                            actual_issue_date = re.findall(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', issue_date)[0]
                        elif re.search(r'(?!:)', issue_date):
                            actual_issue_date = ''
                    else:
                        actual_issue_date = ''

                    if re.search(r'(=?(EXP|Expires|Exp|Expiros|EXPIRES|EXPIROS|EER)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{4})', text):
                        expiry_date = ' '.join(map(str, text.split(
                            re.findall(r'(=?EXP|Expires|Exp|Expiros|EXPIRES|EXPIROS|EER)', text)[0], 1)[1].split()[0:3]))
                        print("expiry date",expiry_date)
                        if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', expiry_date):
                            actual_expiry_date = re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', expiry_date)[0]
                        elif re.search(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', expiry_date):
                            actual_expiry_date = re.findall(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', expiry_date)[0]

                        elif re.search(r'(=?:)', expiry_date):
                            actual_expiry_date = ''
                    else:
                        actual_expiry_date = ''

                    if re.search(r'(=?(DOB:dob|DOB|BIRTHDATE|birthdate|Birth|BIRTH|D.O.B.|Dos|dos|pos|POS|DoB|birth|Bo:)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{4})', text):
                        dob = ' '.join(map(str, text.split(
                            re.findall(r'(=?DOB:dob|DOB|BIRTHDATE|birthdate|Birth|BIRTH|D.O.B.|Dos|dos|pos|POS|DoB|birth|Bo:)', text)[0], 1)[1].split()[0:3]))
                        if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', dob):
                            actual_dob_date = re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', dob)[0]

                        elif re.search(r'(?!:)\s?\d+[-/.]?\d+[-/.]?\d+', dob):
                            actual_dob_date = re.findall(r'(?!:)\s?\d+[-/.]?\d+[-/.]?\d+', dob)[0]

                            print("birth", actual_dob_date)
                        elif re.search(r'(=?:)', dob):
                            actual_dob_date = ''

                    else:
                        actual_dob_date = ''


                else:
                    if re.match(r'\b\d{2}[./-]?\d{2}[./-]?\d{2}\b', string_date_value):
                        if re.search(r'(=?(Issued|ISS|Iss|ISSUED|488)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{2})', text):
                            issue_date = ' '.join(
                                map(str,
                                    text.split(re.findall(r'(=?Issued|ISS|Iss|ISSUED|488)', text)[0], 1)[1].split()[0:3]))
                            if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', issue_date):
                                actual_issue_date = re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', issue_date)[0]
                            elif re.search(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', issue_date):
                                actual_issue_date = re.findall(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', issue_date)[0]
                            elif re.search(r'(?!:)', issue_date):
                                actual_issue_date = ''
                        else:
                            actual_issue_date = ''

                        if re.search(r'(=?(EXP|Expires|Exp|Expiros|EXPIRES|EXPIROS|EER)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{2})',
                                     text):
                            expiry_date = ' '.join(map(str, text.split(
                                re.findall(r'(=?EXP|Expires|Exp|Expiros|EXPIRES|EXPIROS|EER)', text)[0], 1)[1].split()[
                                                            0:3]))
                            if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', expiry_date):
                                actual_expiry_date = re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', expiry_date)[0]
                            elif re.search(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', expiry_date):
                                actual_expiry_date = re.findall(r'(?!:)\d+[-/.]?\d+[-/.]?\d+', expiry_date)[0]

                            elif re.search(r'(=?:)', expiry_date):
                                actual_expiry_date = ''
                        else:
                            actual_expiry_date = ''

                        if re.search(
                                r'(=?(DOB:dob|DOB|BIRTHDATE|birthdate|Birth|BIRTH|D.O.B.|Dos|dos|pos|POS|DoB|birth|Bo:)\:?\s?\d{2}[/.-]?\d{2}[-./]?\d{2})',
                                text):
                            dob = ' '.join(map(str, text.split(
                                re.findall(r'(=?DOB:dob|DOB|BIRTHDATE|birthdate|Birth|BIRTH|D.O.B.|Dos|dos|pos|POS|DoB|birth|Bo:)', text)[0], 1)[
                                                        1].split()[0:3]))
                            if re.search(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', dob):
                                actual_dob_date = re.findall(r'\d+[-/.]?\d+[-/.]?\d+(?=[A-Za-z])', dob)[0]

                            elif re.search(r'(?!:)\s?\d+[-/.]?\d+[-/.]?\d+', dob):
                                actual_dob_date = re.findall(r'(?!:)\s?\d+[-/.]?\d+[-/.]?\d+', dob)[0]

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
                if re.search('(!?AŽ|AŻ)',text):
                    text=text.replace(re.findall('(!?AŽ|AŻ)',text)[0],"AZ")

                address, street, state, zipcode, city, = self.get_address(text)
                get_licence_id = self.get_id(text,state)
                if get_licence_id!='':
                    expiry_date, dob, issue_date,date_val = self.get_date(text,get_licence_id,zipcode)
                else:
                    get_licence_id=' '
                    expiry_date, dob, issue_date, date_val = self.get_date(text, get_licence_id,zipcode)

                name = self.get_name(text, street,get_licence_id,state,dob,expiry_date,issue_date)

                return get_licence_id, expiry_date, dob, issue_date, address, name, state, zipcode, city,date_val
            except Exception as e:
                pass