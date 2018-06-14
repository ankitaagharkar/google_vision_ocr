import difflib,time
import sys
import json
import re
import threading
import time
from multiprocessing import Queue
import os
import subprocess
import requests
from PIL import Image


sys.path.insert(0, '../all_documents')
sys.path.insert(0, '../all_documents')
sys.path.insert(0, '../image_processing')
sys.path.insert(0, '../image_text')

import get_ssn_paystub_location
import get_ssn_details
import get_paystub_details
import image_denoising
import get_all_locations
import confidence_score
import LicenseOCR
import PassportOCR

DEBUG=False

class Scan_OCR:

    def __init__(self):
        self.regular_earnings = ["Regular", "Earnings", "Wages", "Regular Wages", "Regular Time",
                                 "Base Salary", "Regular Salary", "Salary","Regular Earnings"]
        self.Vacation = ["Holiday", "Holiday Time", "Holiday Premiu", "Float Holiday", "Vacation"]
        self.Overtime = ["Overtime", "St Time O/T"]
        self.post_deduction_personal = ["Personal Deduction"]
        self.post_deduction_life = ["Life Deduction"]
        self.post_deduction_accident = ["Accident"]
        self.Bonus = ["Bonus"]
        self.commission = ["Commission"]
        self.federal_taxes = ["Federal Taxes", "Federal Income Tax", "Federal Witholdings",
                              "Federal W/H", "Fed Tax", "Fed Income Tax", "Fed Witholdings",
                              "Fed W/H", "FFD W/H", "FFD Taxes", "FFD Tax",'Fed Wh','Fed Whcember']
        self.SSI = ["Social Security Tax","SSI Tax", "Social Security Tax", "Socail Security", "FICA", "Soc Sec"]
        self.Medicare = ["Medicare Tax", "FED Medicare Tax", "Medicare"]
        self.tax_di = ["DI", "Disability Tax"]
        self.tax_oasdi = ["OASDI",'Fed OASDI/EE']
        self.suf = ['dr', 'jr', 'sr', 'II', 'III', 'IV', 'VI', 'VII', 'VIII', 'XI', '3rd', '1st', '2nd',
                    '4th', '5th', '6th', '7th', '8th', '9th', '10th']
        self.State = ["State Income Tax", "Withholding Tax", "State Income", "SIT"]
        self.City = ["Cit Income Tax", "City Re"]
        self.tax_unemp=["Unemployment Tax","Unemployment"]
        self.pre_duction_K = ["401K", "401K$", "401(K)"]
        self.pre_duction_medicare = ["Medical Pre Tax", "Medical", "Med125", "Med Pre Tax","Fed MED/EE"]
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
        self.passport_details = Queue()

        self.confidence_text = confidence_score.text_score()
        self.lic = LicenseOCR.LicenseOCR()
        # self.pass_loc=get_all_locations.get_all_location()
        self.sp_location = get_ssn_paystub_location.get_all_sp_location()
        self.ssn = get_ssn_details.SSN_details()
        self.passport = PassportOCR.Passport_Details()
        self.Paystub = get_paystub_details.Paystub_details()
        self.denoising = image_denoising.Denoising()
        self.score = confidence_score.text_score()
        try:
            with open('../config/config.json') as data_file:
                self.config = json.load(data_file)
            with open('../config/filtering.json', 'r') as data:
                self.state_value = json.load(data)
        except Exception as e:
            print("we are in file",e)

    def custom_print(self, *arg):
        if DEBUG:
            print(arg)

    def image_processing_threading(self,image_path,doc_type):
        try:

            image=self.denoising.image_conversion_smooth(image_path,doc_type)
            self.image_processing.put(image)
        except Exception as e:
            self.custom_print("Exception in all_details image_processing fun.",e)

    def get_doc(self,path, doc_type):
        try:

            self.text, description, result, keys, values, texts = self.sp_location.get_text(path)

            if 'SSN' in doc_type:
                SSN_Number,name,date = self.ssn.get_all_snn_details(self.text)
                self.scan_text.put((self.text, SSN_Number,name,date,keys,values))

        except Exception as e:
            self.custom_print("Exception in all_details get_doc fun.", e)

    def get_passport_details(self,image_path):
        try:

            self.text, description, result, keys, values, texts = self.sp_location.get_text(image_path)
            passport_number, name, dob, issue_date, expiry_date = self.passport.passport_all_details(self.text)
            self.passport_details.put((self.text, passport_number,name,dob,issue_date,expiry_date,result, keys, values))

        except Exception as e:
            self.custom_print("Exception in all_details get_doc fun.", e)

    def get_doc_text(self,path,doc_type):

        # self.text,description,result,_,_,_ = self.Location.get_text(path,doc_type)
        employer_full_address, employer_street, employer_state, employer_zipcode, employer_city, employee_full_address, employee_street, employee_state, employee_zipcode, employee_city, start_date, pay_frequency, string_date_value, employer_name, employee_name, current_gross_pay, ytd_gross_pay, current_net_pay, ytd_net_pay, taxes, current_taxes, ytd_taxes, rate_taxes, hrs_taxes, earnings, current_earnings, ytd_earnings, rate_regular, hrs_regular, pre_deduction, current_pre_deduction, ytd_pre_deduction, rate_pre_deduction, hrs_pre_deduction, post_deduction, current_post_deduction, ytd_post_deduction, rate_post_deduction, hrs_post_deduction, total_calculated_taxes, current_total_calculated_taxes, ytd_total_calculated_taxes, hrs_total_calculated_taxes, rate_total_calculated_taxes, total_calculated_regular, current_total_calculated_regular, ytd_total_calculated_regular, hrs_total_calculated_regular, rate_total_calculated_regular, total_calculated_pre, current_total_calculated_pre, ytd_total_calculated_pre, hrs_total_calculated_pre, rate_total_calculated_pre, total_calculated_post, current_total_calculated_post, ytd_total_calculated_post, hrs_total_calculated_post, rate_total_calculated_post, total_taxes, current_total_taxes, ytd_total_taxes, hrs_total_taxes, rate_total_taxes, total_regular, current_total_regular, ytd_total_regular, hrs_total_regular, rate_total_regular, total_pre, current_total_pre, ytd_total_pre, hrs_total_pre, rate_total_pre, total_post, current_total_post, ytd_total_post, hrs_total_post, rate_total_post, employment_Start_date, pay_date,position,result_output_data,employee_id,text_value,emp_start_date = self.Paystub.get_details(path)
        self.text=text_value
        self.doc_text.put((self.text,employer_full_address, employer_street, employer_state, employer_zipcode, employer_city, employee_full_address, employee_street, employee_state, employee_zipcode, employee_city, start_date, pay_frequency, string_date_value, employer_name, employee_name, current_gross_pay, ytd_gross_pay, current_net_pay, ytd_net_pay, taxes, current_taxes, ytd_taxes, rate_taxes, hrs_taxes, earnings, current_earnings, ytd_earnings, rate_regular, hrs_regular, pre_deduction, current_pre_deduction, ytd_pre_deduction, rate_pre_deduction, hrs_pre_deduction, post_deduction, current_post_deduction, ytd_post_deduction, rate_post_deduction, hrs_post_deduction, total_calculated_taxes, current_total_calculated_taxes, ytd_total_calculated_taxes, hrs_total_calculated_taxes, rate_total_calculated_taxes, total_calculated_regular, current_total_calculated_regular, ytd_total_calculated_regular, hrs_total_calculated_regular, rate_total_calculated_regular, total_calculated_pre, current_total_calculated_pre, ytd_total_calculated_pre, hrs_total_calculated_pre, rate_total_calculated_pre, total_calculated_post, current_total_calculated_post, ytd_total_calculated_post, hrs_total_calculated_post, rate_total_calculated_post, total_taxes, current_total_taxes, ytd_total_taxes, hrs_total_taxes, rate_total_taxes, total_regular, current_total_regular, ytd_total_regular, hrs_total_regular, rate_total_regular, total_pre, current_total_pre, ytd_total_pre, hrs_total_pre, rate_total_pre, total_post, current_total_post, ytd_total_post, hrs_total_post, rate_total_post, employment_Start_date,pay_date,position,result_output_data,employee_id,emp_start_date))

    def get_lic_text(self, path, doc_type):

        self.text,description,result,keys,values,texts = self.Location.get_text(path, doc_type)
        self.lic_text.put((self.text, description,result,keys,values,texts))

    def image_to_pdf(self, image_path, doc_type):

        try:
            filename = os.path.basename(image_path)

            image_path1 =  str(self.config["system_pdf_path"]) + filename

            filename1 = filename.split('.', 1)[0] + ".png"
            f_path =  str(self.config["system_pdf_path"])+ filename1
            f_path_png = f_path
            filename1 = os.path.basename(f_path)
            filename2 = filename1.split('.', 1)[0] + ".jpg"

            if 'SSN' in doc_type:
                process = subprocess.call(
                    'convert -density 250 -trim ' + image_path1 + ' -quality 100 -append ' + f_path,
                    shell=True)
            elif 'License' in doc_type or 'Passport' in doc_type:

                filename1 = filename.split('.', 1)[0] + ".jpg"
                f_path = str(self.config["system_pdf_path"]) + filename1
                process = subprocess.call('convert -density 300 -trim ' +image_path1+ ' -quality 100 -append '+f_path,shell=True)

            else:
                process = subprocess.call('convert -density 300 -trim ' +image_path1+ ' -quality 100 -append '+f_path_png,shell=True)
                f_path = str(self.config["system_pdf_path"]) + filename2
                process = subprocess.call('convert '+f_path_png+ ' -background white -alpha remove ' +f_path,shell=True)
            print("done")
            self.img2pdf.put(f_path)

        except Exception as e:
            self.custom_print("Exception in all_details image2pdf fun.", e)
            pass

    def get_image_text(self, path):
        self.text, description, result, keys, values, texts_description = self.Location.get_text(
            path)
        self.get_image_text.put((self.text, description, result, keys, values, texts_description))

    def get_license_confidences(self, data, text, result):
        dict, date_score, address_score, license_score, other_score,f_name_score,m_name_score,l_name_score,data = self.confidence_text.license_confidence(
            data, text, result)
        self.get_license_confidence.put(
            (dict, date_score, address_score, license_score, other_score,f_name_score,m_name_score,l_name_score,data))

    def get_ssn_pay_location(self, value_json, image, doc_type, result=''):

        if 'SSN' in doc_type:
            ssn_location, name_location, date_location, filename = self.sp_location.ssn_get_location(
                value_json, image)
            self.location.put((ssn_location, name_location, date_location, filename))

        elif 'Paystub' in doc_type:

            emp_name, employee_name, emp_address, employee_address, regular1, regular2, regular3, regular4, regular5, regular6, regular7, regular8, regular9, regular10, tax1, tax2, tax3, tax4, tax5, tax6, tax7, tax8, tax9, tax10, deduction1, deduction2, deduction3, deduction4, deduction5, deduction6, deduction7, deduction8, deduction9, deduction10, deduction11, deduction12, deduction13, deduction14, deduction15, pay_start_date, pay_end_date, pay_date, dict_location, filename, value_data = self.sp_location.paystub_get_location(
                value_json, image, result)
            self.location.put(
                (emp_name, employee_name, emp_address, employee_address, regular1, regular2,
                 regular3, regular4, regular5, regular6, regular7, regular8, regular9,
                 regular10, tax1, tax2, tax3, tax4, tax5, tax6, tax7, tax8, tax9, tax10,
                 deduction1, deduction2, deduction3, deduction4, deduction5, deduction6,
                 deduction7, deduction8, deduction9, deduction10, deduction11, deduction12,
                 deduction13, deduction14, deduction15, pay_start_date, pay_end_date,
                 pay_date, dict_location, filename, value_data))

        elif 'Passport' in doc_type:
            self.passport_no, self.passport_dict, filename = self.sp_location.get_passport_location(value_json, image,result)
            self.location.put((self.passport_no, self.passport_dict, filename))

    def get_location(self, value_json, image, doc_type, result):
        try:
            self.Location = get_all_locations.get_all_location(result)
            if 'License' in doc_type:
                address_location, licence_id_location, dict, filename = self.Location.get_license_location(
                    value_json, image)
                self.location.put((address_location, licence_id_location, dict, filename))

        except Exception as e:
            self.custom_print("Exception in all_details get_location fun.", e)

    def get_license_all_details(self, path):
        try:
            response, licence_id, expiry_date, dob, issue_date, address, name, state, zipcode, city, date_val, result, pdf_image_path = self.lic.run(
                path)
            self.get_license_details.put((response, licence_id, expiry_date, dob, issue_date,
                                          address, name, state, zipcode, city, date_val, result,
                                          pdf_image_path))
        except:
            response = licence_id = expiry_date = dob = issue_date = address = name = state = zipcode = city = date_val = result = pdf_image_path = ''
            self.get_license_details.put((response, licence_id, expiry_date, dob, issue_date,
                                          address, name, state, zipcode, city, date_val, result,
                                          pdf_image_path))

    def confidence_score(self, path, doc_type, data, keys='', values=''):
        try:

            if 'SSN' in doc_type:
                ssn_score, ssn_name_score, ssn_date_score = self.score.ssn_confidence(data, keys,values)
                self.confidence.put((ssn_score, ssn_name_score, ssn_date_score))

            elif 'Paystub' in doc_type:
                self.text, description, result, keys, values, texts = self.sp_location.get_text(
                    path)
                regular1_scrore, regular2_scrore, regular3_scrore, regular4_scrore, regular5_scrore, regular6_scrore, regular7_scrore, \
                regular8_scrore, regular9_scrore, regular10_scrore, tax1_scrore, tax2_scrore, tax3_scrore, tax4_scrore, tax5_scrore, \
                tax6_scrore, tax7_scrore, tax8_scrore, tax9_scrore, tax10_scrore, deduction1_scrore, deduction2_scrore, deduction3_scrore, \
                deduction4_scrore, deduction5_scrore, deduction6_scrore, deduction7_scrore, deduction8_scrore, deduction9_scrore, deduction10, deduction11_scrore, deduction12_scrore, deduction13_scrore, deduction14_scrore, deduction15_scrore, \
                pay_end_date_scrore, pay_start_date_scrore, pay_date_scrore, employee_address_scrore, employee_name_scrore, \
                employer_address_scrore, employer_name_scrore, other_scrore = self.score.paystub_confidence(
                    data, keys,
                    values)

                self.confidence.put((regular1_scrore, regular2_scrore, regular3_scrore,
                                     regular4_scrore, regular5_scrore, regular6_scrore,
                                     regular7_scrore, \
                                     regular8_scrore, regular9_scrore, regular10_scrore,
                                     tax1_scrore, tax2_scrore, tax3_scrore, tax4_scrore,
                                     tax5_scrore, \
                                     tax6_scrore, tax7_scrore, tax8_scrore, tax9_scrore,
                                     tax10_scrore, deduction1_scrore, deduction2_scrore,
                                     deduction3_scrore, \
                                     deduction4_scrore, deduction5_scrore, deduction6_scrore,
                                     deduction7_scrore, deduction8_scrore, deduction9_scrore,
                                     deduction10, deduction11_scrore, deduction12_scrore,
                                     deduction13_scrore, deduction14_scrore, deduction15_scrore, \
                                     pay_end_date_scrore, pay_start_date_scrore, pay_date_scrore,
                                     employee_address_scrore, employee_name_scrore, \
                                     employer_address_scrore, employer_name_scrore, other_scrore))

            elif 'Passport' in doc_type:

                passport_no_score,passport_fn_score,passport_mn_score,passport_ln_score,passport_date_score = self.score.passport_confidence(data, keys,values)
                self.confidence.put((passport_no_score,passport_fn_score,passport_mn_score,passport_ln_score,passport_date_score))

        except Exception as e:
            self.custom_print("Exception in all_details confidence_score fun.", e)

    def get_license_response(self, data, response, conf_result, doc_type, zipcode, text, image_path,result, pdf_image_path):
        time.sleep(5)
        global detected_null_value_count, partial_not_detected, add, detected_value_count
        detected_value_count = 0
        actual_value = list(data.keys())
        actual_value = sorted(actual_value)
        add_value = list(data.values())
        detected_null_value_count = add_value.count('')
        partial_not_detected, partial_detected = [], []

        for i in range(len(response['fields'])):
            for j in range(len(actual_value)):
                if response['fields'][i]['name'] == actual_value[j]:
                    response['fields'][i]['field_value_original'] = data[actual_value[j]]
                    pass
        if pdf_image_path == '':
            thread = threading.Thread(target=self.get_location,
                                      args=(data, image_path, doc_type, result))
        else:
            thread = threading.Thread(target=self.get_location,
                                      args=(data, pdf_image_path, doc_type, result))
        thread.setName("Location Thread")
        thread.start()
        (address_location, licence_id_location, dict_location, file_path1) = self.location.get()
        thread = threading.Thread(target=self.get_license_confidences,
                                  args=(data, text, conf_result,))
        thread.setName("Confidence Thread")
        thread.start()
        (date_dict, date_score, address_score, license_score,other_score,f_name_score,m_name_score,l_name_score,adata) = self.get_license_confidence.get()
        reg = ''

        state_regex = re.findall(
            r"\b(!?AL|AK|AS|AZ|AŽ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE"
            r"|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)",
            zipcode)
        if state_regex != []:
            for i in range(len(self.state_value['data'])):
                if self.state_value['data'][i]['state'] in state_regex[0]:
                    reg = self.state_value['data'][i]['license_id']
        licence_id = re.findall(reg, self.text)
        if licence_id == []:
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
                                if self.config['high_accuracy'][0] <= f_name_score <= \
                                        self.config['high_accuracy'][1]:
                                    response['fields'][i]['confidence'] = f_name_score
                                elif self.config['medium_accuracy'][0] <= f_name_score <= \
                                        self.config['medium_accuracy'][1]:
                                    response['fields'][i]['confidence'] = f_name_score
                                else:
                                    response['fields'][i]['field_value_original'] = ''
                            else:
                                response['fields'][i]['confidence'] = f_name_score

            elif response['fields'][i]['name'] == "last_name":
                self.location_val.clear()
                for key, value in dict_location.items():
                    self.location_val.append(value)
                    key = key.replace(',', '')
                    if response['fields'][i]['field_value_original'] is not "":
                        if key in response['fields'][i]['field_value_original']:
                            response['fields'][i]['location'] = str(self.location_val)
                            if self.config['field_level'] == "True":
                                if self.config['high_accuracy'][0] <= l_name_score <= \
                                        self.config['high_accuracy'][1]:
                                    response['fields'][i]['confidence'] = l_name_score
                                elif self.config['medium_accuracy'][0] <= l_name_score <= \
                                        self.config['medium_accuracy'][1]:
                                    response['fields'][i]['confidence'] = l_name_score
                                else:
                                    response['fields'][i]['field_value_original'] = ''
                            else:
                                response['fields'][i]['confidence'] = l_name_score

            elif response['fields'][i]['name'] == "middle_name":
                self.location_val.clear()
                for key, value in dict_location.items():
                    self.location_val.append(value)
                    key = key.replace(',', '')
                    if response['fields'][i]['field_value_original'] is not "":
                        if key in response['fields'][i]['field_value_original']:
                            response['fields'][i]['location'] = str(self.location_val)
                            if self.config['field_level'] == "True":
                                if self.config['high_accuracy'][0] <= m_name_score <= \
                                        self.config['high_accuracy'][1]:
                                    response['fields'][i]['confidence'] = m_name_score
                                elif self.config['medium_accuracy'][0] <= m_name_score <= \
                                        self.config['medium_accuracy'][1]:
                                    response['fields'][i]['confidence'] = m_name_score
                                else:
                                    response['fields'][i]['field_value_original'] = ''
                            else:
                                response['fields'][i]['confidence'] = m_name_score

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
        # return self.scan_result, file_path
        self.get_response.put((file_path))

    def all_details(self, response):

        global text, detected_null_value_count, file_path1
        try:

            doc_id = int(response['doc_id'])
            app_id = response['application_id']
            filename = response["uploaded_file_name"]

            print("GETTING RESPONSE")
            image_process_resp = requests.post(self.config['base_url'] + '/getUploadedFile',
                                               data={"application_id": app_id, "dir_type": 1, "file_name": filename},verify=False)

            image_process_data = image_process_resp.content
            if re.search(r'(!?(&|!|@|#|\$|\^|\*|\-|\'|\"))', filename):
                filename = filename.replace(re.findall(r'(!?(&|!|@|#|\$|\^|\*|\-|\'|\"))', filename)[0][0], "")
            with open("../images/documents_upload/" + filename, "wb") as downloaded_image:
                downloaded_image.write(bytearray(image_process_data))
                downloaded_image.close()
            print("GOT RESPONSE")

            r = requests.post(self.config['base_url'] + '/getAllDocumentsMaster',verify=False)
            resp_dict = json.loads(json.dumps(r.json()))
            print("all document resp")
            value = resp_dict.get('records')
            json_val = dict([(value[i]['id'], value[i]['name']) for i in range(len(value))])

            if 'License' in json_val[doc_id]:
                data = {}
                thread = threading.Thread(target=self.get_license_all_details,
                                          args=("../images/documents_upload/" + filename,))
                thread.start()
                thread.join(999999)
                (text_response, licence_id, expiry_date, dob, issue_date, address, name, state,
                 zipcode, city, date_val, result, pdf_image_path) = self.get_license_details.get()
                if licence_id == ' ' and expiry_date == '' and dob == '' and issue_date == '' and address == '' and name == '' and state == '' and zipcode == '' and city == '' and date_val:
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
                        name_val = name.split()
                        if len(name_val) == 2:
                            if re.search(r'\b(!?[A-Za-z]+\s[A-Za-z])\b', name):
                                self.name_value.clear()
                                self.name_value.append(' ')
                                self.name_value.append(name_val[0])
                                self.name_value.append(name_val[1])
                        else:
                            pass

                    if re.search('(!?JR|Jr|jr|jR)', name):
                        if self.name_value.index(re.findall(r'(!?JR|Jr|jr|jR)', name)[0]) == 1:
                            self.name_value[1] = self.name_value[1] + " " + self.name_value[2]
                            self.name_value.pop(2)
                        elif self.name_value.index(re.findall('(!?JR|Jr|jr|jR)', name)[0]) == 3:
                            self.name_value[2] = self.name_value[2] + " " + self.name_value[3]
                            self.name_value.pop(3)

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
                            'last_name': self.name_value[0], 'address': address,
                            'license_id': licence_id,
                            "middle_name": "", "state": state, "postal_code": zipcode, "city": city,
                            "date_val": date_val}
                elif 'FN_MN_LN_SUF' == name_seq:

                    if len(self.name_value) == 3:
                        data = {'first_name': self.name_value[0], 'dob': dob,
                                'issue_date': issue_date,
                                'expiration_date': expiry_date,
                                'last_name': self.name_value[2], 'address': address,
                                'license_id': licence_id,
                                "middle_name": self.name_value[1], "state": state,
                                "postal_code": zipcode,
                                "city": city, "date_val": date_val}
                    elif len(self.name_value) == 4:
                        data = {'first_name': self.name_value[0], 'dob': dob,
                                'issue_date': issue_date,
                                'expiration_date': expiry_date,
                                'last_name': self.name_value[2] + " " + self.name_value[3],
                                'address': address, 'license_id': licence_id,
                                "middle_name": self.name_value[1], "state": state,
                                "postal_code": zipcode,
                                "city": city, "date_val": date_val}
                    elif len(self.name_value) == 5:
                        data = {'first_name': self.name_value[0] + " " + self.name_value[1] + " " +
                                              self.name_value[2], 'dob': dob,
                                'issue_date': issue_date,
                                'expiration_date': expiry_date,
                                'last_name': self.name_value[4],
                                'address': address, 'license_id': licence_id,
                                "middle_name": self.name_value[3], "state": state,
                                "postal_code": zipcode,
                                "city": city, "date_val": date_val}
                    else:
                        data = {'first_name': self.name_value[0], 'dob': dob,
                                'issue_date': issue_date,
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
                                "middle_name": self.name_value[2] + " " + self.name_value[3],
                                "state": state,
                                "postal_code": zipcode, "city": city,
                                "date_val": date_val}
                    elif len(self.name_value) == 5:
                        data = {'first_name': self.name_value[3], 'dob': dob,
                                'issue_date': issue_date, 'expiration_date': expiry_date,
                                'last_name': self.name_value[0] + " " + self.name_value[1] + " " +
                                             self.name_value[2], 'address': address,
                                'license_id': licence_id,
                                "middle_name": self.name_value[4], "state": state,
                                "postal_code": zipcode, "city": city,
                                "date_val": date_val}
                    else:
                        data = {'first_name': self.name_value[1], 'dob': dob,
                                'issue_date': issue_date,
                                'expiration_date': expiry_date, 'last_name': self.name_value[0],
                                'address': address,
                                'license_id': licence_id, "middle_name": '', "state": state,
                                "postal_code": zipcode, "city": city, "date_val": date_val}
                text, conf_result = self.lic.get_word_confidence(text_response)
                self.text = text
                thread = threading.Thread(target=self.get_license_response,
                                          args=(data, response, conf_result, json_val[doc_id], zipcode,text,"../images/documents_upload/" + filename,result, pdf_image_path,))

                thread.start()
                thread.join(999999)
                (file_path1)=self.get_response.get()
                # file_path1 = self.get_license_response(data, response, conf_result, json_val[doc_id], zipcode,text,"../images/documents_upload/" + filename,result, pdf_image_path)

            elif 'SSN' in json_val[doc_id]:
                if filename.rsplit('.', 1)[1] == 'pdf':
                    thread = threading.Thread(target=self.image_to_pdf,
                                              args=("../images/documents_upload/" + filename,
                                                    json_val[doc_id],))
                    thread.start()
                    path = self.img2pdf.get()
                    name_file = os.path.basename(path)
                    f_path = "../images/documents_upload/" + name_file
                    image_path=f_path
                    # image_path=f_path
                    # thread = threading.Thread(target=self.image_processing_threading,
                    #                           args=(f_path, json_val[doc_id],))
                else:
                    image_path = "../images/documents_upload/" + filename
                    # thread = threading.Thread(target=self.image_processing_threading, args=(
                    # "../images/documents_upload/" + filename, json_val[doc_id],))
                # thread.start()
                # image_path = self.image_processing.get()
                thread = threading.Thread(target=self.get_doc, args=(image_path, json_val[doc_id],))
                thread.start()
                (self.text, SSN_Number, name, date, conf_keys, conf_values) = self.scan_text.get()
                if SSN_Number == '' and name == '' and date == '':
                    file_path = ''
                    self.scan_result['error_msg'] = "Incorrect Document or Unable to Scan"
                    self.scan_result['status'] = "INCORRECT_DOCUMENT"

                    return self.scan_result, file_path
                else:
                    actual_name = name.split()
                    if len(actual_name) > 3:
                        actual_name.pop(0)

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

                    thread = threading.Thread(target=self.get_ssn_pay_location,
                                              args=(add, image_path, json_val[doc_id],))
                    thread.start()
                    (ssn_number_location, name_location, date_location,
                     file_path1) = self.location.get()

                    thread = threading.Thread(target=self.confidence_score, args=(
                    image_path, json_val[doc_id], add, conf_keys, conf_values,))
                    thread.start()
                    (ssn_score, ssn_name_score, ssn_date_score) = self.confidence.get()

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
                                        elif self.config['medium_accuracy'][0] <= int(
                                                ssn_date_score) <= \
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
                                        elif self.config['medium_accuracy'][0] <= int(
                                                ssn_name_score) <= \
                                                self.config['medium_accuracy'][1]:
                                            response['fields'][i]['confidence'] = ssn_name_score
                                        else:
                                            response['fields'][i]['field_value_original'] = ''
                                    else:
                                        response['fields'][i]['confidence'] = ssn_name_score
                self.scan_result = response

                detected_null_value_count = detected_value_count = 0
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

                if re.search('PDF',filename.rsplit('.', 1)[1],re.IGNORECASE):
                    thread = threading.Thread(target=self.image_to_pdf,
                                              args=("../images/documents_upload/" + filename,
                                                    json_val[doc_id],))
                    thread.start()
                    thread.join()
                    f_path = self.img2pdf.get()
                    name_file = os.path.basename(f_path)
                    f_path = "../images/documents_upload/" + name_file

                    thread = threading.Thread(target=self.get_doc_text,
                                              args=(f_path, json_val[doc_id],))

                else:
                    f_path = "../images/documents_upload/" + filename
                    image = Image.open(f_path)
                    width, height = image.size

                    thread = threading.Thread(target=self.get_doc_text, args=(
                        "../images/documents_upload/" + filename, json_val[doc_id],))
                    # file_path1=f_path
                thread.start()
                (
                    self.text, employer_full_address, employer_street, employer_state,
                    employer_zipcode,
                    employer_city, employee_full_address, employee_street, employee_state,
                    employee_zipcode, employee_city, start_date, pay_frequency, string_date_value,
                    employer_name, employee_name, current_gross_pay, ytd_gross_pay, current_net_pay,
                    ytd_net_pay, taxes, current_taxes, ytd_taxes, rate_taxes, hrs_taxes, earnings,
                    current_earnings, ytd_earnings, rate_regular, hrs_regular, pre_deduction,
                    current_pre_deduction, ytd_pre_deduction, rate_pre_deduction, hrs_pre_deduction,
                    post_deduction, current_post_deduction, ytd_post_deduction, rate_post_deduction,
                    hrs_post_deduction, total_calculated_taxes, current_total_calculated_taxes,
                    ytd_total_calculated_taxes, hrs_total_calculated_taxes,
                    rate_total_calculated_taxes,
                    total_calculated_regular, current_total_calculated_regular,
                    ytd_total_calculated_regular, hrs_total_calculated_regular,
                    rate_total_calculated_regular, total_calculated_pre,
                    current_total_calculated_pre,
                    ytd_total_calculated_pre, hrs_total_calculated_pre, rate_total_calculated_pre,
                    total_calculated_post, current_total_calculated_post, ytd_total_calculated_post,
                    hrs_total_calculated_post, rate_total_calculated_post, total_taxes,
                    current_total_taxes, ytd_total_taxes, hrs_total_taxes, rate_total_taxes,
                    total_regular, current_total_regular, ytd_total_regular, hrs_total_regular,
                    rate_total_regular, total_pre, current_total_pre, ytd_total_pre, hrs_total_pre,
                    rate_total_pre, total_post, current_total_post, ytd_total_post, hrs_total_post,
                    rate_total_post, employment_Start_date, pay_date, position, result_output_data,
                    employee_id,emp_start_date) = self.doc_text.get()

                name_value = []
                j = 0
                k = 0
                l = 0
                m = 0
                n = 0
                o = 0
                p = 0
                q = 0
                r = 0
                s = 0
                t = 0
                u = 0
                earn=[]
                pre=[]
                post=[]
                tax=[]

                temp_emp = employee_name
                employee_name = employee_name.replace(',', ' ')
                name_value = employee_name.split()
                if name_value == []:
                    name_value.append('')
                    name_value.append('')
                    name_value.append('')
                if len(name_value) == 2:
                    name_value.append(name_value[1])
                    name_value[1] = ''
                elif len(name_value) == 1:
                    name_value.append('')
                    name_value.append('')
                elif len(name_value) > 3:
                    name_value[2] = name_value[2] + " " + name_value[3]
                    name_value.pop(3)
                if ',' in temp_emp and name_value != []:
                    last_name = name_value[0]
                    if name_value[1] == '':
                        first_name = name_value[2]
                        middle_name = name_value[1]
                    else:
                        first_name = name_value[1]
                        middle_name = name_value[2]
                elif ',' not in temp_emp and name_value != []:
                    last_name = name_value[2]
                    first_name = name_value[0]
                    middle_name = name_value[1]
                time.sleep(1)
                for i in range(len(response['fields'])):
                    if 'regular_earn' in response['fields'][i]['name']:
                        if len(earnings) > 0:
                            for a in range(len(earnings)):
                                x = difflib.get_close_matches(earnings[a].lower(),
                                                              [vt.lower() for vt in self.regular_earnings],
                                                              cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = earnings[a]
                                    response['fields'][i]['field_value_original'] = current_earnings[a]
                                    response['fields'][i]['optional_value'] = ytd_earnings[a]
                                    response['fields'][i]['hrs'] = hrs_regular[a]
                                    response['fields'][i]['rates'] = rate_regular[a]
                                    earn.append(earnings[a])
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

                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''
                    elif 'regular_bonus' in response['fields'][i]['name']:
                        if len(earnings) > 0:
                            for a in range(len(earnings)):
                                x = difflib.get_close_matches(earnings[a].lower(),
                                                              [vt.lower() for vt in self.Bonus],
                                                              cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = earnings[a]
                                    response['fields'][i]['field_value_original'] = current_earnings[a]
                                    response['fields'][i]['optional_value'] = ytd_earnings[a]
                                    response['fields'][i]['hrs'] = hrs_regular[a]
                                    response['fields'][i]['rates'] = rate_regular[a]
                                    earn.append(earnings[a])
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
                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''
                    elif 'regular_vacation' in response['fields'][i]['name']:
                        if len(earnings) > 0:
                            for w in range(len(earnings)):
                                x = difflib.get_close_matches(earnings[w].lower(),
                                                              [vt.lower() for vt in self.Vacation],
                                                              cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = earnings[w]
                                    response['fields'][i]['field_value_original'] = \
                                        current_earnings[w]
                                    response['fields'][i]['optional_value'] = ytd_earnings[w]
                                    response['fields'][i]['hrs'] = hrs_regular[w]
                                    response['fields'][i]['rates'] = rate_regular[w]
                                    earn.append(earnings[a])
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
                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''
                    elif 'regular_overtime' in response['fields'][i]['name']:
                        if len(earnings) > 0:
                            for a in range(len(earnings)):
                                x = difflib.get_close_matches(earnings[a].lower(),
                                                              [vt.lower() for vt in self.Overtime],
                                                              cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = earnings[a]
                                    response['fields'][i]['field_value_original'] = \
                                        current_earnings[a]
                                    response['fields'][i]['optional_value'] = ytd_earnings[a]
                                    response['fields'][i]['hrs'] = hrs_regular[a]
                                    response['fields'][i]['rates'] = rate_regular[a]
                                    earn.append(earnings[a])
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
                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''
                    elif 'regular_commision' in response['fields'][i]['name']:
                        if len(earnings) > 0:
                            for a in range(len(earnings)):
                                x = difflib.get_close_matches(earnings[a].lower(),
                                                              [vt.lower() for vt in self.commission],
                                                              cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = earnings[a]
                                    response['fields'][i]['field_value_original'] = \
                                        current_earnings[a]
                                    response['fields'][i]['optional_value'] = ytd_earnings[a]
                                    response['fields'][i]['hrs'] = hrs_regular[a]
                                    response['fields'][i]['rates'] = rate_regular[a]
                                    earn.append(earnings[a])
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
                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''

                    elif 'tax_federal' in response['fields'][i]['name']:
                        if len(taxes) > 0:
                            for a in range(len(taxes)):
                                x = difflib.get_close_matches(taxes[a].lower(),
                                                              [vt.lower() for vt in self.federal_taxes],
                                                              cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = taxes[a]
                                    response['fields'][i]['field_value_original'] = current_taxes[a]
                                    response['fields'][i]['optional_value'] = ytd_taxes[a]
                                    response['fields'][i]['hrs'] = hrs_taxes[a]
                                    response['fields'][i]['rates'] = rate_taxes[a]
                                    tax.append(taxes[a])
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
                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''
                    elif 'tax_state' in response['fields'][i]['name']:
                        if len(taxes) > 0:
                            for a in range(len(taxes)):
                                x = difflib.get_close_matches(taxes[a].lower(),
                                                              [vt.lower() for vt in self.State],
                                                              cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = taxes[a]
                                    response['fields'][i]['field_value_original'] = \
                                        current_taxes[a]
                                    response['fields'][i]['optional_value'] = ytd_taxes[a]
                                    response['fields'][i]['hrs'] = hrs_taxes[a]
                                    response['fields'][i]['rates'] = rate_taxes[a]
                                    tax.append(taxes[a])
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
                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''
                    elif 'tax_city' in response['fields'][i]['name']:
                        if len(taxes) > 0:
                            for a in range(len(taxes)):
                                x = difflib.get_close_matches(taxes[a].lower(),
                                                              [vt.lower() for vt in self.City], cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = taxes[a]
                                    response['fields'][i]['field_value_original'] = current_taxes[a]
                                    response['fields'][i]['optional_value'] = ytd_taxes[a]
                                    response['fields'][i]['hrs'] = hrs_taxes[a]
                                    response['fields'][i]['rates'] = rate_taxes[a]
                                    tax.append(taxes[a])
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
                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''
                    elif 'tax_medicare' in response['fields'][i]['name']:
                        if len(taxes) > 0:
                            for a in range(len(taxes)):
                                x = difflib.get_close_matches(taxes[a].lower(),
                                                              [vt.lower() for vt in self.Medicare],
                                                              cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = taxes[a]
                                    response['fields'][i]['field_value_original'] = current_taxes[a]
                                    response['fields'][i]['optional_value'] = ytd_taxes[a]
                                    response['fields'][i]['hrs'] = hrs_taxes[a]
                                    response['fields'][i]['rates'] = rate_taxes[a]
                                    tax.append(taxes[a])
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
                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''
                    elif 'tax_ss' in response['fields'][i]['name']:
                        if len(taxes) > 0:
                            for a in range(len(taxes)):
                                x = difflib.get_close_matches(taxes[a].lower(),
                                                              [vt.lower() for vt in self.SSI], cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = taxes[a]
                                    response['fields'][i]['field_value_original'] = current_taxes[a]
                                    response['fields'][i]['optional_value'] = ytd_taxes[a]
                                    response['fields'][i]['hrs'] = hrs_taxes[a]
                                    response['fields'][i]['rates'] = rate_taxes[a]
                                    tax.append(taxes[a])
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
                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''
                    elif 'tax_di' in response['fields'][i]['name']:
                        if len(taxes) > 0:
                            for a in range(len(taxes)):
                                x = difflib.get_close_matches(taxes[a].lower(),
                                                              [vt.lower() for vt in self.tax_di],
                                                              cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = taxes[a]
                                    response['fields'][i]['field_value_original'] = \
                                        current_taxes[a]
                                    response['fields'][i]['optional_value'] = ytd_taxes[a]
                                    response['fields'][i]['hrs'] = hrs_taxes[a]
                                    response['fields'][i]['rates'] = rate_taxes[a]
                                    tax.append(taxes[a])
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
                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''
                    elif 'tax_oasdi' in response['fields'][i]['name']:
                        if len(taxes) > 0:
                            for a in range(len(taxes)):
                                x = difflib.get_close_matches(taxes[a].lower(),
                                                              [vt.lower() for vt in self.tax_oasdi],
                                                              cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = taxes[a]
                                    response['fields'][i]['field_value_original'] = \
                                        current_taxes[a]
                                    response['fields'][i]['optional_value'] = ytd_taxes[a]
                                    response['fields'][i]['hrs'] = hrs_taxes[a]
                                    response['fields'][i]['rates'] = rate_taxes[a]
                                    tax.append(taxes[a])
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
                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''
                    elif 'tax_unemployment' in response['fields'][i]['name']:
                        if len(taxes) > 0:
                            for a in range(len(taxes)):
                                x = difflib.get_close_matches(taxes[a].lower(),
                                                              [vt.lower() for vt in self.tax_unemp],
                                                              cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = taxes[a]
                                    response['fields'][i]['field_value_original'] = current_taxes[a]
                                    response['fields'][i]['optional_value'] = ytd_taxes[a]
                                    response['fields'][i]['hrs'] = hrs_taxes[a]
                                    response['fields'][i]['rates'] = rate_taxes[a]
                                    tax.append(taxes[a])
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
                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''

                    elif 'pre_deduction_401k' in response['fields'][i]['name']:
                        if len(pre_deduction) > 0:
                            for a in range(len(pre_deduction)):
                                x = difflib.get_close_matches(pre_deduction[a].lower(),
                                                              [vt.lower() for vt in self.pre_duction_K],
                                                              cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = pre_deduction[a]
                                    response['fields'][i]['field_value_original'] = \
                                        current_pre_deduction[a]
                                    response['fields'][i]['optional_value'] = ytd_pre_deduction[
                                        a]
                                    response['fields'][i]['hrs'] = hrs_pre_deduction[a]
                                    response['fields'][i]['rates'] = rate_pre_deduction[a]
                                    pre.append(pre_deduction[a])
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


                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''
                    elif 'pre_deduction_medical' in response['fields'][i]['name']:
                        if len(pre_deduction) > 0:
                            for a in range(len(pre_deduction)):
                                x = difflib.get_close_matches(pre_deduction[a].lower(),
                                                              [vt.lower() for vt in
                                                               self.pre_duction_medicare],
                                                              cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = pre_deduction[a]
                                    response['fields'][i]['field_value_original'] = current_pre_deduction[a]
                                    response['fields'][i]['optional_value'] = ytd_pre_deduction[a]
                                    response['fields'][i]['hrs'] = hrs_pre_deduction[a]
                                    response['fields'][i]['rates'] = rate_pre_deduction[a]
                                    pre.append(pre_deduction[a])
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

                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''
                    elif 'pre_deduction_vision' in response['fields'][i]['name']:
                        if len(pre_deduction) > 0:
                            for a in range(len(pre_deduction)):
                                x = difflib.get_close_matches(pre_deduction[a].lower(),
                                                              [vt.lower() for vt in
                                                               self.pre_duction_vision], cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = pre_deduction[a]
                                    response['fields'][i]['field_value_original'] = current_pre_deduction[a]
                                    response['fields'][i]['optional_value'] = ytd_pre_deduction[a]
                                    response['fields'][i]['hrs'] = hrs_pre_deduction[a]
                                    response['fields'][i]['rates'] = rate_pre_deduction[a]
                                    pre.append(pre_deduction[a])
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
                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''
                    elif 'pre_deduction_health' in response['fields'][i]['name']:
                        if len(pre_deduction) > 0:
                            for a in range(len(pre_deduction)):
                                x = difflib.get_close_matches(pre_deduction[a].lower(),
                                                              [vt.lower() for vt in
                                                               self.pre_duction_health], cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = pre_deduction[a]
                                    response['fields'][i]['field_value_original'] = current_pre_deduction[a]
                                    response['fields'][i]['optional_value'] = ytd_pre_deduction[a]
                                    response['fields'][i]['hrs'] = hrs_pre_deduction[a]
                                    response['fields'][i]['rates'] = rate_pre_deduction[a]
                                    pre.append(pre_deduction[a])
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


                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''
                    elif 'pre_deduction_dental' in response['fields'][i]['name']:
                        if len(pre_deduction) > 0:
                            for a in range(len(pre_deduction)):
                                x = difflib.get_close_matches(pre_deduction[a].lower(),
                                                              [vt.lower() for vt in
                                                               self.pre_duction_dental], cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = pre_deduction[a]
                                    response['fields'][i]['field_value_original'] = \
                                        current_pre_deduction[a]
                                    response['fields'][i]['optional_value'] = ytd_pre_deduction[
                                        a]
                                    response['fields'][i]['hrs'] = hrs_pre_deduction[a]
                                    response['fields'][i]['rates'] = rate_pre_deduction[a]
                                    pre.append(pre_deduction[a])
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


                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''

                    elif 'post_deduction_personal' in response['fields'][i]['name']:
                        if len(post_deduction) > 0:
                            for a in range(len(post_deduction)):
                                x = difflib.get_close_matches(post_deduction[a].lower(),
                                                              [vt.lower() for vt in
                                                               self.post_deduction_personal], cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = post_deduction[a]
                                    response['fields'][i]['field_value_original'] = current_post_deduction[
                                        a]
                                    response['fields'][i]['optional_value'] = ytd_post_deduction[a]
                                    response['fields'][i]['hrs'] = hrs_post_deduction[a]
                                    response['fields'][i]['rates'] = rate_post_deduction[a]
                                    post.append(post_deduction[a])
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

                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''
                    elif 'post_deduction_life' in response['fields'][i]['name']:
                        if len(post_deduction) > 0:
                            for a in range(len(post_deduction)):
                                x = difflib.get_close_matches(post_deduction[a].lower(),
                                                              [vt.lower() for vt in
                                                               self.post_deduction_life], cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = post_deduction[a]
                                    response['fields'][i]['field_value_original'] = \
                                        current_post_deduction[a]
                                    response['fields'][i]['optional_value'] = \
                                        ytd_post_deduction[a]
                                    response['fields'][i]['hrs'] = hrs_post_deduction[a]
                                    response['fields'][i]['rates'] = rate_post_deduction[a]
                                    post.append(post_deduction[a])
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

                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''
                    elif 'post_deduction_accident' in response['fields'][i]['name']:
                        if len(post_deduction) > 0:
                            for a in range(len(post_deduction)):
                                x = difflib.get_close_matches(post_deduction[a].lower(),
                                                              [vt.lower() for vt in
                                                               self.post_deduction_accident], cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = post_deduction[a]
                                    response['fields'][i]['field_value_original'] = current_post_deduction[
                                        a]
                                    response['fields'][i]['optional_value'] = ytd_post_deduction[a]
                                    response['fields'][i]['hrs'] = hrs_post_deduction[a]
                                    response['fields'][i]['rates'] = rate_post_deduction[a]
                                    post.append(post_deduction[a])
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

                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''
                    elif 'post_deduction_disability' in response['fields'][i]['name']:
                        if len(post_deduction) > 0:
                            for a in range(len(post_deduction)):
                                x = difflib.get_close_matches(post_deduction[a].lower(),
                                                              [vt.lower() for vt in
                                                               self.post_duction_disability], cutoff=0.85)
                                if x:
                                    response['fields'][i]['alias'] = post_deduction[a]
                                    response['fields'][i]['field_value_original'] = \
                                        current_post_deduction[a]
                                    response['fields'][i]['optional_value'] = \
                                        ytd_post_deduction[a]
                                    response['fields'][i]['hrs'] = hrs_post_deduction[a]
                                    response['fields'][i]['rates'] = rate_post_deduction[a]
                                    post.append(post_deduction[a])
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


                        else:
                            response['fields'][i]['alias'] = ''
                            response['fields'][i]['field_value_original'] = ''
                            response['fields'][i]['optional_value'] = ''
                            response['fields'][i]['hrs'] = ''
                            response['fields'][i]['rates'] = ''
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
                        response['fields'][i]['field_value_original'] = first_name
                        response['fields'][i]['optional_value'] = ""
                    elif 'employee_ln' == response['fields'][i]['name']:
                        response['fields'][i]['field_value_original'] = last_name
                        response['fields'][i]['optional_value'] = ""
                    elif 'employee_mn' == response['fields'][i]['name']:
                        response['fields'][i]['field_value_original'] = middle_name
                        response['fields'][i]['optional_value'] = ""
                    elif 'employee_number' == response['fields'][i]['name']:
                        response['fields'][i]['field_value_original'] = employee_id
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
                        response['fields'][i]['field_value_original'] = emp_start_date
                        response['fields'][i]['optional_value'] = ""
                    elif 'pay_frequency' == response['fields'][i]['name']:
                        response['fields'][i]['field_value_original'] = pay_frequency
                        response['fields'][i]['optional_value'] = ""
                    elif 'employee_address' == response['fields'][i]['name']:
                        response['fields'][i]['field_value_original'] = employee_full_address
                        response['fields'][i]['optional_value'] = ""
                    elif 'tax_total_manual' == response['fields'][i]['name']:

                        if n < len(total_calculated_taxes):
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

                            response['fields'][i]['alias'] = 'Total on Document'
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

                            response['fields'][i]['alias'] = 'Total on Document'
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

                            response['fields'][i]['alias'] = 'Total on Document'
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

                            response['fields'][i]['alias'] = 'Total on Document'
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
                    elif 'employee_zip' == response['fields'][i]['name']:
                        response['fields'][i]['field_value_original'] = employee_zipcode
                        response['fields'][i]['optional_value'] = ""
                    elif 'employer_zip' == response['fields'][i]['name']:
                        response['fields'][i]['field_value_original'] = employer_zipcode
                        response['fields'][i]['optional_value'] = ""

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
                            earn.append(earnings[k])
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
                            tax.append(taxes[j])
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
                                pre.append(pre_deduction[l])
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
                                post.append(post_deduction[m])
                                m = m + 1
                            else:
                                response['fields'][i]['alias'] = ''
                                response['fields'][i]['field_value_original'] = ''
                                response['fields'][i]['optional_value'] = ''
                                response['fields'][i]['hrs'] = ''
                                response['fields'][i]['rates'] = ''

                if earn!=[]:
                    if pre!=[] or post!=[] or tax!=[]:
                        if current_gross_pay!='' or current_net_pay!='':

                            self.scan_result = response
                            self.scan_result['error_msg'] = "Successfully Scanned"
                            self.scan_result["status"] = "SUCCESSFUL"
                        else:
                            self.scan_result = response
                            self.scan_result[
                                'error_msg'] = "Successfully uploaded with partially scanned"
                            self.scan_result['status'] = "PARTIAL_DETECTION"
                    else:
                        self.scan_result = response
                        self.scan_result[
                            'error_msg'] = "Successfully uploaded with partially scanned"
                        self.scan_result['status'] = "PARTIAL_DETECTION"
                else:
                    self.scan_result = response
                    self.scan_result[
                        'error_msg'] = "Successfully uploaded with partially scanned"
                    self.scan_result['status'] = "PARTIAL_DETECTION"


                self.scan_result['raw_data'] = self.text
                file_path1 = f_path
                print(self.scan_result)
                print(file_path1)

                return self.scan_result, file_path1

            elif 'Passport' in json_val[doc_id]:
                passport={}
                if filename.rsplit('.', 1)[1] == 'pdf':
                    thread = threading.Thread(target=self.image_to_pdf,
                                              args=("../images/documents_upload/" + filename,
                                                    json_val[doc_id],))
                    thread.start()
                    path = self.img2pdf.get()
                    name_file = os.path.basename(path)
                    f_path = "../images/documents_upload/" + name_file
                    # image_path=f_path
                    thread = threading.Thread(target=self.image_processing_threading,
                                              args=(f_path, json_val[doc_id],))
                else:
                    thread = threading.Thread(target=self.image_processing_threading, args=(
                    "../images/documents_upload/" + filename, json_val[doc_id],))
                thread.start()
                image_path = self.image_processing.get()
                thread = threading.Thread(target=self.get_passport_details, args=(image_path,))
                thread.start()
                (self.text, passport_number, name, dob, issue_date, expiry_date,result, keys, values) = self.passport_details.get()
                if passport_number == '' and name == '' and dob == ''and issue_date == ''and expiry_date == '':
                    file_path = ''
                    self.scan_result['error_msg'] = "Incorrect Document or Unable to Scan"
                    self.scan_result['status'] = "INCORRECT_DOCUMENT"
                    return self.scan_result, file_path
                else:
                    if len(name.split())==3:
                        passport={'passport_no':passport_number,'first_name':name.split()[1],'middle_name':name.split()[2],'last_name':name.split()[0],'dob':dob,'issue_date':issue_date,'expiration_date':expiry_date}
                    elif len(name.split())==2:
                        passport={'passport_no':passport_number,'first_name':name.split()[1],'middle_name':'','last_name':name.split()[0],'dob':dob,'issue_date':issue_date,'expiration_date':expiry_date}
                    elif len(name.split()) == 4:
                        passport = {'passport_no': passport_number, 'first_name': name.split()[1],
                                    'middle_name': name.split()[2]+" "+name.split()[3], 'last_name': name.split()[0], 'dob': dob,
                                    'issue_date': issue_date, 'expiration_date': expiry_date}

                    actual_value = list(passport.keys())
                    actual_value = sorted(actual_value)
                    time.sleep(2)
                    for i in range(len(response['fields'])):
                        for j in range(len(actual_value)):
                            if response['fields'][i]['name'] == actual_value[j]:
                                response['fields'][i]['field_value_original'] = passport[actual_value[j]]
                                pass

                    thread = threading.Thread(target=self.get_ssn_pay_location,args=(passport, image_path, json_val[doc_id],result,))
                    thread.start()
                    (passport_no_location,passport_dict_location, file_path1) = self.location.get()

                    thread = threading.Thread(target=self.confidence_score, args=(image_path, json_val[doc_id], passport,keys, values,))
                    thread.start()
                    (passport_no_score,passport_fn_score,passport_mn_score,passport_ln_score,passport_date_score) = self.confidence.get()

                    for i in range(len(response['fields'])):

                        if response['fields'][i]['name'] == "passport_no":
                            self.location_val.clear()
                            for key, value in passport_no_location.items():
                                self.location_val.append(value)
                                if key in response['fields'][i]['field_value_original']:
                                    response['fields'][i]['location'] = str([self.location_val])
                                    if self.config['field_level'] == "True":

                                        if self.config['high_accuracy'][0] <= int(passport_no_score) <= self.config['high_accuracy'][1]:
                                            response['fields'][i]['confidence'] = passport_no_score

                                        elif self.config['medium_accuracy'][0] <= int(passport_no_score) <= self.config['medium_accuracy'][1]:
                                            response['fields'][i]['confidence'] = passport_no_score

                                        else:
                                            response['fields'][i]['field_value_original'] = ''
                                    else:
                                        response['fields'][i]['confidence'] = passport_no_score

                        elif response['fields'][i]['name'] == "dob":
                            self.location_val.clear()
                            for key, value in passport_dict_location.items():
                                self.location_val.append(value)
                                if key in response['fields'][i]['field_value_original']:
                                    response['fields'][i]['location'] = str([self.location_val])
                                    if self.config['field_level'] == "True":

                                        if self.config['high_accuracy'][0] <= int(passport_date_score) <=self.config['high_accuracy'][1]:
                                            response['fields'][i]['confidence'] = passport_date_score

                                        elif self.config['medium_accuracy'][0] <= int( passport_date_score) <= self.config['medium_accuracy'][1]:
                                            response['fields'][i]['confidence'] = passport_date_score

                                        else:
                                            response['fields'][i]['field_value_original'] = ''
                                    else:
                                        response['fields'][i]['confidence'] = passport_date_score

                        elif response['fields'][i]['name'] == "issue_date":
                            self.location_val.clear()
                            for key, value in passport_dict_location.items():
                                self.location_val.append(value)
                                if key in response['fields'][i]['field_value_original']:
                                    response['fields'][i]['location'] = str([self.location_val])
                                    if self.config['field_level'] == "True":

                                        if self.config['high_accuracy'][0] <= int(passport_date_score) <= \
                                                self.config['high_accuracy'][1]:
                                            response['fields'][i]['confidence'] = passport_date_score

                                        elif self.config['medium_accuracy'][0] <= int(passport_date_score) <= \
                                                self.config['medium_accuracy'][1]:
                                            response['fields'][i]['confidence'] = passport_date_score

                                        else:
                                            response['fields'][i]['field_value_original'] = ''
                                    else:
                                        response['fields'][i]['confidence'] = passport_date_score

                        elif response['fields'][i]['name'] == "expiration_date":
                            self.location_val.clear()
                            for key, value in passport_dict_location.items():
                                self.location_val.append(value)
                                if key in response['fields'][i]['field_value_original']:
                                    response['fields'][i]['location'] = str([self.location_val])
                                    if self.config['field_level'] == "True":

                                        if self.config['high_accuracy'][0] <= int(passport_date_score) <= \
                                                self.config['high_accuracy'][1]:
                                            response['fields'][i]['confidence'] = passport_date_score

                                        elif self.config['medium_accuracy'][0] <= int(passport_date_score) <= \
                                                self.config['medium_accuracy'][1]:
                                            response['fields'][i]['confidence'] = passport_date_score

                                        else:
                                            response['fields'][i]['field_value_original'] = ''
                                    else:
                                        response['fields'][i]['confidence'] = passport_date_score

                        elif response['fields'][i]['name'] == "first_name":
                            self.location_val.clear()
                            for key, value in passport_dict_location.items():
                                self.location_val.append(value)
                                if key in response['fields'][i]['field_value_original']:
                                    response['fields'][i]['location'] = str([self.location_val])
                                    if self.config['field_level'] == "True":

                                        if self.config['high_accuracy'][0] <= int(passport_fn_score) <= \
                                                self.config['high_accuracy'][1]:
                                            response['fields'][i]['confidence'] = passport_fn_score

                                        elif self.config['medium_accuracy'][0] <= int(passport_fn_score) <= \
                                                self.config['medium_accuracy'][1]:
                                            response['fields'][i]['confidence'] = passport_fn_score

                                        else:
                                            response['fields'][i]['field_value_original'] = ''
                                    else:
                                        response['fields'][i]['confidence'] = passport_fn_score

                        elif response['fields'][i]['name'] == "middle_name":
                            self.location_val.clear()
                            for key, value in passport_dict_location.items():
                                self.location_val.append(value)
                                if key in response['fields'][i]['field_value_original']:
                                    response['fields'][i]['location'] = str([self.location_val])
                                    if self.config['field_level'] == "True":

                                        if self.config['high_accuracy'][0] <= int(passport_mn_score) <= \
                                                self.config['high_accuracy'][1]:
                                            response['fields'][i]['confidence'] = passport_mn_score

                                        elif self.config['medium_accuracy'][0] <= int(passport_mn_score) <= \
                                                self.config['medium_accuracy'][1]:
                                            response['fields'][i]['confidence'] = passport_mn_score

                                        else:
                                            response['fields'][i]['field_value_original'] = ''
                                    else:
                                        response['fields'][i]['confidence'] = passport_mn_score

                        elif response['fields'][i]['name'] == "last_name":
                            self.location_val.clear()
                            for key, value in passport_dict_location.items():
                                self.location_val.append(value)
                                if key in response['fields'][i]['field_value_original']:
                                    response['fields'][i]['location'] = str([self.location_val])
                                    if self.config['field_level'] == "True":

                                        if self.config['high_accuracy'][0] <= int(passport_ln_score) <= \
                                                self.config['high_accuracy'][1]:
                                            response['fields'][i]['confidence'] = passport_ln_score

                                        elif self.config['medium_accuracy'][0] <= int(passport_ln_score) <= \
                                                self.config['medium_accuracy'][1]:
                                            response['fields'][i]['confidence'] = passport_ln_score

                                        else:
                                            response['fields'][i]['field_value_original'] = ''
                                    else:
                                        response['fields'][i]['confidence'] = passport_ln_score

                        else:
                            pass

                self.scan_result = response
                detected_null_value_count = detected_value_count = 0

                for i in range(len(response['fields'])):
                    if response['fields'][i]['field_value_original'] == '':
                        detected_null_value_count = detected_null_value_count + 1
                    else:
                        detected_value_count = detected_value_count + 1

                identification_score = int((detected_value_count / len(response['fields'])) * 100)
                all_confidence_score = int(passport_no_score) + int(passport_fn_score)+ int(passport_mn_score)+ int(passport_ln_score) + int(passport_date_score)
                document_score = int((all_confidence_score / 3))
                if document_score > 100:
                    document_score = 100
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

                    elif self.config['medium_accuracy'][0] <= document_score <= self.config['medium_accuracy'][1]:
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

                        for key, value in passport.items():
                            if value == '' or value == ' ':
                                partial_not_detected.append(key)

                            else:
                                partial_detected.append(key)

                        for i in range(len(partial_not_detected)):
                            if partial_not_detected[i] == 'passport_no':
                                partial_not_detected[i] = partial_not_detected[i].replace(
                                    'passport_no',
                                    "Passport Number")

                            elif partial_not_detected[i] == 'first_name':
                                partial_not_detected[i] = partial_not_detected[i].replace(
                                    'first_name',
                                    "First Name")

                            elif partial_not_detected[i] == 'middle_name':
                                partial_not_detected[i] = partial_not_detected[i].replace(
                                    'middle_name',
                                    "Middle Name")

                            elif partial_not_detected[i] == 'last_name':
                                partial_not_detected[i] = partial_not_detected[i].replace(
                                    'last_name',
                                    "Last Name")

                            elif partial_not_detected[i] == 'dob':
                                partial_not_detected[i] = partial_not_detected[i].replace(
                                    'dob',
                                    "Date Of Birth")

                            elif partial_not_detected[i] == 'issue_date':
                                partial_not_detected[i] = partial_not_detected[i].replace(
                                    'issue_date',
                                    "Issued Date")

                            else:
                                partial_not_detected[i] = partial_not_detected[i].replace(
                                    'expiration_date',
                                    "Expiry Date")

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

            self.scan_result['raw_data'] = self.text
            # self.custom_print("Resposne.", self.scan_result)
            print("Resposne.", self.scan_result)
            file_path = file_path1
            self.scan_result['processed_file_name'] = file_path
            return self.scan_result, file_path
        except Exception as E:
            self.custom_print("Exception in all_details main fun.", E)

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