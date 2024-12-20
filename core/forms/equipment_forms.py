from django import forms
from core.models.equipment import Equipment

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'
        widgets = {
            'equipment_type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'tip': forms.TextInput(attrs={'class': 'form-control'}),
            'zav_nomer': forms.TextInput(attrs={'class': 'form-control'}),
            'inv_nomer': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'reg_nomer': forms.TextInput(attrs={'class': 'form-control'}),
            'kol_vo': forms.NumberInput(attrs={'class': 'form-control'}),
            'klass_toch': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'predel': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'period_poverk': forms.TextInput(attrs={'class': 'form-control'}),
            'category_si': forms.TextInput(attrs={'class': 'form-control'}),
            'organ_poverk': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'data_poverk': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'srok_poverk': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'other': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Определяем поля для левой и правой колонки
        self.left_fields = [
            'equipment_type',
            'name',
            'tip',
            'zav_nomer',
            'inv_nomer',
            'reg_nomer',
            'kol_vo',
        ]
        
        self.right_fields = [
            'klass_toch',
            'predel',
            'period_poverk',
            'category_si',
            'organ_poverk',
            'data_poverk',
            'srok_poverk',
            'other',
        ]