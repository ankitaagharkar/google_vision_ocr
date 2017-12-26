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
    def get_address_zipcode(self,full_address,zipcode):
        try:
            code = zipcode.split()
            city = ' '.join(map(str, full_address.split(code[0], 1)[0].split()[-2:]))
            return code[0], code[1], city
        except Exception as e:
            print(e)