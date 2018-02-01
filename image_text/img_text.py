from google.cloud import vision
import io

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

detect_document(r"C:\Users\ankitaa\Desktop\idocufy\Images\Paystub\1.jpg")