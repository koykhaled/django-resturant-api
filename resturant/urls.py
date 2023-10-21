from django.urls import path
from .views import Manager

urlpatterns = [
    path("manager",Manager.as_view())
]
