import re


def replace(actual_name):
    actual_name=re.sub(r"\s?(!?HGT|Earnings|GIN| AD| SU |MWAberty|FILE|Beginning|Statement|ll| l|JTD|LICENSE"
                       r"|USA|EYES|PAYTOTHE|DiP|DIP|IS| TO | THE |ORDER|No|Payro| OC | OF | LN | EN | AP |Expires|Name|DENONE|NONE"
                       r"|Address|CLASS|CLASSE|CLASEXP|EXP|ISS|SExr|Payroll|Attn|GEXP|Class|DM|Height|Expiros"
                       r"|Cass|ORGAN|DONOR|DONORJawa|DOB|ub|CD)", "", actual_name)
    actual_name = actual_name.replace(' EXL', "GU")
    # actual_name = actual_name.replace(' HGT ', "")
    # actual_name = actual_name.replace(' Earnings ', "")
    # actual_name = actual_name.replace(' GIN ', "")
    # actual_name = actual_name.replace(' AD ', "")
    # actual_name = actual_name.replace(' FILE ', "")
    # actual_name = actual_name.replace(' Beginning ', "")
    # actual_name = actual_name.replace(' Statement ', "")
    actual_name = actual_name.replace(':', "")
    # actual_name = actual_name.replace(' l ', "")
    # actual_name = actual_name.replace(' JTD ', "")
    # actual_name = actual_name.replace(' LICENSE ', "")
    # actual_name = actual_name.replace(' USA ', "")
    # actual_name = actual_name.replace(' EYES ', "")
    # actual_name = actual_name.replace(' PAYTOTHE ', "")
    # actual_name = actual_name.replace(' TO ', "")
    # actual_name = actual_name.replace(' THE ', "")
    # actual_name = actual_name.replace(' ORDER ', "")
    # actual_name = actual_name.replace(' No ', "")
    # actual_name = actual_name.replace(' Payro ', "")
    # actual_name = actual_name.replace(' OC ', "")
    # actual_name = actual_name.replace(' OF  ', "")
    # actual_name = actual_name.replace(' LN  ', "")
    # actual_name = actual_name.replace(' EN  ', "")
    # actual_name = actual_name.replace(' AP ', "")
    # actual_name = actual_name.replace(' Expires ', "")
    # actual_name = actual_name.replace(' Name ', "")
    # actual_name = actual_name.replace(' DENONE ', "")
    # actual_name = actual_name.replace(' NONE ', "")
    # actual_name = actual_name.replace(' Address ', "")
    # actual_name = actual_name.replace(' CLASS D ', "")
    # actual_name = actual_name.replace(' CLASSE ', "")
    # actual_name = actual_name.replace(' CLASEXP ', "")
    # actual_name = actual_name.replace(' EXP ', "")
    # actual_name = actual_name.replace(' CLASS ', "")
    # actual_name = actual_name.replace(' ISS ', "")
    # actual_name = actual_name.replace(' SExr ', "")

    # actual_name = actual_name.replace(' Payroll ', "")
    # actual_name = actual_name.replace(' Attn ', "")
    # actual_name = actual_name.replace(' GEXP ', "")
    # actual_name = actual_name.replace(' Class ', "")
    # actual_name = actual_name.replace(' DM ', "")
    # actual_name = actual_name.replace(' Height ', "")
    # actual_name = actual_name.replace(' Expires ', "")
    # actual_name = actual_name.replace(' Expiros ', "")
    # actual_name = actual_name.replace(' Expires ', "")
    # actual_name = actual_name.replace(' VA ', "")
    # actual_name = actual_name.replace(' Name ', "")
    # actual_name = actual_name.replace(' DENONE ', "")
    # actual_name = actual_name.replace(' NONE ', "")
    # actual_name = actual_name.replace(' Address ', "")
    # actual_name = actual_name.replace(' CLASS D ', "")
    # actual_name = actual_name.replace(' CLASSE ', "")
    # actual_name = actual_name.replace(' CLASEXP ', "")
    # actual_name = actual_name.replace(' EXP ', "")
    # actual_name = actual_name.replace(' CLASS ', "")
    # actual_name = actual_name.replace(' Cass ', "")
    # actual_name = actual_name.replace(' ISS ', "")
    # actual_name = actual_name.replace(' SExr ', "")

    # actual_name = actual_name.replace(' GEXP ', "")
    # actual_name = actual_name.replace(' ORGAN ', "")
    # actual_name = actual_name.replace(' DONOR ', "")
    # actual_name = actual_name.replace(' DONORJawa ', "")
    # actual_name = actual_name.replace(' DOB ', "")
    # actual_name = actual_name.replace(' ub ', "")
    # actual_name = actual_name.replace(' CD ', "")
    return actual_name

