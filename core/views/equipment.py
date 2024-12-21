from django.shortcuts import get_object_or_404, redirect, render
from django.db import models  # Добавляем этот импорт
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from core.models.equipment import Equipment
from core.forms.equipment_forms import EquipmentForm
from django.contrib import messages
from django.urls import reverse
from datetime import datetime
import csv
import io
from django.http import HttpResponse
from core.forms.import_forms import CSVImportForm

# Базовые миксины для оборудования
class BaseEquipmentMixin:
    template_name_suffix = None
    equipment_type_name = None
    equipment_type_name_accusative = None
    url_prefix = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'equipment_type_name': self.equipment_type_name,
            'equipment_type_name_accusative': self.equipment_type_name_accusative,
            'create_url': f'{self.url_prefix}-create',
            'update_url': f'{self.url_prefix}-update',
            'delete_url': f'{self.url_prefix}-delete',
            'cancel_url': reverse_lazy(f'{self.url_prefix}-list'),
        })
        return context

class BaseEquipmentListView(LoginRequiredMixin, BaseEquipmentMixin, ListView):
    template_name = 'equipment/equipment_list.html'
    context_object_name = 'equipment_list'
    paginate_by = 30
    ordering = ['-id']

    def get_queryset(self):
        # Получаем базовый queryset
        queryset = super().get_queryset()
        
        # Фильтруем по типу оборудования, если он определен
        if hasattr(self, 'equipment_type_filter'):
            queryset = queryset.filter(equipment_type=self.equipment_type_filter)
        
        # Применяем поиск, если есть
        search_query = self.request.GET.get('search')
        if search_query:
            search_fields = [field.name for field in self.model._meta.fields 
                           if isinstance(field, (models.CharField, models.TextField))]
            
            q_objects = Q()
            for field in search_fields:
                q_objects |= Q(**{f"{field}__icontains": search_query})
            
            queryset = queryset.filter(q_objects)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_query': self.request.GET.get('search', ''),
        })
        return context

class BaseEquipmentCreateView(LoginRequiredMixin, SuccessMessageMixin, BaseEquipmentMixin, CreateView):
    template_name = 'equipment/equipment_form.html'
    
    def get_success_url(self):
        return reverse_lazy(f'{self.url_prefix}-list')

class BaseEquipmentUpdateView(LoginRequiredMixin, SuccessMessageMixin, BaseEquipmentMixin, UpdateView):
    template_name = 'equipment/equipment_form.html'
    
    def get_success_url(self):
        return reverse_lazy(f'{self.url_prefix}-list')

class BaseEquipmentDeleteView(LoginRequiredMixin, SuccessMessageMixin, BaseEquipmentMixin, DeleteView):
    template_name = 'equipment/equipment_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy(f'{self.url_prefix}-list')

# Представления для оборудования с фильтрацией по типу
class MeasurementToolListView(BaseEquipmentListView):
    model = Equipment
    equipment_type_name = 'Средство измерения'
    equipment_type_name_accusative = 'средство измерения'
    equipment_type_filter = 'measurement_tool'
    url_prefix = 'measurement-tool'


class MeasurementToolCreateView(BaseEquipmentCreateView):
    model = Equipment
    form_class = EquipmentForm
    equipment_type_name = 'Средство измерения'
    equipment_type_name_accusative = 'средство измерения'
    equipment_type_filter = 'measurement_tool'
    url_prefix = 'measurement-tool'
    success_message = "Элемент успешно создан"


class MeasurementToolUpdateView(BaseEquipmentUpdateView):
    model = Equipment
    form_class = EquipmentForm
    equipment_type_name = 'Средство измерения'
    equipment_type_name_accusative = 'средство измерения'
    equipment_type_filter = 'measurement_tool'
    url_prefix = 'measurement-tool'
    success_message = "Элемент успешно обновлен"


class MeasurementToolDeleteView(BaseEquipmentDeleteView):
    model = Equipment
    equipment_type_name = 'Средство измерения'
    equipment_type_name_accusative = 'средство измерения'
    equipment_type_filter = 'measurement_tool'
    url_prefix = 'measurement-tool'
    success_message = "Элемент успешно удален"


# Представления для испытательного оборудования
class TestingEquipmentListView(BaseEquipmentListView):
    model = Equipment
    equipment_type_name = 'Испытательное оборудование'
    equipment_type_name_accusative = 'испытательное оборудование'
    equipment_type_filter = 'testing_equipment'
    url_prefix = 'testing-equipment'


