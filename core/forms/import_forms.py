from django import forms

class CSVImportForm(forms.Form):
    csv_file = forms.FileField(
        label='Выберите CSV файл',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'})
    )