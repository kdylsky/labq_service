from django.urls import path
from api2.views import LabqAPIView

urlpatterns=[
    path("api2/<str:gubn>", LabqAPIView.as_view())
]