from django import forms
from models import UploadedVideo

class UploadVideoForm(forms.ModelForm):

	class Meta:
		model = UploadedVideo
		fields = ('UploaderName', 'Video')