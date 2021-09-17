#EIA North America Rig Counts
import requests
import json
import os

url_eia_total = os.environ.get('EIA_API_RIGCNT_TOTAL')
url_eia_ng = os.environ.get('EIA_API_RIGCNT_NG')
url_eia_crude = os.environ.get('EIA_API_RIGCNT_CRUDE')
url_database = os.environ.get('LINK_RIGCNT')
token = os.environ.get('PA_API_TOKEN')

#Retrieve monthly (Natural Gas only)rig count from EIA website
url = url_eia_ng
resp = requests.get(url)
data_NGrigs = json.loads(resp.text)

#Retrieve monthly (Crude Oil only)rig count from EIA website
url = url_eia_crude
resp = requests.get(url)
data_CLrigs = json.loads(resp.text)

#Retrieve monthly total rig count from EIA website
url = url_eia_total
resp = requests.get(url)
data_Totalrigs = json.loads(resp.text)

#Check if database is updated with latest data. If no, then update

#Get the most recent datapoint from EIA data
year = data_Totalrigs['series'][0]['data'][0][0][:4]
month = data_Totalrigs['series'][0]['data'][0][0][4:6]
current_date = year + '-' + month

#Get the last datapoint from database
url = url_database
data = requests.get(url)
rigs = json.loads(data.text)
last_date = rigs[-1]['date']

#Update the database if current_date != last_date
if current_date == last_date:
    print('current_date:', current_date, 'is equal to last_date:', last_date, '- Database not updated')

else:
    headers = {'Authorization': token}

    payload = {
    'date': current_date,
    'total_oil': data_CLrigs['series'][0]['data'][0][1],
    'total_gas': data_NGrigs['series'][0]['data'][0][1],
    'total_rigs': data_Totalrigs['series'][0]['data'][0][1],
    }

    resp = requests.post(url, headers=headers, data=payload)
    print(resp)


