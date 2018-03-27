import re,sys
sys.path.insert(0, '../all_documents')
import avoid
class SSN_details:

    def get_all_snn_details(self,text):
        try:
            # text = text_value.replace(' ', '')
            print(text)
            data = re.findall(
                r'(((?!000|666)(?:[0-6]\d{2}|7[0-2][0-9]|73[0-3]|7[5-6][0-9]|77[0-2]))[-.]+?((?!00)\d{2})[-.]+?(((?!0000)\d{4})))',
                text)
            print("ssn_number", data)
            if data == []:
                ssn_number = "null"
            else:
                ssn_number = data[0][0]
                # print(text)
                name = ' '.join(map(str, text.split(ssn_number, 1)[1].split()[5:9]))
                actual_name = name.split('2', 1)
                actual_name = "".join(actual_name)
                actual_name=actual_name.split('SIGNATURE')
                actual_name =actual_name[0]
                actual_name=avoid.replace(actual_name)
                actual_name=actual_name.replace('.',"")
                val = re.findall(
                    r'(([1-9]|0[0-9]|1[0-2])\s?[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])\s?[./-](19|20|21|22)\d\d|(0[0-9]|1[0-2])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-]\d\d|(0[0-9]|1[0-2])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-](19|20|21|22)\d\d|(0[0-9]|1[0-9])\s?(0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-](19|20|21|22)\d\d|(0[0-9]|1[0-9])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])\s?(19|20|21|22)\d\d)',
                    text)
                date=val[0][0]
            return ssn_number,actual_name,date
        except Exception as E:

            data,name,date = "",'',''
            return data,name,date

