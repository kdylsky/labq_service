from rest_framework import serializers
from api2.models import DrainPipe, DetailDrainPipe, RainFall, DetailRainFall

class DrainPipeSchema(serializers.ModelSerializer):
    GUBN = serializers.IntegerField(source="gubn")
    GUBN_NAM = serializers.CharField(max_length=10, source="gubn_nam")

    class Meta:
        model = DrainPipe
        fields = "GUBN", "GUBN_NAM"
    

class DetailDrainPipeSchema(serializers.ModelSerializer):
    GUBN = serializers.IntegerField(source="drainpipe.gubn")
    IDN = serializers.CharField(max_length=15, source="idn")
    MEA_YMD = serializers.CharField(max_length=30, source="mea_ymd")
    MEA_WAL = serializers.FloatField(source="mea_wal")
    SIG_STA = serializers.CharField(max_length=20, source="sig_sta")
    REMARK = serializers.CharField(max_length=None, source="remark")
    
    class Meta:
        model = DetailDrainPipe
        fields = "GUBN", "IDN", "MEA_YMD", "MEA_WAL", "SIG_STA", "REMARK"