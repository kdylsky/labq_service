from django.urls import path
from api.views import RainFallPipeAPi

urlpatterns=[
    path("api/<str:gubn>", RainFallPipeAPi.as_view())
]