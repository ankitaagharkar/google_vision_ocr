import sys
from cgitb import text

from PIL import Image

sys.path.insert(0, '../all_documents')
sys.path.insert(0, '../all_documents')
sys.path.insert(0, '../image_processing')
sys.path.insert(0, '../image_text')

import threading,json
import  LicenseOCR
import get_ssn_details
import get_paystub_details
import image_denoising
import get_all_locations
import confidence_score
import LicenseOCR
import json
import re
import threading
from multiprocessing import Queue
from urllib.request import urlopen
import os
import subprocess
import requests
import get_ssn_paystub_location



class Scan_OCR:
    def __init__(self):
        self.regular_earnings = ["Regular", "Earnings", "Wages", "Regular Wages", "Regular Time",
                                 "Base Salary", "Regular Salary", "Salary"]
        self.Vacation = ["Holiday", "Holiday Time", "Holiday Premiu", "Float Holiday", "Vacation"]
        self.Overtime = ["Overtime", "St Time O/T"]
        self.post_deduction_personal = ["Personal Deduction"]
        self.post_deduction_life = ["Life Deduction"]
        self.post_deduction_accident = ["Accident"]
        self.Bonus = ["Bonus"]
        self.commission = ["Commission"]
        self.federal_taxes = ["Federal Taxes", "Federal Income Tax", "Federal Witholdings",
                              "Federal W/H", "Fed Tax", "Fed Income Tax", "Fed Witholdings",
                              "Fed W/H", "FFD W/H", "FFD Taxes", "FFD Tax"]
        self.SSI = ["SSI Tax", "Social Security Tax", "Socail Security", "FICA", "Soc Sec"]
        self.Medicare = ["Medicare Tax", "FED Medicare Tax", "Medicare"]
        self.tax_di = ["DI", "Disability Tax"]
        self.tax_oasdi = ["OASDI"]
        self.State = ["State Income Tax", "Withholding Tax", "State Income", "SIT"]
        self.City = ["Cit Income Tax", "City Re"]
        self.pre_duction_K = ["401K", "401K$", "401(K)"]
        self.pre_duction_medicare = ["Medical Pre Tax", "Medical", "Med125", "Med Pre Tax"]
        self.pre_duction_vision = ["Vision Pre Tax", "Vision"]
        self.pre_duction_health = ["Hlth Sau", "Health", "Health Pre Tax"]
        self.pre_duction_dental = ["Dental Pre Tax", "Dental"]
        self.post_duction_disability = ["Voluntary Disability", "State DI"]

        self.scan_result = {}
        self.text = ''
        self.name_value = []
        self.location_val = []
        self.confidence = Queue()
        self.scan_text = Queue()
        self.image_processing = Queue()
        self.lic_text = Queue()
        self.img2pdf = Queue()
        self.doc_text = Queue()
        self.get_image_text = Queue()
        self.location = Queue()
        self.get_response = Queue()
        self.get_license_confidence = Queue()
        self.get_license_details = Queue()
        self.get_ssn_confidence = Queue()
        self.get_paystub_confidence = Queue()
        self.get_date_image = Queue()

        self.confidence_text = confidence_score.text_score()
        self.lic = LicenseOCR.LicenseOCR()
        self.sp_location = get_ssn_paystub_location.get_all_sp_location()
        self.ssn = get_ssn_details.SSN_details()
        self.Paystub = get_paystub_details.Paystub_details()
        self.denoising = image_denoising.Denoising()
        self.score = confidence_score.text_score()

        with open('../config/config.json') as data_file:
            self.config = json.load(data_file)
        with open('../config/filtering.json', 'r') as data:
            self.state_value = json.load(data)

    def image_processing_threading(self,image_path,doc_type):
        try:

            image=self.denoising.image_conversion_smooth(image_path,doc_type)
            #print("in img pro",image)
            self.image_processing.put(image)
        except Exception as e:
            print(e)
            pass
    def get_doc(self,path, doc_type):
        try:

            self.text, description, result, keys, values, texts = self.sp_location.get_text(path)

            if 'SSN' in doc_type:
                SSN_Number,name,date = self.ssn.get_all_snn_details(self.text)
                self.scan_text.put((self.text, SSN_Number,name,date,keys,values))

        except Exception as e:
            print(e)
    def get_doc_text(self,path,doc_type):

        # self.text,description,result,_,_,_ = self.Location.get_text(path,doc_type)
        employer_full_address, employer_street, employer_state, employer_zipcode, employer_city, employee_full_address, employee_street, employee_state, employee_zipcode, employee_city, start_date, pay_frequency, string_date_value, employer_name, employee_name, current_gross_pay, ytd_gross_pay, current_net_pay, ytd_net_pay, taxes, current_taxes, ytd_taxes, rate_taxes, hrs_taxes, earnings, current_earnings, ytd_earnings, rate_regular, hrs_regular, pre_deduction, current_pre_deduction, ytd_pre_deduction, rate_pre_deduction, hrs_pre_deduction, post_deduction, current_post_deduction, ytd_post_deduction, rate_post_deduction, hrs_post_deduction, total_calculated_taxes, current_total_calculated_taxes, ytd_total_calculated_taxes, hrs_total_calculated_taxes, rate_total_calculated_taxes, total_calculated_regular, current_total_calculated_regular, ytd_total_calculated_regular, hrs_total_calculated_regular, rate_total_calculated_regular, total_calculated_pre, current_total_calculated_pre, ytd_total_calculated_pre, hrs_total_calculated_pre, rate_total_calculated_pre, total_calculated_post, current_total_calculated_post, ytd_total_calculated_post, hrs_total_calculated_post, rate_total_calculated_post, total_taxes, current_total_taxes, ytd_total_taxes, hrs_total_taxes, rate_total_taxes, total_regular, current_total_regular, ytd_total_regular, hrs_total_regular, rate_total_regular, total_pre, current_total_pre, ytd_total_pre, hrs_total_pre, rate_total_pre, total_post, current_total_post, ytd_total_post, hrs_total_post, rate_total_post, employment_Start_date, pay_date,position,result = self.Paystub.get_details(path)
        self.doc_text.put((self.text,employer_full_address, employer_street, employer_state, employer_zipcode, employer_city, employee_full_address, employee_street, employee_state, employee_zipcode, employee_city, start_date, pay_frequency, string_date_value, employer_name, employee_name, current_gross_pay, ytd_gross_pay, current_net_pay, ytd_net_pay, taxes, current_taxes, ytd_taxes, rate_taxes, hrs_taxes, earnings, current_earnings, ytd_earnings, rate_regular, hrs_regular, pre_deduction, current_pre_deduction, ytd_pre_deduction, rate_pre_deduction, hrs_pre_deduction, post_deduction, current_post_deduction, ytd_post_deduction, rate_post_deduction, hrs_post_deduction, total_calculated_taxes, current_total_calculated_taxes, ytd_total_calculated_taxes, hrs_total_calculated_taxes, rate_total_calculated_taxes, total_calculated_regular, current_total_calculated_regular, ytd_total_calculated_regular, hrs_total_calculated_regular, rate_total_calculated_regular, total_calculated_pre, current_total_calculated_pre, ytd_total_calculated_pre, hrs_total_calculated_pre, rate_total_calculated_pre, total_calculated_post, current_total_calculated_post, ytd_total_calculated_post, hrs_total_calculated_post, rate_total_calculated_post, total_taxes, current_total_taxes, ytd_total_taxes, hrs_total_taxes, rate_total_taxes, total_regular, current_total_regular, ytd_total_regular, hrs_total_regular, rate_total_regular, total_pre, current_total_pre, ytd_total_pre, hrs_total_pre, rate_total_pre, total_post, current_total_post, ytd_total_post, hrs_total_post, rate_total_post, employment_Start_date,pay_date,position,result))
    def get_lic_text(self, path, doc_type):

        self.text,description,result,keys,values,texts = self.Location.get_text(path, doc_type)
        self.lic_text.put((self.text, description,result,keys,values,texts))
    def image_to_pdf(self, image_path, doc_type):
        try:
            filename = os.path.basename(image_path)
            print(filename)
            print(type(filename))
            image_path1="C:/Users/ankitaa/PycharmProjects/iDocufy_Ocr_Final/images/documents_upload/" + filename
            print(image_path1)
            filename1 = filename.split('.', 1)[0] + ".jpg"
            f_path= "C:/Users/ankitaa/PycharmProjects/iDocufy_Ocr_Final/images/documents_upload/" + filename1
            #process = subprocess.Popen(['C:\\Program Files (x86)\\ImageMagick-6.9.3-Q16\\convert.exe', '-density', ' 300','-trim', image_path1, '-quality', '100',f_path,shell=True])
            process = subprocess.call('convert -density 300 -trim ' +image_path1+ ' -quality 100 '+f_path,shell=True)
            # if 'Paystub' in doc_type:
            #     _, filename = os.path.split(image_path)
            #
            #     src_pdf = PyPDF2.PdfFileReader(open(image_path, "rb"))
            #     file = self.c.pdf_page_to_png(src_pdf, doc_type, pagenum=0, resolution=300)
            #     filename = filename.rsplit('.', 1)[0] + ".jpg"
            #     # print('in paystub', filename)
            #     file.save(filename="../images/documents_upload/" + filename)
            #     path = "../images/documents_upload/" + filename
            # else:
            #     _, filename1 = os.path.split(image_path)
            #     src_pdf = PyPDF2.PdfFileReader(open(image_path, "rb"), strict=False)
            #     file = self.c.pdf_page_to_png(src_pdf, doc_type, pagenum=0, resolution=300)
            #     filename1 = filename1.rsplit('.', 1)[0] + ".jpg"
            #     file.save(filename="../images/documents_upload/"+filename1)
            #     path = "../images/documents_upload/"+filename1
            print(process)

            # path="../images/documents_upload"+filename1

            self.img2pdf.put(f_path)
        except Exception as e:
            print("in image to pdf",e)
            pass
    def get_image_text(self,path):
        self.text, description, result, keys, values, texts_description = self.Location.get_text(path)
        self.get_image_text.put((self.text, description, result, keys, values, texts_description))
    def get_license_confidences(self,data,text,result):
        dict, date_score, address_score, license_score, other_score=self.confidence_text.license_confidence(data,text,result)
        self.get_license_confidence.put((dict, date_score, address_score, license_score, other_score))
    def get_ssn_pay_location(self,value_json,image,doc_type,result):
        if 'SSN' in doc_type:
            ssn_location, name_location, date_location, filename = self.sp_location.ssn_get_location(value_json, image)
            self.location.put((ssn_location, name_location, date_location, filename))
        elif 'Paystub' in doc_type:

            emp_name, employee_name, emp_address, employee_address, regular1, regular2, regular3, regular4, regular5, regular6, regular7, regular8, regular9, regular10, tax1, tax2, tax3, tax4, tax5, tax6, tax7, tax8, tax9, tax10, deduction1, deduction2, deduction3, deduction4, deduction5, deduction6, deduction7, deduction8, deduction9, deduction10, deduction11, deduction12, deduction13, deduction14, deduction15, pay_start_date, pay_end_date, pay_date, dict_location, filename, value_data = self.sp_location.paystub_get_location(value_json, image,result)
            self.location.put((emp_name, employee_name, emp_address, employee_address, regular1, regular2,
                           regular3, regular4, regular5, regular6, regular7, regular8, regular9,
                       regular10, tax1, tax2, tax3, tax4, tax5, tax6, tax7, tax8, tax9, tax10,
                       deduction1, deduction2, deduction3, deduction4, deduction5, deduction6,
                       deduction7, deduction8, deduction9, deduction10, deduction11, deduction12,
                       deduction13, deduction14, deduction15, pay_start_date, pay_end_date,
                       pay_date, dict_location, filename, value_data))
    def get_location(self,value_json,image,doc_type,result):
        try:
            self.Location = get_all_locations.get_all_location(result)
            if 'License' in doc_type:
                address_location, licence_id_location, dict,filename=self.Location.get_license_location(value_json,image)
                self.location.put((address_location, licence_id_location, dict,filename))

        except Exception as e:
            print(e)
    def get_license_all_details(self,path):
        try:
            response, licence_id, expiry_date, dob, issue_date, address, name, state, zipcode, city, date_val,result,pdf_image_path=self.lic.run(path)
            self.get_license_details.put((response, licence_id, expiry_date, dob, issue_date, address, name, state, zipcode, city, date_val,result,pdf_image_path))
        except:
            response=licence_id = expiry_date = dob = issue_date = address = name = state = zipcode = city = date_val =result=pdf_image_path= ''
            self.get_license_details.put((response, licence_id, expiry_date, dob, issue_date,
                                          address, name, state, zipcode, city, date_val, result,
                                          pdf_image_path))
    def confidence_score(self,path, doc_type,data,keys='',values=''):
        try:

            if 'SSN' in doc_type:
                ssn_score,ssn_name_score,ssn_date_score=self.score.ssn_confidence(data,keys,values)
                self.confidence.put((ssn_score,ssn_name_score,ssn_date_score))
            elif 'Paystub' in doc_type:
                self.text, description, result, keys, values, texts = self.sp_location.get_text(
                    path)
                regular1_scrore, regular2_scrore, regular3_scrore, regular4_scrore, regular5_scrore, regular6_scrore, regular7_scrore, \
                regular8_scrore, regular9_scrore, regular10_scrore, tax1_scrore, tax2_scrore, tax3_scrore, tax4_scrore, tax5_scrore, \
                tax6_scrore, tax7_scrore, tax8_scrore, tax9_scrore, tax10_scrore, deduction1_scrore, deduction2_scrore, deduction3_scrore, \
                deduction4_scrore, deduction5_scrore, deduction6_scrore, deduction7_scrore, deduction8_scrore, deduction9_scrore, deduction10,deduction11_scrore,deduction12_scrore,deduction13_scrore,deduction14_scrore,deduction15_scrore, \
                pay_end_date_scrore, pay_start_date_scrore, pay_date_scrore,employee_address_scrore, employee_name_scrore, \
                employer_address_scrore, employer_name_scrore, other_scrore=self.score.paystub_confidence(data,keys,
                                                                                                          values)

                self.confidence.put((regular1_scrore,regular2_scrore,regular3_scrore,regular4_scrore,regular5_scrore,regular6_scrore,regular7_scrore,\
            regular8_scrore,regular9_scrore,regular10_scrore,tax1_scrore,tax2_scrore,tax3_scrore,tax4_scrore,tax5_scrore,\
            tax6_scrore,tax7_scrore,tax8_scrore,tax9_scrore,tax10_scrore,deduction1_scrore,deduction2_scrore,deduction3_scrore,\
            deduction4_scrore,deduction5_scrore,deduction6_scrore,deduction7_scrore,deduction8_scrore,deduction9_scrore,deduction10,deduction11_scrore,deduction12_scrore,deduction13_scrore,deduction14_scrore,deduction15_scrore,\
            pay_end_date_scrore,pay_start_date_scrore,pay_date_scrore,employee_address_scrore,employee_name_scrore,\
            employer_address_scrore,employer_name_scrore,other_scrore))

        except Exception as e:
            print(e)
    def get_license_response(self,data,response,conf_result,doc_type,zipcode,text,image_path,result,pdf_image_path):
        global detected_null_value_count, partial_not_detected, add, detected_value_count
        detected_value_count=0
        actual_value = list(data.keys())
        actual_value = sorted(actual_value)
        add_value = list(data.values())
        detected_null_value_count = add_value.count('')
        # print("detected_null_value_count value", detected_null_value_count, int(len(add_value) / 2))
        partial_not_detected, partial_detected = [], []

        for i in range(len(response['fields'])):
            for j in range(len(actual_value)):
                if response['fields'][i]['name'] == actual_value[j]:
                    response['fields'][i]['field_value_original'] = data[actual_value[j]]
                    pass
        if pdf_image_path=='':
            thread = threading.Thread(target=self.get_location, args=(data, image_path,doc_type,result))
        else:
            thread = threading.Thread(target=self.get_location,
                                      args=(data, pdf_image_path, doc_type, result))
        thread.setName("Location Thread")
        thread.start()
        (address_location, licence_id_location, dict_location, file_path1) = self.location.get()
        thread = threading.Thread(target=self.get_license_confidences,args=(data,text,conf_result,))
        thread.setName("Confidence Thread")
        thread.start()
        (date_dict, date_score, address_score, license_score, other_score) = self.get_license_confidence.get()
        reg = ''
        state_regex = re.findall(r"\b(!?AL|AK|AS|AZ|AŽ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE"
            r"|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)",zipcode)
        if state_regex != []:
            for i in range(len(self.state_value['data'])):
                if self.state_value['data'][i]['state'] in state_regex[0]:
                    reg = self.state_value['data'][i]['license_id']
                    # print("regex_state_value",self.state_value['data'][i]['state'],self.regex_value)
            print("state regex", reg)
        licence_id = re.findall(reg, self.text)
        if licence_id == []:
            print("in license details")
            license_score = 45
        for i in range(len(response['fields'])):

            if response['fields'][i]['name'] == "address":
                for key, value in address_location.items():
                    self.location_val.append(value)
                    if response['fields'][i]['field_value_original'] != '':
                        if key in response['fields'][i]['field_value_original']:
                            response['fields'][i]['location'] = str(list(self.location_val))
                            if self.config['field_level'] == "True":
                                if self.config['high_accuracy'][0] <= address_score <= \
                                        self.config['high_accuracy'][1]:
                                    response['fields'][i]['confidence'] = address_score
                                elif self.config['medium_accuracy'][0] <= address_score <= \
                                        self.config['medium_accuracy'][1]:
                                    response['fields'][i]['confidence'] = address_score
                                else:
                                    response['fields'][i]['field_value_original'] = ''
                            else:
                                response['fields'][i]['confidence'] = address_score

            elif response['fields'][i]['name'] == "license_id":
                self.location_val.clear()
                for key, value in licence_id_location.items():
                    # print("License key",key)
                    self.location_val.append(value)
                    if response['fields'][i]['field_value_original'] != '':
                        if key in response['fields'][i]['field_value_original']:
                            response['fields'][i]['location'] = str(list(self.location_val))
                            if self.config['field_level'] == "True":
                                if self.config['high_accuracy'][0] <= license_score <= \
                                        self.config['high_accuracy'][1]:
                                    response['fields'][i]['confidence'] = license_score
                                elif self.config['medium_accuracy'][0] <= license_score <= \
                                        self.config['medium_accuracy'][1]:
                                    response['fields'][i]['confidence'] = license_score
                                else:
                                    response['fields'][i]['field_value_original'] = ''
                            else:
                                response['fields'][i]['confidence'] = license_score

            elif response['fields'][i]['name'] == "dob":
                self.location_val.clear()
                for key, value in dict_location.items():
                    self.location_val.append(value)
                    if response['fields'][i]['field_value_original'] != '':
                        if key in response['fields'][i]['field_value_original']:
                            response['fields'][i]['location'] = str(list(self.location_val))
                            if self.config['field_level'] == "True":
                                if self.config['high_accuracy'][0] <= date_score <= \
                                        self.config['high_accuracy'][1]:
                                    response['fields'][i]['confidence'] = date_score
                                elif self.config['medium_accuracy'][0] <= date_score <= \
                                        self.config['medium_accuracy'][1]:
                                    response['fields'][i]['confidence'] = date_score
                                else:
                                    response['fields'][i]['field_value_original'] = ''
                            else:
                                response['fields'][i]['confidence'] = date_score

            elif response['fields'][i]['name'] == "first_name":
                self.location_val.clear()
                for key, value in dict_location.items():
                    self.location_val.append(value)
                    key = key.replace(',', '')
                    if response['fields'][i]['field_value_original'] is not "":
                        if key in response['fields'][i]['field_value_original']:
                            response['fields'][i]['location'] = str(self.location_val)
                            if self.config['field_level'] == "True":
                                if self.config['high_accuracy'][0] <= other_score <= \
                                        self.config['high_accuracy'][1]:
                                    response['fields'][i]['confidence'] = other_score + 2
                                elif self.config['medium_accuracy'][0] <= other_score <= \
                                        self.config['medium_accuracy'][1]:
                                    response['fields'][i]['confidence'] = other_score + 2
                                else:
                                    response['fields'][i]['field_value_original'] = ''
                            else:
                                response['fields'][i]['confidence'] = other_score + 2

            elif response['fields'][i]['name'] == "last_name":
                self.location_val.clear()
                for key, value in dict_location.items():
                    self.location_val.append(value)
                    key = key.replace(',', '')
                    if response['fields'][i]['field_value_original'] is not "":
                        if key in response['fields'][i]['field_value_original']:
                            response['fields'][i]['location'] = str(self.location_val)
                            if self.config['field_level'] == "True":
                                if self.config['high_accuracy'][0] <= other_score <= \
                                        self.config['high_accuracy'][1]:
                                    response['fields'][i]['confidence'] = other_score + 1
                                elif self.config['medium_accuracy'][0] <= other_score <= \
                                        self.config['medium_accuracy'][1]:
                                    response['fields'][i]['confidence'] = other_score + 1
                                else:
                                    response['fields'][i]['field_value_original'] = ''
                            else:
                                response['fields'][i]['confidence'] = other_score + 1

            elif response['fields'][i]['name'] == "middle_name":
                self.location_val.clear()
                for key, value in dict_location.items():
                    self.location_val.append(value)
                    key = key.replace(',', '')
                    if response['fields'][i]['field_value_original'] is not "":
                        if key in response['fields'][i]['field_value_original']:
                            response['fields'][i]['location'] = str(self.location_val)
                            if self.config['field_level'] == "True":
                                if self.config['high_accuracy'][0] <= other_score <= \
                                        self.config['high_accuracy'][1]:
                                    response['fields'][i]['confidence'] = other_score + 3
                                elif self.config['medium_accuracy'][0] <= other_score <= \
                                        self.config['medium_accuracy'][1]:
                                    response['fields'][i]['confidence'] = other_score + 3
                                else:
                                    response['fields'][i]['field_value_original'] = ''
                            else:
                                response['fields'][i]['confidence'] = other_score + 3

            elif response['fields'][i]['name'] == "issue_date":
                self.location_val.clear()
                for key, value in dict_location.items():
                    self.location_val.append(value)
                    if response['fields'][i]['field_value_original'] != '':
                        if key in response['fields'][i]['field_value_original']:
                            response['fields'][i]['location'] = str(list(self.location_val))
                            if self.config['field_level'] == "True":
                                if self.config['high_accuracy'][0] <= date_score <= \
                                        self.config['high_accuracy'][1]:
                                    response['fields'][i]['confidence'] = date_score
                                elif self.config['medium_accuracy'][0] <= date_score <= \
                                        self.config['medium_accuracy'][1]:
                                    response['fields'][i]['confidence'] = date_score
                                else:
                                    response['fields'][i]['field_value_original'] = ''
                            else:
                                response['fields'][i]['confidence'] = date_score

            elif response['fields'][i]['name'] == "expiration_date":
                self.location_val.clear()
                for key, value in dict_location.items():
                    self.location_val.append(value)
                    if response['fields'][i]['field_value_original'] != '':
                        if key in response['fields'][i]['field_value_original']:
                            response['fields'][i]['location'] = str(list(self.location_val))
                            if self.config['field_level'] == "True":
                                if self.config['high_accuracy'][0] <= date_score <= \
                                        self.config['high_accuracy'][1]:
                                    response['fields'][i]['confidence'] = date_score
                                elif self.config['medium_accuracy'][0] <= date_score <= \
                                        self.config['medium_accuracy'][1]:
                                    response['fields'][i]['confidence'] = date_score
                                else:
                                    response['fields'][i]['field_value_original'] = ''
                            else:
                                response['fields'][i]['confidence'] = date_score

            else:
                self.location_val.clear()
                for key, value in dict_location.items():
                    self.location_val.append(value)
                    key = key.replace(',', '')
                    if response['fields'][i]['field_value_original'] is not "":
                        if key in response['fields'][i]['field_value_original']:
                            response['fields'][i]['location'] = str(self.location_val)
                            if self.config['field_level'] == "True":
                                if self.config['high_accuracy'][0] <= other_score <= \
                                        self.config['high_accuracy'][1]:
                                    response['fields'][i]['confidence'] = other_score
                                elif self.config['medium_accuracy'][0] <= other_score <= \
                                        self.config['medium_accuracy'][1]:
                                    response['fields'][i]['confidence'] = other_score
                                else:
                                    response['fields'][i]['field_value_original'] = ''
                            else:
                                response['fields'][i]['confidence'] = other_score
        self.scan_result = response
        print(self.scan_result)
        for i in range(len(response['fields'])):
            if response['fields'][i]['field_value_original'] == '':
                detected_null_value_count = detected_null_value_count + 1
            else:
                detected_value_count = detected_value_count + 1
        identification_score = int((detected_value_count / len(response['fields'])) * 100)
        all_confidence_score = license_score + address_score + date_score + other_score
        document_score = int((all_confidence_score / 4))
        if identification_score > 100:
            identification_score = 100
        if 33 >= identification_score:
            self.scan_result[
                'error_msg'] = "Document upload was NOT successful due to unclear image or unrecognizable image; please [upload document again] or [rescan image].  Note: Please ensure that the full document is visible, and make sure there are no markings on the document that might be blocking any text or numbers.\n\n\tIdentication Score: " + str(
                identification_score) + "\n\n\tAccuracy Score: " + str(document_score)
            self.scan_result['status'] = "INCORRECT_DOCUMENT"

        if self.config['document_level'] == "True":
            if self.config['high_accuracy'][0] <= document_score <= self.config['high_accuracy'][1]:
                self.scan_result[
                    'error_msg'] = "Document upload successful; please review information before proceeding to next step.\n\n\tIdentication Score: " + str(
                    identification_score) + "\n\n\tAccuracy Score: " + str(document_score)
                self.scan_result["status"] = "SUCCESSFUL"
            elif self.config['medium_accuracy'][0] <= document_score <= \
                    self.config['medium_accuracy'][1]:
                self.scan_result[
                    'error_msg'] = "Document upload successful, but some information may not have been read correctly; please review any fields in [orange] carefully and make any appropriate corrections before proceeding to next step \n\n\tIdentication Score: " + str(
                    identification_score) + "\n\n\tAccuracy Score: " + str(document_score)
                self.scan_result['status'] = "PARTIAL_DETECTION"
            else:
                self.scan_result[
                    'error_msg'] = "Document upload was NOT successful due to unclear image or unrecognizable image; please [upload document again] or [rescan image].  Note: Please ensure that the full document is visible, and make sure there are no markings on the document that might be blocking any text or numbers. \n\n\tIdentication Score: " + str(
                    identification_score) + "\n\n\tAccuracy Score: " + str(document_score)
                self.scan_result['status'] = "INCORRECT_DOCUMENT"
        else:

            if detected_null_value_count != 0:
                # print("in If statement")
                for key, value in data.items():
                    if value == '' or value == ' ':
                        partial_not_detected.append(key)

                    else:
                        partial_detected.append(key)
                for i in range(len(partial_not_detected)):
                    if partial_not_detected[i] == 'first_name':
                        partial_not_detected[i] = partial_not_detected[i].replace('first_name',
                                                                                  "First Name")

                    elif partial_not_detected[i] == 'last_name':
                        partial_not_detected[i] = partial_not_detected[i].replace('last_name',
                                                                                  "Last Name")

                    elif partial_not_detected[i] == 'middle_name':
                        partial_not_detected[i] = partial_not_detected[i].replace('middle_name',
                                                                                  "Middle Name")

                    elif partial_not_detected[i] == 'address':
                        partial_not_detected[i] = partial_not_detected[i].replace('address',
                                                                                  "Address")

                    elif partial_not_detected[i] == 'zipcode':
                        partial_not_detected[i] = partial_not_detected[i].replace('zipcode',
                                                                                  "Zipcode")

                    elif partial_not_detected[i] == 'city':
                        partial_not_detected[i] = partial_not_detected[i].replace('city', "City")

                    elif partial_not_detected[i] == 'state':
                        partial_not_detected[i] = partial_not_detected[i].replace('state', "State")

                    elif partial_not_detected[i] == 'dob':
                        partial_not_detected[i] = partial_not_detected[i].replace('dob',
                                                                                  "Date of Birth")

                    elif partial_not_detected[i] == 'issue_date':
                        partial_not_detected[i] = partial_not_detected[i].replace('issue_date',
                                                                                  "Issue Date")

                    elif partial_not_detected[i] == 'expiration_date':
                        partial_not_detected[i] = partial_not_detected[i].replace('expiration_date',
                                                                                  "Expiry Date")

                    elif partial_not_detected[i] == 'license_id':
                        partial_not_detected[i] = partial_not_detected[i].replace('license_id',
                                                                                  "License Id")

                self.scan_result[
                    'error_msg'] = "Document upload successful, but some information may not have been read correctly; please review any fields in [orange] carefully and make any appropriate corrections before proceeding to next step \n\n\tIdentication Score: " + str(
                    identification_score) + "\n\n\tAccuracy Score: " + str(document_score)
                # self.scan_result['error_msg'] = "Field(s) Not Detected: "+",".join(map(str,partial_not_detected))

                self.scan_result['status'] = "PARTIAL_DETECTION"
            else:
                self.scan_result[
                    'error_msg'] = "Document upload successful; please review information before proceeding to next step. \n\n\tIdentication Score: " + str(
                    identification_score) + "\n\n\tAccuracy Score: " + str(document_score)
                self.scan_result["status"] = "SUCCESSFUL"
        file_path = file_path1
        return self.scan_result,file_path
        # self.get_response.put((self.scan_result,file_path))
    def all_details(self, response):

        global text, detected_null_value_count
        try:
            detected_value_count=0
            f_path=''
            file_path=''
            doc_id = int(response['doc_id'])
            application_id=response['application_id']
            url = self.config['base_url'] + response['file_path']
            url=url.replace(" ","%20")

            image_on_web = urlopen(url)
            filename = os.path.basename(url)
            if re.search(r'(!?(&|!|@|#|\$|\^|\*))',filename):
                filename=filename.replace(re.findall(r'(!?(&|!|@|#|\$|\^|\*))',filename)[0],"")
            buf = image_on_web.read()
            with open("../images/documents_upload/" + filename, "wb") as downloaded_image:
                downloaded_image.write(buf)
                downloaded_image.close()
                image_on_web.close()

            r = requests.post(self.config['base_url']+'/getAllDocumentsMaster')
            resp_dict = json.loads(json.dumps(r.json()))
            c = requests.post(self.config['base_url'] + '/getAccuracyBands')
            confidence_band = json.loads(json.dumps(c.json()))
            value = resp_dict.get('records')
            json_val = dict([(value[i]['id'], value[i]['name']) for i in range(len(value))])
            if 'License' in json_val[doc_id]:
                data={}
                thread = threading.Thread(target=self.get_license_all_details,args=("../images/documents_upload/" + filename,))
                thread.start()
                (text_response, licence_id, expiry_date, dob, issue_date, address, name, state, zipcode, city, date_val,result,pdf_image_path)=self.get_license_details.get()
                if licence_id ==' ' and expiry_date =='' and dob =='' and issue_date =='' and address =='' and name =='' and state =='' and zipcode =='' and city =='' and date_val:
                    self.scan_result[
                        'error_msg'] = "Document upload was NOT successful due to unclear image or unrecognizable image; please [upload document again] or [rescan image].  Note: Please ensure that the full document is visible, and make sure there are no markings on the document that might be blocking any text or numbers."
                    self.scan_result['status'] = "INCORRECT_DOCUMENT"
                if name == '':
                    self.name_value.append(' ')
                    self.name_value.append(' ')
                    self.name_value.append(' ')
                else:
                    self.name_value = name.split()
                    if state.lower() == 'nj':
                        name_val=name.split()
                        if len(name_val)==2:
                            if re.search(r'\b(!?[A-Za-z]+\s[A-Za-z])\b', name):
                                self.name_value.clear()
                                self.name_value.append(' ')
                                self.name_value.append(name_val[0])
                                self.name_value.append(name_val[1])

                        else:
                            pass
                    # if self.name_value
                    if re.search('(!?JR|Jr|jr|jR)', name):
                        if self.name_value.index(re.findall(r'(!?JR|Jr|jr|jR)', name)[0]) == 1:
                            self.name_value[1] = self.name_value[1] + " " + self.name_value[2]
                            self.name_value.pop(2)
                        elif self.name_value.index(re.findall('(!?JR|Jr|jr|jR)', name)[0]) == 3:
                            self.name_value[2] = self.name_value[2] + " " + self.name_value[3]
                            self.name_value.pop(3)
                    print(self.name_value)
                print("len of name", len(self.name_value))
                name_seq = ''

                for i in range(len(self.state_value['data'])):
                    if self.state_value['data'][i]['state'] == state:
                        name_seq = self.state_value['data'][i]['name_seq']
                if len(self.name_value) == 0:
                    data = {'first_name': "", 'dob': dob, 'issue_date': issue_date,
                           'expiration_date': expiry_date,
                           'last_name': "", 'address': address, 'license_id': licence_id,
                           "middle_name": "", "state": state, "postal_code": zipcode, "city": city,
                           "date_val": date_val}
                elif len(self.name_value) == 1:
                    data = {'first_name': "", 'dob': dob, 'issue_date': issue_date,
                           'expiration_date': expiry_date,
                           'last_name': self.name_value[0], 'address': address, 'license_id': licence_id,
                           "middle_name": "", "state": state, "postal_code": zipcode, "city": city,
                           "date_val": date_val}
                elif 'FN_MN_LN_SUF' == name_seq:
        
                    if len(self.name_value) == 3:
                        data = {'first_name': self.name_value[0], 'dob': dob, 'issue_date': issue_date,
                               'expiration_date': expiry_date,
                               'last_name': self.name_value[2], 'address': address,
                               'license_id': licence_id,
                               "middle_name": self.name_value[1], "state": state, "postal_code": zipcode,
                               "city": city, "date_val": date_val}
                    elif len(self.name_value) == 4:
                        data = {'first_name': self.name_value[0], 'dob': dob, 'issue_date': issue_date,
                               'expiration_date': expiry_date,
                               'last_name': self.name_value[2] + " " + self.name_value[3],
                               'address': address, 'license_id': licence_id,
                               "middle_name": self.name_value[1], "state": state, "postal_code": zipcode,
                               "city": city, "date_val": date_val}
                    else:
                        data = {'first_name': self.name_value[0], 'dob': dob, 'issue_date': issue_date,
                               'expiration_date': expiry_date, 'last_name': self.name_value[1],
                               'address': address,
                               'license_id': licence_id, "middle_name": '', "state": state,
                               "postal_code": zipcode, "city": city, "date_val": date_val}
                elif 'LN_FN_MN_SUF' == name_seq:
                    if len(self.name_value) == 3:
                        data = {'first_name': self.name_value[1], 'dob': dob,
                               'issue_date': issue_date, 'expiration_date': expiry_date,
                               'last_name': self.name_value[0], 'address': address,
                               'license_id': licence_id,
                               "middle_name": self.name_value[2], "state": state,
                               "postal_code": zipcode, "city": city, "date_val": date_val}
                    elif len(self.name_value) == 4:
                        data = {'first_name': self.name_value[1], 'dob': dob,
                               'issue_date': issue_date, 'expiration_date': expiry_date,
                               'last_name': self.name_value[0], 'address': address,
                               'license_id': licence_id,
                               "middle_name": self.name_value[2] + " " + self.name_value[3], "state": state,
                               "postal_code": zipcode, "city": city,
                               "date_val": date_val}
                    else:
                        data = {'first_name': self.name_value[1], 'dob': dob,
                               'issue_date': issue_date,
                               'expiration_date': expiry_date, 'last_name': self.name_value[0],
                               'address': address,
                               'license_id': licence_id, "middle_name": '', "state": state,
                               "postal_code": zipcode, "city": city, "date_val": date_val}
                text,conf_result=self.lic.get_word_confidence(text_response)
                self.text=text
                self.scan_result, file_path1=self.get_license_response(data,response,conf_result,json_val[doc_id],zipcode,text,"../images/documents_upload/" + filename,result,pdf_image_path)

            elif 'SSN' in json_val[doc_id]:
                flag = False
                if filename.rsplit('.', 1)[1] == 'pdf':
                    thread = threading.Thread(target=self.image_to_pdf,
                                              args=("../images/documents_upload/" + filename,
                                                    json_val[doc_id],))
                    thread.start()
                    path = self.img2pdf.get()
                    name_file = os.path.basename(path)
                    f_path = "../images/documents_upload/" + name_file
                    thread = threading.Thread(target=self.image_processing_threading,
                                              args=(f_path, json_val[doc_id],))
                else:
                    thread = threading.Thread(target=self.image_processing_threading,args=("../images/documents_upload/" + filename,json_val[doc_id],))
                thread.start()
                image_path = self.image_processing.get()
                thread = threading.Thread(target=self.get_doc, args=(
                "../images/documents_upload/" + filename, json_val[doc_id],))
                thread.start()
                (self.text, SSN_Number, name, date, conf_keys, conf_values) = self.scan_text.get()
                if SSN_Number == '' or name == '' or date == '':
                    file_path = ''
                    self.scan_result['error_msg'] = "Incorrect Document or Unable to Scan"
                    self.scan_result['status'] = "INCORRECT_DOCUMENT"
                    # print(self.scan_result)
                    return self.scan_result, file_path
                else:
                    actual_name = name.split()
                    if len(actual_name) > 3:
                        actual_name.pop(0)
                    # print("self.name_value", self.name_value)
                    add = {}
                    if len(actual_name) == 1:
                        add = {"ssn_number": SSN_Number, "ssn_firstname": '',
                               "ssn_lastname":
                                   '', "ssn_middlename": '', 'ssn_date': date,
                               'ssn_name': ""}
                    if len(actual_name) == 2:
                        add = {"ssn_number": SSN_Number, "ssn_firstname": actual_name[0],
                               "ssn_lastname":
                                   actual_name[1], "ssn_middlename": '', 'ssn_date': date,
                               'ssn_name': ""}
                    elif len(actual_name) == 3:
                        add = {"ssn_number": SSN_Number, "ssn_firstname": actual_name[0],
                               "ssn_lastname":
                                   actual_name[2], "ssn_middlename": actual_name[1],
                               'ssn_date': date, 'ssn_name': ""}

                    actual_value = list(add.keys())
                    actual_value = sorted(actual_value)

                    for i in range(len(response['fields'])):
                        for j in range(len(actual_value)):
                            if response['fields'][i]['name'] == actual_value[j]:
                                response['fields'][i]['field_value_original'] = add[actual_value[j]]
                                pass

                    thread = threading.Thread(target=self.get_ssn_pay_location, args=(add, image_path, json_val[doc_id],))
                    thread.start()
                    (ssn_number_location, name_location, date_location,file_path1) = self.location.get()

                    thread = threading.Thread(target=self.confidence_score, args=(image_path, json_val[doc_id], add, conf_keys, conf_values,))
                    thread.start()
                    (ssn_score, ssn_name_score, ssn_date_score) = self.confidence.get()
                    print(type(ssn_score))
                    for i in range(len(response['fields'])):

                        if response['fields'][i]['name'] == "ssn_number":
                            self.location_val.clear()
                            for key, value in ssn_number_location.items():
                                self.location_val.append(value)
                                if key in response['fields'][i]['field_value_original']:
                                    response['fields'][i]['location'] = str([self.location_val])
                                    if self.config['field_level'] == "True":
                                        if self.config['high_accuracy'][0] <= int(ssn_score) <= \
                                                self.config['high_accuracy'][1]:
                                            response['fields'][i]['confidence'] = ssn_score
                                        elif self.config['medium_accuracy'][0] <= int(ssn_score) <= \
                                                self.config['medium_accuracy'][1]:
                                            response['fields'][i]['confidence'] = ssn_score
                                        else:
                                            response['fields'][i]['field_value_original'] = ''
                                    else:
                                        response['fields'][i]['confidence'] = ssn_score
                        elif response['fields'][i]['name'] == "ssn_date":
                            self.location_val.clear()
                            for key, value in date_location.items():
                                self.location_val.append(value)
                                if key in response['fields'][i]['field_value_original']:
                                    response['fields'][i]['location'] = str([self.location_val])
                                    if self.config['field_level'] == "True":
                                        if self.config['high_accuracy'][0] <= int(ssn_date_score) <= \
                                                self.config['high_accuracy'][1]:
                                            response['fields'][i]['confidence'] = ssn_date_score
                                        elif self.config['medium_accuracy'][0] <= int(ssn_date_score) <= \
                                                self.config['medium_accuracy'][1]:
                                            response['fields'][i]['confidence'] = ssn_date_score
                                        else:
                                            response['fields'][i]['field_value_original'] = ''
                                    else:
                                        response['fields'][i]['confidence'] = ssn_date_score
                        else:
                            self.location_val.clear()
                            for key, value in name_location.items():
                                self.location_val.append(value)
                                if key in response['fields'][i]['field_value_original']:
                                    response['fields'][i]['location'] = str([self.location_val])
                                    if self.config['field_level'] == "True":
                                        if self.config['high_accuracy'][0] <= int(ssn_name_score) <= \
                                                self.config['high_accuracy'][1]:
                                            response['fields'][i]['confidence'] = ssn_name_score
                                        elif self.config['medium_accuracy'][0] <= int(ssn_name_score) <= \
                                                self.config['medium_accuracy'][1]:
                                            response['fields'][i]['confidence'] = ssn_name_score
                                        else:
                                            response['fields'][i]['field_value_original'] = ''
                                    else:
                                        response['fields'][i]['confidence'] = ssn_name_score
                self.scan_result = response
                print(self.scan_result)
                for i in range(len(response['fields'])):
                    if response['fields'][i]['field_value_original'] == '':
                        detected_null_value_count = detected_null_value_count + 1
                    else:
                        detected_value_count = detected_value_count + 1
                identification_score = int((detected_value_count / len(response['fields'])) * 100)
                all_confidence_score = int(ssn_score) + int(ssn_name_score) + int(ssn_date_score)
                document_score = int((all_confidence_score / 3))
                if identification_score > 100:
                    identification_score = 100
                if 33 >= identification_score:
                    self.scan_result[
                        'error_msg'] = "Document upload was NOT successful due to unclear image or unrecognizable image; please [upload document again] or [rescan image].  Note: Please ensure that the full document is visible, and make sure there are no markings on the document that might be blocking any text or numbers.\n\n\tIdentication Score: " + str(
                        identification_score) + "\n\n\tAccuracy Score: " + str(document_score)
                    self.scan_result['status'] = "INCORRECT_DOCUMENT"

                if self.config['document_level'] == "True":
                    if self.config['high_accuracy'][0] <= document_score <= \
                            self.config['high_accuracy'][1]:
                        self.scan_result[
                            'error_msg'] = "Document upload successful; please review information before proceeding to next step.\n\n\tIdentication Score: " + str(
                            identification_score) + "\n\n\tAccuracy Score: " + str(document_score)
                        self.scan_result["status"] = "SUCCESSFUL"
                    elif self.config['medium_accuracy'][0] <= document_score <= \
                            self.config['medium_accuracy'][1]:
                        self.scan_result[
                            'error_msg'] = "Document upload successful, but some information may not have been read correctly; please review any fields in [orange] carefully and make any appropriate corrections before proceeding to next step \n\n\tIdentication Score: " + str(
                            identification_score) + "\n\n\tAccuracy Score: " + str(document_score)
                        self.scan_result['status'] = "PARTIAL_DETECTION"
                    else:
                        self.scan_result[
                            'error_msg'] = "Document upload was NOT successful due to unclear image or unrecognizable image; please [upload document again] or [rescan image].  Note: Please ensure that the full document is visible, and make sure there are no markings on the document that might be blocking any text or numbers. \n\n\tIdentication Score: " + str(
                            identification_score) + "\n\n\tAccuracy Score: " + str(document_score)
                        self.scan_result['status'] = "INCORRECT_DOCUMENT"
                else:
                    partial_not_detected, partial_detected = [], []
                    if detected_null_value_count != 0:
                        # print("in If statement")
                        for key, value in add.items():
                            if value == '' or value == ' ':
                                partial_not_detected.append(key)

                            else:
                                partial_detected.append(key)
                        for i in range(len(partial_not_detected)):
                            if partial_not_detected[i] == 'ssn_number':
                                partial_not_detected[i] = partial_not_detected[i].replace(
                                    'ssn_number',
                                    "Social Security Number")

                            elif partial_not_detected[i] == 'ssn_lastname':
                                partial_not_detected[i] = partial_not_detected[i].replace(
                                    'ssn_lastname',
                                    "Last Name")

                            elif partial_not_detected[i] == 'ssn_middlename':
                                partial_not_detected[i] = partial_not_detected[i].replace(
                                    'ssn_middlename',
                                    "Middle Name")
                            elif partial_not_detected[i] == 'ssn_firstname':
                                partial_not_detected[i] = partial_not_detected[i].replace(
                                    'ssn_firstname',
                                    "First Name")



                        self.scan_result[
                            'error_msg'] = "Document upload successful, but some information may not have been read correctly; please review any fields in [orange] carefully and make any appropriate corrections before proceeding to next step \n\n\tIdentication Score: " + str(
                            identification_score) + "\n\n\tAccuracy Score: " + str(document_score)
                        # self.scan_result['error_msg'] = "Field(s) Not Detected: "+",".join(map(str,partial_not_detected))

                        self.scan_result['status'] = "PARTIAL_DETECTION"
                    else:
                        self.scan_result[
                            'error_msg'] = "Document upload successful; please review information before proceeding to next step. \n\n\tIdentication Score: " + str(
                            identification_score) + "\n\n\tAccuracy Score: " + str(document_score)
                        self.scan_result["status"] = "SUCCESSFUL"
            elif 'Paystub' in json_val[doc_id]:
                if filename.rsplit('.', 1)[1] == 'pdf':
                    thread = threading.Thread(target=self.image_to_pdf,
                                              args=("../images/documents_upload/" + filename,
                                                    json_val[doc_id],))
                    thread.start()
                    path = self.img2pdf.get()
                    name_file = os.path.basename(path)
                    f_path = "../images/documents_upload/" + name_file
                    thread = threading.Thread(target=self.get_doc_text,
                                              args=(f_path, json_val[doc_id],))

                else:
                    f_path = "../images/documents_upload/" + filename
                    thread = threading.Thread(target=self.get_doc_text, args=(
                    "../images/documents_upload/" + filename, json_val[doc_id],))
                thread.start()
                (
                self.text, employer_full_address, employer_street, employer_state, employer_zipcode,
                employer_city, employee_full_address, employee_street, employee_state,
                employee_zipcode, employee_city, start_date, pay_frequency, string_date_value,
                employer_name, employee_name, current_gross_pay, ytd_gross_pay, current_net_pay,
                ytd_net_pay, taxes, current_taxes, ytd_taxes, rate_taxes, hrs_taxes, earnings,
                current_earnings, ytd_earnings, rate_regular, hrs_regular, pre_deduction,
                current_pre_deduction, ytd_pre_deduction, rate_pre_deduction, hrs_pre_deduction,
                post_deduction, current_post_deduction, ytd_post_deduction, rate_post_deduction,
                hrs_post_deduction, total_calculated_taxes, current_total_calculated_taxes,
                ytd_total_calculated_taxes, hrs_total_calculated_taxes, rate_total_calculated_taxes,
                total_calculated_regular, current_total_calculated_regular,
                ytd_total_calculated_regular, hrs_total_calculated_regular,
                rate_total_calculated_regular, total_calculated_pre, current_total_calculated_pre,
                ytd_total_calculated_pre, hrs_total_calculated_pre, rate_total_calculated_pre,
                total_calculated_post, current_total_calculated_post, ytd_total_calculated_post,
                hrs_total_calculated_post, rate_total_calculated_post, total_taxes,
                current_total_taxes, ytd_total_taxes, hrs_total_taxes, rate_total_taxes,
                total_regular, current_total_regular, ytd_total_regular, hrs_total_regular,
                rate_total_regular, total_pre, current_total_pre, ytd_total_pre, hrs_total_pre,
                rate_total_pre, total_post, current_total_post, ytd_total_post, hrs_total_post,
                rate_total_post, employment_Start_date, pay_date, position,result1) = self.doc_text.get()
                if current_gross_pay == '' and current_net_pay == '' and pay_frequency == '' and employee_full_address == '' and employer_full_address == '' and employee_name == '' and employee_city == '' and employee_state == '' and employer_name == '' and employer_city == '' and employer_state == '' and start_date == '':
                    file_path = ''
                    self.scan_result['error_msg'] = "Incorrect Document or Unable to Scan"
                    self.scan_result['status'] = "INCORRECT_DOCUMENT"
                    return self.scan_result, file_path


                else:
                    name_value = employee_name.split()
                    if name_value == []:
                        name_value.append('')
                        name_value.append('')
                        name_value.append('')
                    if len(name_value) == 2:
                        name_value.append(name_value[1])
                        name_value[1] = ''
                    pra=prb=prc=prd=pre=poa=pob=poc=pod=f=g=h=b = c = d = e =j = k = l = m = n = o = p = q = r = s = t = u = v=x=y=z=0

                    for i in range(len(response['fields'])):
                        if 'regular_earn' in response['fields'][i]['name']:
                            for a in range(len(earnings)):
                                if self.regular_earnings[b].lower() in earnings[a].lower():
                                    response['fields'][i]['alias'] = earnings[a]
                                    response['fields'][i]['field_value_original'] = \
                                    current_earnings[a]
                                    response['fields'][i]['optional_value'] = ytd_earnings[a]
                                    response['fields'][i]['hrs'] = hrs_regular[a]
                                    response['fields'][i]['rates'] = rate_regular[a]
                                    earnings.pop(a)
                                    current_earnings.pop(a)
                                    ytd_earnings.pop(a)
                                    hrs_regular.pop(a)
                                    rate_regular.pop(a)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''

                            b = b + 1
                        elif 'regular_bonus' in response['fields'][i]['name']:
                            for a in range(len(earnings)):

                                if self.Bonus[c].lower() in earnings[a].lower():
                                    response['fields'][i]['alias'] = earnings[a]
                                    response['fields'][i]['field_value_original'] = \
                                    current_earnings[a]
                                    response['fields'][i]['optional_value'] = ytd_earnings[a]
                                    response['fields'][i]['hrs'] = hrs_regular[a]
                                    response['fields'][i]['rates'] = rate_regular[a]
                                    earnings.pop(a)
                                    current_earnings.pop(a)
                                    ytd_earnings.pop(a)
                                    hrs_regular.pop(a)
                                    rate_regular.pop(a)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''
                            c = c + 1
                        elif 'regular_vacation' in response['fields'][i]['name']:
                            for w in range(len(earnings)):

                                if self.Vacation[d].lower() in earnings[w].lower():
                                    response['fields'][i]['alias'] = earnings[w]
                                    response['fields'][i]['field_value_original'] = \
                                    current_earnings[w]
                                    response['fields'][i]['optional_value'] = ytd_earnings[w]
                                    response['fields'][i]['hrs'] = hrs_regular[w]
                                    response['fields'][i]['rates'] = rate_regular[w]
                                    earnings.pop(w)
                                    current_earnings.pop(w)
                                    ytd_earnings.pop(w)
                                    hrs_regular.pop(w)
                                    rate_regular.pop(w)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''
                            d = d + 1
                        elif 'regular_overtime' in response['fields'][i]['name']:
                            for a in range(len(earnings)):

                                if self.Overtime[e].lower() in earnings[a].lower():
                                    response['fields'][i]['alias'] = earnings[a]
                                    response['fields'][i]['field_value_original'] = \
                                    current_earnings[a]
                                    response['fields'][i]['optional_value'] = ytd_earnings[a]
                                    response['fields'][i]['hrs'] = hrs_regular[a]
                                    response['fields'][i]['rates'] = rate_regular[a]
                                    earnings.pop(a)
                                    current_earnings.pop(a)
                                    ytd_earnings.pop(a)
                                    hrs_regular.pop(a)
                                    rate_regular.pop(a)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''
                            e = e + 1
                        elif 'regular_commision' in response['fields'][i]['name']:
                            for a in range(len(earnings)):

                                if self.commission[f].lower() in earnings[a].lower():
                                    response['fields'][i]['alias'] = earnings[a]
                                    response['fields'][i]['field_value_original'] = \
                                    current_earnings[a]
                                    response['fields'][i]['optional_value'] = ytd_earnings[a]
                                    response['fields'][i]['hrs'] = hrs_regular[a]
                                    response['fields'][i]['rates'] = rate_regular[a]
                                    earnings.pop(a)
                                    current_earnings.pop(a)
                                    ytd_earnings.pop(a)
                                    hrs_regular.pop(a)
                                    rate_regular.pop(a)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''
                            f = f + 1

                        elif 'tax_federal' in response['fields'][i]['name']:
                            for a in range(len(taxes)):

                                if self.federal_taxes[f].lower() in taxes[a].lower():
                                    response['fields'][i]['alias'] = taxes[a]
                                    response['fields'][i]['field_value_original'] = current_taxes[a]
                                    response['fields'][i]['optional_value'] = ytd_taxes[a]
                                    response['fields'][i]['hrs'] = hrs_taxes[a]
                                    response['fields'][i]['rates'] = rate_taxes[a]
                                    taxes.pop(a)
                                    current_taxes.pop(a)
                                    ytd_taxes.pop(a)
                                    hrs_taxes.pop(a)
                                    rate_taxes.pop(a)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''
                            f = f + 1
                            # if response['fields'][i]['field_value_original']=='':
                            #     f=0
                            #     for a in range(len(pre_deduction)):
                            #
                            #         if self.federal_taxes[f].lower() in pre_deduction[a].lower():
                            #             response['fields'][i]['alias'] = pre_deduction[a]
                            #             response['fields'][i]['field_value_original'] = current_pre_deduction[a]
                            #             response['fields'][i]['optional_value'] =ytd_pre_deduction[a]
                            #             response['fields'][i]['hrs'] = hrs_pre_deduction[a]
                            #             response['fields'][i]['rates'] = rate_pre_deduction[a]
                            #             taxes.pop(a)
                            #             break
                            #         else:
                            #             response['fields'][i]['alias'] = ''
                            #             response['fields'][i]['field_value_original'] = ''
                            #             response['fields'][i]['optional_value'] = ''
                            #             response['fields'][i]['hrs'] = ''
                            #             response['fields'][i]['rates'] = ''
                            #     f = f + 1
                            # if response['fields'][i]['field_value_original']=='':
                            #     f=0
                            #     for a in range(len(post_deduction)):
                            #
                            #         if self.federal_taxes[f].lower() in post_deduction[a].lower():
                            #             response['fields'][i]['alias'] = post_deduction[a]
                            #             response['fields'][i]['field_value_original'] = current_post_deduction[a]
                            #             response['fields'][i]['optional_value'] =ytd_post_deduction[a]
                            #             response['fields'][i]['hrs'] = hrs_post_deduction[a]
                            #             response['fields'][i]['rates'] = rate_post_deduction[a]
                            #             taxes.pop(a)
                            #             break
                            #         else:
                            #             response['fields'][i]['alias'] = ''
                            #             response['fields'][i]['field_value_original'] = ''
                            #             response['fields'][i]['optional_value'] = ''
                            #             response['fields'][i]['hrs'] = ''
                            #             response['fields'][i]['rates'] = ''
                            #     f = f + 1
                        elif 'tax_state' in response['fields'][i]['name']:
                            for a in range(len(taxes)):

                                if self.State[g].lower() in taxes[a].lower():
                                    response['fields'][i]['alias'] = taxes[a]
                                    response['fields'][i]['field_value_original'] = current_taxes[a]
                                    response['fields'][i]['optional_value'] = ytd_taxes[a]
                                    response['fields'][i]['hrs'] = hrs_taxes[a]
                                    response['fields'][i]['rates'] = rate_taxes[a]
                                    taxes.pop(a)
                                    current_taxes.pop(a)
                                    ytd_taxes.pop(a)
                                    hrs_taxes.pop(a)
                                    rate_taxes.pop(a)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''
                            g = g + 1
                        elif 'tax_city' in response['fields'][i]['name']:
                            for a in range(len(taxes)):

                                if self.City[h].lower() in taxes[a].lower():
                                    response['fields'][i]['alias'] = taxes[a]
                                    response['fields'][i]['field_value_original'] = current_taxes[a]
                                    response['fields'][i]['optional_value'] = ytd_taxes[a]
                                    response['fields'][i]['hrs'] = hrs_taxes[a]
                                    response['fields'][i]['rates'] = rate_taxes[a]
                                    taxes.pop(a)
                                    current_taxes.pop(a)
                                    ytd_taxes.pop(a)
                                    hrs_taxes.pop(a)
                                    rate_taxes.pop(a)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''
                            h = h + 1
                        elif 'tax_medicare' in response['fields'][i]['name']:
                            for a in range(len(taxes)):

                                if self.Medicare[v].lower() in taxes[a].lower():
                                    response['fields'][i]['alias'] = taxes[a]
                                    response['fields'][i]['field_value_original'] = current_taxes[a]
                                    response['fields'][i]['optional_value'] = ytd_taxes[a]
                                    response['fields'][i]['hrs'] = hrs_taxes[a]
                                    response['fields'][i]['rates'] = rate_taxes[a]
                                    taxes.pop(a)
                                    current_taxes.pop(a)
                                    ytd_taxes.pop(a)
                                    hrs_taxes.pop(a)
                                    rate_taxes.pop(a)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''
                            v = v + 1
                        elif 'tax_ss' in response['fields'][i]['name']:
                            for a in range(len(taxes)):

                                if self.SSI[x].lower() in taxes[a].lower():
                                    response['fields'][i]['alias'] = taxes[a]
                                    response['fields'][i]['field_value_original'] = current_taxes[a]
                                    response['fields'][i]['optional_value'] = ytd_taxes[a]
                                    response['fields'][i]['hrs'] = hrs_taxes[a]
                                    response['fields'][i]['rates'] = rate_taxes[a]
                                    taxes.pop(a)
                                    current_taxes.pop(a)
                                    ytd_taxes.pop(a)
                                    hrs_taxes.pop(a)
                                    rate_taxes.pop(a)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''
                            x = x + 1
                        elif 'tax_di' in response['fields'][i]['name']:
                            for a in range(len(taxes)):

                                if self.tax_di[y].lower() in taxes[a].lower():
                                    response['fields'][i]['alias'] = taxes[a]
                                    response['fields'][i]['field_value_original'] = current_taxes[a]
                                    response['fields'][i]['optional_value'] = ytd_taxes[a]
                                    response['fields'][i]['hrs'] = hrs_taxes[a]
                                    response['fields'][i]['rates'] = rate_taxes[a]
                                    taxes.pop(a)
                                    current_taxes.pop(a)
                                    ytd_taxes.pop(a)
                                    hrs_taxes.pop(a)
                                    rate_taxes.pop(a)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''
                            y = y + 1
                        elif 'tax_oasdi' in response['fields'][i]['name']:
                            for a in range(len(taxes)):

                                if self.tax_oasdi[z].lower() in taxes[a].lower():
                                    response['fields'][i]['alias'] = taxes[a]
                                    response['fields'][i]['field_value_original'] = current_taxes[a]
                                    response['fields'][i]['optional_value'] = ytd_taxes[a]
                                    response['fields'][i]['hrs'] = hrs_taxes[a]
                                    response['fields'][i]['rates'] = rate_taxes[a]
                                    taxes.pop(a)
                                    current_taxes.pop(a)
                                    ytd_taxes.pop(a)
                                    hrs_taxes.pop(a)
                                    rate_taxes.pop(a)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''
                            z = z + 1

                        elif 'pre_deduction_401k' in response['fields'][i]['name']:
                            for a in range(len(pre_deduction)):

                                if self.pre_duction_K[pra].lower() in pre_deduction[a].lower():
                                    response['fields'][i]['alias'] = pre_deduction[a]
                                    response['fields'][i]['field_value_original'] = \
                                    current_pre_deduction[a]
                                    response['fields'][i]['optional_value'] = ytd_pre_deduction[a]
                                    response['fields'][i]['hrs'] = hrs_pre_deduction[a]
                                    response['fields'][i]['rates'] = rate_pre_deduction[a]
                                    pre_deduction.pop(a)
                                    current_pre_deduction.pop(a)
                                    ytd_pre_deduction.pop(a)
                                    hrs_pre_deduction.pop(a)
                                    rate_pre_deduction.pop(a)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''

                            pra = pra + 1
                        elif 'pre_deduction_medical' in response['fields'][i]['name']:
                            for a in range(len(pre_deduction)):

                                if self.pre_duction_medicare[prb].lower() in pre_deduction[
                                    a].lower():
                                    response['fields'][i]['alias'] = pre_deduction[a]
                                    response['fields'][i]['field_value_original'] = \
                                    current_pre_deduction[a]
                                    response['fields'][i]['optional_value'] = ytd_pre_deduction[a]
                                    response['fields'][i]['hrs'] = hrs_pre_deduction[a]
                                    response['fields'][i]['rates'] = rate_pre_deduction[a]
                                    pre_deduction.pop(a)
                                    current_pre_deduction.pop(a)
                                    ytd_pre_deduction.pop(a)
                                    hrs_pre_deduction.pop(a)
                                    rate_pre_deduction.pop(a)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''

                            prb = prb + 1
                        elif 'pre_deduction_vision' in response['fields'][i]['name']:
                            for a in range(len(pre_deduction)):

                                if self.pre_duction_vision[prc].lower() in pre_deduction[a].lower():
                                    response['fields'][i]['alias'] = pre_deduction[a]
                                    response['fields'][i]['field_value_original'] = \
                                    current_pre_deduction[a]
                                    response['fields'][i]['optional_value'] = ytd_pre_deduction[a]
                                    response['fields'][i]['hrs'] = hrs_pre_deduction[a]
                                    response['fields'][i]['rates'] = rate_pre_deduction[a]
                                    pre_deduction.pop(a)
                                    current_pre_deduction.pop(a)
                                    ytd_pre_deduction.pop(a)
                                    hrs_pre_deduction.pop(a)
                                    rate_pre_deduction.pop(a)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''

                            prc = prc + 1
                        elif 'pre_deduction_health' in response['fields'][i]['name']:
                            for a in range(len(pre_deduction)):

                                if self.pre_duction_health[prd].lower() in pre_deduction[a].lower():
                                    response['fields'][i]['alias'] = pre_deduction[a]
                                    response['fields'][i]['field_value_original'] = \
                                    current_pre_deduction[a]
                                    response['fields'][i]['optional_value'] = ytd_pre_deduction[a]
                                    response['fields'][i]['hrs'] = hrs_pre_deduction[a]
                                    response['fields'][i]['rates'] = rate_pre_deduction[a]
                                    pre_deduction.pop(a)
                                    current_pre_deduction.pop(a)
                                    ytd_pre_deduction.pop(a)
                                    hrs_pre_deduction.pop(a)
                                    rate_pre_deduction.pop(a)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''

                            prd = prd + 1
                        elif 'pre_deduction_dental' in response['fields'][i]['name']:
                            for a in range(len(pre_deduction)):

                                if self.pre_duction_dental[pre].lower() in pre_deduction[a].lower():
                                    response['fields'][i]['alias'] = pre_deduction[a]
                                    response['fields'][i]['field_value_original'] = \
                                    current_pre_deduction[a]
                                    response['fields'][i]['optional_value'] = ytd_pre_deduction[a]
                                    response['fields'][i]['hrs'] = hrs_pre_deduction[a]
                                    response['fields'][i]['rates'] = rate_pre_deduction[a]
                                    pre_deduction.pop(a)
                                    current_pre_deduction.pop(a)
                                    ytd_pre_deduction.pop(a)
                                    hrs_pre_deduction.pop(a)
                                    rate_pre_deduction.pop(a)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''

                            pre = pre + 1

                        elif 'post_deduction_personal' in response['fields'][i]['name']:
                            for a in range(len(post_deduction)):

                                if self.post_deduction_personal[poa].lower() in post_deduction[
                                    a].lower():
                                    response['fields'][i]['alias'] = post_deduction[a]
                                    response['fields'][i]['field_value_original'] = \
                                    current_post_deduction[a]
                                    response['fields'][i]['optional_value'] = ytd_post_deduction[a]
                                    response['fields'][i]['hrs'] = hrs_post_deduction[a]
                                    response['fields'][i]['rates'] = rate_post_deduction[a]
                                    post_deduction.pop(a)
                                    current_post_deduction.pop(a)
                                    ytd_post_deduction.pop(a)
                                    hrs_post_deduction.pop(a)
                                    rate_post_deduction.pop(a)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''

                            poa = poa + 1
                        elif 'post_deduction_life' in response['fields'][i]['name']:
                            for a in range(len(post_deduction)):

                                if self.post_deduction_life[pob].lower() in post_deduction[
                                    a].lower():
                                    response['fields'][i]['alias'] = post_deduction[a]
                                    response['fields'][i]['field_value_original'] = \
                                    current_post_deduction[a]
                                    response['fields'][i]['optional_value'] = ytd_post_deduction[a]
                                    response['fields'][i]['hrs'] = hrs_post_deduction[a]
                                    response['fields'][i]['rates'] = rate_post_deduction[a]
                                    post_deduction.pop(a)
                                    current_post_deduction.pop(a)
                                    ytd_post_deduction.pop(a)
                                    hrs_post_deduction.pop(a)
                                    rate_post_deduction.pop(a)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''
                            pob = pob + 1
                        elif 'post_deduction_accident' in response['fields'][i]['name']:
                            for a in range(len(post_deduction)):

                                if self.post_deduction_accident[poc].lower() in post_deduction[
                                    a].lower():
                                    response['fields'][i]['alias'] = post_deduction[a]
                                    response['fields'][i]['field_value_original'] = \
                                    current_post_deduction[a]
                                    response['fields'][i]['optional_value'] = ytd_post_deduction[a]
                                    response['fields'][i]['hrs'] = hrs_post_deduction[a]
                                    response['fields'][i]['rates'] = rate_post_deduction[a]
                                    post_deduction.pop(a)
                                    current_post_deduction.pop(a)
                                    ytd_post_deduction.pop(a)
                                    hrs_post_deduction.pop(a)
                                    rate_post_deduction.pop(a)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''

                            poc = poc + 1
                        elif 'post_deduction_disability' in response['fields'][i]['name']:
                            for a in range(len(post_deduction)):

                                if self.post_duction_disability[pod].lower() in post_deduction[
                                    a].lower():
                                    response['fields'][i]['alias'] = post_deduction[a]
                                    response['fields'][i]['field_value_original'] = \
                                    current_post_deduction[a]
                                    response['fields'][i]['optional_value'] = ytd_post_deduction[a]
                                    response['fields'][i]['hrs'] = hrs_post_deduction[a]
                                    response['fields'][i]['rates'] = rate_post_deduction[a]
                                    post_deduction.pop(a)
                                    current_post_deduction.pop(a)
                                    ytd_post_deduction.pop(a)
                                    hrs_post_deduction.pop(a)
                                    rate_post_deduction.pop(a)
                                    break
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''

                            pod = pod + 1
                        #     else:
                        #         response['fields'][i]['alias'] = ''
                        #         response['fields'][i]['field_value_original'] = ''
                        #         response['fields'][i]['optional_value'] = ''
                        #         response['fields'][i]['hrs'] = ''
                        #         response['fields'][i]['rates'] = ''

                        elif 'gross_pay' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = current_gross_pay
                            response['fields'][i]['optional_value'] = ytd_gross_pay
                        elif 'net_pay' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = current_net_pay
                            response['fields'][i]['optional_value'] = ytd_net_pay
                        elif 'employee_fn' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = name_value[0]
                            response['fields'][i]['optional_value'] = ""
                        elif 'employee_ln' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = name_value[2]
                            response['fields'][i]['optional_value'] = ""
                        elif 'employee_mn' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = name_value[1]
                            response['fields'][i]['optional_value'] = ""
                        elif 'employee_number' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = ""
                            response['fields'][i]['optional_value'] = ""
                        elif 'employer_address' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = employer_full_address
                            response['fields'][i]['optional_value'] = ""
                        elif 'employer/company_code' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = ""
                            response['fields'][i]['optional_value'] = ""
                        elif 'pay_period_end_date' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = employment_Start_date
                            response['fields'][i]['optional_value'] = ""
                        elif 'pay_period_start_date' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = start_date
                            response['fields'][i]['optional_value'] = ""
                        elif 'pay_date' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = pay_date
                            response['fields'][i]['optional_value'] = ""
                        elif 'state_unemployment' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = ""
                            response['fields'][i]['optional_value'] = ""
                        elif 'position' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = position
                            response['fields'][i]['optional_value'] = ""
                        elif 'employer_name' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = employer_name
                            response['fields'][i]['optional_value'] = ""
                        elif 'employer_city' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = employer_city
                            response['fields'][i]['optional_value'] = ""
                        elif 'employee_city' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = employee_city
                            response['fields'][i]['optional_value'] = ""
                        elif 'employer_state' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = employer_state
                            response['fields'][i]['optional_value'] = ""
                        elif 'employee_state' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = employee_state
                            response['fields'][i]['optional_value'] = ""
                        elif 'employment_start_date' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = ""
                            response['fields'][i]['optional_value'] = ""
                        elif 'pay_frequency' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = pay_frequency
                            response['fields'][i]['optional_value'] = ""
                        elif 'employee_address' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = employee_full_address
                            response['fields'][i]['optional_value'] = ""
                        elif 'tax_total_manual' == response['fields'][i]['name']:
                            print("total taxes len", len(total_calculated_taxes))
                            if n < len(total_calculated_taxes):
                                print(total_calculated_taxes, current_total_calculated_taxes,
                                      ytd_total_calculated_taxes)
                                response['fields'][i]['alias'] = 'Total Calculated'
                                response['fields'][i]['field_value_original'] = \
                                current_total_calculated_taxes[n]
                                response['fields'][i]['optional_value'] = \
                                ytd_total_calculated_taxes[n]
                                response['fields'][i]['hrs'] = hrs_total_calculated_taxes[n]
                                response['fields'][i]['rates'] = rate_total_calculated_taxes[n]
                                n = n + 1
                            else:
                                response['fields'][i]['alias'] = ''
                                response['fields'][i]['field_value_original'] = ''
                                response['fields'][i]['optional_value'] = ''
                                response['fields'][i]['hrs'] = ''
                                response['fields'][i]['rates'] = ''
                        elif 'regular_total_manual' == response['fields'][i]['name']:
                            if o < len(total_calculated_regular):

                                response['fields'][i]['alias'] = 'Total Calculated'
                                response['fields'][i]['field_value_original'] = \
                                current_total_calculated_regular[o]
                                response['fields'][i]['optional_value'] = \
                                ytd_total_calculated_regular[o]
                                response['fields'][i]['hrs'] = hrs_total_calculated_regular[o]
                                response['fields'][i]['rates'] = rate_total_calculated_regular[o]
                                o = o + 1
                            else:
                                response['fields'][i]['alias'] = ''
                                response['fields'][i]['field_value_original'] = ''
                                response['fields'][i]['optional_value'] = ''
                                response['fields'][i]['hrs'] = ''
                                response['fields'][i]['rates'] = ''
                        elif 'pre_deduction_total_manual' == response['fields'][i]['name']:
                            if p < len(total_calculated_pre):

                                response['fields'][i]['alias'] = 'Total Calculated'
                                response['fields'][i]['field_value_original'] = \
                                current_total_calculated_pre[p]
                                response['fields'][i]['optional_value'] = ytd_total_calculated_pre[
                                    p]
                                response['fields'][i]['hrs'] = hrs_total_calculated_pre[p]
                                response['fields'][i]['rates'] = rate_total_calculated_pre[p]
                                p = p + 1
                            else:
                                response['fields'][i]['alias'] = ''
                                response['fields'][i]['field_value_original'] = ''
                                response['fields'][i]['optional_value'] = ''
                                response['fields'][i]['hrs'] = ''
                                response['fields'][i]['rates'] = ''
                        elif 'post_deduction_total_manual' == response['fields'][i]['name']:
                            if q < len(total_calculated_post):

                                response['fields'][i]['alias'] = 'Total Calculated'
                                response['fields'][i]['field_value_original'] = \
                                current_total_calculated_post[q]
                                response['fields'][i]['optional_value'] = ytd_total_calculated_post[
                                    q]
                                response['fields'][i]['hrs'] = hrs_total_calculated_post[q]
                                response['fields'][i]['rates'] = rate_total_calculated_post[q]
                                q = q + 1
                            else:
                                response['fields'][i]['alias'] = ''
                                response['fields'][i]['field_value_original'] = ''
                                response['fields'][i]['optional_value'] = ''
                                response['fields'][i]['hrs'] = ''
                                response['fields'][i]['rates'] = ''
                        elif 'tax_total_auto' == response['fields'][i]['name']:
                            if r < len(total_taxes):

                                response['fields'][i]['alias'] = total_taxes[r]
                                response['fields'][i]['field_value_original'] = current_total_taxes[
                                    r]
                                response['fields'][i]['optional_value'] = ytd_total_taxes[r]
                                response['fields'][i]['hrs'] = hrs_total_taxes[r]
                                response['fields'][i]['rates'] = rate_total_taxes[r]
                                r = r + 1
                            else:
                                response['fields'][i]['alias'] = ''
                                response['fields'][i]['field_value_original'] = ''
                                response['fields'][i]['optional_value'] = ''
                                response['fields'][i]['hrs'] = ''
                                response['fields'][i]['rates'] = ''
                        elif 'regular_total_auto' == response['fields'][i]['name']:
                            if s < len(total_regular):

                                response['fields'][i]['alias'] = total_regular[s]
                                response['fields'][i]['field_value_original'] = \
                                current_total_regular[s]
                                response['fields'][i]['optional_value'] = ytd_total_regular[s]
                                response['fields'][i]['hrs'] = hrs_total_regular[s]
                                response['fields'][i]['rates'] = rate_total_regular[s]
                                s = s + 1
                            else:
                                response['fields'][i]['alias'] = ''
                                response['fields'][i]['field_value_original'] = ''
                                response['fields'][i]['optional_value'] = ''
                                response['fields'][i]['hrs'] = ''
                                response['fields'][i]['rates'] = ''
                        elif 'pre_deduction_total_auto' == response['fields'][i]['name']:
                            if t < len(total_pre):

                                response['fields'][i]['alias'] = total_pre[t]
                                response['fields'][i]['field_value_original'] = current_total_pre[t]
                                response['fields'][i]['optional_value'] = ytd_total_pre[t]
                                response['fields'][i]['hrs'] = hrs_total_pre[t]
                                response['fields'][i]['rates'] = rate_total_pre[t]
                                t = t + 1
                            else:
                                response['fields'][i]['alias'] = ''
                                response['fields'][i]['field_value_original'] = ''
                                response['fields'][i]['optional_value'] = ''
                                response['fields'][i]['hrs'] = ''
                                response['fields'][i]['rates'] = ''
                        elif 'post_deduction_total_auto' == response['fields'][i]['name']:
                            if u < len(total_post):

                                response['fields'][i]['alias'] = total_post[u]
                                response['fields'][i]['field_value_original'] = current_total_post[
                                    u]
                                response['fields'][i]['optional_value'] = ytd_total_post[u]
                                response['fields'][i]['hrs'] = hrs_total_post[u]
                                response['fields'][i]['rates'] = rate_total_post[u]
                                u = u + 1
                            else:
                                response['fields'][i]['alias'] = ''
                                response['fields'][i]['field_value_original'] = ''
                                response['fields'][i]['optional_value'] = ''
                                response['fields'][i]['hrs'] = ''
                                response['fields'][i]['rates'] = ''
                        else:
                            pass

                    for i in range(len(response['fields'])):
                        if 'regular' in response['fields'][i]['alias']:
                            if k < len(earnings):

                                response['fields'][i]['alias'] = earnings[k]
                                response['fields'][i]['field_value_original'] = current_earnings[k]
                                response['fields'][i]['optional_value'] = ytd_earnings[k]
                                response['fields'][i]['hrs'] = hrs_regular[k]
                                response['fields'][i]['rates'] = rate_regular[k]
                                k = k + 1
                            else:
                                response['fields'][i]['alias'] = ''
                                response['fields'][i]['field_value_original'] = ''
                                response['fields'][i]['optional_value'] = ''
                                response['fields'][i]['hrs'] = ''
                                response['fields'][i]['rates'] = ''
                        elif 'tax' == response['fields'][i]['alias']:
                            if j < len(taxes):

                                response['fields'][i]['alias'] = taxes[j]
                                response['fields'][i]['field_value_original'] = current_taxes[j]
                                response['fields'][i]['optional_value'] = ytd_taxes[j]
                                response['fields'][i]['hrs'] = hrs_taxes[j]
                                response['fields'][i]['rates'] = rate_taxes[j]
                                j = j + 1
                            else:
                                response['fields'][i]['alias'] = ''
                                response['fields'][i]['field_value_original'] = ''
                                response['fields'][i]['optional_value'] = ''
                                response['fields'][i]['hrs'] = ''
                                response['fields'][i]['rates'] = ''
                        elif 'other' == response['fields'][i]['alias']:
                            if 'pre deduction' == response['fields'][i]['section_name']:
                                if l < len(pre_deduction):
                                    response['fields'][i]['alias'] = pre_deduction[l]
                                    response['fields'][i]['field_value_original'] = \
                                    current_pre_deduction[l]
                                    response['fields'][i]['optional_value'] = ytd_pre_deduction[l]
                                    response['fields'][i]['hrs'] = hrs_pre_deduction[l]
                                    response['fields'][i]['rates'] = rate_pre_deduction[l]
                                    l = l + 1
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''
                            elif 'post deduction' == response['fields'][i]['section_name']:
                                if m < len(post_deduction):
                                    response['fields'][i]['alias'] = post_deduction[m]
                                    response['fields'][i]['field_value_original'] = \
                                    current_post_deduction[m]
                                    response['fields'][i]['optional_value'] = ytd_post_deduction[m]
                                    response['fields'][i]['hrs'] = hrs_post_deduction[m]
                                    response['fields'][i]['rates'] = rate_post_deduction[m]
                                    m = m + 1
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] = ''
                    print("in main paystub response", response)
                    thread=threading.Thread(target=self.get_ssn_pay_location,args=(response, "../images/documents_upload/" + filename,json_val[doc_id],result1,))
                    thread.start()
                    (emp_name, employee_name, emp_address, employee_address, regular1, regular2, regular3, regular4,
                     regular5, regular6, regular7, regular8, regular9, regular10, tax1, tax2, tax3, tax4, tax5, tax6,
                     tax7, tax8, tax9, tax10, deduction1, deduction2, deduction3, deduction4, deduction5, deduction6,
                     deduction7, deduction8, deduction9, deduction10, deduction11, deduction12, deduction13,
                     deduction14, deduction15, pay_start_date, pay_end_date, pay_date, dict_location, file_path1,
                     value_json) = self.location.get()
                    thread = threading.Thread(target=self.confidence_score, args=("../images/documents_upload/" + filename, json_val[doc_id], value_json,))
                    thread.start()
                    (regular1_scrore,regular2_scrore,regular3_scrore,regular4_scrore,regular5_scrore,regular6_scrore,regular7_scrore,\
                    regular8_scrore,regular9_scrore,regular10_scrore,tax1_scrore,tax2_scrore,tax3_scrore,tax4_scrore,tax5_scrore,\
                    tax6_scrore,tax7_scrore,tax8_scrore,tax9_scrore,tax10_scrore,deduction1_scrore,deduction2_scrore,deduction3_scrore,\
                    deduction4_scrore,deduction5_scrore,deduction6_scrore,deduction7_scrore,deduction8_scrore,deduction9_scrore,deduction10,deduction11_scrore,deduction12_scrore,deduction13_scrore,deduction14_scrore,deduction15_scrore,\
                    pay_end_date_scrore,pay_start_date_scrore,pay_date_scrore,employee_address_scrore,employee_name_scrore,\
                    employer_address_scrore,employer_name_scrore,other_scrore) = self.confidence.get()
                    # # # #
                    # for i in range(len(response['fields'])):
                    #
                    #         if response['fields'][i]['name'] == "employer_name":
                    #             self.location_val.clear()
                    #             for key, value in emp_name.items():
                    #                 self.location_val.append(value)
                    #                 if key in response['fields'][i]['field_value_original']:
                    #                     response['fields'][i]['location'] = str(list(self.location_val))
                    #                     response['fields'][i]['confidence'] = employer_name_scrore-7
                    #
                    #         elif response['fields'][i]['name'] == "pay_period_start_date":
                    #             self.location_val.clear()
                    #             for key, value in pay_start_date.items():
                    #                 self.location_val.append(value)
                    #                 if key in response['fields'][i]['field_value_original']:
                    #                     response['fields'][i]['location'] = str(list(self.location_val))
                    #             response['fields'][i]['confidence'] = pay_start_date_scrore-4
                    #
                    #         elif response['fields'][i]['name'] == "pay_period_end_date":
                    #             self.location_val.clear()
                    #             for key, value in pay_end_date.items():
                    #                 self.location_val.append(value)
                    #                 if key in response['fields'][i]['field_value_original']:
                    #                     response['fields'][i]['location'] = str(list(self.location_val))
                    #             response['fields'][i]['confidence'] = pay_end_date_scrore-2
                    #
                    #         elif response['fields'][i]['name'] == "pay_date":
                    #             self.location_val.clear()
                    #             for key, value in pay_date.items():
                    #                 self.location_val.append(value)
                    #                 if key in response['fields'][i]['field_value_original']:
                    #                     response['fields'][i]['location'] = str(list(self.location_val))
                    #             response['fields'][i]['confidence'] = pay_date_scrore-3
                    #
                    #         elif response['fields'][i]['name'] == "employee_mn":
                    #             self.location_val.clear()
                    #             for key, value in employee_name.items():
                    #                 self.location_val.append(value)
                    #                 if key in response['fields'][i]['field_value_original']:
                    #                     response['fields'][i]['location'] = str(list(self.location_val))
                    #             response['fields'][i]['confidence'] = employee_name_scrore-6
                    #
                    #         elif response['fields'][i]['name'] == "employee_ln":
                    #             self.location_val.clear()
                    #             for key, value in employee_name.items():
                    #                 self.location_val.append(value)
                    #                 if key in response['fields'][i]['field_value_original']:
                    #                     response['fields'][i]['location'] = str(list(self.location_val))
                    #             response['fields'][i]['confidence'] = employee_name_scrore-6
                    #         elif response['fields'][i]['name'] == "employee_fn":
                    #             self.location_val.clear()
                    #             for key, value in employee_name.items():
                    #                 self.location_val.append(value)
                    #                 if key in response['fields'][i]['field_value_original']:
                    #                     response['fields'][i]['location'] = str(list(self.location_val))
                    #             response['fields'][i]['confidence'] = employee_name_scrore-6
                    #
                    #         elif response['fields'][i]['name'] == "employer_address":
                    #             self.location_val.clear()
                    #             for key, value in emp_address.items():
                    #                 self.location_val.append(value)
                    #                 if key in response['fields'][i]['field_value_original']:
                    #                     response['fields'][i]['location'] = str(list(self.location_val))
                    #                     response['fields'][i]['confidence'] = employer_address_scrore-3
                    #
                    #         elif response['fields'][i]['name'] == "employee_address":
                    #             self.location_val.clear()
                    #             for key, value in employee_address.items():
                    #                 self.location_val.append(value)
                    #                 if key in response['fields'][i]['field_value_original']:
                    #                     response['fields'][i]['location'] = str(list(self.location_val))
                    #                     response['fields'][i]['confidence'] = employee_address_scrore-2
                    #
                    #         elif "regular" in  response['fields'][i]['name']:
                    #
                    #             self.location_val.clear()
                    #             if "regular1" in  response['fields'][i]['name']:
                    #                 if regular1!={}:
                    #                     for key, value in regular1.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if regular1_scrore!=0:
                    #                         response['fields'][i]['confidence'] = regular1_scrore-1
                    #             elif "regular2" in  response['fields'][i]['name']:
                    #                 if regular2!={}:
                    #                     for key, value in regular2.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if regular2_scrore!=0:
                    #                         response['fields'][i]['confidence'] = regular2_scrore-5
                    #             elif "regular3" in  response['fields'][i]['name']:
                    #                 if regular3!={}:
                    #                     for key, value in regular3.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if regular3_scrore != 0:
                    #                         response['fields'][i]['confidence'] = regular3_scrore-2
                    #             elif "regular4" in  response['fields'][i]['name']:
                    #                 if regular4!={}:
                    #                     for key, value in regular4.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if regular4_scrore != 0:
                    #                         response['fields'][i]['confidence'] = regular4_scrore-1
                    #             elif "regular5" in  response['fields'][i]['name']:
                    #                 if regular5!={}:
                    #                     for key, value in regular5.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if regular5_scrore != 0:
                    #                         response['fields'][i]['confidence'] = regular5_scrore-3
                    #             elif "regular6" in  response['fields'][i]['name']:
                    #                 if regular6!={}:
                    #                     for key, value in regular6.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if regular6_scrore != 0:
                    #                         response['fields'][i]['confidence'] = regular6_scrore-4
                    #             elif "regular7" in  response['fields'][i]['name']:
                    #                 if regular7!={}:
                    #                     for key, value in regular7.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if regular7_scrore != 0:
                    #                         response['fields'][i]['confidence'] = regular7_scrore-3
                    #             elif "regular8" in  response['fields'][i]['name']:
                    #                 if regular8!={}:
                    #                     for key, value in regular8.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if regular8_scrore != 0:
                    #                         response['fields'][i]['confidence'] = regular8_scrore-5
                    #             elif "regular9" in  response['fields'][i]['name']:
                    #                 if regular9!={}:
                    #                     for key, value in regular9.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if regular9_scrore != 0:
                    #                         response['fields'][i]['confidence'] = regular9_scrore-2
                    #             elif "regular10" in  response['fields'][i]['name']:
                    #                 if regular10!={}:
                    #                     for key, value in regular10.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if regular10_scrore != 0:
                    #                         response['fields'][i]['confidence'] = regular10_scrore-1
                    #
                    #         elif "tax" in  response['fields'][i]['name']:
                    #
                    #             self.location_val.clear()
                    #             if "tax1" in  response['fields'][i]['name']:
                    #                 if tax1!={}:
                    #                     for key, value in tax1.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if tax1_scrore!=0:
                    #                         response['fields'][i]['confidence'] = tax1_scrore-1
                    #             elif "tax2" in  response['fields'][i]['name']:
                    #                 if tax2!={}:
                    #                     for key, value in tax2.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if tax2_scrore!=0:
                    #                         response['fields'][i]['confidence'] = tax2_scrore-5
                    #             elif "tax3" in  response['fields'][i]['name']:
                    #                 if tax3!={}:
                    #                     for key, value in tax3.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if tax3_scrore!=0:
                    #                         response['fields'][i]['confidence'] = tax3_scrore-2
                    #             elif "tax4" in  response['fields'][i]['name']:
                    #                 if tax4!={}:
                    #                     for key, value in tax4.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if tax4_scrore!=0:
                    #                         response['fields'][i]['confidence'] = tax4_scrore-1
                    #             elif "tax5" in  response['fields'][i]['name']:
                    #                 if tax5!={}:
                    #                     for key, value in tax5.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if tax5_scrore!=0:
                    #                         response['fields'][i]['confidence'] = tax5_scrore-3
                    #
                    #             elif "tax6" in  response['fields'][i]['name']:
                    #                 if tax6!={}:
                    #                     for key, value in tax6.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if tax6_scrore!=0:
                    #                         response['fields'][i]['confidence'] = tax6_scrore-4
                    #
                    #             elif "tax7" in  response['fields'][i]['name']:
                    #                 if tax7!={}:
                    #                     for key, value in tax7.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if tax7_scrore!=0:
                    #                         response['fields'][i]['confidence'] = tax7_scrore-3
                    #
                    #             elif "tax8" in  response['fields'][i]['name']:
                    #                 if tax8!={}:
                    #                     for key, value in tax8.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if tax8_scrore!=0:
                    #                         response['fields'][i]['confidence'] = tax8_scrore-5
                    #
                    #             elif "tax9" in  response['fields'][i]['name']:
                    #                 if tax9!={}:
                    #                     for key, value in tax9.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if tax9_scrore!=0:
                    #                         response['fields'][i]['confidence'] = tax9_scrore-2
                    #
                    #             elif "tax10" in  response['fields'][i]['name']:
                    #                 if tax10!={}:
                    #                     for key, value in tax10.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if tax10_scrore!=0:
                    #                         response['fields'][i]['confidence'] = tax10_scrore-1
                    #
                    #         elif "other" in  response['fields'][i]['name']:
                    #             self.location_val.clear()
                    #             if "other1" in  response['fields'][i]['name']:
                    #                 if deduction1!={}:
                    #                     for key, value in deduction1.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if deduction1_scrore!=0:
                    #                         response['fields'][i]['confidence'] = deduction1_scrore-6
                    #             elif "other2" in  response['fields'][i]['name']:
                    #                 if deduction2!={}:
                    #                     for key, value in deduction2.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if deduction2_scrore!=0:
                    #                         response['fields'][i]['confidence'] = deduction2_scrore-5
                    #             elif "other3" in  response['fields'][i]['name']:
                    #                 if deduction3!={}:
                    #                     for key, value in deduction3.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if deduction3_scrore!=0:
                    #                         response['fields'][i]['confidence'] = deduction3_scrore-7
                    #             elif "other4" in  response['fields'][i]['name']:
                    #                 if deduction4!={}:
                    #                     for key, value in deduction4.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if deduction4_scrore!=0:
                    #                         response['fields'][i]['confidence'] = deduction4_scrore-3
                    #             elif "other5" in  response['fields'][i]['name']:
                    #                 if deduction5!={}:
                    #                     for key, value in deduction5.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if deduction5_scrore!=0:
                    #                         response['fields'][i]['confidence'] = deduction5_scrore-4
                    #             elif "other6" in  response['fields'][i]['name']:
                    #                 if deduction6!={}:
                    #                     for key, value in deduction6.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if deduction6_scrore!=0:
                    #                         response['fields'][i]['confidence'] = deduction6_scrore-4
                    #             elif "other7" in  response['fields'][i]['name']:
                    #                 if deduction7!={}:
                    #                     for key, value in deduction7.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if deduction7_scrore!=0:
                    #                         response['fields'][i]['confidence'] = deduction7_scrore-3
                    #             elif "other8" in  response['fields'][i]['name']:
                    #                 if deduction8!={}:
                    #                     for key, value in deduction8.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if deduction8_scrore!=0:
                    #                         response['fields'][i]['confidence'] = deduction8_scrore-5
                    #             elif "other9" in  response['fields'][i]['name']:
                    #                 if deduction9!={}:
                    #                     for key, value in deduction9.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if deduction9_scrore!=0:
                    #                         response['fields'][i]['confidence'] = deduction9_scrore-2
                    #             elif "other10" in  response['fields'][i]['name']:
                    #                 if deduction10!={}:
                    #                     for key, value in deduction10.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if deduction10_scrore10 != 0:
                    #                         response['fields'][i]['confidence'] = deduction10_scrore-1
                    #
                    #             elif "other11" in  response['fields'][i]['name']:
                    #                 if deduction11!={}:
                    #                     for key, value in deduction11.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if deduction_scrore11!=0:
                    #                         response['fields'][i]['confidence'] = deduction11_scrore-1
                    #             elif "other12" in  response['fields'][i]['name']:
                    #                 if deduction12!={}:
                    #                     for key, value in deduction12.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if deduction12_scrore!=0:
                    #                         response['fields'][i]['confidence'] = deduction12_scrore-1
                    #             elif "other13" in  response['fields'][i]['name']:
                    #                 if deduction13!={}:
                    #                     for key, value in deduction13.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if deduction13_scrore!=0:
                    #                         response['fields'][i]['confidence'] = deduction13_scrore-1
                    #             elif "other14" in  response['fields'][i]['name']:
                    #                 if deduction14!={}:
                    #                     for key, value in deduction14.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if deduction14_scrore!=0:
                    #                         response['fields'][i]['confidence'] = deduction14_scrore-1
                    #             elif "other15" in  response['fields'][i]['name']:
                    #                 if deduction15!={}:
                    #                     for key, value in deduction15.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     if deduction15_scrore!=0:
                    #                         response['fields'][i]['confidence'] = deduction15_scrore-1
                    #
                    #         else:
                    #             self.location_val.clear()
                    #             for key, value in dict_location.items():
                    #                 self.location_val.clear()
                    #                 self.location_val.append(value)
                    #                 key = key.replace(',', '')
                    #                 if key in response['fields'][i]['field_value_original']:
                    #                     response['fields'][i]['location'] = str(self.location_val)
                    #                     response['fields'][i]['confidence'] = other_scrore

                    self.scan_result = response
                    self.scan_result['error_msg'] = "Successfully Scanned"
                    self.scan_result["status"] = "SUCCESSFUL"
                    file_path = f_path
                file_path = f_path
            self.scan_result['raw_data'] = self.text
            print("all response", self.scan_result)
            file_path=file_path1
            return self.scan_result, file_path
        except Exception as E:
            print(E)
    def rejected_image(self, path):
        filename = os.path.basename(path)
        image = Image.open(path)
        width, height = image.size
        logo = Image.open(r"../api/red-rejected-stamp-4.png")
        logo.thumbnail(((width / 2), (height / 2)), Image.ANTIALIAS)
        image_copy = image.copy()
        position = (10, 10)
        # position = ((image_copy.width - logo.width), (image_copy.height - logo.height))
        image_copy.paste(logo, position, logo)
        image_copy.save('../images/rejected/' + filename)
        b = os.path.getsize(path)
        B = int(b)
        KB = int(1024)
        MB = int(KB ** 2)  # 1,048,576
        GB = int(KB ** 3)  # 1,073,741,824
        TB = int(KB ** 4)  # 1,099,511,627,776
        if B < KB:
            print('{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte'))
        elif KB <= B < MB:
            size = str(int(B / KB)) + " KB"
        elif MB <= B < GB:
            size = str(int(B / MB)) + " MB"
        elif GB <= B < TB:
            size = str(int(B / GB)) + " GB"
        elif TB <= B:
            size = str(int(B / TB)) + " TB"
        resolution = str(width) + "*" + str(height)
        return '../images/rejected/' + filename, size, resolution