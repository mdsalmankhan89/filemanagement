 
 


filepath = "C:\\Users\\salman\\Desktop\\DjangoLearning\\projects\\DataIngestion\\filemanagement\\fileingest\\code\\Media\\AP&ISA_202002Feb_Maximo_Resoln_wos_BI_20200310.xlsx"
rule = {"columns":["col7","col8","col9"]}
csvfolderroot =  "C:\\Users\\salman\\Desktop\\DjangoLearning\\projects\\DataIngestion\\filemanagement\\fileingest\\code\\Media\\"

def exceltocsv(filepath):
    book = openpyxl.load_workbook(filepath)
    for sheetname in book.sheetnames:
        
        xl_sheet = book[sheetname]
        no_of_rows = xl_sheet.max_row
        
        counter = 1
        while counter < no_of_rows:
            columns=[]
            
            for cell in xl_sheet[counter]:
                columns.append(cell.value)

            if [item for item in rule["columns"] if item not in columns]:
                counter = counter + 1
                if counter > 50:
                    break
                continue
            else:
                col_offset = 0
                for val in columns:
                    if val is None:
                        col_offset += 1
                
                rowstart = counter-1

                xl_sheet.delete_cols(1, col_offset)
                xl_sheet.delete_rows(1,rowstart)

                break
            if counter > 50:
                print("header not found")
    book.save(filepath)

    df = pd.read_excel(filepath, sheet_name=None)
     
    for key, value in df.items():
	    df[key].to_csv('%s%s.csv' %(csvfolderroot ,key),index =None, header= True)		 

exceltocsv(filepath)