class TestingEquipmentCreateView(BaseEquipmentCreateView):
    model = Equipment
    form_class = EquipmentForm
    equipment_type_name = 'Испытательное оборудование'
    equipment_type_name_accusative = 'испытательное оборудование'
    equipment_type_filter = 'testing_equipment'
    url_prefix = 'testing-equipment'
    success_message = "Элемент успешно создан"


class TestingEquipmentUpdateView(BaseEquipmentUpdateView):
    model = Equipment
    form_class = EquipmentForm
    equipment_type_name = 'Испытательное оборудование'
    equipment_type_name_accusative = 'испытательное оборудование'
    equipment_type_filter = 'testing_equipment'
    url_prefix = 'testing-equipment'
    success_message = "Элемент успешно обновлен"


class TestingEquipmentDeleteView(BaseEquipmentDeleteView):
    model = Equipment
    equipment_type_name = 'Испытательное оборудование'
    equipment_type_name_accusative = 'испытательное оборудование'
    equipment_type_filter = 'testing_equipment'
    url_prefix = 'testing-equipment'
    success_message = "Элемент успешно удален"


# Представления для вспомогательного оборудования
class AuxiliaryEquipmentListView(BaseEquipmentListView):
    model = Equipment
    equipment_type_name = 'Вспомогательное оборудование'
    equipment_type_name_accusative = 'вспомогательное оборудование'
    equipment_type_filter = 'auxiliary_equipment'
    url_prefix = 'auxiliary-equipment'


class AuxiliaryEquipmentCreateView(BaseEquipmentCreateView):
    model = Equipment
    form_class = EquipmentForm
    equipment_type_name = 'Вспомогательное оборудование'
    equipment_type_name_accusative = 'вспомогательное оборудование'
    equipment_type_filter = 'auxiliary_equipment'
    url_prefix = 'auxiliary-equipment'
    success_message = "Элемент успешно создан"


class AuxiliaryEquipmentUpdateView(BaseEquipmentUpdateView):
    model = Equipment
    form_class = EquipmentForm
    equipment_type_name = 'Вспомогательное оборудование'
    equipment_type_name_accusative = 'вспомогательное оборудование'
    equipment_type_filter = 'auxiliary_equipment'
    url_prefix = 'auxiliary-equipment'
    success_message = "Элемент успешно обновлен"


class AuxiliaryEquipmentDeleteView(BaseEquipmentDeleteView):
    model = Equipment
    equipment_type_name = 'Вспомогательное оборудование'
    equipment_type_name_accusative = 'вспомогательное оборудование'
    equipment_type_filter = 'auxiliary_equipment'
    url_prefix = 'auxiliary-equipment'
    success_message = "Элемент успешно удален"

@login_required
def duplicate_equipment(request, pk, equipment_type):
    """Дублирование записи оборудования с учётом типа"""
    source_equipment = get_object_or_404(Equipment, pk=pk)
    source_equipment.pk = None  # Обнуляем первичный ключ для создания нового объекта
    source_equipment.name = f"{source_equipment.name} (копия)"  # Добавляем пометку
    source_equipment.save()
    
    messages.success(request, f"Элемент успешно скопирован")
    return redirect(f'{equipment_type}-list')

@login_required
def delete_all_equipment(request, equipment_type):
    equipment_type_mapping = {
        'measurement': ('measurement_tool', 'средств измерений', 'measurement-tool-list'),
        'testing': ('testing_equipment', 'испытательного оборудования', 'testing-equipment-list'),
        'auxiliary': ('auxiliary_equipment', 'вспомогательного оборудования', 'auxiliary-equipment-list'),
    }

    if equipment_type not in equipment_type_mapping:
        messages.error(request, 'Неверный тип оборудования')
        return redirect('equipment-list')

    equipment_type_value, equipment_type_name, redirect_url_name = equipment_type_mapping[equipment_type]

    if request.method == 'POST':
        # Удаляем все записи данного типа
        deleted_count = Equipment.objects.filter(equipment_type=equipment_type_value).delete()[0]
        messages.success(request, f'Удалено записей: {deleted_count}')
        return redirect(redirect_url_name)

    # Получаем количество записей для отображения
    items_count = Equipment.objects.filter(equipment_type=equipment_type_value).count()

    return render(request, 'equipment/delete_all_confirm.html', {
        'equipment_type_name': equipment_type_name,
        'items_count': items_count,
        'cancel_url': redirect_url_name
    })


