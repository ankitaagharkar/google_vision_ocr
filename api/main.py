import json
import time
from datetime import datetime
import sys

import requests
from flask import Flask, request
sys.path.insert(0, '../Main_OCR')
import all_details
app = Flask(__name__)
file_path=''
response={}
def load_details():
    scan_ocr=all_details.Scan_OCR()
    with open('../config/config.json','r') as data_file:
        config = json.load(data_file)
    return scan_ocr,config

@app.route("/", methods=['GET'])
def index():
    return "Welcome to iDocufy"
@app.route("/api/ocr", methods=['POST'])
def scan():
    global file_path,response
    scan_ocr, config = load_details()
    try:


        requests_json = request.json
        start = datetime.now()
        print("request time",start)

        response,file_path=scan_ocr.all_details(requests_json)

        print(type(response))
        response_val=json.dumps(response)
        response_time = datetime.now() - start
        print("response time", response_time)
        return response_val
    except Exception as e:
        print("in api",e)
    finally:
        try:
            print(file_path)
            files = {'upload_file': open(file_path, 'rb')}
            data_val = requests.post(config['upload_url'], files=files,data=response)
        except Exception as e:
            print("in finally block",e)
            pass

if __name__ == '__main__':
    _,config = load_details()
    app.run(host=config['development'],port=config['development_port'], threaded=True,debug=True)
