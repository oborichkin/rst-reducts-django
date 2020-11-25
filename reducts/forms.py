from django import forms

class DatasetForm(forms.Form):
    csv_string = forms.CharField(widget=forms.Textarea)
    c_attributes = forms.CharField()
    d_attributes = forms.CharField()