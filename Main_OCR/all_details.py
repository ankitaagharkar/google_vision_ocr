import json
import threading
from multiprocessing import Process, Queue
from time import sleep
from urllib.request import urlopen
import sys
import os
import PyPDF2
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
        self.paystub_block=paystub_block_values.get_all_location()

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

        employer_full_address, employer_street, employer_state, employer_zipcode, employer_city, employee_full_address,\
        employee_street, employee_state, employee_zipcode, employee_city, start_date, pay_frequency, string_date_value,\
        employer_name, employee_name,earnings, current_earnings,ytd_earnings, deduction, current_deduction,\
        ytd_deduction,other, current_other, ytd_other, current_gross_net, current_net, ytd_gross_pay, ytd_net_pay, \
        pay_end_date,pay_date = self.Paystub.get_details(
            self.text,path,description,result)
        self.doc_text.put((self.text, employer_full_address, employer_street, employer_state, employer_zipcode,
                           employer_city, employee_full_address,employee_street, employee_state, employee_zipcode,
                           employee_city, start_date, pay_frequency, string_date_value,employer_name, employee_name,
                           earnings, current_earnings,ytd_earnings, deduction, current_deduction,ytd_deduction,other,
                           current_other, ytd_other, current_gross_net, current_net, ytd_gross_pay, ytd_net_pay,
                           pay_end_date,pay_date))
    def image_to_pdf(self, image_path, doc_type):
        try:

            if 'Pay Stub' in doc_type:
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
                file = self.c.pdf_page_to_png(src_pdf, doc_type,pagenum=0, resolution=220)
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
            elif 'Pay Stub' in doc_type:
                emp_name, employee_name, emp_address, employee_address, regular1, regular2, regular3, regular4, regular5, regular6, regular7, regular8, regular9, regular10, tax1, tax2, tax3, tax4, tax5, tax6, tax7, tax8, tax9, tax10, deduction1, deduction2, deduction3, deduction4, deduction5, deduction6, deduction7, deduction8, deduction9, deduction10, pay_start_date, pay_end_date, pay_date, dict_location,filename,value_data = self.Location.paystub_get_location(value_json, image, application_id, base_url)
                self.location.put((emp_name, employee_name, emp_address, employee_address, regular1, regular2, regular3, regular4,regular5, regular6, regular7, regular8, regular9, regular10,tax1, tax2, tax3, tax4, tax5, tax6, tax7, tax8,tax9, tax10, deduction1, deduction2, deduction3, deduction4,deduction5, deduction6, deduction7, deduction8, deduction9,deduction10, pay_start_date, pay_end_date, pay_date, dict_location,filename,value_data))
        except Exception as e:
            print(e)
    def get_doc(self,path, doc_type):
        try:
            self.text,self.description,self.result = self.Location.get_text(path, doc_type)
            if 'License' in doc_type:

                licence_id, max_date, min_date, iss_date, address, name, state, zipcode, city,date_val = self.licence.get_licence_details1(self.text)
                self.scan_text.put((self.text, licence_id, max_date, min_date, iss_date, address, name, state, zipcode, city,date_val))
            elif 'SSN' in doc_type:
                SSN_Number = self.ssn.get_all_snn_details(self.text)
                self.scan_text.put((self.text, SSN_Number))

        except Exception as e:
            print(e)
    def confidence_score(self,path, doc_type,data):
        try:
            text_val = self.score.get_confidence_score(path)
            if 'License' in doc_type:
                date_dict,date_score,address_score,license_score,other_score=self.score.license_confidence(data,self.text)
                self.confidence.put((date_dict,date_score,address_score,license_score,other_score))
            elif 'SSN' in doc_type:
                ssn_score=self.score.ssn_confidence(data)
                self.confidence.put((ssn_score))
            elif 'Pay Stub' in doc_type:
                regular1_scrore, regular2_scrore, regular3_scrore, regular4_scrore, regular5_scrore, regular6_scrore, regular7_scrore, \
                regular8_scrore, regular9_scrore, regular10_scrore, tax1_scrore, tax2_scrore, tax3_scrore, tax4_scrore, tax5_scrore, \
                tax6_scrore, tax7_scrore, tax8_scrore, tax9_scrore, tax10_scrore, deduction1_scrore, deduction2_scrore, deduction3_scrore, \
                deduction4_scrore, deduction5_scrore, deduction6_scrore, deduction7_scrore, deduction8_scrore, deduction9_scrore, deduction10, \
                pay_end_date_scrore, pay_start_date_scrore, pay_date_scrore,employee_address_scrore, employee_name_scrore, \
                employer_address_scrore, employer_name_scrore, other_scrore=self.score.paystub_confidence(data)

                self.confidence.put((regular1_scrore,regular2_scrore,regular3_scrore,regular4_scrore,regular5_scrore,regular6_scrore,regular7_scrore,\
            regular8_scrore,regular9_scrore,regular10_scrore,tax1_scrore,tax2_scrore,tax3_scrore,tax4_scrore,tax5_scrore,\
            tax6_scrore,tax7_scrore,tax8_scrore,tax9_scrore,tax10_scrore,deduction1_scrore,deduction2_scrore,deduction3_scrore,\
            deduction4_scrore,deduction5_scrore,deduction6_scrore,deduction7_scrore,deduction8_scrore,deduction9_scrore,deduction10,\
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
                        self.name_value = name.split()
                        #print(self.name_value)
                    if len(self.name_value) == 1:
                        add = {'first_name': "", 'dob': dob, 'issue_date': iss_date,
                               'expiration_date': exp_date,
                               'last_name': self.name_value[0], 'address': address, 'license_id': licence_id,
                               "middle_name": "", "state": state, "postal_code": zipcode, "city": city,
                               "date_val": date_val}
                    elif len(self.name_value) > 2:
                        add = {'first_name': self.name_value[1], 'dob': dob, 'issue_date': iss_date, 'expiration_date': exp_date,
                               'last_name': self.name_value[0], 'address': address, 'license_id': licence_id,
                               "middle_name": self.name_value[2],"state":state,"postal_code":zipcode,"city":city,"date_val":date_val}
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
            elif 'Pay Stub' in json_val[doc_id]:
                if filename.rsplit('.', 1)[1] == 'pdf':
                    thread = threading.Thread(target=self.image_to_pdf,
                                              args=("../images/documents_upload/" + filename, json_val[doc_id],))
                    thread.start()
                    path=self.img2pdf.get()
                    _,filename=os.path.split(path)
                    #print("in display paystub",path)
                    thread = threading.Thread(target=self.get_doc_text, args=(path, json_val[doc_id],))

                else:
                    thread = threading.Thread(target=self.get_doc_text, args=("../images/documents_upload/" + filename,json_val[doc_id],))
                thread.start()
                (self.text, employer_full_address, employer_street, employer_state, employer_zipcode,
                           employer_city, employee_full_address,employee_street, employee_state, employee_zipcode,
                           employee_city, start_date, pay_frequency, string_date_value,employer_name, employee_name,
                           earnings, current_earnings,ytd_earnings, deduction, current_deduction,ytd_deduction,other,
                           current_other, ytd_other, current_gross_net, current_net, ytd_gross_pay, ytd_net_pay,
                           pay_end_date,pay_date)=self.doc_text.get()
                print("in paystub details",earnings,current_earnings,ytd_earnings)
                if current_gross_net == '' and current_net == '' and pay_frequency == '' and employee_full_address=='' and employer_full_address=='' and employee_name == '' and employee_city == '' and employee_state == '' and employer_name == '' and employer_city == '' and employer_state == '' and start_date == '':
                    file_path = ''
                    self.scan_result['error_msg'] = "Incorrect Document or Unable to Scan"
                    self.scan_result['status'] = "INCORRECT_DOCUMENT"
                    return self.scan_result, file_path
                else:
                    j=0
                    k=0
                    l=0
                    for i in range(len(response['fields'])):
                        if 'regular' in response['fields'][i]['alias']:
                            if k < len(earnings):

                                response['fields'][i]['alias'] = earnings[k]
                                response['fields'][i]['field_value_original'] = current_earnings[k]
                                response['fields'][i]['optional_value'] = ytd_earnings[k]
                                k = k + 1
                            else:
                                response['fields'][i]['alias'] = ''
                                response['fields'][i]['field_value_original'] = ''
                                response['fields'][i]['optional_value'] = ''
                        elif 'tax' in response['fields'][i]['name']:
                            if j < len(deduction):

                                response['fields'][i]['alias'] = deduction[j]
                                response['fields'][i]['field_value_original'] = current_deduction[j]
                                response['fields'][i]['optional_value'] = ytd_deduction[j]
                                j = j + 1
                            else:
                                response['fields'][i]['alias'] = ''
                                response['fields'][i]['field_value_original'] = ''
                                response['fields'][i]['optional_value'] = ''
                        elif 'other' in response['fields'][i]['name']:
                            if l < len(other):
                                response['fields'][i]['alias'] = other[l]
                                response['fields'][i]['field_value_original'] = current_other[l]
                                response['fields'][i]['optional_value'] = ytd_other[l]
                                l = l + 1
                            else:
                                response['fields'][i]['alias'] = ''
                                response['fields'][i]['field_value_original'] = ''
                                response['fields'][i]['optional_value'] = ''
                        elif 'gross_pay' in response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = current_gross_net
                            response['fields'][i]['optional_value'] = ytd_gross_pay
                        elif 'net_pay' in response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = current_net
                            response['fields'][i]['optional_value'] = ytd_net_pay
                        elif 'employee_name' in response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = employee_name
                            response['fields'][i]['optional_value'] = ""
                        elif 'employee_number' in response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = ""
                            response['fields'][i]['optional_value'] = ""
                        elif 'employer_address' in response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = employer_full_address
                            response['fields'][i]['optional_value'] = ""
                        elif 'employer/company_code' in response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = ""
                            response['fields'][i]['optional_value'] = ""
                        elif 'pay_period_end_date' in response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = pay_end_date
                            response['fields'][i]['optional_value'] =""
                        elif 'pay_period_start_date' in response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = start_date
                            response['fields'][i]['optional_value'] =""
                        elif 'pay_date' in response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = pay_date
                            response['fields'][i]['optional_value'] = ""
                        elif 'state_unemployment' in response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = ""
                            response['fields'][i]['optional_value'] = ""
                        elif 'position' in response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = ""
                            response['fields'][i]['optional_value'] = ""
                        elif 'employer_name' in response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = employer_name
                            response['fields'][i]['optional_value'] = ""
                        elif 'employer_city' in response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = employer_city
                            response['fields'][i]['optional_value'] = ""
                        elif 'employee_city' in response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = employee_city
                            response['fields'][i]['optional_value'] = ""
                        elif 'employer_state' in response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = employer_state
                            response['fields'][i]['optional_value'] = ""
                        elif 'employee_state' in response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = employee_state
                            response['fields'][i]['optional_value'] = ""
                        elif 'employment_start_date' in response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = ""
                            response['fields'][i]['optional_value'] = ""
                        elif 'pay_frequency' in response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = pay_frequency
                            response['fields'][i]['optional_value'] = ""
                        elif 'employee_address' in response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = employee_full_address
                            response['fields'][i]['optional_value'] = ""
                        elif 'mi' in response['fields'][i]['name']:
                            response['fields'][i]['field_value_original'] = ""
                            response['fields'][i]['optional_value'] = ""
                        else:
                            pass

                    # actual_value = list(add.keys())
                    # actual_value = sorted(actual_value)
                    # add_value = list(add.values())
                    # detected_null_value_count = add_value.count('')
                    # partial_not_detected, partial_detected = [], []
                    #
                    # for i in range(len(response['fields'])):
                    #     for j in range(len(actual_value)):
                    #         if response['fields'][i]['name'] == actual_value[j]:
                    #             response['fields'][i]['field_value_original'] = add[actual_value[j]]
                    # #             pass
                    # thread = threading.Thread(target=self.get_location, args=(
                    # response, "../images/documents_upload/" + filename, application_id, self.config['base_url'],
                    # json_val[doc_id],))
                    # thread.start()
                    # (emp_name, employee_name, emp_address, employee_address, regular1, regular2, regular3, regular4,regular5, regular6, regular7, regular8, regular9, regular10,tax1, tax2, tax3, tax4, tax5, tax6, tax7, tax8,tax9, tax10, deduction1, deduction2, deduction3, deduction4,deduction5, deduction6, deduction7, deduction8, deduction9,deduction10, pay_start_date, pay_end_date, pay_date, dict_location,file_path,value_json) = self.location.get()
                    # print("in details val",value_json)
                    # thread = threading.Thread(target=self.confidence_score, args=("../images/documents_upload/" + filename, json_val[doc_id], value_json,))
                    # thread.start()
                    # (regular1_scrore,regular2_scrore,regular3_scrore,regular4_scrore,regular5_scrore,regular6_scrore,regular7_scrore,\
                    # regular8_scrore,regular9_scrore,regular10_scrore,tax1_scrore,tax2_scrore,tax3_scrore,tax4_scrore,tax5_scrore,\
                    # tax6_scrore,tax7_scrore,tax8_scrore,tax9_scrore,tax10_scrore,deduction1_scrore,deduction2_scrore,deduction3_scrore,\
                    # deduction4_scrore,deduction5_scrore,deduction6_scrore,deduction7_scrore,deduction8_scrore,deduction9_scrore,deduction10,\
                    # pay_end_date_scrore,pay_start_date_scrore,pay_date_scrore,employee_address_scrore,employee_name_scrore,\
                    # employer_address_scrore,employer_name_scrore,other_scrore) = self.confidence.get()
                    # #
                    # for i in range(len(response['fields'])):
                    #         x=0
                    #         if response['fields'][i]['name'] == "employer_name":
                    #             self.location_val.clear()
                    #             for key, value in emp_name.items():
                    #                 self.location_val.append(value)
                    #                 if key in response['fields'][i]['field_value_original'] :
                    #                     response['fields'][i]['location'] = str(list(self.location_val))
                    #                     response['fields'][i]['confidence'] = employer_name_scrore
                    #
                    #         elif response['fields'][i]['name'] == "employee_name":
                    #             self.location_val.clear()
                    #             for key, value in employee_name.items():
                    #                 self.location_val.append(value)
                    #                 if key in response['fields'][i]['field_value_original'] :
                    #                     response['fields'][i]['location'] = str(list(self.location_val))
                    #                     response['fields'][i]['confidence'] = employee_name_scrore
                    #
                    #         elif response['fields'][i]['name'] == "employer_address":
                    #             self.location_val.clear()
                    #             for key, value in employer_address.items():
                    #                 self.location_val.append(value)
                    #                 if key in response['fields'][i]['field_value_original'] :
                    #                     response['fields'][i]['location'] = str(list(self.location_val))
                    #                     response['fields'][i]['confidence'] = employer_address_scrore
                    #
                    #         elif response['fields'][i]['name'] == "employee_address":
                    #             self.location_val.clear()
                    #             for key, value in employee_address.items():
                    #                 self.location_val.append(value)
                    #                 if key in response['fields'][i]['field_value_original'] :
                    #                     response['fields'][i]['location'] = str(list(self.location_val))
                    #                     response['fields'][i]['confidence'] = employee_address_scrore
                    #         elif "regular" in  response['fields'][i]['name']:
                    #             var_name = "regular" + str(x)
                    #             self.location_val.clear()
                    #             if "1" in var_name:
                    #                 if regular1!={}:
                    #                     for key, value in regular1.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     response['fields'][i]['confidence'] = regular1_scrore
                    #             elif "2" in var_name:
                    #                 if regular2!={}:
                    #                     for key, value in regular2.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     response['fields'][i]['confidence'] = regular2_scrore
                    #             elif "3" in var_name:
                    #                 if regular3!={}:
                    #                     for key, value in regular3.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     response['fields'][i]['confidence'] = regular3_scrore
                    #             elif "4" in var_name:
                    #                 if regular4!={}:
                    #                     for key, value in regular4.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     response['fields'][i]['confidence'] = regular4_scrore
                    #             elif "5" in var_name:
                    #                 if regular5!={}:
                    #                     for key, value in regular5.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     response['fields'][i]['confidence'] = regular5_scrore
                    #             elif "6" in var_name:
                    #                 if regular6!={}:
                    #                     for key, value in regular6.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     response['fields'][i]['confidence'] = regular6_scrore
                    #             elif "7" in var_name:
                    #                 if regular7!={}:
                    #                     for key, value in regular7.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                             response['fields'][i]['confidence'] = regular7_scrore
                    #             elif "8" in var_name:
                    #                 if regular8!={}:
                    #                     for key, value in regular8.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     response['fields'][i]['confidence'] = regular8_scrore
                    #             elif "9" in var_name:
                    #                 if regular9!={}:
                    #                     for key, value in regular9.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     response['fields'][i]['confidence'] = regular9_scrore
                    #             elif "10" in var_name:
                    #                 if regular10!={}:
                    #                     for key, value in regular10.items():
                    #                         self.location_val.append(value)
                    #                         if key in response['fields'][i]['field_value_original']:
                    #                             response['fields'][i]['location'] = str(list(self.location_val))
                    #                     response['fields'][i]['confidence'] = regular10_scrore
                    #             x=x+1
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
                    # if detected_null_value_count >= int(len(actual_value) / 2):
                    #     for key, value in add.items():
                    #         if value == 'null':
                    #             partial_not_detected.append(key)
                    #         else:
                    #             partial_detected.append(key)
                    #     self.scan_result['error_msg'] = "Partially Detected:" + ", ".join(
                    #         map(str, partial_detected)) + "\nUnable to Detectect" + ", ".join(
                    #         map(str, partial_not_detected))
                    #
                    #     self.scan_result['status'] = "PARTIAL_DETECTION"
                    #
                    # else:

                    self.scan_result['error_msg'] = "Successfully Scanned"
                    self.scan_result["status"] = "SUCCESSFUL"
                    file_path = "../images/documents_upload/" + filename

            #print(self.text)
            self.scan_result['raw_data'] = self.text
            print("all response", self.scan_result)
            # data=json.dumps(self.scan_result)
            return self.scan_result,file_path
        except Exception as e:
            print("in main",e)
                




