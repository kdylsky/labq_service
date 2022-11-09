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


class RainFallSchema(serializers.ModelSerializer):
    GU_CODE = serializers.IntegerField(source="gu_code")
    GU_NAME = serializers.CharField(max_length=10, source="gu_name")

    class Meta:
        model = RainFall
        fields = "GU_CODE", "GU_NAME"


class DetailRainFallSechema(serializers.ModelSerializer):
    GU_CODE = serializers.IntegerField(source="rainfall.gu_code")
    RAINGAUGE_CODE = serializers.IntegerField(source="raingauge_code")
    RAINGAUGE_NAME = serializers.CharField(max_length=10, source="raingauge_name")
    RAINFALL10 = serializers.IntegerField(source="rainfall10")
    RECEIVE_TIME =serializers.CharField(max_length=30, source="receive_time")

    class Meta:
        model = DetailRainFall
        fields = "GU_CODE", "RAINGAUGE_CODE", "RAINGAUGE_NAME", "RAINFALL10", "RECEIVE_TIME"


class DrainPipeSerialize(serializers.ModelSerializer):
    class Meta:
        model = DrainPipe
        fields = "__all__"


class DetailDrainPipeSerialize(serializers.ModelSerializer):
    class Meta:
        model = DetailDrainPipe
        fields = "__all__"


class RainFallSerialize(serializers.ModelSerializer):
    class Meta:
        model = RainFall
        fields = "__all__"


class DetailRainFallSerialize(serializers.ModelSerializer):
    class Meta:
        model = DetailRainFall
        fields = "__all__"
