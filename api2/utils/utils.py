from api.utils.utils import UrlSetter
from api.utils.data_enums import DataTpye
from api2.serializers import DrainPipeSchema, DetailDrainPipeSchema, RainFallSchema, DetailRainFallSechema
from api2.models import DrainPipe, DetailDrainPipe, RainFall, DetailRainFall
from api2.utils.slack_bot import post_message
from django.conf import settings

data = DataTpye()

class UpdateData:
    def __init__(self, gubn_code: str)-> None:
        self.urlsetter = UrlSetter(gubn_code)

    def _get_drainpipe(self)-> dict:
        """이미 정의된 하수도 OpenAPI 데이터 요청 함수"""
        return self.urlsetter.get_drainfall_list("DrainpipeMonitoringInfo")
    
    def _get_rainall(self)-> dict:
        """이미 정의된 강수량 OpenAPI 데이터 요청 함수"""
        return self.urlsetter.get_rainfall_list("ListRainfallService")

    def update_drainpipe(self)-> None:
        """
        phase1
        - 구정보 업데이트
        
        phase2
        - 구별 하수도 상세 정보 업데이트
        """
        pipe_data = self._get_drainpipe()
        serialize_one = DrainPipeSchema(data=pipe_data, many=True, partial=True)
        serialize_one.is_valid(raise_exception=True)
        self._drainpipe_partial_update(serialize_one.data)
        
        serialize_two = DetailDrainPipeSchema(data=pipe_data, many=True,partial=True)
        serialize_two.is_valid(raise_exception=True)    
        self._detaildrainpipe_partial_update(pipe_data)

    def _drainpipe_partial_update(self, data: dict)-> None:
        obj, flag = DrainPipe.objects.get_or_create(
            gubn=data[0]["GUBN"],
            defaults={
                "gubn_nam": data[0]["GUBN_NAM"]
            }
        )
        obj.save()
    
    def _detaildrainpipe_partial_update(self, data: dict)-> None:
        for i in data:
            obj, flag = DetailDrainPipe.objects.update_or_create(
                gubn=DrainPipe.objects.get(gubn=int(i["GUBN"])),
                idn=i["IDN"],
                remark=i["REMARK"],
                defaults={
                    "mea_ymd":i["MEA_YMD"],
                    "mea_wal":i["MEA_WAL"],
                    "sig_sta":i["SIG_STA"]
                } 
            )
            if not flag:
                obj.mea_ymd = i["MEA_YMD"]
                obj.mea_wal = i["MEA_WAL"]
                obj.sig_sta = i["SIG_STA"]
            obj.save()
            msg = self._message_drainpipe(obj.mea_wal, obj.idn)
            if msg:
                post_message(settings.SLACK_CHANNEL, msg)

    def update_rainfall(self)-> None:
        """
        phase1
        - 구정보 업데이트
        
        phase2
        - 구별 강우량 상세 정보 업데이트
        """
        rain_data = self._get_rainall()
        serialize_one = RainFallSchema(data=rain_data,many=True, partial=True)
        serialize_one.is_valid(raise_exception=True)
        self._rainfall_partial_update(serialize_one.data)
        
        serialize_two = DetailRainFallSechema(data=rain_data, many=True,partial=True)
        serialize_two.is_valid(raise_exception=True)    
        self._detailrainfall_partial_update(rain_data)
    
    def _rainfall_partial_update(self, data: dict)-> None:
        obj, flag = RainFall.objects.get_or_create(
            gu_code=data[0]["GU_CODE"],
            defaults={
                "gu_name": data[0]["GU_NAME"]
            }
        )
        obj.save()

    def _detailrainfall_partial_update(self, data: dict)-> None:
        for i in data:
            obj, flag = DetailRainFall.objects.update_or_create(
                gu_code = RainFall.objects.get(gu_code=int(i["GU_CODE"])),
                raingauge_code = i["RAINGAUGE_CODE"],
                raingauge_name = i["RAINGAUGE_NAME"],
                defaults={
                    "rainfall10":i["RAINFALL10"],
                    "receive_time":i["RECEIVE_TIME"]
                } 
            )
            if not flag:
                obj.rainfall10 = i["RAINFALL10"]
                obj.receive_time = i["RECEIVE_TIME"]
            obj.save()
            msg = self._message_rainfall(obj.rainfall10, obj.gu_code)
            if msg:
                post_message(settings.SLACK_CHANNEL, msg)

    def _message_drainpipe(self, mea_wal, idn)-> str:
        msg = None
        if mea_wal >= 1:
            msg = f"{idn} 위험 수위를 확인하세요"
        elif mea_wal >= 0.8:
            msg = f"{idn} 경고 수위를 확인하세요"
        elif mea_wal >= 0.5:
            msg = f"{idn} 주의 수위를 확인하세요"  
        return msg
    
    def _message_rainfall(self, rainfall10, gu_code)-> str:
        msg = None
        
        if int(rainfall10) >= 200:
            msg = f"{gu_code} 대피하세요!!"
        elif int(rainfall10) >= 100:
            msg = f"{gu_code} 위험입니다."
        return msg