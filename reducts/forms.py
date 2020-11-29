from django import forms

class DatasetForm(forms.Form):
    csv_string = forms.CharField(widget=forms.Textarea, label="Данные в формате CSV:")
    c_attributes = forms.CharField(label="Индексы условных атрибутов через запятую:")
    d_attributes = forms.CharField(label="Индексы целевых атрибутов через запятую:")