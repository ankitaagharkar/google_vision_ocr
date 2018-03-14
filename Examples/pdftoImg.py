from PIL import Image
import os
import subprocess
from subprocess import call

def pdfToImage(pdf_path):
    for root, dirs, files in os.walk(os.getcwd()):
        dir ,file = os.path.split(pdf_path)
        print(dir , file)
        destDirectory = os.path.abspath("pdfToimage")
        if not os.path.exists(destDirectory):
            os.mkdir(destDirectory)
        f_path = os.path.join(root, destDirectory)
        print("filePath",f_path)
        print(pdf_path)
        process = subprocess.Popen(['soffice', '--headless', '--convert-to', 'png', pdf_path])
        process.wait()
        # f_name =file.split('.')[0]
        save_path = os.path.join(f_path, file[:-4] + ".png")
        return save_path


if __name__ == '__main__':
    pdf_path = r"C:\Users\ankitaa\PycharmProjects\iDocufy_OCR\Examples\1.pdf"
    pdfToImage(pdf_path)