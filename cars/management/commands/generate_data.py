# import random
# from cars.models import Car, Drive, EngineType, BodyType, TransmissionType
# from django.contrib.auth.models import User

# user = User.objects.first()  

# for i in range(10):  
#     car = Car.objects.create(
#         name= "Автомобиль {i+1}" ,
#         drive=Drive.objects.order_by("?").first(), 
#         etype=EngineType.objects.order_by("?").first(),  
#         btype=BodyType.objects.order_by("?").first(),  
#         trtype=TransmissionType.objects.order_by("?").first(),  
#         user=user,  
#     )
#     print(f"Создан автомобиль : {car.name}")
from django.core.management.base import BaseCommand
from faker import Faker
from cars.models import Car, Drive, EngineType, BodyType, TransmissionType
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        user = User.objects.first()  # Используем первого пользователя
        
        if not user:
            self.stdout.write(self.style.ERROR("Нет доступных пользователей."))
            return

        for i in range(1, 11):  # Генерируем 10 записей
            car = Car.objects.create(
                name=f"Автомобиль {i}",
                drive=Drive.objects.order_by("?").first(),
                etype=EngineType.objects.order_by("?").first(),
                btype=BodyType.objects.order_by("?").first(),
                trtype=TransmissionType.objects.order_by("?").first(),
                user=user,
            )
            self.stdout.write(self.style.SUCCESS(f"Создан автомобиль: {car.name}"))
