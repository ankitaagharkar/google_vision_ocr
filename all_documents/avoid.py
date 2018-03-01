import re


def replace(actual_name):
    actual_name1 = actual_name.replace('DONAR', "")
    actual_name1 = actual_name.replace(' BE ', " ")
    actual_name1 = actual_name1.replace('KAROLA', "")
    actual_name1 = actual_name1.replace('B-', "")
    actual_name1 = actual_name1.replace('Exo', "")
    actual_name1 = actual_name1.replace(' IMWHS ', "")
    actual_name1 = actual_name1.replace('MEmp', "")
    actual_name1 = actual_name1.replace('Notes', "")
    actual_name1 = actual_name1.replace(' OLI ', "")
    actual_name1 = actual_name1.replace('Vlas', "")
    actual_name1 = actual_name1.replace('Exp', "")
    actual_name1 = actual_name1.replace('LICENCE', "")
    actual_name1 = actual_name1.replace('bentu', "")
    actual_name1 = actual_name1.replace('ORGAN', "")
    actual_name1 = actual_name1.replace('nacrtaa', "")
    actual_name1 = actual_name1.replace('RUOSEPH', "JOSEPH")
    actual_name1 = actual_name1.replace('IUOSEPH', "JOSEPH")
    actual_name1 = actual_name1.replace('OONOR', "")
    actual_name1 = actual_name1.replace('ires', "")
    actual_name1 = actual_name1.replace('Dups', "")
    actual_name1 = actual_name1.replace('Neder', "")
    actual_name1 = actual_name1.replace('dass', "")
    actual_name1 = actual_name1.replace('AOhio', "")
    actual_name1 = actual_name1.replace('OD.', "")
    actual_name1 = actual_name1.replace('DRIVER', "")
    actual_name1 = actual_name1.replace(' EXL', "GU")
    actual_name1 = actual_name1.replace(':', "")
    actual_name1 = actual_name1.replace('JTD', "")
    actual_name1 = actual_name1.replace('LICENSE', "")
    actual_name1 = actual_name1.replace('License', "")
    actual_name1 = actual_name1.replace('Null', "")
    actual_name1 = actual_name1.replace(' USA ', "")
    actual_name1 = actual_name1.replace('EYES', "")
    actual_name1 = actual_name1.replace('PAYTOTHE', "")
    actual_name1 = actual_name1.replace(' TO ', "")
    actual_name1 = actual_name1.replace('THE', "")
    actual_name1 = actual_name1.replace('ORDER', "")
    actual_name1 = actual_name1.replace('No', "")
    actual_name1 = actual_name1.replace('Payro', "")
    actual_name1 = actual_name1.replace(' OC ', "")
    actual_name1 = actual_name1.replace(' OF', "")
    actual_name1 = actual_name1.replace(' LN', "")
    actual_name1 = actual_name1.replace(' EN ', "")
    actual_name1 = actual_name1.replace(' AP ', "")
    actual_name1 = actual_name1.replace('Expires', "")
    actual_name1 = actual_name1.replace('Name', "")
    actual_name1 = actual_name1.replace('DENONE', "")
    actual_name1 = actual_name1.replace('NONE', "")
    actual_name1 = actual_name1.replace('Address', "")
    actual_name1 = actual_name1.replace('CLASS D', "")
    actual_name1 = actual_name1.replace('CLASS', "")
    actual_name1 = actual_name1.replace('CLASSE', "")
    actual_name1 = actual_name1.replace('CLASEXP', "")
    actual_name1 = actual_name1.replace('EXP', "")
    actual_name1 = actual_name1.replace('CEXP', "")
    actual_name1 = actual_name1.replace('ISS', "")
    actual_name1 = actual_name1.replace('SExr', "")
    actual_name1 = actual_name1.replace('Payroll', "")
    actual_name1 = actual_name1.replace('Attn', "")
    actual_name1 = actual_name1.replace('GEXP', "")
    actual_name1 = actual_name1.replace('Class D', "")
    actual_name1 = actual_name1.replace('Class', "")
    actual_name1 = actual_name1.replace('class D', "")
    actual_name1 = actual_name1.replace('class C', "")
    actual_name1 = actual_name1.replace('class', "")
    actual_name1 = actual_name1.replace(' DM ', "")
    actual_name1 = actual_name1.replace('Height', "")
    actual_name1 = actual_name1.replace('Expires', "")
    actual_name1 = actual_name1.replace('Expiros', "")
    actual_name1 = actual_name1.replace('Expires', "")
    actual_name1 = actual_name1.replace(' arark ', "")
    actual_name1 = actual_name1.replace(' VA ', "")
    actual_name1 = actual_name1.replace('Name', "")
    actual_name1 = actual_name1.replace('NOWY', "")
    actual_name1 = actual_name1.replace('DENONE', "")
    actual_name1 = actual_name1.replace('NONE', "")
    actual_name1 = actual_name1.replace('Address', "")
    actual_name1 = actual_name1.replace('CLASS D', "")
    actual_name1 = actual_name1.replace('CLASS C', "")
    actual_name1 = actual_name1.replace('CLASS', "")
    actual_name1 = actual_name1.replace('CLASSE', "")
    actual_name1 = actual_name1.replace('CLASEXP', "")
    actual_name1 = actual_name1.replace('EXP', "")
    actual_name1 = actual_name1.replace('Cass D', "")
    actual_name1 = actual_name1.replace('Cass', "")
    actual_name1 = actual_name1.replace(' ISS ', "")
    actual_name1 = actual_name1.replace('SExr', "")
    actual_name1 = actual_name1.replace('GEXP', "")
    actual_name1 = actual_name1.replace('ORGAN', "")
    actual_name1 = actual_name1.replace('DONOR', "")
    actual_name1 = actual_name1.replace('DONORJawa', "")
    actual_name1 = actual_name1.replace('DOB', "")
    actual_name1 = actual_name1.replace('ub', "")
    actual_name1 = actual_name1.replace('Cit', "")
    actual_name1 = actual_name1.replace('exp ', "")
    actual_name1 = actual_name1.replace('=', " ")
    actual_name1 = actual_name1.replace(',', " ")
    actual_name1 = actual_name1.replace('@', " ")
    actual_name1 = actual_name1.replace('#', " ")
    actual_name1 = actual_name1.replace('%', " ")
    actual_name1 = actual_name1.replace('class', "")
    actual_name1 = actual_name1.replace('^', " ")
    actual_name1 = actual_name1.replace('CGA', "")
    actual_name1 = actual_name1.replace('CONG', "")
    actual_name1 = actual_name1.replace('identifier', "")
    actual_name1 = actual_name1.replace('EENHANCED', "")
    actual_name1 = actual_name1.replace(' am ', "")
    actual_name1 = actual_name1.replace(' Mal ', "")
    actual_name1 = actual_name1.replace(' OL ', "")
    actual_name1 = actual_name1.replace('GIN', "")
    actual_name1 = actual_name1.replace('CASS', "")
    actual_name1 = actual_name1.replace('ADP ', "")
    actual_name1 = actual_name1.replace('CITY', "")
    actual_name1 = actual_name1.replace(' SU ', "")
    actual_name1 = actual_name1.replace('MWAberty', "")
    actual_name1 = actual_name1.replace('FILE', "")
    actual_name1 = actual_name1.replace('WILLIAMS RICHARD NI', "WILLIAMS RICHARD J")
    actual_name1 = actual_name1.replace('Beginning', "")
    actual_name1 = actual_name1.replace('Beginning', "")
    actual_name1 = actual_name1.replace('igs', "")
    actual_name1 = actual_name1.replace('exo ', "")
    actual_name1 = actual_name1.replace('Statement', "")
    actual_name1 = actual_name1.replace('Single', "")
    actual_name1 = actual_name1.replace('Exemptions', "")
    actual_name1 = actual_name1.replace('Parasti', "")
    actual_name1 = actual_name1.replace('JR', "")
    # actual_name1 = actual_name1.replace('NG ', "")
    actual_name1 = actual_name1.replace(' ICE', "")
    actual_name1 = actual_name1.replace('Prestas', "")
    actual_name1 = actual_name1.replace('Ss ', "")
    actual_name1 = actual_name1.replace('ss ', "")
    actual_name1 = actual_name1.replace('EX-', "")
    actual_name1 = actual_name1.replace('E-', "")
    actual_name1 = actual_name1.replace('SBE C', "")
    actual_name1 = actual_name1.replace('EX ', "")
    actual_name1 = actual_name1.replace('Ex ', "")
    actual_name1 = actual_name1.replace('Ex ', "")
    actual_name1 = actual_name1.replace('owances', "")
    actual_name1 = actual_name1.replace(' DRI', "DR")
    actual_name1 = actual_name1.replace('Issued', "")
    actual_name1 = actual_name1.replace('Iss ', "")
    actual_name1 = actual_name1.replace('HS ', "")
    actual_name1 = actual_name1.replace('EARLENE MICHELLEPUIG ', "SHAEARLENE MICHELLE PUIG")
    actual_name1 = actual_name1.replace('Maso', "")
    actual_name1 = actual_name1.replace(' EER ', "")
    actual_name1 = actual_name1.replace('Federa', "")
    actual_name1 = actual_name1.replace('NY ', "")
    actual_name1 = actual_name1.replace(' UN ', "")
    actual_name1 = actual_name1.replace('Exr ', "")
    # actual_name1 = actual_name1.replace('Is ', "")
    actual_name1 = actual_name1.replace('un ', "")

    actual_name1 = re.sub(r"\b(!?es |iss |er |or |EN |EXP|HGT|Is |Earnings|Donor |AP |=|,|@|#|%|^|CGA| ER |CONG|EENHANCED|am|Mal| OL |GIN|CASS C |D |AD | SU |MWAberty|FILE|Beginning|Statement|ll|l |JTD|LICENSE| USA |EYES|DXP|FN|PAYTOTHE|DiP|DIP| IS | TO |THE |ORDER|No |Payro| OC | OF |LN | ADP |Expires|Name|DENONE|NONE|Address|CLASSE|CLASEXP|ISS|SExr|Payroll|Attn|GEXP|class|Class| DM |Height|Expiros|Cass|CLASS|ClassE|ORGAN|DONORJawa|DOB|ub|CD)",
        "",actual_name1)
    # actual_name1 = re.sub(
    #     r"\s(=?EXP|HGT|Earnings|Donor|AP |=|,|@|#|%|^|ER |CGA|CONG|EENHANCED|am|Mal| OL |GIN|CASS|C |D | AD | SU |MWAberty|FILE|Beginning|Statement|ll|l |JTD|LICENSE|USA |EYES|DXP|FN|PAYTOTHE|DiP|DIP|IS | TO |THE |ORDER|No |Payro| OC | OF |LN |EN |ADP |Expires|Name|DENONE|NONE|Address|CLASSE|CLASEXP|EXP|ISS|SExr|Payroll|Attn|GEXP|Class|DM |Height|Expiros|Cass|CLASS|ClassE|ORGAN|DONORJawa|DOB|ub|CD)\b",
    #     "", actual_name1)
    return actual_name1

