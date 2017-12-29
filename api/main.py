import json
import time
from datetime import datetime
import sys
from flask import Flask, request
sys.path.insert(0, '../Main_OCR')
import all_details

app = Flask(__name__)

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
    scan_ocr,_=load_details()
    requests = request.json
    start = datetime.now()
    print("request time",start)
    print(requests)
    response=scan_ocr.all_details(requests)
    response_time = datetime.now() - start
    print("response time", response_time)
    return response

if __name__ == '__main__':
    _,config = load_details()
    app.run(host=config['development'],port=config['development_port'], debug=True)
