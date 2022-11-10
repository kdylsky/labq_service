from api.utils.data_enums import DataTpye
from api2.models import RainFall, DrainPipe, DetailRainFall, DetailDrainPipe
from api2.serializers import DrainPipeSerialize, DetailDrainPipeSerialize, RainFallSerialize, DetailRainFallSerialize 

class LabqRepo:
    def __init__(self):
        self.rain_model = RainFall
        self.pipe_model = DrainPipe
        self.detail_rain_model = DetailRainFall
        self.detail_pipe_model = DetailDrainPipe
        self.type = DataTpye()    
    
    def get_drainpipe(self, gubn: str)-> dict:
        """데이터베이스 저장된 하수도 정보 출력"""
        pipe = self.pipe_model.objects.get(gubn=int(gubn))
        detail_pipe = self.detail_pipe_model.objects.filter(gubn=pipe)        
        pipe_serial = DrainPipeSerialize(instance=pipe)
        detail_pipe_serial = DetailDrainPipeSerialize(instance=detail_pipe, many=True)
        return pipe_serial.data, detail_pipe_serial.data

    def get_rainfall(self, gubn: str)-> dict:
        """데이터베이스 저장된 강수량 정보 출력"""
        rainfall = self.rain_model.objects.get(gu_name=self.type.data[gubn]["gu_name"])     
        detail_rainfall = self.detail_rain_model.objects.filter(gu_code=rainfall)
        rainfall_serial = RainFallSerialize(instance=rainfall)
        detail_rainfall_serial = DetailRainFallSerialize(instance=detail_rainfall, many=True)
        return rainfall_serial.data, detail_rainfall_serial.data