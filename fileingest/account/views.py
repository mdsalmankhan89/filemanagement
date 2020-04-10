from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.files.storage import FileSystemStorage

from .forms import FileForm
from .models import Files, FileLogs

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
	filelist = Files.objects.all()
	fileloglist = FileLogs.objects.all()
	if request.method == 'POST':
		form = FileForm(request.POST, request.FILES)
		if form.is_valid():
#			fs = form.save(commit=False)
#			fs.user = request.user
#			fs.save()
			handle_files(request.FILES['files'],request.user)
			return render(request, 'upload.html', { 'form' : form, 'filelist' : filelist, 'fileloglist' : fileloglist })
	else:
		form = FileForm()
	return render(request, 'upload.html', { 'form' : form, 'filelist' : filelist, 'fileloglist' : fileloglist })
	

def handle_files(csv_file, user):

   newfile = Files(files=csv_file,user=user)
   newfile.save()

   entry = FileLogs(uploadid=Files.objects.get(uploadid=newfile.uploadid), files=csv_file, logs='File Loaded new')
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