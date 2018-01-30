
import io

import re
from google.cloud import vision
from google.cloud import vision_v1p1beta1 as vision
def detect_document(path):
    data = {'first_name': "MICHAEL", 'dob': '03-03-1982', 'issue_date': '02-15-2014',
             'expiration_date': '03-03-2020',
             'last_name': 'VERRELLI', 'address': '8100 LORDSHIP RD', 'license_id': '157217830',
             "middle_name": "J", "state": 'CT', "postal_code": '06615', "city": 'STRATFORD',
             "date_val": '03-03-1982 02-15-2014 03-03-2020'}
    keys,values=[],[]
    dict,address_val={},{}
    full_address=''
    address_confidence=0.0
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            block_words = []
            for paragraph in block.paragraphs:
                block_words.extend(paragraph.words)
            block_text = ''
            block_symbols = []
            for word in block_words:
                block_symbols.extend(word.symbols)
                word_text = ''
                for symbol in word.symbols:
                    word_text = word_text + symbol.text
                print(u'Word text: {} (confidence: {})\n'.format(
                    word_text, word.confidence))
                keys.append(word_text)
                values.append(word.confidence)

    result = zip(keys,values)
    for key, value in enumerate(result):
        for key1, value1 in data.items():
            if value[0]!='' and value1!='':
                if re.search(r'\b(=?' + re.escape(value[0]) + r')\b', value1):

                    if value[0] in data['date_val']:
                        dict[value[0]]=value[1]
                        date_confidence_score=0.0
                        for key3,value3 in dict.items():
                            date_confidence_score=date_confidence_score+value3
                        date_score=date_confidence_score/len(dict)
                    elif value[0] in data['license_id']:
                        address_val=value[1]
                        # address_confidence=address_confidence+float(value[1])
                        # full_address=full_address+" "+value[0]
    print(address_val)

detect_document(r"C:\Users\ankitaa\Desktop\idocufy\Images\Valid Licence and SSN\CT DL Example 091117.jpg")