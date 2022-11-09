from django.urls import path
from api2.views import TestAPI

urlpatterns=[
    path("api2", TestAPI.as_view())
]