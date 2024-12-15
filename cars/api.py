from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from cars.models import Car, Drive, EngineType, BodyType, TransmissionType
from rest_framework.response import Response
from rest_framework import status
from cars.serializers import CarCreateSerializer, CarSerializer, DriveSerializer, DriveCreateSerializer, EngineTypeCreateSerializer, EngineTypeSerializer, BodyTypeCreateSerializer, BodyTypeSerializer, TransmissionTypeSerializer, TransmissionTypeCreateSerializer

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import action
from django.contrib.auth.models import User

from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Max, Min

import openpyxl
from django.http import HttpResponse

class UserViewset(GenericViewSet):
    @action(url_path="info", detail=False, methods=["GET"])
    def get_info(self, request, *args, **kwargs):
        data = {
            "is_authenticated": request.user.is_authenticated
        }
        if request.user.is_authenticated:
            data.update({
                "username": request.user.username,
                "user_id": request.user.id,
            })
        return Response(data)

    @action(url_path="login", detail=False, methods=["POST"])
    def login(self, request, *args, **kwargs):
        username = request.data.get("user")
        password = request.data.get("pass")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"success": True})
        return Response({"success": False, "error": "Invalid credentials"}, status=400)

    @action(url_path="logout", detail=False, methods=["GET"])
    def logout(self, request, *args, **kwargs):
        logout(request)
        return Response({"success": True})
    

class CarsViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        # Привязываем текущего пользователя к автомобилю
        serializer.save(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return CarCreateSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        qs = super().get_queryset()
        # фильтруем по текущему юзеру
        qs = qs.filter(user=self.request.user)
        return qs
   
    
    @action(detail=False, methods=["GET"], url_path="stats")
    def stats(self, request, *args, **kwargs):
        data = {
            "total_cars": Car.objects.count(),
            "total_drives": Drive.objects.count(),
            "total_engine_types": EngineType.objects.count(),
            "total_body_types": BodyType.objects.count(),
            "total_transmission_types": TransmissionType.objects.count(),
        }
        return Response(data)
    
    @action(detail=False, methods=['get'], url_path='export')
    def export_cars(self, request):
        # Создаем Excel-файл
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Cars"
        ws.append(["Название", "Тип привода", "Тип двигателя", "Тип кузова", "Тип КПП", "Пользователь"])

        for car in Car.objects.all():
            ws.append([
                car.name,
                car.drive.name if car.drive else "",
                car.etype.etype if car.etype else "",
                car.btype.btype if car.btype else "",
                car.trtype.trtype if car.trtype else "",
                car.user.username if car.user else "",
            ])

        # Отправляем файл в ответе
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=cars.xlsx'
        wb.save(response)
        return response

class DriveViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Drive.objects.all()
    serializer_class = DriveSerializer
    
    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return DriveCreateSerializer
        return super().get_serializer_class()
    
class EngineTypeViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = EngineType.objects.all()
    serializer_class = EngineTypeSerializer
    
    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return EngineTypeCreateSerializer
        return super().get_serializer_class()
    
class BodyTypeViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = BodyType.objects.all()
    serializer_class = BodyTypeSerializer
    
    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return BodyTypeCreateSerializer
        return super().get_serializer_class()
    
class TransmissionTypeViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = TransmissionType.objects.all()
    serializer_class = TransmissionTypeSerializer
    
    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return TransmissionTypeCreateSerializer
        return super().get_serializer_class()