import re
import xlrd 
import os 
import json
import openpyxl

script_path = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(script_path))
FILES_FOLDER = os.path.join(PROJECT_ROOT, 'Media\\')
SCRIPTS_FOLDER = os.path.join(PROJECT_ROOT, 'Scripts\\')

# Read config json file and store in an object
f = open(os.path.join(SCRIPTS_FOLDER, 'metadata.json'))
json_string = f.read()
config = json.loads(json_string)
f.close()

filename = "AP&ISA_202002Feb_Maximo_Resoln_wos_BI_20200310.xlsx"
filepath = os.path.join(FILES_FOLDER, filename)

ruleid  = 2  # to be taken as an input 

rule = config[ruleid]



if (re.search(rule["pattern_period"],filename,re.IGNORECASE)): #1st check for 
	period = re.search(rule["pattern_period"],filename,re.IGNORECASE).group()[:6]
	book = xlrd.open_workbook(filepath)
	
	for sheetname in book.sheet_names():
		xl_sheet = book.sheet_by_index(sheetname)
		print(xl_sheet.row_values(0)) 
	#	a = ["col1","col7","col8","col9"]
	#	diff = list(set(a) - set(xl_sheet.row(0)))
	#	print((xl_sheet.row(0))[0])
	#	print(diff)
	
 