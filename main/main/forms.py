from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()
    res = (0, 0)