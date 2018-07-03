import io
# from wand.image import Image as I
import re
from wand.image import Image
import PyPDF2
from wand.api import library
from ctypes import c_void_p, c_size_t
# Tell Python's wand library about the MagickWand Compression Quality (not Image's Compression Quality)
library.MagickSetCompressionQuality.argtypes = [c_void_p, c_size_t]


class Common:
    def __init__(self):
        self.result=[]


    def find_between_r(self,s, first, last):
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""

    def getUniqueItems(self,iterable):
        seen = set()
        for item in iterable:
            if item not in seen:
                seen.add(item)
                self.result.append(item)
        return self.result
    def get_address_zipcode(self,full_address,zipcode, extra=False):
        try:
            full_address=full_address.replace('  ',' ')
            if not extra:
                if re.search('\w?\.?\w+\.?\s\d+|\w+\s\d+',zipcode):
                    if not re.search(r'[A-Za-z]{4,}',zipcode):
                        if re.search('\w?\.?\w+\.?\s\d+',zipcode):
                            pass
                        else:
                            zipcode = zipcode.replace(' ', "")
                            zipcode = zipcode[0:2] + " " + zipcode[2:]
                        code = zipcode.split()
                        city = ' '.join(map(str, full_address.split(" "+code[0]+" ", 1)[0].split()[-2:]))
                        return code[0], code[1], city
                    else:
                        code = zipcode.split()
                        city = ' '.join(map(str, full_address.split(" " + code[0]+" ", 1)[0].split()[-2:]))
                        return code[0], code[1], city
                else:
                    code=[]
                    #todo: for zipcode like LO SE10
                    if re.search(r'[A-Za-z]+\s\w+',zipcode):
                        code = zipcode.split()
                        city = ' '.join(map(str, full_address.split(" " + code[0]+" ", 1)[0].split()[-2:]))
                    elif re.search(r'[A-Za-z]+\s\w+\s\w+',zipcode):
                        code = zipcode.split()
                        city = ' '.join(map(str, full_address.split(" " + code[0]+" ", 1)[0].split()[-2:]))
                        code[1]=code[1]+" "+code[2]
                    else:
                        code.append(zipcode)
                        city = ' '.join(map(str, full_address.split(" "+code[0]+" ", 1)[0].split()[-2:]))
                        code.append("")
                    return code[0], code[1], city
            else:
                # if re.search('\w+\s\d+', zipC):
                state = [zipco for zipco in zipcode if zipco.isalpha() and len(zipco) == 2][0]
                full_address_as_list = full_address.split()
                indexOfState = full_address_as_list.index(state)
                try:
                    fullZipCode = full_address_as_list[indexOfState+1:]
                    fullZipCode = ''.join(map(str, fullZipCode))
                except Exception as e:
                    print(e)
                    fullZipCode = ''
                try:
                    if len(full_address_as_list)>2:
                        city = " ".join(full_address_as_list[indexOfState - 2:indexOfState])

                    else:
                        city = full_address_as_list[indexOfState - 1]
                except Exception as e:
                    print(e)
                    city = ''
                return state, fullZipCode, city


        except Exception as e:
            print(e)

    # def pdf_page_to_png(self,src_pdf,doc_type, resolution=150, pagenum=0):
    #     try:
    #
    #         dst_pdf = PyPDF2.PdfFileWriter()
    #         dst_pdf.addPage(src_pdf.getPage(pagenum))
    #
    #         pdf_bytes = io.BytesIO()
    #         dst_pdf.write(pdf_bytes)
    #         pdf_bytes.seek(0)
    #         img = Image(file=pdf_bytes, resolution=resolution)
    #         # if 'License' in doc_type:
    #         #     # img.resize(width=960, height=960)
    #         # library.MagickSetCompressionQuality(img.wand, 0)
    #         # img.convert("jpg")
    #
    #         return img
    #     except Exception as E:
    #         print(E)