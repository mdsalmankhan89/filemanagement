import openpyxl
import os
import re 


 
def validateFileExtension(filepath,validationResult):

    extension  = os.path.splitext(filepath)[1]

    #check if extension is correct
    if re.search(".xlsx",extension,re.IGNORECASE):
        validationResult.update({'extension':True})
    else:
        validationResult.update({'extension':False})

    return validationResult

def validateFileNamePattern(rules,filepath,validationResult,module):
    filename = os.path.basename(filepath)
    validationResult.update({'filename_pattern':["",filename,False]})
    
    for rule in rules:
        ruleJSON = json.loads(rule.ruleJSON)
        if re.search(ruleJSON["filename_pattern"],filename,re.IGNORECASE) and re.search(ruleJSON["module"],module,re.IGNORECASE):
            validationResult.update({'filename_pattern':[ruleJSON["filename_pattern"],filename,True]})
    
    return validationResult

def validatePeriodPattern(rules,filepath,validationResult):
    filename = os.path.basename(filepath)
    validationResult.update({'period_pattern':["",filename,"",False]})

    for rule in rules:
        ruleJSON = json.loads(rule.ruleJSON)

        if re.search(ruleJSON["filename_pattern"],filename,re.IGNORECASE) and re.search(ruleJSON["module"],module,re.IGNORECASE):

            if re.search(ruleJSON["pattern_period"],filename,re.IGNORECASE):
                validationResult.update({'period_pattern':[ruleJSON["period_pattern"],filename,(re.search(ruleJSON["pattern_period"],filename,re.IGNORECASE)).group(0),True]})
                break
            else:
                validationResult.update({'period_pattern':[ruleJSON["period_pattern"],filename,"",False]})

    return validationResult

def validateSheets(rules,filepath,validationResult):
    expectedsheets = {}

    book = openpyxl.load_workbook(filepath)
    presentSheets = book.sheetnames

    for rule in rules:
        ruleJSON = json.loads(rule.ruleJSON)

        if (re.search(ruleJSON["module"],module,re.IGNORECASE) and re.search(ruleJSON["period_pattern"],validationResult["period_pattern"][0],re.IGNORECASE) and re.search(ruleJSON["filename_pattern"],validationResult["filename_pattern"][0],re.IGNORECASE)):
            if ([item for item in ruleJSON["sheetname_pattern"] if item not in presentSheets]):
                expectedsheets.update({ruleJSON["sheetname_pattern"]:True})
            else:
                expectedsheets.update({ruleJSON["sheetname_pattern"]:False})
    
    if [item for item in [False] if item not in expectedsheets.values()]:
        validationResult.update({'sheetname_pattern':[expectedsheets,False]})
    else:
        validationResult.update({'sheetname_pattern':[expectedsheets,True]})
    
    return validationResult



