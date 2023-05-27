import requests
import pandas as pd
from datetime import datetime
import country_converter as coco

res = requests.get('https://api.henleypassportindex.com/api/passports')
data = res.json()

code_list = [{'code': item.get('code'), 'country': item.get('name')} for item in data if item.get('code') != '']
# sort by country name instead of code
code_list = sorted(code_list, key=lambda k: k['country'])

origin_lst = []
origin_code_lst = []
destination_lst = []
destination_code_lst = []
requirement = []
visa_free_count_lst = []
visa_required_count_lst = []
origin_for_count = []
visa_free = 'Visa Free'
e_visa = 'eVisa'
visa_required = 'Visa Required'

for origin in code_list:
    origin_country = origin.get('country')
    if origin.get('code') == 'FW':
        origin_code = 'GLP'
    else:
        origin_code = coco.convert(names=origin.get('code'), to='ISO3')
    origin_for_count.append(origin_country)
    count_vf = 0
    count_vr = 0
    res = requests.get('https://api.henleypassportindex.com/api/passports/' + origin.get('code') + '/countries')
    data = res.json()
    for destination in data['default']:
        destination_country = destination.get('name')
        if destination.get('code') == 'FW':
            destination_code = 'GLP'
        else:
            destination_code = coco.convert(names=destination.get('code'), to='ISO3')
        origin_lst.append(origin_country)
        origin_code_lst.append(origin_code)
        destination_lst.append(destination_country)
        destination_code_lst.append(destination_code)
        is_visa_free = destination.get('pivot').get('is_visa_free')
        if str(is_visa_free) == "1":
            count_vf += 1
            requirement.append(visa_free)
        else:
            if str(origin_country) == str(destination_country):
                requirement.append("N/A")
            else:
                if str(destination.get('pivot').get('visa_access_id')) == "3":
                    requirement.append(e_visa)
                    count_vf += 1
                else:
                    count_vr += 1
                    requirement.append(visa_required)

    visa_free_count_lst.append(count_vf)
    visa_required_count_lst.append(count_vr)

today_date = datetime.today().strftime('%Y-%m-%d')
file_name = "henley-passport-index" + "-" + today_date + ".csv"

pd_1 = pd.DataFrame({'Origin': origin_lst, 'Origin Code': origin_code_lst,
                     'Destination': destination_lst, 'Destination Code': destination_code_lst,
                     'Requirement': requirement})
pd_1.to_csv(file_name, index=False)

# filter unique countries in origin_lst
origin_lst = list(set(origin_lst))
# filter unique countries in destination_lst
destination_lst = list(set(destination_lst))

print(
    "Total number of countries in origin_lst: " + str(len(origin_lst)),
    "Total number of countries in destination_lst: " + str(len(destination_lst))
)

today_date = datetime.today().strftime('%Y-%m-%d')
file_name = "henley-passport-index-count" + "-" + today_date + ".csv"

pd_2 = pd.DataFrame(
    {'Origin': origin_for_count, 'Origin Code': [d['code'] for d in code_list],
     'Visa Free': visa_free_count_lst, 'Visa Required': visa_required_count_lst})
pd_2.to_csv(file_name, index=False)

print(pd_2.sort_values('Visa Required').to_string())

pd_1.to_csv('visa_requirements.csv', sep=',', encoding='utf-8')
pd_2.to_csv('visa_free_statistics.csv', sep=',', encoding='utf-8')
