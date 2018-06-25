import difflib

import googlemaps,re


def main():
    output=[{'name': [], 'address': ['Indeed, Inc. 6433 Champion Grandview Way Building 1 Austin, TX 78750']}, {'name': [], 'address': ['Indeed, Inc. 6433 Champion Grandview Way Building 1 Austin, TX 78750', "Gregory O'Connell 28 Somerset Road Mahopac, NY 10541"]}, {'name': [], 'address': ['6433 Champion Grandview Way Building 1 Austin, TX 78750']}, {'name': [], 'address': ['6433 Champion Grandview Way Building 1 Austin, TX 78750', "Gregory O'Connell 28 Somerset Road Mahopac, NY 10541"]}]

    address_name=[]
    code=''
    replace_val=''
    new_ouput={}
    google_ouput=[]
    main_output=[]
    with open("../config/states", "r") as all_state_val:
        state_name = all_state_val.read().replace('\n', '')
    with open("../config/postal_code_regex", "r") as post_val:
        post_code = post_val.read()
    for i in range(len(output)):
        if output[i]["name"]==[]:
            name=''
        else:
            name=output[i]["name"][0]
        if len(output[i]["address"])>1:
            temp_address_name=name+" "+output[i]["address"][0]+" "+output[i]["address"][1]


            data = re.findall(r'(\s|\,)\b(!?' + state_name + ')(\s|\.|\,|\-|\,\s)+(' + post_code + ')', temp_address_name)
            code = " ".join(map(str, data[0]))
            code = code.replace('   ', ' ').lstrip()
            code = code.replace('   ', ' ').rstrip()
            a=temp_address_name
            address_name.append(temp_address_name.split(code)[0]+" "+code)
            address_name.append(a.split(code)[1])


        else:
            temp_address_name = name + " " + output[i]["address"][0]
        # print(address_name)
            data = re.findall(r'(\s|\,)\b(!?' + state_name + ')(\s|\.|\,|\-|\,\s)+(' + post_code + ')', temp_address_name)
            code = " ".join(map(str, data[0]))
            code = code.replace('   ', ' ').lstrip()
            code = code.replace('   ', ' ').rstrip()
            address_name.append(temp_address_name.split(code)[0] + " " + code)
    # print(address_name)



    for i in range(len(address_name)):
            print(address_name[i])
            gmaps = googlemaps.Client(key='AIzaSyCao8hUleolUVnfFVI3CmBHECSbO1FZFpg')
            if not re.search(r'(!?ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)',address_name[i].split()[0],
                         re.IGNORECASE) or not re.search('([A-Za-z]+\s?\d+)?|\d+', address_name[i].split()[0],
                                                     re.IGNORECASE):
                json_val = gmaps.geocode(address_name[i])
                # print(json_val)
                new_ouput={}
                for j in range(len(json_val[0]['address_components'])):
                    # #print(json_val[0]['address_components'][i]['types'])
                    if json_val[0]['address_components'][j]['types'] == ['route']:
                        replace_val = " ".join(map(str, json_val[0]['formatted_address'].split()[:-1])).replace(',',
                                                                                                                '').replace(
                            json_val[0]['address_components'][j]['short_name'],
                            json_val[0]['address_components'][j]['long_name'])
                        # print(replace_val)

                        if address_name[i] != json_val[0]['formatted_address']:
                            x = difflib.get_close_matches(json_val[0]['formatted_address'].lower(), [vt.lower() for vt in google_ouput],
                                                          cutoff=0.95)
                            if not x:
                                google_ouput.append(json_val[0]['formatted_address'])
                                address_name[i]=address_name[i].replace(',', '')
                                address_name[i]=address_name[i].replace('  ', ' ')
                                new_ouput['name'] = address_name[i].split(replace_val.split()[0])[0]
                                new_ouput['address'] = address_name[i].replace(new_ouput['name'], '')
                                main_output.append(new_ouput)
                                break

    print(main_output)


main()