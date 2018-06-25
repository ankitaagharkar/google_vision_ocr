import re

import googlemaps
# output={'address': ['MALCOLM CLAY 11', '7023 SOUDER STREET', 'PHILADELPHIA PA 19149']}
# output={"address": ['6433 Champion Grandview Way Building 1 Austin, TX 78750', "Gregory O'Connell 28 Somerset Road Mahopac, NY 10541"]}


# if 'address' in output:
#     if len(output["address"]) > 1:
#         replace_val = ''
#         gmaps = googlemaps.Client(key='AIzaSyCao8hUleolUVnfFVI3CmBHECSbO1FZFpg')
#         json_val = gmaps.geocode(" ".join(map(str, output['address'])))
#         print(json_val)
#         for i in range(len(json_val[0]['address_components'])):
#             # #print(json_val[0]['address_components'][i]['types'])
#             if json_val[0]['address_components'][i]['types'] == ['route']:
#                 replace_val = " ".join(map(str, json_val[0]['formatted_address'].split()[:-1])).replace(',',
#                                                                                                         '').replace(
#                     json_val[0]['address_components'][i]['short_name'],
#                     json_val[0]['address_components'][i]['long_name'])
#                 print(replace_val)
#             if output['address'][0] != json_val[0]['formatted_address']:
#                 output['name'] = output['address'][0].replace(',', '').replace(replace_val, '')
#         output['address'][0] = output['address'][0].replace(output['name'], '')
#         output['name']=[output['name']]
#
#
# if 'address' in output:
#     if len(output["address"]) > 1:
#         replace_val = ''
#         gmaps = googlemaps.Client(key='AIzaSyCao8hUleolUVnfFVI3CmBHECSbO1FZFpg')
#         if re.search(r'(!?ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)', output['address'][0].split()[0],
#                          re.IGNORECASE) or  re.search('([A-Za-z]+\s?\d+)?|\d+', output['address'][0].split()[0],re.IGNORECASE):
#             json_val = gmaps.geocode(" ".join(map(str, output['address'][1])))
#             print(json_val)
#             for i in range(len(json_val[0]['address_components'])):
#                 # #print(json_val[0]['address_components'][i]['types'])
#                 if json_val[0]['address_components'][i]['types'] == ['route']:
#                     replace_val = " ".join(map(str, json_val[0]['formatted_address'].split()[:-1])).replace(',',
#                                                                                                             '').replace(
#                         json_val[0]['address_components'][i]['short_name'],
#                         json_val[0]['address_components'][i]['long_name'])
#                     print(replace_val)
#                 if output['address'][1] != json_val[0]['formatted_address']:
#                     output['name'] = output['address'][1].replace(',', '').replace(replace_val, '')
#             output['address'][1] = output['address'][1].replace(output['name'], '')
#             output['name']=[output['name']]
# # if 'address' in output:
# #     if len(output["address"])>1:
# #         import googlemaps
# #
# #         replace_val=''
# #         gmaps = googlemaps.Client(key='AIzaSyCao8hUleolUVnfFVI3CmBHECSbO1FZFpg')
# #         json_val = gmaps.geocode(output['address'][1])
# #         print(json_val)
# #         for i in range(len(json_val[0]['address_components'])):
# #             # #print(json_val[0]['address_components'][i]['types'])
# #             if json_val[0]['address_components'][i]['types'] == ['route']:
# #                 replace_val = " ".join(map(str, json_val[0]['formatted_address'].split()[:-1])).replace(',','').replace(json_val[0]['address_components'][i]['short_name'],
# #                     json_val[0]['address_components'][i]['long_name'])
# #                 print(replace_val)
# #             if output['address'][1] != json_val[0]['formatted_address']:
# #                 output['name'] = output['address'][1].replace(',', '').replace(replace_val, '')
# #                 output['address1'] = [output['address'][1].replace(output['name'], '')]
# #         output['address'][1] = output['address'][1].replace(output['address'][1], '')
#                 # break
#         print(output)


