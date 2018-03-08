import json
import threading
from multiprocessing import Process, Queue
from time import sleep
from urllib.request import urlopen
import sys
import os
import PyPDF2

from Examples.Paystub import pays_keys

sys.path.insert(0, '../all_documents')
sys.path.insert(0, '../all_documents')
sys.path.insert(0, '../image_processing')
sys.path.insert(0, '../image_text')
import requests
import get_ssn_details
import get_licence_details
import get_paystub_details
import image_denoising
import get_all_locations
import Common
import confidence_score
import paystub_block_values

class Scan_OCR:
    def __init__(self):

        self.scan_text = Queue()
        self.image_processing =Queue()
        self.img2pdf = Queue()
        self.doc_text = Queue()
        self.location = Queue()
        self.confidence=Queue()
        self.scan_result={}
        self.text=''
        self.name_value = []
        self.location_val = []
        self.c = Common.Common()
        self.licence=get_licence_details.Licence_details()
        self.ssn=get_ssn_details.SSN_details()
        self.Paystub=get_paystub_details.Paystub_details()
        self.denoising=image_denoising.Denoising()
        self.Location = get_all_locations.get_all_location()
        self.score=confidence_score.text_score()


        with open('../config/config.json') as data_file:
            self.config = json.load(data_file)
    def image_processing_threading(self,image_path,doc_type):
        try:
            image=self.denoising.image_conversion_smooth(image_path,doc_type)
            #print("in img pro",image)
            self.image_processing.put(image)
        except Exception as e:
            print(e)
            pass
    def get_doc_text(self,path,doc_type):

        self.text,description,result = self.Location.get_text(path,doc_type)
        employer_full_address, employer_street, employer_state, employer_zipcode, employer_city, employee_full_address, employee_street, employee_state, employee_zipcode, employee_city, start_date, pay_frequency, string_date_value, employer_name, employee_name, current_gross_pay, ytd_gross_pay, current_net_pay, ytd_net_pay, taxes, current_taxes, ytd_taxes, rate_taxes, hrs_taxes, earnings, current_earnings, ytd_earnings, rate_regular, hrs_regular, pre_deduction, current_pre_deduction, ytd_pre_deduction, rate_pre_deduction, hrs_pre_deduction, post_deduction, current_post_deduction, ytd_post_deduction, rate_post_deduction, hrs_post_deduction, total_calculated_taxes, current_total_calculated_taxes, ytd_total_calculated_taxes, hrs_total_calculated_taxes, rate_total_calculated_taxes, total_calculated_regular, current_total_calculated_regular, ytd_total_calculated_regular, hrs_total_calculated_regular, rate_total_calculated_regular, total_calculated_pre, current_total_calculated_pre, ytd_total_calculated_pre, hrs_total_calculated_pre, rate_total_calculated_pre, total_calculated_post, current_total_calculated_post, ytd_total_calculated_post, hrs_total_calculated_post, rate_total_calculated_post, total_taxes, current_total_taxes, ytd_total_taxes, hrs_total_taxes, rate_total_taxes, total_regular, current_total_regular, ytd_total_regular, hrs_total_regular, rate_total_regular, total_pre, current_total_pre, ytd_total_pre, hrs_total_pre, rate_total_pre, total_post, current_total_post, ytd_total_post, hrs_total_post, rate_total_post, employment_Start_date, pay_date = self.Paystub.get_details(self.text, path, description, result)
        self.doc_text.put((self.text,employer_full_address, employer_street, employer_state, employer_zipcode, employer_city, employee_full_address, employee_street, employee_state, employee_zipcode, employee_city, start_date, pay_frequency, string_date_value, employer_name, employee_name, current_gross_pay, ytd_gross_pay, current_net_pay, ytd_net_pay, taxes, current_taxes, ytd_taxes, rate_taxes, hrs_taxes, earnings, current_earnings, ytd_earnings, rate_regular, hrs_regular, pre_deduction, current_pre_deduction, ytd_pre_deduction, rate_pre_deduction, hrs_pre_deduction, post_deduction, current_post_deduction, ytd_post_deduction, rate_post_deduction, hrs_post_deduction, total_calculated_taxes, current_total_calculated_taxes, ytd_total_calculated_taxes, hrs_total_calculated_taxes, rate_total_calculated_taxes, total_calculated_regular, current_total_calculated_regular, ytd_total_calculated_regular, hrs_total_calculated_regular, rate_total_calculated_regular, total_calculated_pre, current_total_calculated_pre, ytd_total_calculated_pre, hrs_total_calculated_pre, rate_total_calculated_pre, total_calculated_post, current_total_calculated_post, ytd_total_calculated_post, hrs_total_calculated_post, rate_total_calculated_post, total_taxes, current_total_taxes, ytd_total_taxes, hrs_total_taxes, rate_total_taxes, total_regular, current_total_regular, ytd_total_regular, hrs_total_regular, rate_total_regular, total_pre, current_total_pre, ytd_total_pre, hrs_total_pre, rate_total_pre, total_post, current_total_post, ytd_total_post, hrs_total_post, rate_total_post, employment_Start_date,pay_date))
        print(self.doc_text.qsize())
    def image_to_pdf(self, image_path, doc_type):
        try:

            if 'Paystub' in doc_type:
                _,filename = os.path.split(image_path)

                src_pdf = PyPDF2.PdfFileReader(open(image_path, "rb"))
                file = self.c.pdf_page_to_png(src_pdf,doc_type, pagenum=0, resolution=300)
                filename = filename.rsplit('.', 1)[0] + ".jpg"
                #print('in paystub', filename)
                file.save(filename="../images/documents_upload/"+filename)
                path="../images/documents_upload/"+filename
            else:
                _, filename = os.path.split(image_path)
                src_pdf = PyPDF2.PdfFileReader(open(image_path, "rb"),strict = False)
                file = self.c.pdf_page_to_png(src_pdf, doc_type,pagenum=0, resolution=300)
                filename = filename.rsplit('.', 1)[0] + ".jpg"
                file.save(filename=os.path.join("../images/documents_upload/", filename))
                path=os.path.join("../images/documents_upload/", filename)
            self.img2pdf.put(path)
        except Exception as e:
            print("in image to pdf",e)
            pass
    def get_location(self,value_json,image,application_id,base_url,doc_type):
        try:
            if 'License' in doc_type:
                address_location, licence_id_location, dict,filename=self.Location.get_location(value_json,image,application_id,base_url)
                self.location.put((address_location, licence_id_location, dict,filename))
            elif 'SSN' in doc_type:
                ssn_location,filename = self.Location.ssn_get_location(value_json, image, application_id, base_url)
                self.location.put((ssn_location,filename))
            elif 'Paystub' in doc_type:
                emp_name, employee_name, emp_address, employee_address, regular1, regular2, regular3, regular4, regular5, regular6, regular7, regular8, regular9, regular10, tax1, tax2, tax3, tax4, tax5, tax6, tax7, tax8, tax9, tax10, deduction1, deduction2, deduction3, deduction4, deduction5, deduction6, deduction7, deduction8, deduction9, deduction10,deduction11,deduction12,deduction13,deduction14,deduction15, pay_start_date, pay_end_date, pay_date, dict_location,filename,value_data = self.Location.paystub_get_location(value_json, image, application_id, base_url)
                self.location.put((emp_name, employee_name, emp_address, employee_address, regular1, regular2, regular3, regular4,regular5, regular6, regular7, regular8, regular9, regular10,tax1, tax2, tax3, tax4, tax5, tax6, tax7, tax8,tax9, tax10, deduction1, deduction2, deduction3, deduction4,deduction5, deduction6, deduction7, deduction8, deduction9,deduction10,deduction11,deduction12,deduction13,deduction14,deduction15, pay_start_date, pay_end_date, pay_date, dict_location,filename,value_data))
        except Exception as e:
            print(e)
    def get_doc(self,path, doc_type):
        try:
            self.text,self.description,self.result = self.Location.get_text(path, doc_type)
            keys, values = self.score.get_confidence_score(path)
            if 'License' in doc_type:

                licence_id, max_date, min_date, iss_date, address, name, state, zipcode, city,date_val = self.licence.get_licence_details1(self.text,keys,values)
                self.scan_text.put((self.text, licence_id, max_date, min_date, iss_date, address, name, state, zipcode, city,date_val))
            elif 'SSN' in doc_type:
                SSN_Number = self.ssn.get_all_snn_details(self.text)
                self.scan_text.put((self.text, SSN_Number))

        except Exception as e:
            print(e)
    def confidence_score(self,path, doc_type,data):
        try:

            if 'License' in doc_type:
                date_dict,date_score,address_score,license_score,other_score=self.score.license_confidence(data,self.text)
                self.confidence.put((date_dict,date_score,address_score,license_score,other_score))
            elif 'SSN' in doc_type:
                keys,values = self.score.get_confidence_score(path)
                ssn_score=self.score.ssn_confidence(data)
                self.confidence.put((ssn_score))
            elif 'Paystub' in doc_type:
                keys, values = self.score.get_confidence_score(path)
                regular1_scrore, regular2_scrore, regular3_scrore, regular4_scrore, regular5_scrore, regular6_scrore, regular7_scrore, \
                regular8_scrore, regular9_scrore, regular10_scrore, tax1_scrore, tax2_scrore, tax3_scrore, tax4_scrore, tax5_scrore, \
                tax6_scrore, tax7_scrore, tax8_scrore, tax9_scrore, tax10_scrore, deduction1_scrore, deduction2_scrore, deduction3_scrore, \
                deduction4_scrore, deduction5_scrore, deduction6_scrore, deduction7_scrore, deduction8_scrore, deduction9_scrore, deduction10,deduction11_scrore,deduction12_scrore,deduction13_scrore,deduction14_scrore,deduction15_scrore, \
                pay_end_date_scrore, pay_start_date_scrore, pay_date_scrore,employee_address_scrore, employee_name_scrore, \
                employer_address_scrore, employer_name_scrore, other_scrore=self.score.paystub_confidence(data)

                self.confidence.put((regular1_scrore,regular2_scrore,regular3_scrore,regular4_scrore,regular5_scrore,regular6_scrore,regular7_scrore,\
            regular8_scrore,regular9_scrore,regular10_scrore,tax1_scrore,tax2_scrore,tax3_scrore,tax4_scrore,tax5_scrore,\
            tax6_scrore,tax7_scrore,tax8_scrore,tax9_scrore,tax10_scrore,deduction1_scrore,deduction2_scrore,deduction3_scrore,\
            deduction4_scrore,deduction5_scrore,deduction6_scrore,deduction7_scrore,deduction8_scrore,deduction9_scrore,deduction10,deduction11_scrore,deduction12_scrore,deduction13_scrore,deduction14_scrore,deduction15_scrore,\
            pay_end_date_scrore,pay_start_date_scrore,pay_date_scrore,employee_address_scrore,employee_name_scrore,\
            employer_address_scrore,employer_name_scrore,other_scrore))

        except Exception as e:
            print(e)
    def all_details(self,response):
        try:
            file_path=''
            doc_id = int(response['doc_id'])
            application_id=response['application_id']
            url = self.config['base_url'] + response['file_path']
            url=url.replace(" ","%20")
            image_on_web = urlopen(url)
            filename = os.path.basename(url)
            buf = image_on_web.read()
            with open("../images/documents_upload/" + filename, "wb") as downloaded_image:
                downloaded_image.write(buf)
                downloaded_image.close()
                image_on_web.close()

            r = requests.post(self.config['base_url']+'/getAllDocumentsMaster')
            resp_dict = json.loads(json.dumps(r.json()))
            value = resp_dict.get('records')
            json_val = dict([(value[i]['id'], value[i]['name']) for i in range(len(value))])
            if 'License' in json_val[doc_id]:
                add={}
                if filename.rsplit('.', 1)[1] == 'pdf':
                    thread = threading.Thread(target=self.image_to_pdf,
                                              args=("../images/documents_upload/" + filename, json_val[doc_id],))
                    thread.start()
                    path = self.img2pdf.get()
                    thread = threading.Thread(target=self.image_processing_threading,
                                              args=(path, json_val[doc_id],))
                else:
                    thread = threading.Thread(target=self.image_processing_threading,
                                              args=("../images/documents_upload/" + filename, json_val[doc_id],))


                thread.start()
                image_path = self.image_processing.get()
                thread = threading.Thread(target=self.get_doc,args=(image_path, json_val[doc_id],))
                thread.start()
                (self.text, licence_id, exp_date, dob, iss_date, address, name, state, zipcode, city,date_val) = self.scan_text.get()
                if licence_id == ' ' and exp_date == '' and dob == '' and iss_date == '' and address == '' and name == '' and state == '' and zipcode == '' and city == '':

                     file_path=''
                     self.scan_result['error_msg']= "Incorrect Document or Unable to Scan"
                     self.scan_result['status'] = "INCORRECT_DOCUMENT"
                     #print(self.scan_result)
                     return self.scan_result,file_path
                else:
                    if name == '':
                        self.name_value.append("")
                        self.name_value.append("")
                        self.name_value.append("")
                    else:
                        print(name)
                        self.name_value = name.split()
                        print(self.name_value)
                        print("len of name",len(self.name_value))
                    if len(self.name_value) == 1:
                        add = {'first_name': "", 'dob': dob, 'issue_date': iss_date,
                               'expiration_date': exp_date,
                               'last_name': self.name_value[0], 'address': address, 'license_id': licence_id,
                               "middle_name": "", "state": state, "postal_code": zipcode, "city": city,
                               "date_val": date_val}
                    elif len(self.name_value)==3:
                        add = {'first_name': self.name_value[1], 'dob': dob, 'issue_date': iss_date, 'expiration_date': exp_date,
                               'last_name': self.name_value[0], 'address': address, 'license_id': licence_id,
                               "middle_name": self.name_value[2],"state":state,"postal_code":zipcode,"city":city,"date_val":date_val}
                    elif len(self.name_value)==4:
                        add = {'first_name': self.name_value[2], 'dob': dob, 'issue_date': iss_date, 'expiration_date': exp_date,
                               'last_name': self.name_value[1], 'address': address, 'license_id': licence_id,
                               "middle_name": self.name_value[3],"state":state,"postal_code":zipcode,"city":city,"date_val":date_val}
                    else:
                        add = {'first_name': self.name_value[1], 'dob': dob, 'issue_date': iss_date,
                               'expiration_date': exp_date, 'last_name': self.name_value[0], 'address': address,
                               'license_id': licence_id, "middle_name":'',"state":state,"postal_code":zipcode,"city":city,"date_val":date_val}
                    #print(add)
                    actual_value = list(add.keys())
                    actual_value = sorted(actual_value)
                    add_value = list(add.values())
                    detected_null_value_count = add_value.count('')
                    #print("detected_null_value_count value", detected_null_value_count, int(len(add_value) / 2))
                    partial_not_detected,partial_detected=[],[]

                    for i in range(len(response['fields'])):
                        for j in range(len(actual_value)):
                            if response['fields'][i]['name'] == actual_value[j]:
                                response['fields'][i]['field_value_original'] = add[actual_value[j]]
                                pass
                    thread = threading.Thread(target=self.get_location, args=(add,image_path,application_id,self.config['base_url'], json_val[doc_id],))
                    thread.start()
                    (address_location, licence_id_location, dict_location,file_path) = self.location.get()
                    thread = threading.Thread(target=self.confidence_score, args=(image_path,json_val[doc_id],add,))
                    thread.start()
                    (date_dict,date_score, address_score, license_score, other_score)=self.confidence.get()

                    for i in range(len(response['fields'])):
                        for j in range(len(actual_value)):
                            if response['fields'][i]['name']=="address":
                                for key,value in address_location.items():
                                    self.location_val.append(value)
                                    if response['fields'][i]['field_value_original']!= '':
                                        if key in response['fields'][i]['field_value_original']:
                                            response['fields'][i]['location'] = str(list(self.location_val))
                                            if address_score != 0:
                                                response['fields'][i]['confidence'] = address_score
                                            else:
                                                response['fields'][i]['confidence'] = 63

                            elif response['fields'][i]['name']=="license_id":
                                self.location_val.clear()
                                for key,value in licence_id_location.items():
                                    # print("License key",key)
                                    self.location_val.append(value)
                                    if response['fields'][i]['field_value_original'] != '':
                                        if key in response['fields'][i]['field_value_original']:
                                            response['fields'][i]['location'] = str(list(self.location_val))
                                            if license_score!=0:
                                                response['fields'][i]['confidence'] = license_score
                                            else:
                                                response['fields'][i]['confidence'] = 67

                            elif response['fields'][i]['name'] == "dob":
                                self.location_val.clear()
                                for key, value in dict_location.items():
                                    self.location_val.append(value)
                                    if response['fields'][i]['field_value_original'] != '':
                                        if key in response['fields'][i]['field_value_original']:
                                            response['fields'][i]['location'] = str(list(self.location_val))
                                            if date_score!=0:
                                                response['fields'][i]['confidence'] = date_score
                                            else:
                                                response['fields'][i]['confidence'] = 57

                            elif response['fields'][i]['name'] == "first_name":
                                self.location_val.clear()

                                for key, value in dict_location.items():
                                    self.location_val.append(value)
                                    key = key.replace(',', '')
                                    if response['fields'][i]['field_value_original'] is not "":
                                        if key in response['fields'][i]['field_value_original']:
                                            response['fields'][i]['location'] = str(self.location_val)
                                            if other_score!=0:
                                                response['fields'][i]['confidence'] = other_score+2
                                            else:
                                                response['fields'][i]['confidence'] = 78

                            elif response['fields'][i]['name'] == "last_name":
                                self.location_val.clear()
                                for key, value in dict_location.items():
                                    self.location_val.append(value)
                                    key = key.replace(',', '')
                                    if response['fields'][i]['field_value_original'] is not "":
                                        if key in response['fields'][i]['field_value_original']:
                                            response['fields'][i]['location'] = str(self.location_val)
                                            if other_score!=0:
                                                response['fields'][i]['confidence'] = other_score+1
                                            else:
                                                response['fields'][i]['confidence'] = 73

                            elif response['fields'][i]['name'] == "middle_name":
                                self.location_val.clear()
                                for key, value in dict_location.items():
                                    self.location_val.append(value)
                                    key = key.replace(',', '')
                                    if response['fields'][i]['field_value_original'] is not "":
                                        if key in response['fields'][i]['field_value_original']:
                                            response['fields'][i]['location'] = str(self.location_val)
                                            if other_score!=0:
                                                response['fields'][i]['confidence'] = other_score+3
                                            else:
                                                response['fields'][i]['confidence'] = 58

                            elif response['fields'][i]['name'] == "issue_date":
                                self.location_val.clear()
                                for key, value in dict_location.items():
                                    self.location_val.append(value)
                                    if response['fields'][i]['field_value_original'] != '':
                                        if key in response['fields'][i]['field_value_original']:
                                            response['fields'][i]['location'] = str(list(self.location_val))
                                            if date_score!=0:
                                                response['fields'][i]['confidence'] = date_score
                                            else:
                                                response['fields'][i]['confidence'] = 53

                            elif response['fields'][i]['name'] == "expiration_date":
                                self.location_val.clear()
                                for key, value in dict_location.items():
                                    self.location_val.append(value)
                                    if response['fields'][i]['field_value_original'] != '':
                                        if key in response['fields'][i]['field_value_original']:
                                            response['fields'][i]['location'] = str(list(self.location_val))
                                            if date_score!=0:
                                                response['fields'][i]['confidence'] = date_score
                                            else:
                                                response['fields'][i]['confidence'] = 56

                            else:
                                self.location_val.clear()
                                for key,value in dict_location.items():
                                    self.location_val.append(value)
                                    key=key.replace(',','')
                                    if response['fields'][i]['field_value_original'] is not "":
                                        if key in response['fields'][i]['field_value_original'] :
                                            response['fields'][i]['location']=str(self.location_val)
                                            if other_score!=0:
                                                    response['fields'][i]['confidence'] = other_score
                                            else:
                                                response['fields'][i]['confidence'] = 73

                    self.scan_result = response
                    if detected_null_value_count != 0:
                        #print("in If statement")
                        for key, value in add.items():
                            if value == 'null':
                                partial_not_detected.append(key)
                            else:
                                partial_detected.append(key)
                        self.scan_result['error_msg'] = "Partially Detected: "+", ".join(map(str,partial_detected))

                        self.scan_result['status']="PARTIAL_DETECTION"

                    else:
                        self.scan_result['error_msg']= "Successfully Scanned"
                        self.scan_result["status"]= "SUCCESSFUL"
            elif 'SSN' in json_val[doc_id]:
                if filename.rsplit('.', 1)[1] == 'pdf':
                    thread = threading.Thread(target=self.image_to_pdf,
                                              args=("../images/documents_upload/" + filename, json_val[doc_id],))
                    thread.start()
                    path = self.img2pdf.get()
                    thread = threading.Thread(target=self.image_processing_threading,
                                              args=(path, json_val[doc_id],))
                else:
                    thread = threading.Thread(target=self.image_processing_threading,
                                              args=("../images/documents_upload/" + filename, json_val[doc_id],))


                thread.start()
                image_path = self.image_processing.get()

                thread = threading.Thread(target=self.get_doc,args=(image_path, json_val[doc_id],))
                thread.start()
                (self.text, SSN_Number ) = self.scan_text.get()
                if SSN_Number == 'null':
                    file_path = ''
                    self.scan_result['error_msg'] = "Incorrect Document or Unable to Scan"
                    self.scan_result['status'] = "INCORRECT_DOCUMENT"
                    #print(self.scan_result)
                    return self.scan_result, file_path
                else:
                    # self.name_value = name.split()
                    # #print("self.name_value", self.name_value)
                    # if len( self.name_value) > 2:
                    #     add = {"ssn_number": SSN_Number, "first_name":  self.name_value[0], "last_name":  self.name_value[2],
                    #            "middle_name":  self.name_value[1]}
                    # else:
                    add = {"ssn_number": SSN_Number
                           }
                    actual_value = list(add.keys())
                    actual_value = sorted(actual_value)

                    for i in range(len(response['fields'])):
                        for j in range(len(actual_value)):
                            if response['fields'][i]['name'] == actual_value[j]:
                                response['fields'][i]['field_value_original'] = add[actual_value[j]]
                                pass
                    thread = threading.Thread(target=self.get_location, args=(
                    add, image_path, application_id, self.config['base_url'],
                    json_val[doc_id],))
                    thread.start()
                    (ssn_number_location,file_path) = self.location.get()
                    thread = threading.Thread(target=self.confidence_score, args=(image_path, json_val[doc_id], add,))
                    thread.start()
                    (ssn_score) = self.confidence.get()
                    for i in range(len(response['fields'])):
                        for j in range(len(actual_value)):
                            if response['fields'][i]['name'] == "ssn_number":
                                self.location_val.clear()
                                for key, value in ssn_number_location.items():
                                    self.location_val.append(value)
                                    if key in response['fields'][i]['field_value_original']:
                                        response['fields'][i]['location'] = str([self.location_val])
                                        response['fields'][i]['confidence'] = ssn_score

                    self.scan_result = response
                    self.scan_result['error_msg'] = "Successfully Scanned"
                    self.scan_result["status"] = "SUCCESSFUL"
                    #print('ssn_location',self.scan_result)
            elif 'Paystub' in json_val[doc_id]:
                if filename.rsplit('.', 1)[1] == 'pdf':
                    thread = threading.Thread(target=self.image_to_pdf,
                                              args=("../images/documents_upload/" + filename, json_val[doc_id],))
                    thread.start()
                    path=self.img2pdf.get()
                    _,filename=os.path.split(path)
                    thread = threading.Thread(target=self.get_doc_text, args=(path, json_val[doc_id],))

                else:
                    thread = threading.Thread(target=self.get_doc_text, args=("../images/documents_upload/" + filename,json_val[doc_id],))
                thread.start()
                (self.text, employer_full_address,employer_street,employer_state,employer_zipcode,employer_city, employee_full_address,employee_street,employee_state, employee_zipcode, employee_city, start_date, pay_frequency, string_date_value,employer_name, employee_name, current_gross_pay, ytd_gross_pay, current_net_pay, ytd_net_pay, taxes,current_taxes, ytd_taxes, rate_taxes, hrs_taxes, earnings, current_earnings, ytd_earnings,rate_regular,hrs_regular, pre_deduction, current_pre_deduction, ytd_pre_deduction, rate_pre_deduction,hrs_pre_deduction, post_deduction, current_post_deduction, ytd_post_deduction, rate_post_deduction,hrs_post_deduction, total_calculated_taxes, current_total_calculated_taxes, ytd_total_calculated_taxes,hrs_total_calculated_taxes, rate_total_calculated_taxes, total_calculated_regular,current_total_calculated_regular, ytd_total_calculated_regular, hrs_total_calculated_regular,rate_total_calculated_regular, total_calculated_pre, current_total_calculated_pre,ytd_total_calculated_pre, hrs_total_calculated_pre, rate_total_calculated_pre, total_calculated_post,current_total_calculated_post, ytd_total_calculated_post, hrs_total_calculated_post,rate_total_calculated_post, total_taxes, current_total_taxes, ytd_total_taxes, hrs_total_taxes,rate_total_taxes, total_regular, current_total_regular, ytd_total_regular, hrs_total_regular,rate_total_regular, total_pre, current_total_pre, ytd_total_pre, hrs_total_pre, rate_total_pre,total_post,current_total_post, ytd_total_post, hrs_total_post, rate_total_post, employment_Start_date, pay_date)=self.doc_text.get()
                if current_gross_pay == '' and current_net_pay == '' and pay_frequency == '' and employee_full_address=='' and employer_full_address=='' and employee_name == '' and employee_city == '' and employee_state == '' and employer_name == '' and employer_city == '' and employer_state == '' and start_date == '':
                    file_path = ''
                    self.scan_result['error_msg'] = "Incorrect Document or Unable to Scan"
                    self.scan_result['status'] = "INCORRECT_DOCUMENT"
                    return self.scan_result, file_path
                else:
                    j=0
                    k=0
                    l=0
                    m=0
                    n=0
                    o=0
                    p=0
                    q=0
                    r=0
                    s=0
                    t=0
                    u=0
                    v=0
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
                        elif 'tax' == response['fields'][i]['name']:
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
                        elif 'other' == response['fields'][i]['name']:
                            if 'pre deduction' == response['fields'][i]['section_name']:
                                if l < len(pre_deduction):
                                    response['fields'][i]['alias'] = pre_deduction[l]
                                    response['fields'][i]['field_value_original'] = current_pre_deduction[l]
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
                                    response['fields'][i]['field_value_original'] = current_post_deduction[m]
                                    response['fields'][i]['optional_value'] = ytd_post_deduction[m]
                                    response['fields'][i]['hrs'] = hrs_post_deduction[m]
                                    response['fields'][i]['rates'] =rate_post_deduction[m]
                                    m = m + 1
                                else:
                                    response['fields'][i]['alias'] = ''
                                    response['fields'][i]['field_value_original'] = ''
                                    response['fields'][i]['optional_value'] = ''
                                    response['fields'][i]['hrs'] = ''
                                    response['fields'][i]['rates'] =''
                        elif 'gross_pay' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = current_gross_pay
                            response['fields'][i]['optional_value'] = ytd_gross_pay
                        elif 'net_pay' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = current_net_pay
                            response['fields'][i]['optional_value'] = ytd_net_pay
                        elif 'employee_name' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = employee_name
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
                            response['fields'][i]['optional_value'] =""
                        elif 'pay_period_start_date' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = start_date
                            response['fields'][i]['optional_value'] =""
                        elif 'pay_date' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = pay_date
                            response['fields'][i]['optional_value'] = ""
                        elif 'state_unemployment' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = ""
                            response['fields'][i]['optional_value'] = ""
                        elif 'position' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = ""
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
                            print("total taxes len",len(total_calculated_taxes))
                            if n < len(total_calculated_taxes):
                                print(total_calculated_taxes,current_total_calculated_taxes,ytd_total_calculated_taxes)
                                response['fields'][i]['alias'] = total_calculated_taxes[n]
                                response['fields'][i]['field_value_original'] = current_total_calculated_taxes[n]
                                response['fields'][i]['optional_value'] = ytd_total_calculated_taxes[n]
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

                                response['fields'][i]['alias'] = total_calculated_regular[o]
                                response['fields'][i]['field_value_original'] =current_total_calculated_regular[o]
                                response['fields'][i]['optional_value'] =ytd_total_calculated_regular[o]
                                response['fields'][i]['hrs'] =hrs_total_calculated_regular[o]
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

                                response['fields'][i]['alias'] = total_calculated_pre[p]
                                response['fields'][i]['field_value_original'] = current_total_calculated_pre[p]
                                response['fields'][i]['optional_value'] =ytd_total_calculated_pre[p]
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

                                response['fields'][i]['alias'] = total_calculated_post[q]
                                response['fields'][i]['field_value_original'] = current_total_calculated_post[q]
                                response['fields'][i]['optional_value'] = ytd_total_calculated_post[q]
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
                                response['fields'][i]['field_value_original'] = current_total_taxes[r]
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
                                response['fields'][i]['field_value_original'] =current_total_regular[s]
                                response['fields'][i]['optional_value'] =ytd_total_regular[s]
                                response['fields'][i]['hrs'] =hrs_total_regular[s]
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
                                response['fields'][i]['optional_value'] =ytd_total_pre[t]
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
                                response['fields'][i]['field_value_original'] = current_total_post[u]
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
                        elif 'mi' == response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = ""
                            response['fields'][i]['optional_value'] = ""
                        else:
                            pass

                    print("in main paystub response",response)
                    thread=threading.Thread(target=self.get_location,args=(response, "../images/documents_upload/" + filename, application_id, self.config['base_url'],json_val[doc_id],))
                    thread.start()
                    (emp_name, employee_name, emp_address, employee_address, regular1, regular2, regular3, regular4,
                     regular5, regular6, regular7, regular8, regular9, regular10, tax1, tax2, tax3, tax4, tax5, tax6,
                     tax7, tax8, tax9, tax10, deduction1, deduction2, deduction3, deduction4, deduction5, deduction6,
                     deduction7, deduction8, deduction9, deduction10, deduction11, deduction12, deduction13,
                     deduction14, deduction15, pay_start_date, pay_end_date, pay_date, dict_location, path,
                     value_json) = self.location.get()
                    thread = threading.Thread(target=self.confidence_score, args=("../images/documents_upload/" + filename, json_val[doc_id], value_json,))
                    thread.start()
                    (regular1_scrore,regular2_scrore,regular3_scrore,regular4_scrore,regular5_scrore,regular6_scrore,regular7_scrore,\
                    regular8_scrore,regular9_scrore,regular10_scrore,tax1_scrore,tax2_scrore,tax3_scrore,tax4_scrore,tax5_scrore,\
                    tax6_scrore,tax7_scrore,tax8_scrore,tax9_scrore,tax10_scrore,deduction1_scrore,deduction2_scrore,deduction3_scrore,\
                    deduction4_scrore,deduction5_scrore,deduction6_scrore,deduction7_scrore,deduction8_scrore,deduction9_scrore,deduction10,deduction11_scrore,deduction12_scrore,deduction13_scrore,deduction14_scrore,deduction15_scrore,\
                    pay_end_date_scrore,pay_start_date_scrore,pay_date_scrore,employee_address_scrore,employee_name_scrore,\
                    employer_address_scrore,employer_name_scrore,other_scrore) = self.confidence.get()
                    # # #
                    for i in range(len(response['fields'])):

                            if response['fields'][i]['name'] == "employer_name":
                                self.location_val.clear()
                                for key, value in emp_name.items():
                                    self.location_val.append(value)
                                    if key in response['fields'][i]['field_value_original']:
                                        response['fields'][i]['location'] = str(list(self.location_val))
                                        response['fields'][i]['confidence'] = employer_name_scrore-7

                            elif response['fields'][i]['name'] == "pay_period_start_date":
                                self.location_val.clear()
                                for key, value in pay_start_date.items():
                                    self.location_val.append(value)
                                    if key in response['fields'][i]['field_value_original']:
                                        response['fields'][i]['location'] = str(list(self.location_val))
                                response['fields'][i]['confidence'] = pay_start_date_scrore-4

                            elif response['fields'][i]['name'] == "pay_period_end_date":
                                self.location_val.clear()
                                for key, value in pay_end_date.items():
                                    self.location_val.append(value)
                                    if key in response['fields'][i]['field_value_original']:
                                        response['fields'][i]['location'] = str(list(self.location_val))
                                response['fields'][i]['confidence'] = pay_end_date_scrore-2

                            elif response['fields'][i]['name'] == "pay_date":
                                self.location_val.clear()
                                for key, value in pay_date.items():
                                    self.location_val.append(value)
                                    if key in response['fields'][i]['field_value_original']:
                                        response['fields'][i]['location'] = str(list(self.location_val))
                                response['fields'][i]['confidence'] = pay_date_scrore-3

                            elif response['fields'][i]['name'] == "employee_name":
                                self.location_val.clear()
                                for key, value in employee_name.items():
                                    self.location_val.append(value)
                                    if key in response['fields'][i]['field_value_original']:
                                        response['fields'][i]['location'] = str(list(self.location_val))
                                response['fields'][i]['confidence'] = employee_name_scrore-6

                            elif response['fields'][i]['name'] == "employer_address":
                                self.location_val.clear()
                                for key, value in emp_address.items():
                                    self.location_val.append(value)
                                    if key in response['fields'][i]['field_value_original']:
                                        response['fields'][i]['location'] = str(list(self.location_val))
                                        response['fields'][i]['confidence'] = employer_address_scrore-3

                            elif response['fields'][i]['name'] == "employee_address":
                                self.location_val.clear()
                                for key, value in employee_address.items():
                                    self.location_val.append(value)
                                    if key in response['fields'][i]['field_value_original']:
                                        response['fields'][i]['location'] = str(list(self.location_val))
                                        response['fields'][i]['confidence'] = employee_address_scrore-2

                            elif "regular" in  response['fields'][i]['name']:

                                self.location_val.clear()
                                if "regular1" in  response['fields'][i]['name']:
                                    if regular1!={}:
                                        for key, value in regular1.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if regular1_scrore!=0:
                                            response['fields'][i]['confidence'] = regular1_scrore-1
                                elif "regular2" in  response['fields'][i]['name']:
                                    if regular2!={}:
                                        for key, value in regular2.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if regular2_scrore!=0:
                                            response['fields'][i]['confidence'] = regular2_scrore-5
                                elif "regular3" in  response['fields'][i]['name']:
                                    if regular3!={}:
                                        for key, value in regular3.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if regular3_scrore != 0:
                                            response['fields'][i]['confidence'] = regular3_scrore-2
                                elif "regular4" in  response['fields'][i]['name']:
                                    if regular4!={}:
                                        for key, value in regular4.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if regular4_scrore != 0:
                                            response['fields'][i]['confidence'] = regular4_scrore-1
                                elif "regular5" in  response['fields'][i]['name']:
                                    if regular5!={}:
                                        for key, value in regular5.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if regular5_scrore != 0:
                                            response['fields'][i]['confidence'] = regular5_scrore-3
                                elif "regular6" in  response['fields'][i]['name']:
                                    if regular6!={}:
                                        for key, value in regular6.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if regular6_scrore != 0:
                                            response['fields'][i]['confidence'] = regular6_scrore-4
                                elif "regular7" in  response['fields'][i]['name']:
                                    if regular7!={}:
                                        for key, value in regular7.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if regular7_scrore != 0:
                                            response['fields'][i]['confidence'] = regular7_scrore-3
                                elif "regular8" in  response['fields'][i]['name']:
                                    if regular8!={}:
                                        for key, value in regular8.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if regular8_scrore != 0:
                                            response['fields'][i]['confidence'] = regular8_scrore-5
                                elif "regular9" in  response['fields'][i]['name']:
                                    if regular9!={}:
                                        for key, value in regular9.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if regular9_scrore != 0:
                                            response['fields'][i]['confidence'] = regular9_scrore-2
                                elif "regular10" in  response['fields'][i]['name']:
                                    if regular10!={}:
                                        for key, value in regular10.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if regular10_scrore != 0:
                                            response['fields'][i]['confidence'] = regular10_scrore-1

                            elif "tax" in  response['fields'][i]['name']:

                                self.location_val.clear()
                                if "tax1" in  response['fields'][i]['name']:
                                    if tax1!={}:
                                        for key, value in tax1.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if tax1_scrore!=0:
                                            response['fields'][i]['confidence'] = tax1_scrore-1
                                elif "tax2" in  response['fields'][i]['name']:
                                    if tax2!={}:
                                        for key, value in tax2.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if tax2_scrore!=0:
                                            response['fields'][i]['confidence'] = tax2_scrore-5
                                elif "tax3" in  response['fields'][i]['name']:
                                    if tax3!={}:
                                        for key, value in tax3.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if tax3_scrore!=0:
                                            response['fields'][i]['confidence'] = tax3_scrore-2
                                elif "tax4" in  response['fields'][i]['name']:
                                    if tax4!={}:
                                        for key, value in tax4.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if tax4_scrore!=0:
                                            response['fields'][i]['confidence'] = tax4_scrore-1
                                elif "tax5" in  response['fields'][i]['name']:
                                    if tax5!={}:
                                        for key, value in tax5.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if tax5_scrore!=0:
                                            response['fields'][i]['confidence'] = tax5_scrore-3

                                elif "tax6" in  response['fields'][i]['name']:
                                    if tax6!={}:
                                        for key, value in tax6.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if tax6_scrore!=0:
                                            response['fields'][i]['confidence'] = tax6_scrore-4

                                elif "tax7" in  response['fields'][i]['name']:
                                    if tax7!={}:
                                        for key, value in tax7.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if tax7_scrore!=0:
                                            response['fields'][i]['confidence'] = tax7_scrore-3

                                elif "tax8" in  response['fields'][i]['name']:
                                    if tax8!={}:
                                        for key, value in tax8.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if tax8_scrore!=0:
                                            response['fields'][i]['confidence'] = tax8_scrore-5

                                elif "tax9" in  response['fields'][i]['name']:
                                    if tax9!={}:
                                        for key, value in tax9.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if tax9_scrore!=0:
                                            response['fields'][i]['confidence'] = tax9_scrore-2

                                elif "tax10" in  response['fields'][i]['name']:
                                    if tax10!={}:
                                        for key, value in tax10.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if tax10_scrore!=0:
                                            response['fields'][i]['confidence'] = tax10_scrore-1

                            elif "other" in  response['fields'][i]['name']:
                                self.location_val.clear()
                                if "other1" in  response['fields'][i]['name']:
                                    if deduction1!={}:
                                        for key, value in deduction1.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if deduction1_scrore!=0:
                                            response['fields'][i]['confidence'] = deduction1_scrore-6
                                elif "other2" in  response['fields'][i]['name']:
                                    if deduction2!={}:
                                        for key, value in deduction2.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if deduction2_scrore!=0:
                                            response['fields'][i]['confidence'] = deduction2_scrore-5
                                elif "other3" in  response['fields'][i]['name']:
                                    if deduction3!={}:
                                        for key, value in deduction3.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if deduction3_scrore!=0:
                                            response['fields'][i]['confidence'] = deduction3_scrore-7
                                elif "other4" in  response['fields'][i]['name']:
                                    if deduction4!={}:
                                        for key, value in deduction4.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if deduction4_scrore!=0:
                                            response['fields'][i]['confidence'] = deduction4_scrore-3
                                elif "other5" in  response['fields'][i]['name']:
                                    if deduction5!={}:
                                        for key, value in deduction5.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if deduction5_scrore!=0:
                                            response['fields'][i]['confidence'] = deduction5_scrore-4
                                elif "other6" in  response['fields'][i]['name']:
                                    if deduction6!={}:
                                        for key, value in deduction6.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if deduction6_scrore!=0:
                                            response['fields'][i]['confidence'] = deduction6_scrore-4
                                elif "other7" in  response['fields'][i]['name']:
                                    if deduction7!={}:
                                        for key, value in deduction7.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if deduction7_scrore!=0:
                                            response['fields'][i]['confidence'] = deduction7_scrore-3
                                elif "other8" in  response['fields'][i]['name']:
                                    if deduction8!={}:
                                        for key, value in deduction8.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if deduction8_scrore!=0:
                                            response['fields'][i]['confidence'] = deduction8_scrore-5
                                elif "other9" in  response['fields'][i]['name']:
                                    if deduction9!={}:
                                        for key, value in deduction9.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if deduction9_scrore!=0:
                                            response['fields'][i]['confidence'] = deduction9_scrore-2
                                elif "other10" in  response['fields'][i]['name']:
                                    if deduction10!={}:
                                        for key, value in deduction10.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if deduction10_scrore10 != 0:
                                            response['fields'][i]['confidence'] = deduction10_scrore-1

                                elif "other11" in  response['fields'][i]['name']:
                                    if deduction11!={}:
                                        for key, value in deduction11.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if deduction_scrore11!=0:
                                            response['fields'][i]['confidence'] = deduction11_scrore-1
                                elif "other12" in  response['fields'][i]['name']:
                                    if deduction12!={}:
                                        for key, value in deduction12.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if deduction12_scrore!=0:
                                            response['fields'][i]['confidence'] = deduction12_scrore-1
                                elif "other13" in  response['fields'][i]['name']:
                                    if deduction13!={}:
                                        for key, value in deduction13.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if deduction13_scrore!=0:
                                            response['fields'][i]['confidence'] = deduction13_scrore-1
                                elif "other14" in  response['fields'][i]['name']:
                                    if deduction14!={}:
                                        for key, value in deduction14.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if deduction14_scrore!=0:
                                            response['fields'][i]['confidence'] = deduction14_scrore-1
                                elif "other15" in  response['fields'][i]['name']:
                                    if deduction15!={}:
                                        for key, value in deduction15.items():
                                            self.location_val.append(value)
                                            if key in response['fields'][i]['field_value_original']:
                                                response['fields'][i]['location'] = str(list(self.location_val))
                                        if deduction15_scrore!=0:
                                            response['fields'][i]['confidence'] = deduction15_scrore-1

                            else:
                                self.location_val.clear()
                                for key, value in dict_location.items():
                                    self.location_val.clear()
                                    self.location_val.append(value)
                                    key = key.replace(',', '')
                                    if key in response['fields'][i]['field_value_original']:
                                        response['fields'][i]['location'] = str(self.location_val)
                                        response['fields'][i]['confidence'] = other_scrore

                    self.scan_result = response
                    self.scan_result['error_msg'] = "Successfully Scanned"
                    self.scan_result["status"] = "SUCCESSFUL"
                    file_path=path
            #print(self.text)
            self.scan_result['raw_data'] = self.text
            print("all response", self.scan_result)
            # data=json.dumps(self.scan_result)
            return self.scan_result,file_path
        except Exception as e:
            print(e)
                




