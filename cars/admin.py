from django.contrib import admin
from cars.models import Car, Drive, EngineType, BodyType, TransmissionType

# Register your models here.
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    # pass
    list_display = ['id', 'name', 'drive', 'etype', 'btype', 'trtype', 'picture']
    
@admin.register(Drive)
class DriveAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'picture']
    
@admin.register(EngineType)
class EngineTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'etype', 'description', 'picture']
    
@admin.register(BodyType)
class BodyTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'btype', 'description', 'picture']
    
@admin.register(TransmissionType)
class TransmissionTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'trtype', 'description', 'picture']