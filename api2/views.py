from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from decorators.execption_handler import execption_hanlder
from api.utils.data_enums import DataTpye
from api.utils.exceptions import IncorrectGUBNError
from api2.service import LabqService

labq_service = LabqService()

class LabqAPIView(APIView):
    def get(self, request, *awrg, **kwargs):
        return get_list(request, *awrg, **kwargs)

@execption_hanlder()
@parser_classes([JSONParser])
def get_list(request, *awrg, **kwargs):
    return JsonResponse({"result":"result"})


from api2.utils.utils import UpdateData 

class TestAPI(APIView):
    def get(self,request):
        test = UpdateData()
        test.update()
        return JsonResponse({"result":"result"})
        