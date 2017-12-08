import json
import threading
from multiprocessing import Queue
from urllib.request import urlopen
import config
import os

import requests

from all_documents.get_licence_details import Licence_details
from image_processing.image_denoising import Denoising
from image_text.img_text import detect_document

class Scan_OCR:
    def __init__(self):
        self.scan_text = Queue()
        self.image_processing = Queue()
        self.scan_result={}
        self.name_value = []
        self.licence=Licence_details()
        self.denoising=Denoising()
        with open('../config/config.json') as data_file:
            self.config = json.load(data_file)
    def image_processing_threading(self,image_path,doc_type):
        try:
            image=self.denoising.image_conversion_smooth(image_path,doc_type)
            self.image_processing.put(image)
        except Exception as e:
            print(e)

    def get_doc(self,path, doc_type):
        try:
            text = detect_document(path)
            if 'License' in doc_type:
                licence_id, max_date, min_date, iss_date, address, name = self.licence.get_licence_details1(text)
                self.scan_text.put((text, licence_id, max_date, min_date, iss_date, address, name))
        # elif 'SSN' in doc_type:
        #     SSN_Number, name = SSN_Details.get_SSN_details1(text)
        #     self.scan_text.put((text, SSN_Number, name))
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
            with open("images/documents_upload/" + filename, "wb") as downloaded_image:
                downloaded_image.write(buf)
                downloaded_image.close()
                image_on_web.close()
            if 'License' in json_val[doc_id]:
                thread = threading.Thread(target=self.image_processing_threading, args=("images/documents_upload/"+filename, json_val[doc_id],))
                thread.start()
                image_path=self.image_processing.get()
                thread = threading.Thread(target=self.get_doc, args=(image_path, json_val[doc_id],))
                thread.start()
                (text, licence_id, exp_date, dob, iss_date, address, name) = self.scan_text.get()
                if licence_id == 'null' and exp_date == 'null' and dob == 'null' and iss_date == 'null' and address == 'null' and name == 'null':
                    self.scan_result = {'error_msg': "Invalid image"}
                else:
                        if name == 'null':
                            self.name_value.append('-')
                            self.name_value.append('-')
                            self.name_value.append('-')
                        else:
                            self.name_value = name.split()
                            print("self.name_value", self.name_value)
                        if len(self.name_value) > 2:
                            add = {'first_name': self.name_value[1], 'dob': dob, 'issue_date': iss_date, 'expiration_date': exp_date,
                                   'last_name': self.name_value[0], 'address': address, 'license_id': licence_id,
                                   "middle_name": self.name_value[2]}
                        else:
                            add = {'first_name': self.name_value[0], 'dob': dob, 'issue_date': iss_date,
                                   'expiration_date': exp_date, 'last_name': self.name_value[1], 'address': address,
                                   'license_id': licence_id, "middle_name": '-'}
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
                




