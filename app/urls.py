"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cars import views
from rest_framework.routers import DefaultRouter
from cars import api
from cars.api import CarsViewset, DriveViewset, EngineTypeViewset, BodyTypeViewset, TransmissionTypeViewset, UserViewset


# from cars.views import UserInfoView

router = DefaultRouter()
router.register("cars", CarsViewset, basename = "cars")
router.register("drives", DriveViewset, basename='drives')
router.register("enginetypes", EngineTypeViewset, basename='enginetypes')
router.register("bodytypes", BodyTypeViewset, basename='bodytypes')
router.register("transmissiontypes", TransmissionTypeViewset, basename='transmissiontypes')
router.register("users", UserViewset, basename="user")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ShowCarsView.as_view()),
    path('api/', include(router.urls)),    
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/cars/export/', api.CarsViewset.export_cars, name='export_cars'),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)