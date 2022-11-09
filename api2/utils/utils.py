from api.utils.utils import UrlSetter
from api.utils.data_enums import DataTpye
from api2.serializers import DrainPipeSchema, DetailDrainPipeSchema, RainFallSchema, DetailRainFallSechema
from api2.models import DrainPipe, DetailDrainPipe, RainFall, DetailRainFall

data = DataTpye()

class UpdateData:
    def __init__(self, i):
        self.urlsetter = UrlSetter(i)

    def _get_drainpipe(self):
        return self.urlsetter.get_drainfall_list("DrainpipeMonitoringInfo")
    
    def _get_rainall(self):
        return self.urlsetter.get_rainfall_list("ListRainfallService")

    def update_drainpipe(self):
        pipe_data = self._get_drainpipe()
        serialize_one = DrainPipeSchema(data=pipe_data, many=True, partial=True)
        serialize_one.is_valid(raise_exception=True)
        self._drainpipe_partial_update(serialize_one.data)
        serialize_two = DetailDrainPipeSchema(data=pipe_data, many=True,partial=True)
        serialize_two.is_valid(raise_exception=True)    
        self._detaildrainpipe_partial_update(pipe_data)
    

    def _drainpipe_partial_update(self, data):
        obj, flag = DrainPipe.objects.get_or_create(
            gubn=data[0]["GUBN"],
            defaults={
                "gubn_nam": data[0]["GUBN_NAM"]
            }
        )
        obj.save()
    
    def _detaildrainpipe_partial_update(self, data):
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



    def update_rainfall(self):
        rain_data = self._get_rainall()
        serialize_one = RainFallSchema(data=rain_data,many=True, partial=True)
        serialize_one.is_valid(raise_exception=True)
        self._rainfall_partial_update(serialize_one.data)
        
        serialize_two = DetailRainFallSechema(data=rain_data, many=True,partial=True)
        serialize_two.is_valid(raise_exception=True)    
        self._detailrainfall_partial_update(rain_data)
    
    def _rainfall_partial_update(self, data):
        obj, flag = RainFall.objects.get_or_create(
            gu_code=data[0]["GU_CODE"],
            defaults={
                "gu_name": data[0]["GU_NAME"]
            }
        )
        obj.save()

    def _detailrainfall_partial_update(self, data):
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

class Real_call:
    def call_test(self):
        # for i in data.data.keys():
        for i in ["01", "02"]:
            a = UpdateData(i)
            a.update_drainpipe()
            a.update_rainfall()