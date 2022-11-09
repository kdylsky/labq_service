from django.urls import path
from api.views import RainFallPipeAPi

urlpatterns=[
    path("draninpipe/<str:gubn>", RainFallPipeAPi.as_view())
]