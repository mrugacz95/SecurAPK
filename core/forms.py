from django import forms

from core.models import App

class UploadFileForm(forms.ModelForm):
    class Meta(object):
        model = App
        fields = ['file']
