from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.files.storage import FileSystemStorage

from .forms import FileForm
from .models import Files

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
	if request.method == 'POST':
		form = FileForm(request.POST, request.FILES)
		if form.is_valid():
			fs = form.save(commit=False)
			fs.user = request.user
			fs.save()
			return render(request, 'upload.html', { 'form' : form, 'filelist' : filelist })
	else:
		form = FileForm()
	return render(request, 'upload.html', { 'form' : form, 'filelist' : filelist })
	
#def upload(request):
#	if request.method == 'POST':
#		uploaded_file = request.FILES['document']
#		fs = FileSystemStorage()
#		fs.save(uploaded_file.name, uploaded_file)
#	return render(request,'upload.html')
	
#def file_list(request):
#	filelist = Files.objects.all()
#	return render(request, 'file_list.html', {'filelist' : filelist})
	
#def file_upload(request):
#	if request.method == 'POST':
#		form = FileForm(request.POST, request.FILES)
#		if form.is_valid():
#			form.save()
#			return redirect('file_list')
#		else:
#			form = FileForm()
#	return render(request, 'file_upload.html', { 'form' : form })