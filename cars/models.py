from django.db import models
from django.contrib.auth.models import User

#Трансмиссия
class TransmissionType(models.Model):
    trtype = models.TextField("Тип КПП")
    description = models.TextField("Описание", null=True, blank=True)
    
    picture = models.ImageField("Изображение", null=True, upload_to="transmissiontypes")
    
    class Meta:
        verbose_name = "Тип кпп"
        verbose_name_plural = "Типы кпп"
        
    def __str__(self) -> str:
        return self.trtype

#Кузов
class BodyType(models.Model):
    btype = models.TextField("Тип кузова")
    description = models.TextField("Описание", null=True, blank=True)
    
    picture = models.ImageField("Изображение", null=True, upload_to="bodytypes")
    
    class Meta:
        verbose_name = "Тип кузова"
        verbose_name_plural = "Типы кузовов"
        
    def __str__(self) -> str:
        return self.btype

#Двигатель
class EngineType(models.Model):
    etype = models.TextField("Тип двигателя")     
    description = models.TextField("Описание", null=True, blank=True)

    picture = models.ImageField("Изображение", null=True, upload_to="enginetypes")

    class Meta:
        verbose_name = "Тип двигателя"
        verbose_name_plural = "Типы двигателей"
    
    def __str__(self) -> str:
        return self.etype

#Привод
class Drive(models.Model):
    name = models.TextField("Тип привода")
    description = models.TextField("Описание", null=True, blank=True)
    
    picture = models.ImageField("Изображение", null=True, upload_to="drives")
    
    class Meta:
        verbose_name = "Привод"
        verbose_name_plural = "Приводы"
    
    def __str__(self) -> str:
        return self.name

# Create your models here.
#Автомобиль
class Car(models.Model):
    name = models.TextField("Название")
    # drive_name = models.TextField("Привод")
    drive = models.ForeignKey("Drive", on_delete=models.CASCADE, null=True)
    etype = models.ForeignKey("EngineType", on_delete=models.CASCADE, null=True)
    btype = models.ForeignKey("BodyType", on_delete=models.CASCADE, null=True)
    trtype = models.ForeignKey("TransmissionType", on_delete=models.CASCADE, null=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)
    # owner = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, null=True)
    
    picture = models.ImageField("Изображение", null=True, upload_to="cars")
    
    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        
    def __str__(self) -> str:
        return self.name