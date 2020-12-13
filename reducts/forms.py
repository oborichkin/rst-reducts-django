from django import forms

class DatasetForm(forms.Form):
    csv_string = forms.CharField(widget=forms.Textarea, label="Данные в формате CSV:")
    c_attributes = forms.CharField(label="Индексы условных атрибутов через запятую:")
    d_attributes = forms.CharField(label="Индексы целевых атрибутов через запятую:")


class DefineSystemForm(forms.Form):
    csv_train = forms.CharField(widget=forms.Textarea, label="Входные данные в формате CSV (имя класса - последний столбец):")
    csv_test = forms.CharField(widget=forms.Textarea, label="Тестовые элементы в формате CSV")