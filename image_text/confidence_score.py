import io,sys
import re,json
from google.cloud import vision
from google.cloud import vision_v1p1beta1 as vision
sys.path.insert(0, '../image_text')
sys.path.insert(0, '../all_documents')
import pay_other_confidence
import avoid
class text_score:
    def __init__(self):
        self.keys,self.values=[],[]
        self.dict,self.address_val, self.others,self.f_name,self.l_name,self.m_name={},{},{},{},{},{}
        self.address_confidence = 0.0
        self.ssn_confidence_score=0.0
        self.ssn_name_confidence_score=0.0
        self.date_confidence_score = 0.0
        self.ssn_date_confidence_score = 0.0
        self.license_confidence_score=0.0
        self.f_name_confidence_score=0.0
        self.m_name_confidence_score=0.0
        self.l_name_confidence_score=0.0
        self.f_name_score = 0
        self.m_name_score = 0
        self.l_name_score = 0
        self.date_score, self.address_score, self.other_score,self.license_score, self.ssn_score,self.paystub_score,\
        self.ssn_name_score,self.ssn_date_score=0,0,0,0,0,0,0,0
        self.full_address = ''
        self.result={}
        self.val=[]
        self.paystub={}
        self.date={}
        self.license_id_dict={}
        self.paystub_confidence_score = 0.0
        self.other_confidence=0.0

        self.passport_date_confidence_score = 0.0
        self.passport_fn_confidence_score = 0.0
        self.passport_mn_confidence_score = 0.0
        self.passport_ln_confidence_score = 0.0
        self.passport_no_confidence_score = 0.0

        self.passport_date_score = 0
        self.passport_fn_score = 0
        self.passport_mn_score = 0
        self.passport_ln_score = 0
        self.passport_no_score = 0

        self.emp_name, self.employee_name = {}, {}
        self.emp_address, self.employee_address = {}, {}
        self.regular1, self.regular2, self.regular3, self.regular4, self.regular5, self.regular6, self.regular7, self.regular8, self.regular9, self.regular10 = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
        self.tax1, self.tax2, self.tax3, self.tax4, self.tax5, self.tax6, self.tax7, self.tax8, self.tax9, self.tax10 = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
        self.deduction1, self.deduction2, self.deduction3, self.deduction4, self.deduction5, self.deduction6, self.deduction7, self.deduction8, self.deduction9, self.deduction10,self.deduction11,self.deduction12,self.deduction13,self.deduction14,self.deduction15={},{},{},{},{},{},{},{},{},{},{},{},{},{},{}
        self.pay_start_date, self.pay_end_date, self.pay_date = {}, {}, {}
        self.word,self.license_text,self.regex_value= '','',""
        with open('../config/filtering.json', 'r') as data:
            self.state_value = json.load(data)
        self.pay_val=pay_other_confidence.Confidence_Calculation()
        self.client = vision.ImageAnnotatorClient()
    def license_confidence(self,data,text,result):
        try:

            for key, value in enumerate(result):
                print(value)
                va = value[0]
                va = va.rstrip()
                va = va.lstrip()
                for key1, value1 in data.items():
                    if va != '' and value1 != '':
                        # if value[0] in value1:
                        if re.search(r'(?!' + re.escape(va) + r')', value1):

                            if va in data['date_val']:
                                    self.dict.update({va: value[1]})

                            if any(char in data['first_name'] for char in va):
                                self.f_name.update({va: value[1]})

                            if va in data['first_name']:
                                if self.f_name != {}:
                                    self.f_name.clear()
                                    self.f_name.update({va: value[1]})

                            if any(char in data['middle_name'] for char in va):
                                self.m_name.update({va: value[1]})

                            if va in data['middle_name']:
                                if self.m_name != {}:
                                    self.m_name.clear()
                                    self.m_name.update({va: value[1]})

                            if any(char in data['last_name'] for char in va):
                                self.l_name.update({va: value[1]})

                            if va in data['last_name']:
                                if self.l_name != {}:
                                    self.l_name.clear()
                                    self.l_name.update({va: value[1]})

                            if va in data['address']:
                                self.address_val.update({va: value[1]})

                            elif any(char in data['address'] for char in va):
                                self.address_val.update({va: value[1]})

                            if va in data['license_id']:
                                self.license_id_dict.update({va: value[1]})

                            elif any(char in data['license_id'] for char in va):
                                self.license_id_dict.update({value[0]: value[1]})


                            else:
                                self.others.update({va:value[1]})

            if len(self.f_name)>=1:
                x = 0
                val1 = []
                for key6, value6 in self.f_name.items():
                    if int(value6 * 100) <= 20:
                        if x < 4:
                            self.f_name_score = 0
                            x = x + 1
                            break
                    else:
                        self.f_name_confidence_score = self.f_name_confidence_score + value6
                        val1.append(value6)
                x = x + 1
                self.f_name_score = int((self.f_name_confidence_score / len(self.f_name)) * 100)
                if self.f_name_score > 100:
                    self.f_name_score = 85
            else:
                self.f_name_score=0

            if len(self.m_name) >= 1:
                x = 0
                val1 = []
                for key6, value6 in self.m_name.items():
                    if int(value6 * 100) <= 20:
                        if x < 4:
                            self.m_name_score = 0
                            x = x + 1
                            break
                    else:
                        self.m_name_confidence_score = self.m_name_confidence_score + value6
                        val1.append(value6)
                x = x + 1
                self.m_name_score = int((self.m_name_confidence_score / len(self.m_name)) * 100)
                if self.m_name_score > 100:
                    self.m_name_score = 85
            else:
                self.m_name_score=0

            if len(self.l_name) >= 1:
                x=0
                val1 = []
                for key6, value6 in self.l_name.items():
                    if int(value6*100)<=20:
                        if x < 4:
                            self.l_name_score = 0
                            x=x+1
                            break
                    else:
                        self.l_name_confidence_score = self.l_name_confidence_score + value6
                        val1.append(value6)
                    x = x + 1
                    self.l_name_score = int((self.l_name_confidence_score / len(self.l_name)) * 100)
                    if self.l_name_score > 100:
                        self.l_name_score = 85
            else:
                self.l_name_score=0

            if len(self.license_id_dict)>=1:
                for key5, value5 in self.license_id_dict.items():
                    self.license_confidence_score = self.license_confidence_score + value5
                    self.val.append(value5)
                # print(self.val)
                len_confidence_score=len(self.license_id_dict)
                text = avoid.address_replace(text)
                state_regex = re.findall(
                    r"\b((?=AL|AK|AS|AZ|AŽ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE"
                    r"|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|and|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)[A-Z]{2}[, ])([A-Za-z]+)?\d+",
                    text)
                # print(len(self.state_value['data']))
                if state_regex != []:
                    for i in range(len(self.state_value['data'])):
                        if self.state_value['data'][i]['state'] in state_regex[0][0]:
                            self.regex_value = self.state_value['data'][i]['license_id']
                            # print("regex_state_value", self.state_value['data'][i]['state'], self.regex_value)
                    # print("state regex", self.regex_value)
                licence_id = re.findall(self.regex_value,text)
                if licence_id!=[]:
                    if self.license_confidence_score==0:
                        self.license_score=76
                    else:
                        self.license_score = int((self.license_confidence_score/len_confidence_score) * 100)
                        if self.license_score>100:
                            self.license_score=85
                else:
                    self.license_score=(min(self.val)*100)

            if len(self.address_val) > 1:
                self.val.clear()
                for key3, value3 in self.address_val.items():
                    self.address_confidence = self.address_confidence + value3
                    self.val.append(value3)
                self.address_score = int((min(self.val)+max(self.val))/2*100)
                    # int((self.address_confidence / len(self.address_val)) * 100)
                # if self.address_score > 100:
                #     self.address_score = 97

            for key2, value2 in self.dict.items():
                self.date_confidence_score = self.date_confidence_score + value2

            for key4, value4 in self.others.items():
                self.other_confidence = self.other_confidence + value4

            dict_length=len(self.dict)
            other_length=len(self.others)

            if other_length>=1 and dict_length>=1:
                self.date_score = int((self.date_confidence_score / dict_length) * 100)
                self.other_score = int((self.other_confidence / other_length) * 100)

            else:
                self.date_score=75
                self.other_score=79

            return self.dict,self.date_score,self.address_score,self.license_score,self.other_score,self.f_name_score,self.m_name_score,self.l_name_score,data

        except Exception as e:
            data=''
            return self.dict, self.date_score, self.address_score, self.license_score, self.other_score,self.f_name_score,self.m_name_score,self.l_name_score,data
    def ssn_confidence(self,data,keys,values):
        try:
            result = dict(zip(keys, values))
            for key, value in result.items():
                for key1, value1 in data.items():
                    if key != '' and value1 != '':
                        if re.search(r'\b(=?' + re.escape(key) + r')\b', value1):
                            if key in data['ssn_number']:
                                self.ssn_confidence_score = value
                            elif key in data['ssn_date']:
                                self.ssn_date_confidence_score = self.ssn_date_confidence_score + value
                            else:
                                self.ssn_name_confidence_score = self.ssn_name_confidence_score + value

            self.ssn_score = int((self.ssn_confidence_score * 100))
            if self.ssn_score >= 100:
                self.ssn_score = 87

            self.ssn_date_score = int((self.ssn_date_confidence_score * 100))
            if self.ssn_date_score >= 100:
                self.ssn_date_score=87

            self.ssn_name_score = int((self.ssn_name_confidence_score * 100))
            if self.ssn_name_score >= 100:
                self.ssn_name_score=83

            return str(self.ssn_score),str(self.ssn_name_score),str(self.ssn_date_score)
        except Exception as E:
            return self.ssn_score
    def paystub_confidence(self,data_val,keys,values):
        data={}
        try:
            result=dict(zip(keys,values))
            a = 0
            b = 0
            c = 0

            for key, value in data_val.items():
                if "field_value_original" in data_val[key]:
                    if value['field_value_original'] != "":
                        data.update({key:value})
                else:
                        data.update({key: value})

            # print("in None Data",data)
            for key, value in result.items():

                for key1, value1 in data.items():
                    if key1 != '' and value1 != '':
                        if key1 != '' or key!='':
                            if "field_value_original" in data[key1]:
                                if key in value1['field_value_original']:



                                    if "regular" in value1['alias']:
                                        a = a + 1
                                        var_name = "regular" + str(a)
                                        if "1" in var_name:
                                            self.regular1.update({str(key): value})
                                        if "2" in var_name:
                                            self.regular2.update({str(key): value})
                                        if "3" in var_name:
                                            self.regular3.update({str(key): value})
                                        if "4" in var_name:
                                            self.regular4.update({str(key): value})
                                        if "5" in var_name:
                                            self.regular5.update({str(key): value})
                                        if "6" in var_name:
                                            self.regular6.update({str(key): value})
                                        if "7" in var_name:
                                            self.regular7.update({str(key): value})
                                        if "8" in var_name:
                                            self.regular8.update({str(key): value})
                                        if "9" in var_name:
                                            self.regular9.update({str(key): value})
                                        if "10" in var_name:
                                            self.regular10.update({str(key): value})

                                    elif "tax" in value1['alias']:
                                        b = b + 1
                                        var_name = "tax" + str(b)
                                        if "1" in var_name:
                                            self.tax1.update({str(key): value})
                                        if "2" in var_name:
                                            self.tax2.update({str(key): value})
                                        if "3" in var_name:
                                            self.tax3.update({str(key): value})
                                        if "4" in var_name:
                                            self.tax4.update({str(key): value})
                                        if "5" in var_name:
                                            self.tax5.update({str(key): value})
                                        if "6" in var_name:
                                            self.tax6.update({str(key): value})
                                        if "7" in var_name:
                                            self.tax7.update({str(key): value})
                                        if "8" in var_name:
                                            self.tax8.update({str(key): value})
                                        if "9" in var_name:
                                            self.tax9.update({str(key): value})
                                        if "10" in var_name:
                                            self.tax10.update({str(key): value})

                                    elif "deduction" in value1['alias']:
                                        c = c + 1
                                        var_name = "deduction" + str(c)
                                        if "1" in var_name:
                                            self.deduction1.update({str(key): value})
                                        if "2" in var_name:
                                            self.deduction2.update({str(key): value})
                                        if "3" in var_name:
                                            self.deduction3.update({str(key): value})
                                        if "4" in var_name:
                                            self.deduction4.update({str(key): value})
                                        if "5" in var_name:
                                            self.deduction5.update({str(key): value})
                                        if "6" in var_name:
                                            self.deduction6.update({str(key): value})
                                        if "7" in var_name:
                                            self.deduction7.update({str(key): value})
                                        if "8" in var_name:
                                            self.deduction8.update({str(key): value})
                                        if "9" in var_name:
                                            self.deduction9.update({str(key): value})
                                        if "10" in var_name:
                                            self.deduction10.update({str(key): value})
                                        if "11" in var_name:
                                            self.deduction11.update({str(key): value})
                                        if "12" in var_name:
                                            self.deduction12.update({str(key): value})
                                        if "13" in var_name:
                                            self.deduction13.update({str(key): value})
                                        if "14" in var_name:
                                            self.deduction14.update({str(key): value})
                                        if "15" in var_name:
                                            self.deduction15.update({str(key): value})
                            else:
                                if re.search(r'(?!' + re.escape(key) + r')', value1):
                                    if key in data['pay_period_end_date']:
                                        self.pay_end_date.update({str(key): value})

                                    elif key in data['pay_period_start_date']:
                                        self.pay_start_date.update({str(key): value})

                                    elif key in data['pay_date']:
                                        self.pay_date.update({str(key): value})

                                    elif key in data['employee_address'] :
                                        self.employee_address.update({str(key): value})

                                    elif key in data['employer_address']:
                                        self.emp_address.update({str(key): value})

                                    elif key in data['employee_mn'] :
                                        self.employee_name.update({str(key): value})
                                    elif key in data['employee_ln'] :
                                        self.employee_name.update({str(key): value})
                                    elif key in data['employee_fn'] :
                                        self.employee_name.update({str(key): value})

                                    elif key in data['employer_name']:

                                        self.emp_name.update({str(key): value})
                                    else:

                                        self.dict.update({str(key): value})

            regular1_scrore,regular2_scrore,regular3_scrore,regular4_scrore,regular5_scrore,regular6_scrore,regular7_scrore,\
            regular8_scrore,regular9_scrore,regular10_scrore,tax1_scrore,tax2_scrore,tax3_scrore,tax4_scrore,tax5_scrore,\
            tax6_scrore,tax7_scrore,tax8_scrore,tax9_scrore,tax10_scrore,deduction1_scrore,deduction2_scrore,deduction3_scrore,\
            deduction4_scrore,deduction5_scrore,deduction6_scrore,deduction7_scrore,deduction8_scrore,deduction9_scrore,deduction10,deduction11_scrore,deduction12_scrore,deduction13_scrore,deduction14_scrore,deduction15_scrore,\
            pay_end_date_scrore,pay_start_date_scrore,pay_date_scrore,employee_address_scrore,employee_name_scrore,\
            employer_address_scrore,employer_name_scrore,other_scrore = self.pay_val.all_confidence_scrore(self.regular1,
            self.regular2, self.regular3, self.regular4, self.regular5, self.regular6, self.regular7, self.regular8, self.regular9,
            self.regular10,self.tax1, self.tax2, self.tax3, self.tax4, self.tax5, self.tax6, self.tax7, self.tax8, self.tax9,
            self.tax10,self.deduction1, self.deduction2, self.deduction3,self.deduction4, self.deduction5, self.deduction6,
            self.deduction7, self.deduction8, self.deduction9, self.deduction10,self.deduction11,self.deduction12,self.deduction13,self.deduction14,self.deduction15,self.pay_start_date, self.pay_end_date,
            self.pay_date,self.employee_address,self.emp_address,self.employee_name,self.emp_name,self.dict)

            return regular1_scrore,regular2_scrore,regular3_scrore,regular4_scrore,regular5_scrore,regular6_scrore,regular7_scrore,\
            regular8_scrore,regular9_scrore,regular10_scrore,tax1_scrore,tax2_scrore,tax3_scrore,tax4_scrore,tax5_scrore,\
            tax6_scrore,tax7_scrore,tax8_scrore,tax9_scrore,tax10_scrore,deduction1_scrore,deduction2_scrore,deduction3_scrore,\
            deduction4_scrore,deduction5_scrore,deduction6_scrore,deduction7_scrore,deduction8_scrore,deduction9_scrore,deduction10,deduction11_scrore,deduction12_scrore,deduction13_scrore,deduction14_scrore,deduction15_scrore,\
            pay_end_date_scrore,pay_start_date_scrore,pay_date_scrore,employee_address_scrore,employee_name_scrore,\
            employer_address_scrore,employer_name_scrore,other_scrore

        except Exception as E:
            pass

    def passport_confidence(self,data,keys,values):
        try:
            result = dict(zip(keys, values))
            for key, value in result.items():
                # print(key)
                for key1, value1 in data.items():
                    if key != '' and value1 != '':
                        if key in value1: #re.search(r'\b(=?' + key + r')\b', value1) or
                            if key in data['passport_no']:
                                self.passport_no_confidence_score = value

                            elif key in data['dob']:
                                self.passport_date_confidence_score = self.passport_date_confidence_score + value

                            elif key in data['issue_date']:
                                self.passport_date_confidence_score = self.passport_date_confidence_score + value

                            elif key in data['expiration_date']:
                                self.passport_date_confidence_score = self.passport_date_confidence_score + value

                            elif key in data['first_name']:
                                self.passport_fn_confidence_score = self.passport_fn_confidence_score + value

                            elif key in data['middle_name']:
                                self.passport_mn_confidence_score = self.passport_mn_confidence_score + value

                            elif key in data['last_name']:
                                self.passport_ln_confidence_score = self.passport_ln_confidence_score + value



            self.passport_no_score = int((self.passport_no_confidence_score * 100))
            if self.passport_no_score >= 100:
                self.passport_no_score = 87

            self.passport_date_score = int((self.passport_date_confidence_score * 100))
            if self.passport_date_score >= 100:
                self.passport_date_score=87

            self.passport_fn_score = int((self.passport_fn_confidence_score * 100))
            if self.passport_fn_score >= 100:
                self.passport_fn_score=85

            self.passport_mn_score = int((self.passport_mn_confidence_score * 100))
            if self.passport_mn_score >= 100:
                self.passport_mn_score = 78

            self.passport_ln_score = int((self.passport_ln_confidence_score * 100))
            if self.passport_ln_score >= 100:
                self.passport_ln_score = 88
            return str(self.passport_no_score),str(self.passport_fn_score),str(self.passport_mn_score),str(self.passport_ln_score),str(self.passport_date_score)

        except Exception as E:
            return self.passport_no_score,self.passport_fn_score,self.passport_mn_score,self.passport_ln_score,self.passport_date_score
