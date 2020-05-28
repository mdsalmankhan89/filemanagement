import requests

url = "http://127.0.0.1:8000/account/uploadAPI/"
filepath = 'C:/Users/salman/Desktop/DjangoLearning/projects/DataIngestion/filemanagement/fileingest/code/Media/APISA_202003Mar_Maximo_OpenWO_wos_BI_20200310.xlsx'
payload = {'module': 'Maximo'}
files = [
  ('files', open(filepath,'rb'))
]
headers = {
  'Authorization': 'Token 6c6565ed8deeb1d23fe7802311a397dbfccc1a71'
}

response = requests.request("POST", url, headers=headers, data = payload, files = files)

print(response.text.encode('utf8'))