def address_replace(value):
    if 'NU ' in value:
        value = value.replace('NU ', 'NJ ')
    elif re.search(
            r'\b(\s\d+\s([A-Za-z]+)?\s([A-Za-z]+)?\s?\s([A-Za-z]+)?\s?(\d+)?\s?([A-Za-z]+)?\s?(\d+)?\s?([A-Za-z]+)\s?[#.,/]?\s?(\w*)?\s?(!?NL))',
            value):
        value = value.replace(' NL ', ' NJ ')
    if re.search(
            r'\b(\s\d+\s([A-Za-z]+)?\s([A-Za-z]+)?\s?\s([A-Za-z]+)?\s?(\d+)?\s?([A-Za-z]+)?\s?(\d+)?\s?([A-Za-z]+)\s?[#.,/]?\s?(\w*)?\s?(!?N\.))',
            value):
        value = value.replace('N. ', ' NJ ')
    if ' NJI ' in value:
        value = value.replace(' NJI ', ' NJ ')
    if re.search(
            r'\b(\s\d+\s([A-Za-z]+)?\s([A-Za-z]+)?\s?\s([A-Za-z]+)?\s?(\d+)?\s?([A-Za-z]+)?\s?(\d+)?\s?([A-Za-z]+)\s?[#.,/]?\s?(\w*)?\s?(!? NO))',
            value):
        value = value.replace(' NO ', ' NJ ')
    if ' SU ' in value:
        value = value.replace(' SU ', ' NJ ')
    if '$' in value:
        value = value.replace('$', '6')
    if ' AJ ' in value:
        value = value.replace(' AJ ', ' NJ ')
    if ' NA ' in value:
        value = value.replace(' NA ', ' NJ ')
    if ' NW ' in value:
        value = value.replace(' NW ', ' NJ ')
    if re.search(
            r'\b(\s\d+\s([A-Za-z]+)?\s([A-Za-z]+)?\s?\s([A-Za-z]+)?\s?(\d+)?\s?([A-Za-z]+)?\s?(\d+)?\s?([A-Za-z]+)\s?[#.,/]?\s?(\w*)?\s?(!?NI))',
            value):
        value = value.replace(' NI', ' NJ ')

    if re.search(
            r'\b(\s\d+\s([A-Za-z]+)?\s([A-Za-z]+)?\s?\s([A-Za-z]+)?\s?(\d+)?\s?([A-Za-z]+)?\s?(\d+)?\s?([A-Za-z]+)\s?[#.,/]?\s?(\w*)?\s?(!?J))',
            value):
        value = value.replace(' J ', ' NJ ')

    return value

