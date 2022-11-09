from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from decorators.execption_handler import execption_hanlder
from api2.service import LabqService
from api2.utils.exceptions import IncorrectGUBNError
from api.utils.data_enums import DataTpye


labq_service = LabqService()

class LabqAPIView(APIView):
    def get(self, request, *awrg, **kwargs):
        return get_list(request, *awrg, **kwargs)

@execption_hanlder()
@parser_classes([JSONParser])
def get_list(request, *awrg, **kwargs):
    gubn = kwargs["gubn"]
    data = DataTpye()
    if gubn not in data.data.keys():
        raise IncorrectGUBNError()
    return JsonResponse(labq_service.get_list(gubn), status=status.HTTP_200_OK, safe=False)