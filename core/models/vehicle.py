from django.db import models
from .equipment import Equipment
    

class Vehicle(models.Model):

    def get_photo_path(instance, filename):
        return f'vehicles/{instance.vin}/{filename}'

    FUEL_CHOICES = [
        ('Электрический', 'Электрический'),
        ('Бензиновый', 'Бензиновый'),
        ('Дизельный', 'Дизельный'),
        ('Гибридный', 'Гибридный'),
    ]

    CATEGORY_CHOICES = [
        ('M', 'Категория M'),
        ('M1', 'Категория M1'),
        ('M2', 'Категория M2'),
        ('M3', 'Категория M3'),
        ('N', 'Категория N'),
        ('N1', 'Категория N1'),
        ('N2', 'Категория N2'),
        ('N3', 'Категория N3'),
        ('O', 'Категория O'),
        ('O1', 'Категория O1'),
        ('O2', 'Категория O2'),
        ('O3', 'Категория O3'),
        ('O4', 'Категория O4'),
        ('L', 'Категория L'),
        ('L1e', 'Категория L1e'),
        ('L2e', 'Категория L2e'),
        ('L3e', 'Категория L3e'),
        ('L4e', 'Категория L4e'),
        ('L5e', 'Категория L5e'),
        ('L6e', 'Категория L6e'),
        ('L7e', 'Категория L7e'),
        ('T', 'Категория T'),
        ('T1', 'Категория T1'),
        ('T2', 'Категория T2'),
        ('S', 'Категория S'),
        ('G', 'Категория G'),
        ('A', 'Категория A'),
        ('B', 'Категория B'),
        ('C', 'Категория C'),
        ('D', 'Категория D'),
        ('BE', 'Категория BE'),
        ('CE', 'Категория CE'),
        ('DE', 'Категория DE'),
    ]

    # Данные заказчика
    customer_info = models.CharField("Заказчик (контактные данные для ЮЛ, ФИО для ФЛ)", max_length=255, blank=True, null=True)
    legal_address = models.TextField("Юридический адрес заказчика", blank=True, null=True)
    actual_address = models.TextField("Фактический адрес заказчика", blank=True, null=True)
    
    receive_date = models.DateField("Дата получения объекта", blank=True, null=True)
    customer_infos = models.TextField("Заказчиком предоставлены сведения", blank=True, null=True)
    
    # Основные характеристики ТС
    brand = models.CharField("Марка ТС", max_length=100, blank=True, null=True)
    commercial_name = models.CharField("Коммерческое наименование", max_length=255, blank=True, null=True)
    vehicle_type = models.CharField("Тип", max_length=100, blank=True, null=True)
    chassis = models.CharField("Шасси", max_length=100, blank=True, null=True)
    vin = models.CharField("VIN", max_length=17, blank=True, null=True)
    manufacture_date = models.CharField("Месяц (при наличии) и год выпуска", max_length=100, blank=True, null=True)
    category = models.CharField("Категория ТС", max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    mileage = models.IntegerField("Пробег", blank=True, null=True)
    fuel_type = models.CharField("Тип топлива", max_length=20, choices=FUEL_CHOICES, blank=True, null=True)
    
    # Данные производителя
    manufacturer_name = models.CharField("Наименование изготовителя", max_length=255, blank=True, null=True)
    manufacturer_legal_address = models.TextField("Юридический адрес изготовителя", blank=True, null=True)
    manufacturer_actual_address = models.TextField("Фактический адрес изготовителя", blank=True, null=True)
    
    # Данные испытаний
    test_address = models.TextField("Адрес проведения испытаний", blank=True, null=True)
    test_date = models.DateField("Дата проведения испытаний", blank=True, null=True)
    temperature = models.TextField("Температура воздуха", blank=True, null=True)
    humidity = models.TextField("Относительная влажность", blank=True, null=True)
    pressure = models.TextField("Атмосферное давление", blank=True, null=True)
    additional_info = models.TextField("Иная информация, если требуется для объективности проведения испытаний (фон шумовых помех, комплектность ТС и т.п.)", blank=True, null=True)
    additional_info_two = models.TextField("Дополнительные сведения", blank=True, null=True)

    equipment = models.ManyToManyField(
        Equipment,
        verbose_name="Оборудование",
        blank=True,
        related_name='vehicles'
    )
 

class VehiclePhoto(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, 
        on_delete=models.CASCADE,
        related_name='vehicle_photos'  # Изменили related_name
    )
    image = models.ImageField(
        upload_to='vehicles/%Y/%m/%d/',
        verbose_name="Фотография"
    )
    description = models.CharField(
        "Описание", 
        max_length=200, 
        blank=True
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

class VehicleProtocol(models.Model):
    PROTOCOL_TYPES = [
        ('1', 'Протокол измерений'),
        ('2', 'Протокол испытаний')
    ]
    
    vehicle = models.ForeignKey(
        Vehicle, 
        on_delete=models.CASCADE,
        related_name='protocols'
    )
    protocol_type = models.CharField(
        "Тип протокола",
        max_length=1,
        choices=PROTOCOL_TYPES
    )
    docx_file = models.FileField(
        upload_to='protocols/docx/%Y/%m/%d/',
        null=True,
        blank=True
    )
    pdf_file = models.FileField(
        upload_to='protocols/pdf/%Y/%m/%d/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['vehicle', 'protocol_type']
