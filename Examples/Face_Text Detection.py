

# [START import_client_library]
from google.cloud import vision
# [END import_client_library]
from google.cloud.vision import types
from PIL import Image, ImageDraw

from enum import Enum
import io

from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
# [END imports]


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


def draw_boxes(image, bounds, color):
    """Draw a border around the image using the hints in the vector list."""
    # [START draw_blocks]
    draw = ImageDraw.Draw(image)

    for bound in bounds:
        # print(bound.vertices[0].x, bound.vertices[0].y,
        #     bound.vertices[1].x, bound.vertices[1].y,
        #     bound.vertices[2].x, bound.vertices[2].y,
        #     bound.vertices[3].x, bound.vertices[3].y)
        draw.polygon([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y], None, color)
    return image
# [START def_detect_face]
def detect_face(face_file,feature, max_results=4):
    """Uses the Vision API to detect faces in the given file.
    Args:
        face_file: A file-like object containing an image with faces.
    Returns:
        An array of Face objects with information about the picture.
    """
    # [START get_vision_service]
    client = vision.ImageAnnotatorClient()
    # [END get_vision_service]

    content = face_file.read()
    bounds = []

    content1 = face_file.read()
    image = types.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        print(symbol)
                        if (feature == FeatureType.SYMBOL):
                            bounds.append(symbol.bounding_box)

                    if (feature == FeatureType.WORD):
                        bounds.append(word.bounding_box)

                if (feature == FeatureType.PARA):
                    bounds.append(paragraph.bounding_box)

            if (feature == FeatureType.BLOCK):
                bounds.append(block.bounding_box)

        if (feature == FeatureType.PAGE):
            bounds.append(block.bounding_box)
    face=client.face_detection(image=image).face_annotations
    return face,bounds
# [END def_detect_face]


# [START def_highlight_faces]
def highlight_faces(image, faces,bounds, output_filename):
    im = Image.open(image)
    draw = ImageDraw.Draw(im)

    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        draw.line(box + [box[0]], width=5, fill='#00ff00')
    for bound in bounds:
        # print(bound.vertices[0].x, bound.vertices[0].y,
        #     bound.vertices[1].x, bound.vertices[1].y,
        #     bound.vertices[2].x, bound.vertices[2].y,
        #     bound.vertices[3].x, bound.vertices[3].y)
        draw.polygon([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y], None, 'red')

    im.save(output_filename)
# [END def_highlight_faces]


# [START def_main]
def main(input_filename, output_filename, max_results):
    with open(input_filename, 'rb') as image:
        faces,bounds = detect_face(image,FeatureType.WORD,max_results)

        print('Found {} face{}'.format(
            len(faces), '' if len(faces) == 1 else 's'))

        print('Writing to file {}'.format(output_filename))
        # Reset the file pointer, so we can read the file again
    image.close()
    highlight_faces(input_filename, faces,bounds, output_filename)

if __name__ == '__main__':
    main(r"C:\Users\ankitaa\Desktop\idocufy\Images\Valid Driver Licenses\B60810740.JPG",'Face_Text_Detection.jpg',0)