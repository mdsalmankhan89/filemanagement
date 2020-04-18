from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.files.storage import FileSystemStorage
import json
import re
import os
import openpyxl
from django.conf import settings
from django.conf.urls.static import static


from .forms import FileForm
from .models import Files, FileLogs, FilesData, Rules

# Create your views here.
def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		
		user = auth.authenticate(username=username, password=password)
		
		if user is not None:
			auth.login(request, user)
			return redirect("upload")
		else:
			messages.info(request,"Invalid credentials")
			return redirect('login')
	else:
		return render(request, 'login.html')
		
def logout(request):
	auth.logout(request)
	return redirect("/")
	
def upload(request):

	loglist = []
	
	filemetas = FilesData.objects.filter(userid=request.user.id)
	
	try:
		filelist = Files.objects.filter(user_id=request.user)
	except Files.DoesNotExist:
		filelist = None
	
	fileloglist = FileLogs.objects.all()
	
	if request.method == 'POST':
		form = FileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_files(request.FILES['files'],request.user)
			filelist = Files.objects.filter(user_id=request.user)
			upload_value = request.POST.get('ruleid')
			print(upload_value)
			return render(request, 'upload.html', { 'form' : form, 'filelist' : filelist, 'fileloglist' : fileloglist, 'filemetas' : filemetas  })
	else:
		form = FileForm()
	return render(request, 'upload.html', { 'form' : form, 'filelist' : filelist, 'fileloglist' : fileloglist, 'filemetas' : filemetas })
	

def handle_files(csv_file, user):

   newfile = Files(files=csv_file,user=user)
   newfile.save()

   entry = FileLogs(uploadid=Files.objects.get(uploadid=newfile.uploadid), files=csv_file, logs='File Loaded new')
   entry.save()
   
   validate(csv_file, newfile.files.url, newfile.uploadid)

def validate(csv_file, new_file, uploadid):
	
	print(csv_file)
	filedata = FilesData.objects.get(filename=csv_file) #Need to include user id filter also to fetch rule id
	#filename = "AP&ISA_202002Feb_Maximo_Resoln_wos_BI_20200310.xlsx"
	filename = str(csv_file)
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	FILES_FOLDER = os.path.join(BASE_DIR,'media\\files')
	filepath = os.path.join(FILES_FOLDER,filename)
	#filepath = "C:\\Users\\salman\\Desktop\\DjangoLearning\\projects\\DataIngestion\\filemanagement\\fileingest\\media\\files\\APISA_202002Feb_Maximo_Resoln_wos_BI_20200310.xlsx"
		
	rule = Rules.objects.get(ruleid=filedata.ruleid)
	rule = json.loads(rule.rule)
	
	#1st check if the file name is correct with pattern name and patter period matching strings
	if re.search(rule["pattern_period"],filename,re.IGNORECASE) and re.search(rule["pattern_name"],filename,re.IGNORECASE):
		pattern_period = (re.search(rule["pattern_period"],filename,re.IGNORECASE)).group(0) #extract the period 
		book = openpyxl.load_workbook(filepath) # if yes, open the workbook 
		
		entry = FileLogs(uploadid=Files.objects.get(uploadid=uploadid), files=csv_file, logs='File Name Validation : Successful')
		entry.save()
		sheet_found = 0
		for sheetname in book.sheetnames:
			if re.search(rule["sheetName"],sheetname,re.IGNORECASE): # check if we have the required sheet. 
				entry = FileLogs(uploadid=Files.objects.get(uploadid=uploadid), files=csv_file, logs=('Sheet Name "' + sheetname+ '" Validation : Successful'))
				entry.save()
				sheet_found = 1  

				xl_sheet = book[sheetname]
				if xl_sheet.max_column == 0:
					entry = FileLogs(uploadid=Files.objects.get(uploadid=uploadid), files=csv_file, logs=('No data present in SheetName: ' + sheetname))
					entry.save()
				else:
					columns=[]
					if rule["header"]:
						header = rule["header"]				
						for cell in xl_sheet[header]: 
							columns.append(cell.value)
						#now check for missing columns 						
						missing_columns =  [item for item in rule["columns"] if item not in columns]

						if missing_columns:
							entry = FileLogs(uploadid=Files.objects.get(uploadid=uploadid), files=csv_file, logs=('All expected Columns not present in the Sheet: ' + sheetname))
							entry.save()
						else:
							entry = FileLogs(uploadid=Files.objects.get(uploadid=uploadid), files=csv_file, logs='All validations Successful. Ready to process.')
							entry.save()
						
					else:
						no_of_rows = xl_sheet.max_row
						#searching top 50 rows for headers
						counter = 1
						while counter < no_of_rows:
							for cell in xl_sheet[counter]: 
								columns.append(cell.value)
							if [item for item in rule["columns"] if item not in columns]:
								counter = counter + 1
								if counter > 50:
									break
								continue
							else:
								entry = FileLogs(uploadid=Files.objects.get(uploadid=uploadid), files=csv_file, logs=('Header found at row number: '+ str(counter)))
								entry.save()
								entry = FileLogs(uploadid=Files.objects.get(uploadid=uploadid), files=csv_file, logs='All validations Successful. Ready to process.')
								entry.save() 
								break
						if counter > 50:
							entry = FileLogs(uploadid=Files.objects.get(uploadid=uploadid), files=csv_file, logs=('Header not found in top 50 rows'))
							entry.save()
		if sheet_found == 0:
			entry = FileLogs(uploadid=Files.objects.get(uploadid=uploadid), files=csv_file, logs=('Sheet Name "' + sheetname+ '" Validation : Failed. Expected Sheet Not Found.'))
			entry.save()
	else:
		entry = FileLogs(uploadid=Files.objects.get(uploadid=uploadid), files=csv_file, logs='File Name Validation : Failed')
		entry.save()

   
def register(request):

	if request.method == 'POST':
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		confirmpassword = request.POST['confirmpassword']
		
		if username=='':
			messages.info(request, 'Please provide Username')
			return redirect('register')
		elif password=='':
			messages.info(request, 'Please provide password')
			return redirect('register')
		elif password==confirmpassword:
			if User.objects.filter(username=username).exists():
				messages.info(request, 'Username Taken')
				return redirect('register')
			elif User.objects.filter(email=email).exists():
				messages.info(request, 'Email Taken')
				return redirect('register')
			else:
				user = User.objects.create_user(username=username, password=password, email=email, first_name=firstname, last_name=lastname)
				user.save();
				messages.info(request, 'User Created')
				return redirect('upload')
		else:
			messages.info(request, 'Password Not Matching')
			return redirect('register')
		return redirect('/')
	else:
		return render(request, 'register.html')