from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib import messages
from core.models.vehicle import Vehicle, VehiclePhoto
from core.forms.vehicle_forms import VehicleForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from core.utils.document_generators import generate_protocols
from django.db.models import Q
from core.models.equipment import Equipment

class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = 'vehicle/vehicle_list.html'
    context_object_name = 'vehicles'
    paginate_by = 30
    ordering = ['-id']

    # Определим доступные столбцы
    AVAILABLE_COLUMNS = {
        # Данные заказчика
        'customer_info': 'Заказчик',
        'legal_address': 'Юридический адрес заказчика',
        'actual_address': 'Фактический адрес заказчика',
        'receive_date': 'Дата получения объекта',
        'customer_infos': 'Заказчиком предоставлены сведения',
        
        # Основные характеристики ТС
        'brand': 'Марка ТС',
        'commercial_name': 'Коммерческое наименование',
        'vehicle_type': 'Тип',
        'chassis': 'Шасси',
        'vin': 'VIN',
        'manufacture_date': 'Месяц и год выпуска',
        'category': 'Категория ТС',
        'mileage': 'Пробег',
        'fuel_type': 'Тип топлива',
        
        # Данные производителя
        'manufacturer_name': 'Производитель',
        'manufacturer_legal_address': 'Юридический адрес производителя',
        'manufacturer_actual_address': 'Фактический адрес производителя',
        
        # Данные испытаний
        'test_address': 'Адрес проведения испытаний',
        'test_date': 'Дата проведения испытаний',
        'temperature': 'Температура воздуха',
        'humidity': 'Относительная влажность',
        'pressure': 'Атмосферное давление',
        'additional_info': 'Дополнительная информация',
        'additional_info_two': 'Дополнительные сведения'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        
        if search_query:
            queryset = queryset.filter(
                Q(brand__icontains=search_query) |
                Q(vin__icontains=search_query) |
                Q(customer_info__icontains=search_query) |
                Q(commercial_name__icontains=search_query) |
                Q(manufacturer_name__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        
        # Получаем выбранные столбцы из session или используем значения по умолчанию
        default_columns = ['brand', 'vin', 'customer_info', 'test_date']
        selected_columns = self.request.session.get('vehicle_columns', default_columns)
        
        # Добавляем информацию о столбцах в контекст
        context['available_columns'] = self.AVAILABLE_COLUMNS
        context['selected_columns'] = selected_columns
        
        return context
    
@login_required
def save_column_preferences(request):
    if request.method == 'POST':
        selected_columns = request.POST.getlist('columns')
        request.session['vehicle_columns'] = selected_columns
        messages.success(request, 'Настройки отображения сохранены')
    return redirect('vehicle-list')

class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'vehicle/vehicle_detail.html'
    context_object_name = 'vehicle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = [field for field in Vehicle._meta.fields if field.name != 'id']
        
        # Добавляем отфильтрованное оборудование в контекст
        vehicle = self.get_object()
        context['measurement_tools'] = vehicle.equipment.filter(equipment_type='measurement_tool')
        context['testing_equipment'] = vehicle.equipment.filter(equipment_type='testing_equipment')
        context['auxiliary_equipment'] = vehicle.equipment.filter(equipment_type='auxiliary_equipment')
        
        return context

@login_required
def vehicle_create(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save()
            
            # Получаем список индексов удаленных файлов
            removed_indexes = request.POST.get('removed_files_indexes', '')
            removed_indexes = [int(i) for i in removed_indexes.split(',') if i]
            
            # Обработка фотографий
            photos = request.FILES.getlist('photos')
            for i, photo in enumerate(photos):
                # Сохраняем только те фото, которые не были удалены
                if i not in removed_indexes:
                    VehiclePhoto.objects.create(
                        vehicle=vehicle,
                        image=photo
                    )
            
            messages.success(request, 'Карточка автомобиля успешно создана')
            return redirect('vehicle-detail', pk=vehicle.pk)
    else:
        form = VehicleForm()
    
    return render(request, 'vehicle/vehicle_form.html', {
        'vehicle_form': form
    })

@login_required
def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            vehicle = form.save()
            
            # Получаем список индексов удаленных файлов
            removed_indexes = request.POST.get('removed_files_indexes', '')
            removed_indexes = [int(i) for i in removed_indexes.split(',') if i]
            
            # Обработка фотографий
            photos = request.FILES.getlist('photos')
            for i, photo in enumerate(photos):
                # Сохраняем только те фото, которые не были удалены
                if i not in removed_indexes:
                    VehiclePhoto.objects.create(
                        vehicle=vehicle,
                        image=photo
                    )
            
            # Удаление выбранных существующих фотографий
            if 'delete_photos' in request.POST:
                delete_photos = request.POST.getlist('delete_photos')
                vehicle.vehicle_photos.filter(id__in=delete_photos).delete()
            
            messages.success(request, 'Карточка автомобиля успешно обновлена')
            return redirect('vehicle-detail', pk=vehicle.pk)
    else:
        form = VehicleForm(instance=vehicle)
    
    return render(request, 'vehicle/vehicle_form.html', {
        'vehicle_form': form,
        'vehicle': vehicle
    })

@login_required
def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Карточка автомобиля успешно удалена')
        return redirect('vehicle-list')
    return render(request, 'vehicle/vehicle_confirm_delete.html', {'vehicle': vehicle})

@login_required
def generate_vehicle_protocols(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    print(f"Количество фотографий у автомобиля: {vehicle.vehicle_photos.count()}")
    try:
        protocols = generate_protocols(vehicle)
        if protocols:
            messages.success(request, 'Протоколы успешно сгенерированы')
        else:
            messages.warning(request, 'Не удалось сгенерировать все протоколы')
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        messages.error(request, f'Ошибка при генерации протоколов: {str(e)}\n{error_details}')
    
    return redirect('vehicle-detail', pk=vehicle.pk)

@login_required
def duplicate_vehicle(request, pk):
    # Получаем исходный объект
    source_vehicle = get_object_or_404(Vehicle, pk=pk)
    
    # Создаем копию, исключая pk
    source_vehicle.pk = None
    source_vehicle.brand = f"{source_vehicle.brand} (копия)"  # Добавляем пометку что это копия
    source_vehicle.save()
    
    # Копируем ManyToMany связи для Equipment
    for equipment_item in source_vehicle.equipment.all():
        source_vehicle.equipment.add(equipment_item)

    
    # Копируем фотографии
    for photo in source_vehicle.vehicle_photos.all():
        VehiclePhoto.objects.create(
            vehicle=source_vehicle,
            image=photo.image,
            description=photo.description
        )
    
    messages.success(request, 'Карточка автомобиля успешно скопирована')
    return redirect('vehicle-detail', pk=source_vehicle.pk)