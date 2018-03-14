
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
        process = subprocess.Popen(['soffice', '--headless', '--convert-to', 'png:writer_web_png_Export', pdf_path, '--outdir', f_path])
        process.wait()
        # f_name =file.split('.')[0]
        save_path = os.path.join(f_path, file[:-4] + ".png")
        return save_path

def tiffTopng(tifPath):
    yourpath = os.getcwd()
    for root, dirs, files in os.walk(yourpath, topdown=False):
        for name in files:
            # print(os.path.join(root, name))
            if os.path.splitext(os.path.join(root, name))[1].lower() == ".tif":
                if os.path.isfile(os.path.splitext(os.path.join(root, name))[0] + ".png"):
                    print ("A png file already exists for %s" % name)
                # If a jpeg is *NOT* present, create one from the tiff.
                else:
                    # outfile = os.path.splitext(os.path.join(root, name))[0] + ".png"
                    destDirectory = os.path.abspath("tiffToImage")
                    if not os.path.exists(destDirectory):
                        os.mkdir(destDirectory)
                    f_path = os.path.join(root,destDirectory)
                    # print(f_path)
                    dir ,file = os.path.split(tifPath)
                    # print(dir , file)

                    outfile = os.path.join(f_path,file[:-4] + ".png")
                    print("outfile",outfile)
                    try:
                        im = Image.open(os.path.join(tifPath))
                        print ("Generating png for %s" % file)
                        im.thumbnail(im.size)
                        im.save(outfile, "PNG", quality=200)
                    except Exception as e:
                        print (e)

                    return outfile
if __name__ == '__main__':
    # pdf_path = r"D:\Swapnil\AMC_Project\AMC-AustralianMouldingCompany\1.pdf"
    # pdfToImage(pdf_path)
    tif_path = r"D:\Swapnil\AMC_Project\AMC-AustralianMouldingCompany\ImageProcessing\BELGRAVE SOUTH HOME HARDWARE.tif"
    tiffTopng(tif_path)