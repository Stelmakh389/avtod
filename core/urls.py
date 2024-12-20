from django.urls import path
from core.views import equipment, vehicle, organization, auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse

urlpatterns = [

    path('login/', auth.CustomLoginView.as_view(), name='login'),
    path('logout/', auth.CustomLogoutView.as_view(), name='logout'),

    # Средства измерения
    path('equipment/measurement/', login_required(equipment.MeasurementToolListView.as_view()), name='measurement-tool-list'),
    path('equipment/measurement/create/', login_required(equipment.MeasurementToolCreateView.as_view()), name='measurement-tool-create'),
    path('equipment/measurement/<int:pk>/update/', login_required(equipment.MeasurementToolUpdateView.as_view()), name='measurement-tool-update'),
    path('equipment/measurement/<int:pk>/delete/', login_required(equipment.MeasurementToolDeleteView.as_view()), name='measurement-tool-delete'),

    # Испытательное оборудование
    path('equipment/testing/', login_required(equipment.TestingEquipmentListView.as_view()), name='testing-equipment-list'),
    path('equipment/testing/create/', login_required(equipment.TestingEquipmentCreateView.as_view()), name='testing-equipment-create'),
    path('equipment/testing/<int:pk>/update/', login_required(equipment.TestingEquipmentUpdateView.as_view()), name='testing-equipment-update'),
    path('equipment/testing/<int:pk>/delete/', login_required(equipment.TestingEquipmentDeleteView.as_view()), name='testing-equipment-delete'),

    # Вспомогательное оборудование
    path('equipment/auxiliary/', login_required(equipment.AuxiliaryEquipmentListView.as_view()), name='auxiliary-equipment-list'),
    path('equipment/auxiliary/create/', login_required(equipment.AuxiliaryEquipmentCreateView.as_view()), name='auxiliary-equipment-create'),
    path('equipment/auxiliary/<int:pk>/update/', login_required(equipment.AuxiliaryEquipmentUpdateView.as_view()), name='auxiliary-equipment-update'),
    path('equipment/auxiliary/<int:pk>/delete/', login_required(equipment.AuxiliaryEquipmentDeleteView.as_view()), name='auxiliary-equipment-delete'),

    # Карточки автомобилей
    path('vehicles/', login_required(vehicle.VehicleListView.as_view()), name='vehicle-list'),
    path('vehicles/create/', login_required(vehicle.vehicle_create), name='vehicle-create'),
    path('vehicles/<int:pk>/', login_required(vehicle.VehicleDetailView.as_view()), name='vehicle-detail'),
    path('vehicles/<int:pk>/update/', login_required(vehicle.vehicle_update), name='vehicle-update'),
    path('vehicles/<int:pk>/delete/', login_required(vehicle.vehicle_delete), name='vehicle-delete'),
    path('vehicles/<int:pk>/generate-protocols/', login_required(vehicle.generate_vehicle_protocols), name='generate-protocols'),

    # Для авто
    path('vehicles/<int:pk>/duplicate/', login_required(vehicle.duplicate_vehicle), name='vehicle-duplicate'),

    # Для оборудования
    path('equipment/measurement/<int:pk>/duplicate/', login_required(lambda request, pk: equipment.duplicate_equipment(request, pk, 'measurement-tool')), name='measurement-tool-duplicate'),
    path('equipment/testing/<int:pk>/duplicate/', login_required(lambda request, pk: equipment.duplicate_equipment(request, pk, 'testing-equipment')), name='testing-equipment-duplicate'),
    path('equipment/auxiliary/<int:pk>/duplicate/', login_required(lambda request, pk: equipment.duplicate_equipment(request, pk, 'auxiliary-equipment')), name='auxiliary-equipment-duplicate'),
    # Организация
    path('organization/', organization.OrganizationUpdateView.as_view(), name='organization-detail'),
    
    path('equipment/<str:equipment_type>/import/', login_required(equipment.import_equipment), name='equipment-import'),
    path('equipment/<str:equipment_type>/export/', login_required(equipment.export_equipment), name='equipment-export'),

    path('equipment/<str:equipment_type>/delete-all/', login_required(equipment.delete_all_equipment), name='equipment-delete-all'),

    path('vehicles/save-columns/', login_required(vehicle.save_column_preferences), name='save-column-preferences'),
]