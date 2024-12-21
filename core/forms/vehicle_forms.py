from django import forms
from core.models.vehicle import Vehicle, VehiclePhoto
from core.models.equipment import Equipment


class VehicleForm(forms.ModelForm):
   # Поля для разных типов оборудования
    measurement_tools = forms.ModelMultipleChoiceField(
        queryset=Equipment.objects.filter(equipment_type='measurement_tool'),
        label="Средства измерения",
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    testing_equipment = forms.ModelMultipleChoiceField(
        queryset=Equipment.objects.filter(equipment_type='testing_equipment'),
        label="Испытательное оборудование",
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    auxiliary_equipment = forms.ModelMultipleChoiceField(
        queryset=Equipment.objects.filter(equipment_type='auxiliary_equipment'),
        label="Вспомогательное оборудование",
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
   
    class Meta:
        model = Vehicle
        fields = [
            # Данные заказчика
            'customer_info', 'legal_address', 'actual_address', 
            'receive_date', 'customer_infos',
            # Основные характеристики
            'brand', 'commercial_name', 'vehicle_type', 'chassis',
            'vin', 'manufacture_date', 'category', 'mileage', 'fuel_type',
            # Данные производителя
            'manufacturer_name', 'manufacturer_legal_address', 
            'manufacturer_actual_address',
            # Данные испытаний
            'test_address', 'test_date', 'temperature', 'humidity',
            'pressure', 'additional_info', 'additional_info_two',
        ]
        widgets = {
            # Данные заказчика
            'customer_info': forms.TextInput(attrs={'class': 'form-control'}),
            'legal_address': forms.TextInput(attrs={'class': 'form-control'}),
            'actual_address': forms.TextInput(attrs={'class': 'form-control'}),
            'receive_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'customer_infos': forms.TextInput(attrs={'class': 'form-control'}),
            
            # Основные характеристики
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'commercial_name': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_type': forms.TextInput(attrs={'class': 'form-control'}),
            'chassis': forms.TextInput(attrs={'class': 'form-control'}),
            'vin': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacture_date': forms.TextInput(attrs={'class': 'form-control'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control'}),
            'fuel_type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            
            # Данные производителя
            'manufacturer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer_legal_address': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer_actual_address': forms.TextInput(attrs={'class': 'form-control'}),
            
            # Данные испытаний
            'test_address': forms.TextInput(attrs={'class': 'form-control'}),
            'test_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'temperature': forms.TextInput(attrs={'class': 'form-control'}),
            'humidity': forms.TextInput(attrs={'class': 'form-control'}),
            'pressure': forms.TextInput(attrs={'class': 'form-control'}), 
            'additional_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'additional_info_two': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            # Предзаполняем поля существующими значениями
            self.initial['measurement_tools'] = instance.equipment.filter(equipment_type='measurement_tool')
            self.initial['testing_equipment'] = instance.equipment.filter(equipment_type='testing_equipment')
            self.initial['auxiliary_equipment'] = instance.equipment.filter(equipment_type='auxiliary_equipment')

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # Очищаем существующие связи
            instance.equipment.clear()
            # Добавляем новые связи для каждого типа оборудования
            if self.cleaned_data.get('measurement_tools'):
                instance.equipment.add(*self.cleaned_data['measurement_tools'])
            if self.cleaned_data.get('testing_equipment'):
                instance.equipment.add(*self.cleaned_data['testing_equipment'])
            if self.cleaned_data.get('auxiliary_equipment'):
                instance.equipment.add(*self.cleaned_data['auxiliary_equipment'])
        return instance