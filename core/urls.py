from django.contrib import admin
from django.urls import path, include 
from rest_framework import routers
from .views import *


router = routers.SimpleRouter()
router.register('auth',UserViewSet, basename='user')


urlpatterns = [
    path('api/v1/', include(router.urls)),
]+router.urls