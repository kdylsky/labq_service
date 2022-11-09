import requests as req
from datetime import datetime
from api.utils.exceptions import OpenAPIError
from api.utils.data_enums import  DataTpye
from api.serializers import DrainPipeSchema, RainFallSchema
from django.conf import settings

base = DataTpye()

class UrlSetter:
    def __init__(self, drainpipe_param):
        self.api_key = settings.API_KEY #공공API 요청 key
        self.drainpipe_param = drainpipe_param #url로 들어오는 하수도 구분코드
        self.drainpipe_endparmas= base.data[self.drainpipe_param]["idn_cnt"] #구별 하수도 측정기 수              
        self.rainfall_param =base.data[self.drainpipe_param]["gu_name"] #하수도 구분코드 -> 강수량 구분코드
        self.rainfall_endparms =base.data[self.drainpipe_param]["raingauge_cnt"] # 구별 강수량 계량기 수
        self.time = datetime.now().now().strftime('%Y%m%d%H')  
        self.base_time = datetime.now().now().strftime('%Y%m%d')
    
    def get_drainfall_list(self, service_name):
        """
        하수도 open API 요청 함수
        데이터가 오름차순으로 출력되기 때문에 최신 실시간 정보를위해서 두번 요청이 이루어진다.
        
        1. 현재 몇개의 데이터가 쌓여있는지 확인한다. -> 리스트수 출력
        2. 총 리스트수 - 구별 하수도 측정기 수 = 최신데이터가 쌓이기 시작한 위치
        """
        data = self._call_url(service_name)
        end_idx = data["DrainpipeMonitoringInfo"]["list_total_count"]
        start_idx = end_idx-self.drainpipe_endparmas
        data = self._call_url(service_name, start_idx=start_idx, end_idx=end_idx)
        data=data["DrainpipeMonitoringInfo"]["row"]
        serializer = DrainPipeSchema(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.data
        
    def get_rainfall_list(self, service_name):
        """
        강수량 open API 요청 함수
        """
        data=self._call_url(service_name)
        data=data["ListRainfallService"]["row"]
        serializer= RainFallSchema(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.data
    
    def _call_url(self, service_name, **kwargs):
        if service_name == "DrainpipeMonitoringInfo":
            start_idx= kwargs.get("start_idx",1)
            end_idx = kwargs.get("end_idx",2)
            url = f"http://openapi.seoul.go.kr:8088/{self.api_key}/json/{service_name}/{start_idx+1}/{end_idx}/{self.drainpipe_param}/{self.base_time}/{self.time}"
        
        elif service_name == "ListRainfallService":
            url = f"http://openapi.seoul.go.kr:8088/{self.api_key}/json/{service_name}/1/{self.rainfall_endparms}/{self.rainfall_param}"
        
        res = req.get(url)
        data = res.json()

        if not data.get(service_name):
            msg = res.json()
            raise OpenAPIError(msg) 
        return data