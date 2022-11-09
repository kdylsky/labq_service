from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from decorators.execption_handler import execption_hanlder
from api.service import LabqService
from api.utils.data_enums import DataTpye
from api.utils.exceptions import IncorrectGUBNError

labq_service=LabqService()

class RainFallPipeAPi(APIView):
    def get(self, request, *args, **kwargs):
        return get_list(request, *args, **kwargs)

@execption_hanlder()
@parser_classes([JSONParser])
def get_list(request, *args, **kwargs):
    drainpipe_param = kwargs["gubn"]
    data = DataTpye()
    if drainpipe_param not in data.data.keys():
        raise IncorrectGUBNError()
    return JsonResponse(labq_service.get_list(drainpipe_param), status=status.HTTP_200_OK)