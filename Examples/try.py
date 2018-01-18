import io

from google.cloud import vision
from google.cloud.vision import types

client = vision.ImageAnnotatorClient()
with io.open(r"C:\Users\ankitaa\Desktop\1.jpg", 'rb') as image_file:
    content = image_file.read()
image = types.Image(content=content)
# response = client.document_text_detection(image=image)
# texts = response.full_text_annotation
text_val=[]
response = client.text_detection(image=image)
texts = response.text_annotations
for text in texts[1:]:
    text_val.append(text.description)
    vertices = [(vertex.x, vertex.y)
                for vertex in text.bounding_poly.vertices]
    # result.setdefault(text.description, vertices)
    print(text.description, vertices)
text = " ".join(map(str, text_val))

