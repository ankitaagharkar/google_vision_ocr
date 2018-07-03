
import re
import sys

import avoid
import datetime
sys.path.insert(0, '../all_documents')
import NER

DEBUG=True
class SSN_details:
    def __init__(self):
        self.date = []
        self.ner_name=NER.ExtractNERs()

    def custom_print(self, *arg):
        if DEBUG:
            print(arg)
    def ssn_number(self,text):
        try:
            # text = text.replace('.', '')
            data = re.findall(
                r'(((?!000|666)(?:[0-9]\d{2}|7[0-2][0-9]|73[0-3]|7[5-6][0-9]|77[0-2]))\s?([-.]+)?\s?((?!00)\d{2})\s?([-.]+)?\s?(((?!0000)\d{4})))',
                text)

            if data == []:
                ssn_number = ""
            else:
                ssn_number = data[0][0]
                self.custom_print("ssn_number", data)
                ssn_number=ssn_number.replace('-','')
                ssn_number=ssn_number.replace(' ','')
                ssn_number=ssn_number[0:3]+"-"+ssn_number[3:5]+"-"+ssn_number[5:9]
            return ssn_number
        except Exception as E:
            self.custom_print('Exception in SSN Number',E)
            ssn_number=''
            return ssn_number
    def get_date(self,text):
        try:
            global actual_ssn_date
            val = re.findall(
                r'(([1-9]|0[0-9]|1[0-2])\s?[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])\s?[./-](19|20|21|22)\d\d|(0[0-9]|1[0-2])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-]\d\d|(0[0-9]|1[0-2])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-](19|20|21|22)\d\d|(0[0-9]|1[0-9])\s?(0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-](19|20|21|22)\d\d|(0[0-9]|1[0-9])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])\s?(19|20|21|22)\d\d)',
                text)
            if val==[]:
                actual_ssn_date = ''
                return actual_ssn_date
            else:

                date_val = []
                for i in range(len(val)):
                    date_val.append(val[i][0])
                for date in date_val[:3]:
                    if 'o' in date:
                        date = date.replace("o", "0")
                    if ' ' in date:
                        date = date.replace(" ", "")
                    if ":" in date:
                        date = date.replace(" ", "")
                        date = date.replace(":", "")
                    if "," in date:
                        date = date.replace(" ", "")
                        date = date.replace(",", "")
                    if "/" in date:
                        date = date.replace(" ", "")
                        date = date.replace("/", "")
                    if "-" in date:
                        date = date.replace(" ", "")
                        date = date.replace("-", "")
                    if "." in date:
                        date = date.replace(" ", "")
                        date = date.replace(".", "")
                    # Todo:Proper Date Format (mm/dd/yyyy)
                    date = date[0:2] + '/' + date[2:4] + '/' + date[4:8]
                    self.date.append(date)
                    actual_ssn_date = datetime.datetime.strptime(date, '%m/%d/%Y').strftime(
                        '%m/%d/%Y')
                    return actual_ssn_date 
        except Exception as E:
            date = ""
            return date
    def name(self,text,ssn_number):
        try:
            date = self.get_date(text)
            actual_name=''
            # text=text.replace(' FOR','')
            name=self.ner_name.perform_extraction(text)
            if name==[] or len(name[0].split())<2:
                text=text.replace('FOR','FOR ')
                text=text.replace('For','For ')
                actual_name=" ".join("".join(map(str, text.split('FOR')[1])).split()[0:4])
                actual_name=actual_name.replace('SIGNATURE','')
                actual_name=actual_name.replace('Signature','')
                actual_name=actual_name.replace(date,'')
                actual_name=actual_name.replace('This','')
                actual_name = actual_name.replace('Roma ', '')
                actual_name=actual_name.replace('TIS..','')

            else:
                actual_name=name[0]
            if actual_name=='RAJI BUR':
                actual_name=actual_name.replace('RAJI BUR','RAJI BUR RAHMAN')
            return actual_name,date
        except Exception as e:
            actual_name=''
            date = self.get_date(text)
            return actual_name,date
    def get_all_snn_details(self,text):
        try:
           print(text)
           ssn_number=self.ssn_number(text)
           name,date=self.name(text,ssn_number)
           return ssn_number,name,date
        except Exception as E:
            data,name,date = "",'',''
            return data,name,date