def validateColumns(rules,filepath,validationResult):
    expectedresult = {}
    book = openpyxl.load_workbook(filepath) 

    for sheetname in book.sheetnames:
        partialmatch_Header=0 
        partialmatch_Counter =0 
        partial_delta = []
        xl_sheet = book[sheetname]

        for rule in rules:
            ruleJSON = json.loads(rule.ruleJSON)

            if re.search(ruleJSON["module"],module,re.IGNORECASE) and re.search(ruleJSON["period_pattern"],validationResult["period_pattern"][0],re.IGNORECASE) and re.search(ruleJSON["filename_pattern"],validationResult["filename_pattern"][0],re.IGNORECASE) and re.search(ruleJSON["sheetname_pattern"],sheetname,re.IGNORECASE):
                                
                if ruleJSON["header"] and ruleJSON["column_offset"]:
                    columns=[]
                    for cell in xl_sheet[ruleJSON["header"]]:
                        columns.append(cell.value)
                    missing_columns =  [item for item in ruleJSON["columns"] if item not in columns]

                    if missing_columns:
                        expectedresult.update({"sheetname":[ruleJSON["columns"],missing_columns,ruleJSON["header"],ruleJSON["column_offset"],False,None]})
                    else:
                        expectedresult.update({"sheetname":[ruleJSON["columns"],None,ruleJSON["header"],ruleJSON["column_offset"],True,rule.ruleid]})
                        if ruleJSON["column_offset"] > 0:
                            xl_sheet.delete_cols(1, ruleJSON["column_offset"])
                        if ruleJSON["header"]>1 :
                            xl_sheet.delete_rows(1,(ruleJSON["header"]-1))
                
                if (ruleJSON["header"] == "" or ruleJSON["header"] is None):
                    no_of_rows = xl_sheet.max_row
                    counter = 1
                    while counter < no_of_rows:
                        columns=[]
                        for cell in xl_sheet[counter]:
                            columns.append(cell.value)
                            
                        if [item for item in ruleJSON["columns"] if item not in columns]:
                            if counter==1:
                                partialmatch_Counter = len([item for item in ruleJSON["columns"] if item not in columns])
                                partialmatch_Header = counter
                                partial_delta = [item for item in ruleJSON["columns"] if item not in columns]
                                partial_col_offset = 0
                                for val in columns:
                                    if val is None:
                                        partial_col_offset += 1
                            elif  partialmatch_Counter > len([item for item in ruleJSON["columns"] if item not in columns]):
                                partialmatch_Counter = len([item for item in ruleJSON["columns"] if item not in columns])
                                partialmatch_Header = counter
                                partial_delta = [item for item in ruleJSON["columns"] if item not in columns]
                                partial_col_offset = 0
                                for val in columns:
                                    if val is None:
                                        partial_col_offset += 1
                                        
                            counter = counter + 1
                            if counter > 50:
                                break
                            continue
                        else:
                            if ruleJSON["column_offset"]:
                                if col_offset > 0:
                                    xl_sheet.delete_cols(1, ruleJSON["column_offset"])
                                if counter > 1 :
                                    xl_sheet.delete_rows(1,(counter-1))
                                expectedresult.update({"sheetname":[ruleJSON["columns"],None,counter,ruleJSON["column_offset"],True,rule.ruleid]})
                                
                            else:
                                col_offset = 0
                                for val in columns:
                                    if val is None:
                                        col_offset += 1
                                if col_offset > 0:
                                    xl_sheet.delete_cols(1, col_offset)
                                if counter > 1 :
                                    xl_sheet.delete_rows(1,(counter-1))
                                expectedresult.update({"sheetname":[ruleJSON["columns"],None,counter,col_offset,True,rule.ruleid]})
                            break

                    if counter > 50:
                        print (partialmatch_Counter)
                        print (partialmatch_Header)
                        print (partial_delta )
                        print ("header not found")
                        expectedresult.update({"sheetname":[ruleJSON["columns"],partial_delta,partialmatch_Header,partial_col_offset,False,None]})

    result =[]
    for resvals in expectedresult.values():
        result.append = resvals[4]
    
    if [item for item in [False] if item not in result]:
        validationResult.update({'columns':[expectedresult,False]})
    else:
        validationResult.update({'columns':[expectedresult,True]})

    return validationResult
                

def validate(filepath,module):
    rules = Rules.objects.all()

    validationResult  = {}

    validationResult = validateFileExtension(filepath,validationResult)

    if validationResult["extension"] == True:
        
        validationResult = validateFileNamePattern(rules,filepath,validationResult,module)

        if validationResult["filename_pattern"][2]== True:

            validationResult = validatePeriodPattern(rules,filepath,validationResult)

            if validationResult["period_pattern"][3] == True:

                validationResult = validateSheets(rules,filepath,validationResult)

                if validationResult["sheetname_pattern"][1] ==True:

                    validationResult=validateColumns(rules,filepath,validationResult)

                    if validationResult["columns"][1] == True:
                        print ("success")

