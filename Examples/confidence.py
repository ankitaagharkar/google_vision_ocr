import os
from enum import Enum
import io
from google.cloud.vision import types
from google.cloud import vision
from PIL import Image, ImageDraw
from google.cloud import vision_v1p1beta1 as vision
def detect_document(path):
    """Detects document features in an image."""

    client = vision.ImageAnnotatorClient()
    word_val = []
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            block_words = []
            for paragraph in block.paragraphs:
                block_words.extend(paragraph.words)
                print(u'Paragraph Confidence: {}\n'.format(
                    paragraph.confidence))

            block_text = ''

            block_symbols = []
            for word in block_words:
                block_symbols.extend(word.symbols)
                word_text = ''
                for symbol in word.symbols:
                    word_text = word_text + symbol.text
                    # print(u'\tSymbol text: {} (confidence: {})'.format(
                    #     symbol.text, symbol.confidence))
                print(u'Word text: {} (confidence: {})\n'.format(
                    word_text, word.confidence))

                word_val.append(word_text)
        val=" ".join(map(str,word_val))
        print(val)
                # print(u'Block Content: {}\n'.format())
                # print(u'Block Confidence:\n {}\n'.format(block.confidence))
detect_document(r"C:\Users\ankitaa\Desktop\idocufy\Images\Valid Licence and SSN\CT DL Example 091117.jpg")