import re
import xlrd 
import os 
import json
import openpyxl

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FILES_FOLDER = os.path.join(BASE_DIR,'code\\Media\\')
SCRIPTS_FOLDER = os.path.join(BASE_DIR,'code\\Scripts\\')

# Read config json file and store in an object
f = open(os.path.join(SCRIPTS_FOLDER, 'metadata.json'))
json_string = f.read()
config = json.loads(json_string)
f.close()

ruleList=[]
for rule in config:
	ruleList.append(rule["rulelabel"])

print(ruleList)

