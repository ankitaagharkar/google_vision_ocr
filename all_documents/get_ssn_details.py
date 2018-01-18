import re
class SSN_details:

    def get_all_snn_details(self,text_value):
        try:
            text = text_value.replace(' ', '')
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
                # name = ' '.join(map(str, text.split(data[0][0], 1)[1].split()[0:3]))
                # print(name)
                # name_regex = re.findall(r'[A-Z]{2,}(?:(?!\d))\s?[A-Z]{1,}', name)
                # print("name", name_regex)
                # if name_regex == []:
                #     actual_name = "null"
                # else:
                #     actual_name = " ".join(map(str, name_regex))
                #     actual_name = actual_name.replace('THIS', "")
            return ssn_number
        except Exception as E:

            data = "null"
            return data
