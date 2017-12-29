import json
import threading
from multiprocessing import Queue
from urllib.request import urlopen
import sys
import os
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
class Scan_OCR:
    def __init__(self):
        self.scan_text = Queue()
        self.image_processing = Queue()
        self.location = Queue()
        self.scan_result={}
        self.text=''
        self.name_value = []
        self.location_val = []
        self.licence=get_licence_details.Licence_details()
        self.ssn=get_ssn_details.SSN_details()
        self.Paystub=get_paystub_details.Paystub_details()
        self.denoising=image_denoising.Denoising()
        self.Location = get_all_locations.get_all_location()

        with open('../config/config.json') as data_file:
            self.config = json.load(data_file)
    def image_processing_threading(self,image_path,doc_type):
        try:
            image=self.denoising.image_conversion_smooth(image_path,doc_type)
            self.image_processing.put(image)
        except Exception as e:
            print(e)
    def get_location(self,value_json):
        # try:
            address_location,licence_id_location,dict=self.Location.get_location(value_json)
            self.location.put((address_location,licence_id_location,dict))
        # except Exception as e:
        #     print(e)
    def get_doc(self,path, doc_type):
        try:
            self.text = self.Location.get_text(path)
            if 'License' in doc_type:
                licence_id, max_date, min_date, iss_date, address, name, state, zipcode, city,date_val = self.licence.get_licence_details1(self.text)
                self.scan_text.put((self.text, licence_id, max_date, min_date, iss_date, address, name, state, zipcode, city,date_val))
            elif 'SSN' in doc_type:
                SSN_Number, name = self.ssn.get_all_snn_details(self.text)
                self.scan_text.put((self.text, SSN_Number, name))
            elif 'PayStub' in doc_type:
                Employer_State, Employer_City, Employer_name, employment_Start_date, pay_frequency, gross_pay, net_pay = self.Paystub.get_details(self.text)
                self.scan_text.put((self.text, Employer_State, Employer_City, Employer_name, employment_Start_date, pay_frequency, gross_pay, net_pay))
        except Exception as e:
            print(e)
    def all_details(self,response):
        try:
            doc_id = int(response['doc_id'])
            url = self.config['base_url'] + response['file_path']
            url=url.replace(" ","%20")
            image_on_web = urlopen(url)
            filename = os.path.basename(url)
            r = requests.post(self.config['base_url']+'/getAllDocumentsMaster')
            resp_dict = json.loads(json.dumps(r.json()))
            value = resp_dict.get('records')
            json_val = dict([(value[i]['id'], value[i]['name']) for i in range(len(value))])
            buf = image_on_web.read()
            with open("../images/documents_upload/" + filename, "wb") as downloaded_image:
                downloaded_image.write(buf)
                downloaded_image.close()
                image_on_web.close()
            if 'License' in json_val[doc_id]:
                thread = threading.Thread(target=self.image_processing_threading, args=("../images/documents_upload/"+filename, json_val[doc_id],))
                thread.start()
                image_path=self.image_processing.get()
                thread = threading.Thread(target=self.get_doc, args=(image_path, json_val[doc_id],))
                thread.start()
                (self.text, licence_id, exp_date, dob, iss_date, address, name, state, zipcode, city,date_val) = self.scan_text.get()
                if licence_id == 'null' and exp_date == 'null' and dob == 'null' and iss_date == 'null' and address == 'null' and name == 'null' and state == 'null' and zipcode == 'null' and city == 'null':
                     self.scan_result = {'error_msg': "Invalid document"}
                     return json.dumps(self.scan_result)
                else:
                    if name == '':
                        self.name_value.append('-')
                        self.name_value.append('-')
                        self.name_value.append('-')
                    else:
                        self.name_value = name.split()
                    if len(self.name_value) > 2:
                        add = {'first_name': self.name_value[1], 'dob': dob, 'issue_date': iss_date, 'expiration_date': exp_date,
                               'last_name': self.name_value[0], 'address': address, 'license_id': licence_id,
                               "middle_name": self.name_value[2],"state":state,"postal_code":zipcode,"city":city,"date_val":date_val}
                    else:
                        add = {'first_name': self.name_value[1], 'dob': dob, 'issue_date': iss_date,
                               'expiration_date': exp_date, 'last_name': self.name_value[0], 'address': address,
                               'license_id': licence_id, "middle_name": '-',"state":state,"postal_code":zipcode,"city":city}
                    actual_value = list(add.keys())
                    actual_value = sorted(actual_value)
                    print("actual1", actual_value)
                    for i in range(len(response['fields'])):
                        for j in range(len(actual_value)):
                            if response['fields'][i]['name'] == actual_value[j]:
                                response['fields'][i]['field_value_original'] = add[actual_value[j]]
                                pass
                    # self.scan_result = response
                    thread = threading.Thread(target=self.get_location, args=(add,))
                    thread.start()
                    (address_location,licence_id_location,dict_location) = self.location.get()
                    print("Type",type(address_location),type(licence_id_location),type(dict_location))
                    for i in range(len(response['fields'])):
                        for j in range(len(actual_value)):
                            if response['fields'][i]['name']=="address":

                                for key,value in address_location.items():
                                    self.location_val.append(value)
                                    if key in response['fields'][i]['field_value_original']:
                                        response['fields'][i]['location'] = str(list(self.location_val))
                            elif response['fields'][i]['name']=="license_id":
                                self.location_val.clear()
                                for key,value in licence_id_location.items():
                                    self.location_val.append(value)
                                    if key in response['fields'][i]['field_value_original']:

                                        response['fields'][i]['location'] = str([self.location_val])
                            else:
                                self.location_val.clear()
                                for key,value in dict_location.items():
                                    self.location_val.clear()
                                    self.location_val.append(value)
                                    key=key.replace(',','')
                                    if response['fields'][i]['field_value_original'] in key :
                                        response['fields'][i]['location']=str(self.location_val)
                    self.scan_result = response
                    self.scan_result['error_msg'] = 'null'
            elif 'SSN' in json_val[doc_id]:
                thread = threading.Thread(target=self.image_processing_threading,
                                          args=("../images/documents_upload/" + filename, json_val[doc_id],))
                thread.start()
                image_path = self.image_processing.get()
                thread = threading.Thread(target=self.get_doc, args=(image_path, json_val[doc_id],))
                thread.start()
                (self.text, SSN_Number, name ) = self.scan_text.get()
                if SSN_Number == 'null' and name == 'null':
                     self.scan_result = {'error_msg': "Invalid document"}
                     return json.dumps(self.scan_result)
                else:
                    if name == 'null':
                        self.name_value.append('-')
                        self.name_value.append('-')
                        self.name_value.append('-')
                    else:
                        self.name_value = name.split()
                        print("self.name_value", self.name_value)
                    if len( self.name_value) > 2:
                        add = {"ssn_number": SSN_Number, "first_name":  self.name_value[0], "last_name":  self.name_value[2],
                               "middle_name":  self.name_value[1]}
                    else:
                        add = {"ssn_number": SSN_Number, "first_name":  self.name_value[0], "last_name":  self.name_value[1],
                               "middle_name": "-"
                               }
                    actual_value = list(add.keys())
                    actual_value = sorted(actual_value)
                    print("actual", actual_value)
                    for i in range(len(response['fields'])):
                        for j in range(len(actual_value)):
                            if response['fields'][i]['name'] == actual_value[j]:
                                response['fields'][i]['field_value_original'] = add[actual_value[j]]
                                pass
                    self.scan_result = response
                    self.scan_result['error_msg'] = 'null'
            elif 'PayStub' in json_val[doc_id]:
                thread = threading.Thread(target=self.image_processing_threading,
                                          args=("../images/documents_upload/" + filename, json_val[doc_id],))
                thread.start()
                image_path = self.image_processing.get()
                thread = threading.Thread(target=self.get_doc, args=(image_path, json_val[doc_id],))
                thread.start()
                (self.text, Employer_State, Employer_City, Employer_name, employment_Start_date, pay_frequency, gross_pay, net_pay) = self.scan_text.get()
                if gross_pay == 'null' and net_pay == 'null' and pay_frequency == 'null' and Employer_name == 'null' and Employer_City == 'null' and Employer_State == 'null' and 'employment_Start_date' == 'null':
                    self.scan_result = {'error_msg': "Invalid document"}
                    return json.dumps(self.scan_result)
                else:
                    add = {'gross_pay': gross_pay, 'net_pay': net_pay, 'pay_frequency': pay_frequency,
                           'employer_name': Employer_name,
                           'employer_city': Employer_City, 'employer_state': Employer_State,
                           "employment_start_date": employment_Start_date, 'position': ''}
                    actual_value = list(add.keys())
                    actual_value = sorted(actual_value)
                    print("actual", actual_value)
                    for i in range(len(response['fields'])):
                        for j in range(len(actual_value)):
                            if response['fields'][i]['name'] == actual_value[j]:
                                response['fields'][i]['field_value_original'] = add[actual_value[j]]
                                pass
                    self.scan_result = response
                    self.scan_result['error_msg'] = 'null'
            print(self.scan_result)
            self.scan_result['raw_data'] = self.text
            print("all response", self.scan_result)
            return json.dumps(self.scan_result)
        except Exception as e:
            print(e)
                




