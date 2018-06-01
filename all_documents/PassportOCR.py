import datetime
import difflib
import re
from dateutil.parser import parse
import json


class Passport_Details:
    def __init__(self):
        self.name=[]
        with open('../config/name', 'r') as data_file:
            self.name_list = json.load(data_file)
        with open('../config/surname', 'r') as data_file:
            self.surname_list = json.load(data_file)

    def get_passport_no(self,text):

        try:
            text=text.replace(re.findall(r'\s(!?USA|AUS|IND|NZL|BGR|IRE|ESP|CAN|PAK|PLUSA)',text)[0],'')
            passport_regex=re.findall(r'(!?\d{9}|[A-Z]{2,3}\d{5,6}|[A-Z]{1,2}\d{7,8}|[A-Z]{1,2}\d{6,7})',text)
            passport_number=passport_regex[0].rstrip()
            print(passport_number)
            return passport_number

        except Exception as e:
            print(e)
            passport_number=''
            return passport_number

    def get_passport_name(self,text,passport_number,date_regex):

        try:

            if len(re.findall(passport_number,text))>1:
                text_split=text.split(passport_number)
                name=" ".join(map(str,re.findall(r'\s[A-Z]{2,}\b',text_split[1])[:5]))
                name=name.replace('CANADA','').lstrip()
                name=name.replace('AUS','').lstrip()
                for i in range(len(date_regex)):
                    if name.split()[-1] in date_regex[i]:
                        name=name.replace(name.split()[-1],"")
            else:
                name=''
            # if len(name.split()) >= 2:
            #     if x==[]:
            #         if y==[]:
            #             name=''
            #         else:
            #             if len(name.split())>3:
            #                 name=name.replace(name.split()[-1],'').rstrip()
            #                 name=name.replace(name.split()[-2],'').rstrip()
            #             else:
            #                 name = name.replace(name.split()[-1], '').rstrip()

            if name=='':
                print("passport no not found")
                name_regex = " ".join(map(str, re.findall( r'\b[A-Z]{2,}<<?\s?[A-Z]{2,}<?\s?[A-Z]{2,}<?\s?[A-Z]{2,}|[A-Z]{2,}<<?\s?[A-Z]{2,}<?\s?[A-Z]{2,}|[A-Z]{2,}<<?\s?[A-Z]{2,}\b',text))).replace('<', ' ')
                name = name_regex.replace(re.findall(r'(!?USA|AUS|IND|NZL|BGR|IRE|ESP|CAN|PAK|PLUSA)', name_regex)[0], '', 1).replace('  ',' ')
            else:
                name_regex = " ".join(map(str, re.findall(r'\b[A-Z]{2,}<<?\s?[A-Z]{2,}<?\s?[A-Z]{2,}<?\s?[A-Z]{2,}|[A-Z]{2,}<<?\s?[A-Z]{2,}<?\s?[A-Z]{2,}|[A-Z]{2,}<<?\s?[A-Z]{2,}\b', text))).replace('<',' ')
                if len(re.findall(r'(!?USA|AUS|IND|NZL|BGR|IRE|ESP|CAN|PAK|PLUSA)', name_regex))>0:
                    temp_name = name_regex.replace(re.findall(r'(!?USA|AUS|IND|NZL|BGR|IRE|ESP|CAN|PAK|PLUSA)', name_regex)[0], '', 1).replace('  ', ' ')
                else:
                    temp_name=name_regex
                name=name.replace(re.search('\s\s',name)[0],' ')
                name = name.replace('UNITED', '')
                name = name.replace('STATES', '')
                name = name.replace(' OF', '')
                name_val = name
                if temp_name!='':
                    if temp_name!=name:

                        name=''
                        temp_name_list=temp_name.split()
                        for i in temp_name_list:
                            if i in name_val:
                                name=name+" "+i
                            else:
                                name=name+" "+i
                    else:
                        name=temp_name
                    x = difflib.get_close_matches(name.split()[-1].lower(),[vt.lower() for vt in self.name_list['names']], cutoff=0.90)
                    if not x:
                        name = name.split(name_val.split()[-1])
                        name=name[0]+" "+"".join(name[1].replace('',name_val.split()[-1]))
                        if len(name.split())>2:
                            y = difflib.get_close_matches(name.split()[-2].lower(),[vt.lower() for vt in self.name_list['names']], cutoff=0.90)
                            if not y:
                                name = name.split(name_val.split()[-2])
                                name = name[0]+" "+"".join(name[1].split()[0].replace(name[1].split()[0], name_val.split()[-2]))+" "+name[1].split()[1]

            print(name)
            return name

        except Exception as e:
            print(e)
            name=''
            return name

    def get_all_dates(self,text):

        try:
            issue_date=''
            date_regex,date_val,actual_date=[],[],[]
            val = re.compile('(0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-](0[0-9]|1[0-2])[./-](19|20|21|22)\d\d|(0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-]?\s?(Jan|Feb|Mar|Apr|May|Jun|July|Jul|Aug|Sept|Sep|Oct|Nov|Dec|january|february|march|april|may|june|july|august|september|october|november|december)[./-]?\s?((19|20|21|22)\d+)|(0[1-9]|1[0-9]|2[0-9]|3[0-1])\s(Ean|Fea|Már|Mar|Aib|Bea|Mei|Iúi|Iui|Lún|Lun|MFÓ|MFO|DFO|DFÓ|SAM|NOL)\s?(\/)\s?(Jan|Feb|Mar|Apr|May|Jun|JUNE|July|Jul|Aug|Sept|Sep|Oct|Nov|Dec)\s(\d+|(19|20|21|22)\d+)|(0[1-9]|1[0-9]|2[0-9]|3[0-1])\s(Jan|Feb|Mar|Apr|May|Jun|JUNE|July|Jul|Aug|Sept|Sep|Oct|Nov|Dec)\s?(\/)\s?(jan|fév|Fev|Mar|Avr|Mai|juin|JULN|JUL|Aoû|Aou|sept|sep|oct|Nov|déc|Dec)\s(\d+|(19|20|21|22)\d+)',
                re.IGNORECASE)
            val_reg = val.findall(text)
            for i in range(len(val_reg)):
                date_val.append([x for x in val_reg[i] if x != ''])
                if re.search(r'([A-Za-z]+\s/\s[A-Za-z])'," ".join(date_val[i])):
                    date_regex.append(" ".join(date_val[i][:5]).replace(' / ','/'))

                else:
                    date_regex.append(" ".join(date_val[i][:3]))
            for i in range(len(date_regex)):
                if re.search('\/\s?(!?Jan|Feb|Mar|Apr|May|Jun|June|July|Jul|Aug|Sept|Sep|Oct|Nov|Dec)|(!?Jan|Feb|Mar|Apr|May|Jun|June|July|Jul|Aug|Sept|Sep|Oct|Nov|Dec)\/\s?', date_regex[i],re.IGNORECASE):
                    d = date_regex[i].find(re.findall('Jan|Feb|Mar|Apr|May|Jun|July|Jul|Aug|Sept|Sep|Oct|Nov|Dec', date_regex[i],re.IGNORECASE)[0])
                    if '/' in date_regex[i]:
                        if d == 7:
                            date_regex[i] = date_regex[i].replace(date_regex[i].split('/')[0].split().pop(1), '',1).replace('/', '')
                        if d == 3:
                            date_regex[i] = date_regex[i].replace(date_regex[i].split('/')[1].split().pop(0), '',1).replace('/', '')
                date=parse(date_regex[i])
                actual_date.append(date.strftime('%Y/%m/%d'))
                if datetime.datetime.strptime(actual_date[0],'%Y/%m/%d').year >datetime.datetime.now().year:
                    actual_date[0]=actual_date[0].replace(str(datetime.datetime.strptime(actual_date[0],'%Y/%m/%d').year), str(datetime.datetime.strptime(actual_date[0],'%Y/%m/%d').year-100))
            expiry_date=max(actual_date)
            dob_date=min(actual_date)

            if expiry_date != "" and dob_date != "":
                for date in actual_date:
                    if date > dob_date and date < expiry_date:
                        issue_date = date

            actual_expiry_date = datetime.datetime.strptime(expiry_date,'%Y/%m/%d').strftime('%m/%d/%Y')
            actual_dob_date = datetime.datetime.strptime(dob_date, '%Y/%m/%d').strftime('%m/%d/%Y')
            actual_issue_date = datetime.datetime.strptime(issue_date, '%Y/%m/%d').strftime( '%m/%d/%Y')

            print(actual_dob_date,actual_issue_date,actual_expiry_date)

            return actual_dob_date,actual_issue_date,actual_expiry_date,date_regex

        except Exception as e:
            print(e)
            actual_dob_date,actual_issue_date,actual_expiry_date,date_regex='',"","",""
            return actual_dob_date,actual_issue_date,actual_expiry_date,date_regex

    def passport_all_details(self,text):

        cyrList = 'ΝΑΚΙΑАВЕМСТахУХуОНРеԚԛԜԝҮү•'
        latList = 'NAKIAABEMCTaxyXyOHPeQqWwYy.'
        table = str.maketrans(cyrList, latList)
        text = text.translate(table)
        print(text)
        passport_number=self.get_passport_no(text)
        dob, issue_date, expiry_date,date_regex= self.get_all_dates(text)
        name=self.get_passport_name(text,passport_number,date_regex)


        return passport_number,name,dob,issue_date,expiry_date