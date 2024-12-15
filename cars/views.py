from django.shortcuts import render
from django.http import HttpResponse
from cars.models import Car, Drive
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from rest_framework import status
from cars.serializers import CarSerializer

# Create your views here.

class ShowCarsView(TemplateView):
    template_name = "cars/show_cars.html"
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["cars"] = Car.objects.all()
        return context
    
class CarCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id  # Привязываем к текущему пользователю

        serializer = CarSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]  # Только авторизованные пользователи могут получить доступ

    def get(self, request, *args, **kwargs):
        user = request.user
        data = {
            'is_authenticated': user.is_authenticated,
            'username': user.username,
            'user_id': user.id
        }
        return Response(data)