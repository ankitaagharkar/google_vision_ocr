import cv2
from matplotlib import pyplot as plt

from google.cloud import vision
import io


def guassian_blur(path):


    img = cv2.imread(path)
    b, g, r = cv2.split(img)  # get b,g,r
     # switch it to rgb

    # Denoising
    dst = cv2.fastNlMeansDenoisingColored(img, None, 5, 5, 7, 21)

    b, g, r = cv2.split(dst)  # get b,g,r
    rgb_dst = cv2.merge([r, g, b])  # switch it to rgb

    # plt.subplot(211), plt.imshow(rgb_img)
    # plt.subplot(212), plt.imshow(rgb_dst)
    # plt.show()
    cv2.imwrite('1.jpg',rgb_dst)
    cv2.imshow('frame',rgb_dst)
    cv2.waitKey(0)

def detect_document(path):
    try:
        # text = []
        # vision_client = vision.Client("")
        # with io.open(path, 'rb') as image_file:
        #     content = image_file.read()
        # image = vision_client.image(content=content)
        # document = image.detect_full_text()
        client = vision.ImageAnnotatorClient()
        text,text_val = [],[]
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = client.document_text_detection(image=image)
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                block_words = []
                for paragraph in block.paragraphs:
                    block_words.extend(paragraph.words)
                block_symbols = []
                for word in block_words:
                    block_symbols.extend(word.symbols)
                block_text = ''
                for symbol in block_symbols:
                    test = symbol.property.detected_break
                    if str("SPACE").lower() in str(test).lower():
                        symbol.text = symbol.text + ' '

                    block_text = block_text + symbol.text


                text.append(block_text)

        actual_text=" ".join(map(str,text))
        print(actual_text)

        return actual_text
    except Exception as E:
        print(E)


actual_text=detect_document(r"F:\New_Line_Algorithm\image_text\1.jpg")

import re
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')

string = actual_text

def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]

def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)

def ie_preprocess(document):
    document = ' '.join([i for i in document.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

def extract_names(document):
    names = []
    sentences = ie_preprocess(document)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    return names

if __name__ == '__main__':
    numbers = extract_phone_numbers(string)
    emails = extract_email_addresses(string)
    names = extract_names(string)
    print(numbers)

# guassian_blur(r"C:\Users\ankitaa\Desktop\idocufy\Passport Examples\US Passport 8.JPG")
# guassian_blur(r"C:\Users\ankitaa\Desktop\idocufy\Passport Examples\US Passport 12.JPG")