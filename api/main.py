import json

from flask import Flask, request

from Main_OCR.all_details import Scan_OCR

app = Flask(__name__)

def load_details():
    scan_ocr=Scan_OCR()
    with open('../config/config.json') as data_file:
        config = json.load(data_file)
    return scan_ocr,config

@app.route("/", methods=['GET'])
def index():
    return "Welcome to iDocufy"
@app.route("/api/ocr", methods=['POST'])
def scan():
    scan_ocr,_=load_details()
    requests = request.json
    response=scan_ocr.all_details(requests)
    return response

if __name__ == '__main__':
    _,config = load_details()
    app.run(host=config['development'],port=config['port'], debug=True)