@login_required
def import_equipment(request, equipment_type):
    # Маппинг типов оборудования и URL для редиректа
    equipment_type_mapping = {
        'measurement': ('measurement_tool', 'средств измерений', 'measurement-tool-list'),
        'testing': ('testing_equipment', 'испытательного оборудования', 'testing-equipment-list'),
        'auxiliary': ('auxiliary_equipment', 'вспомогательного оборудования', 'auxiliary-equipment-list'),
    }

    if equipment_type not in equipment_type_mapping:
        messages.error(request, 'Неверный тип оборудования')
        return redirect('equipment-list')

    equipment_type_value, equipment_type_name, redirect_url_name = equipment_type_mapping[equipment_type]

    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            # Получаем все поля модели
            fields = [field.name for field in Equipment._meta.fields if field.name not in ['id', 'equipment_type']]
            
            # Отладочная информация
            print(f"Поля модели: {fields}")
            print(f"Колонки CSV: {reader.fieldnames}")
            
            updated_count = 0
            created_count = 0
            skipped_count = 0
            
            try:
                for row in reader:
                    try:
                        # Получаем ID из строки
                        item_id = row.get('№') or row.get('id')
                        
                        # Очищаем и подготавливаем данные
                        cleaned_data = {'equipment_type': equipment_type_value}
                        for field in fields:
                            if field in row:
                                value = row[field].strip() if row[field] else None
                                # Особая обработка для дат
                                if field in ['data_poverk', 'srok_poverk']:
                                    if not value or value == '':
                                        value = None
                                    else:
                                        try:
                                            value = datetime.strptime(value, '%Y-%m-%d').date()
                                        except ValueError:
                                            print(f"Ошибка преобразования даты для поля {field}")
                                            value = None
                                cleaned_data[field] = value
                        
                        if item_id:
                            # Пытаемся найти существующую запись
                            try:
                                existing_record = Equipment.objects.get(id=item_id)
                                # Обновляем существующую запись
                                for field, value in cleaned_data.items():
                                    setattr(existing_record, field, value)
                                existing_record.save()
                                updated_count += 1
                                print(f"Обновлена запись: {existing_record}")
                            except Equipment.DoesNotExist:
                                # ID не найден в БД
                                skipped_count += 1
                                print(f"Запись с ID {item_id} не найдена в БД")
                                continue
                        else:
                            # Создаем новую запись
                            new_record = Equipment.objects.create(**cleaned_data)
                            created_count += 1
                            print(f"Создана новая запись: {new_record}")
                        
                    except Exception as e:
                        print(f"Ошибка при обработке строки: {str(e)}")
                        skipped_count += 1
                        continue
                
                messages.success(
                    request, 
                    f'Импорт завершен: обновлено {updated_count}, '
                    f'создано {created_count}, пропущено {skipped_count} записей'
                )
                
                return redirect(redirect_url_name)
                
            except Exception as e:
                messages.error(request, f'Ошибка при импорте: {str(e)}')
                print(f"Общая ошибка импорта: {str(e)}")
                return redirect(redirect_url_name)
    else:
        form = CSVImportForm()

    # Получаем заголовки полей для примера
    fields = ['id'] + [field.name for field in Equipment._meta.fields if field.name != 'equipment_type']
    example_header = ','.join(fields)

    return render(request, 'equipment/import_csv.html', {
        'form': form,
        'example_header': example_header,
        'equipment_type_name': equipment_type_name
    })


@login_required
def export_equipment(request, equipment_type):
    # Сопоставление типа оборудования с его значением и названием файла
    equipment_type_mapping = {
        'measurement': ('measurement_tool', 'measurement_tools'),
        'testing': ('testing_equipment', 'testing_equipment'),
        'auxiliary': ('auxiliary_equipment', 'auxiliary_equipment'),
    }
    # Проверка корректности типа оборудования
    if equipment_type not in equipment_type_mapping:
        messages.error(request, 'Неверный тип оборудования')
        return redirect('equipment-list')

    equipment_type_value, file_name = equipment_type_mapping[equipment_type]

    # Получаем поля для экспорта, исключая только equipment_type
    fields = ['id'] + [field.name for field in Equipment._meta.fields if field.name != 'equipment_type']

    # Подготовка HTTP-ответа с CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{file_name}.csv"'
    response.write(u'\ufeff'.encode('utf8'))  # Для корректного отображения кириллицы

    # Запись заголовков в CSV
    writer = csv.writer(response)
    writer.writerow(['№'] + fields[1:])  # Меняем 'id' на '№' в заголовке

    # Получаем записи соответствующего типа оборудования
    items = Equipment.objects.filter(equipment_type=equipment_type_value).values_list(*fields)

    # Записываем строки в CSV
    for item in items:
        row = ['' if value is None else value for value in item]
        writer.writerow(row)

    return response