def name_replace(text_value,date,zip_code):
    text_value = text_value.replace(' EX ', " ")
    text_value = text_value.replace(' DOB ', " ")
    text_value = text_value.replace(' Dob ', " ")
    text_value = text_value.replace(' names ', " ")
    text_value = text_value.replace(' Given ', " ")
    text_value = text_value.replace(' Family ', " ")
    text_value = text_value.replace(' name ', " ")
    text_value = text_value.replace(' Names ', " ")
    text_value = text_value.replace(' Name ', " ")
    text_value = text_value.replace(' Address ', " ")
    text_value = text_value.replace(' dob ', " ")
    text_value = text_value.replace(' CLASSD ', " ")
    text_value = text_value.replace(' C3 ', " ")
    text_value = text_value.replace(' CLASS D ', " ")
    text_value = text_value.replace(' Class D ', " ")
    text_value = text_value.replace(' Ex ', " ")
    text_value = text_value.replace(' ex ', " ")
    name_val, value = '', ''
    text_value = text_value.replace(' a ', "")

    val = date.split(",")
    for i in range(len(val)):
        text_value = text_value.replace(val[i], "")
    if re.search(r'(!?GA|PA)', zip_code):
        if re.search('!?Organ|Donar|ORGAN|DONAR', text_value):
            text_value = text_value.replace(' '.join(map(str, text_value.split(
                re.findall(r"(=?Expires:|EXP|Expires|Exp|Expiros|EXPIRES|EXPIROS|EER)", text_value)[0], 1)[1].split()[
                                                              0:2])), "")
    if re.search('(!?NV|OH|TX|WA|CT|MA|NC|CO|DE|ID|IN|PA|KS|ME|MS|MT|NE|NH|ND|SD|UT|VT|WI)', zip_code):
        if re.search(r'\b\s?(!?8|2)\s?\w+', text_value):
            text_value = text_value.replace('8', ' ', 1)
            text_value = text_value.replace('2', ' ', 1)
    value = text_value.replace(":", "")

    return value



