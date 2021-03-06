from django import forms
from .models import Files

class FileForm(forms.ModelForm):
	class Meta:
		model = Files
		fields = {files}
		
		def form_valid(self, form):
			form.instance.created_by = self.request.user
			return super().form_valid(form)