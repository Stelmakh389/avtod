from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from core.models.organization import Organization
from django.conf import settings
import os
from core.models.equipment import Equipment
from docx2pdf import convert
import subprocess
from datetime import datetime
import copy
from core.models.vehicle import VehicleProtocol

def generate_protocols(vehicle):
    """Генерирует оба типа протоколов"""
    organization = Organization.objects.first()
    
    # Базовый контекст
    base_context = {
        'organization': {},
        'vehicle': {},
        'equipment': {
            'measurement_tools': [],
            'testing_equipment': [],
            'auxiliary_equipment': []
        }
    }
    
    # Добавляем данные организации
    for field in organization._meta.fields:
        if field.name != 'id':
            value = getattr(organization, field.name, '')
            # Проверка на дату
            if hasattr(value, 'strftime'):
                value = value.strftime('%d.%m.%Y')
            base_context['organization'][field.name] = value if value is not None else ''
    
    # Добавляем данные автомобиля
    for field in vehicle._meta.fields:
        if field.name != 'id':
            if field.name == 'fuel_type' and vehicle.fuel_type:
                value = vehicle.get_fuel_type_display()
            elif field.name == 'category' and vehicle.category:
                value = vehicle.get_category_display()
            else:
                value = getattr(vehicle, field.name, '')
            
            # Проверка на дату
            if hasattr(value, 'strftime'):
                value = value.strftime('%d.%m.%Y')
                
            base_context['vehicle'][field.name] = value if value is not None else ''
    
    # Добавляем оборудование по типам
    for equipment in vehicle.equipment.all():
        equip_data = {}
        for field in Equipment._meta.fields:
            if field.name != 'id':
                value = getattr(equipment, field.name, '')
                
                # Проверка на дату
                if hasattr(value, 'strftime'):
                    value = value.strftime('%d.%m.%Y')
                
                equip_data[field.name] = value if value is not None else ''
        
        # Распределяем по типам
        if equipment.equipment_type == 'measurement_tool':
            base_context['equipment']['measurement_tools'].append(equip_data)
        elif equipment.equipment_type == 'testing_equipment':
            base_context['equipment']['testing_equipment'].append(equip_data)
        elif equipment.equipment_type == 'auxiliary_equipment':
            base_context['equipment']['auxiliary_equipment'].append(equip_data)
    
    # Генерируем протоколы
    protocols = []
    for protocol_type in ['1', '2']:
        try:
            protocol = vehicle.protocols.get_or_create(protocol_type=protocol_type)[0]
            protocol_context = copy.deepcopy(base_context)
            
            protocol_context['protocol_type'] = dict(VehicleProtocol.PROTOCOL_TYPES)[protocol_type]
            protocol_context['protocol_date'] = datetime.now().strftime('%d.%m.%Y')
            
            docx_path = generate_docx(vehicle, protocol_type, protocol_context)
            pdf_path = generate_pdf(docx_path)
            
            protocol.docx_file.name = docx_path
            protocol.pdf_file.name = pdf_path
            protocol.save()
            
            protocols.append(protocol)
            
        except Exception as e:
            print(f"Ошибка при генерации протокола {protocol_type}: {str(e)}")
            raise
    
    return protocols

def generate_docx(vehicle, protocol_type, context):
    """Генерирует DOCX из шаблона"""
    from docxtpl import DocxTemplate, InlineImage  # Перенес импорты внутрь функции
    from docx.shared import Mm

    template_name = f'protocol{protocol_type}_template.docx'
    template_path = os.path.join(settings.BASE_DIR, 'core', 'templates', 'documents', template_name)
    
    # Проверяем существование шаблона
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Шаблон протокола не найден: {template_path}")
    
    doc = DocxTemplate(template_path)
    
    try:
        # Подготавливаем фотографии для документа
        context['photos'] = []  # Инициализируем список фото в контексте
        
        for photo in vehicle.vehicle_photos.all():
            if photo.image and os.path.isfile(photo.image.path):  # Исправленная проверка
                try:
                    image = InlineImage(
                        doc,
                        photo.image.path,
                        width=Mm(150)  # ширина 150мм
                    )
                    context['photos'].append({
                        'image': image,
                    })
                    print(f"Фото {photo.id} успешно добавлено")
                except Exception as e:
                    print(f"Ошибка при обработке фото {photo.id}: {str(e)}")
                    continue
            else:
                print(f"Фото {photo.id} не существует или путь неверен")
        
        # Рендерим документ
        doc.render(context)
        
        # Сохраняем результат
        output_path = f'protocols/docx/{vehicle.pk}/protocol_{protocol_type}.docx'
        full_path = os.path.join(settings.MEDIA_ROOT, output_path)
        
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        doc.save(full_path)
        
        return output_path
        
    except Exception as e:
        print(f"Ошибка при генерации документа: {str(e)}")
        raise   

def generate_pdf(docx_path):
    """Конвертирует DOCX в PDF используя LibreOffice"""
    try:
        # Получаем полные пути
        docx_full_path = os.path.join(settings.MEDIA_ROOT, docx_path)
        pdf_path = docx_path.replace('docx', 'pdf').replace('.docx', '.pdf')
        pdf_full_path = os.path.join(settings.MEDIA_ROOT, pdf_path)
        
        # Создаем директорию для PDF если её нет
        os.makedirs(os.path.dirname(pdf_full_path), exist_ok=True)
        
        try:
            process = subprocess.Popen([
                '/usr/bin/libreoffice',
                '--headless',
                '--convert-to',
                'pdf',
                '--outdir',
                os.path.dirname(pdf_full_path),
                docx_full_path
            ], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            env={'HOME': '/tmp'})
            
            stdout, stderr = process.communicate()
            print(f"LibreOffice output: {stdout.decode()}")
            print(f"LibreOffice errors: {stderr.decode()}")
            
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, process.args)
                
            print(f"PDF успешно создан: {pdf_path}")
            
        except FileNotFoundError:
            raise FileNotFoundError("LibreOffice не найден. Установите: sudo apt install libreoffice")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при выполнении LibreOffice: {e}")
            raise
            
        return pdf_path
        
    except Exception as e:
        print(f"Ошибка при конвертации в PDF: {str(e)}")
        raise
