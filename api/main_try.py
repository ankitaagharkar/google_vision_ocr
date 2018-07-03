import json
import threading
from threading import Event
from datetime import datetime
import sys
from multiprocessing import Pool

import requests
from flask import Flask, request
sys.path.insert(0, '../Main_OCR')
import all_details

# import all_details_try
app = Flask(__name__)
_pool = None

file_path=''
response={}
def load_details():

    with open('../config/config.json','r') as data_file:
        config = json.load(data_file)
    return config

@app.route("/", methods=['GET'])
def index():
    print('hello')
    return "Welcome to iDocufy"
@app.route("/api/ocr", methods=['POST'])
def scan():
    global file_path,response
    config = load_details()
    # try:
    requests_json = request.json
    start = datetime.now()
    print("request time",start)
    print(requests_json)
    ready = Event()
    program = all_details.Scan_OCR(ready)
    thread = threading.Thread(target=program.start)
    thread.start()
    thread.join()
    ready.wait()

    response, file_path=program.all_details(requests_json)
    # scan_ocr = all_details.Scan_OCR()
    # response,file_path=scan_ocr.all_details(requests_json)

    response_val=json.dumps(response)
    response_time = datetime.now() - start
    print("response time", response_time)
    return response_val

    # except Exception as e:
    #     print("in api",e)
    # finally:
    #     try:
    #         print(file_path)
    #         files = {'upload_file': open(file_path, 'rb')}
    #         data_val = requests.post(config['upload_url'], files=files,data=response)
    #     except Exception as e:
    #         print("in finally block",e)
    #         pass

if __name__ == '__main__':
    _pool = Pool(processes=3)
    try:
        config = load_details()
        app.run(host=config['development'], port=config['development_port'], debug=True)
    except KeyboardInterrupt:
        _pool.close()
        _pool.join()


    # app.run(threaded=True,debug=True)
