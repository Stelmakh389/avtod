# core/models/equipment.py
from django.db import models

class Equipment(models.Model):
    EQUIPMENT_TYPES = [
        ('measurement_tool', 'Средство измерения'),
        ('testing_equipment', 'Испытательное оборудование'),
        ('auxiliary_equipment', 'Вспомогательное оборудование'),
    ]
    
    
    equipment_type = models.TextField("Тип оборудования", choices=EQUIPMENT_TYPES)
    name = models.TextField("Наименование, модель", blank=True, null=True)
    tip = models.TextField("Тип", blank=True, null=True)
    zav_nomer = models.TextField("Заводской №", blank=True, null=True)
    inv_nomer = models.TextField("Инв. №, год ввода в эксплуатацию", blank=True, null=True)
    reg_nomer = models.TextField("Регистрационный номер СИ в Госреестре СИ", blank=True, null=True)
    kol_vo = models.PositiveIntegerField("Кол-во", blank=True, null=True)
    klass_toch = models.TextField("Класс точности, погрешность /ТТХ", blank=True, null=True)
    predel = models.TextField("Предел (диапазон измерений)", blank=True, null=True)
    period_poverk = models.TextField("Периодичность поверки", blank=True, null=True)
    category_si = models.TextField("Категория СИ", blank=True, null=True)
    organ_poverk = models.TextField("Орган, осуществляющий поверку / Иная инф.", blank=True, null=True)
    data_poverk = models.DateField("Дата последней поверки (месяц/год)", blank=True, null=True)
    srok_poverk = models.DateField("Сроки проведения поверки (месяц/год)", blank=True, null=True)
    other = models.TextField("Примечание", blank=True, null=True)

    def get_name(self):
        return self.name
    
    def __str__(self):
        return self.name or ''