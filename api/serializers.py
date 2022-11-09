from rest_framework import serializers

class DrainPipeSchema(serializers.Serializer):
    """서울시 하수관 Open API 응답 파라이터"""
    IDN=serializers.CharField(max_length=10)
    GUBN=serializers.IntegerField()
    GUBN_NAM=serializers.CharField(max_length=10)
    MEA_YMD=serializers.DateTimeField()
    MEA_WAL=serializers.FloatField()
    SIG_STA=serializers.CharField(max_length=20)
    REMARK=serializers.CharField(max_length=200)
    RISK=serializers.SerializerMethodField()

    def get_RISK(self,obj):
        if obj["MEA_WAL"]>=1 :
            return "위험"
        elif obj["MEA_WAL"]>= 0.05:
            return "경고"
        elif obj["MEA_WAL"]>=0.02:
            return "주의"
        else:
            return "안전"


class RainFallSchema(serializers.Serializer):
    """서울시 강수량 OpenAPI 응답 파라미터"""
    RAINGAUGE_CODE = serializers.FloatField()
    RAINGAUGE_NAME = serializers.CharField(max_length=10)
    GU_CODE = serializers.FloatField()
    GU_NAME = serializers.CharField(max_length=10) 
    RAINFALL10 = serializers.IntegerField()
    RECEIVE_TIME= serializers.DateTimeField()
    RISK=serializers.SerializerMethodField()

    def get_RISK(self,obj):
        if obj["RAINFALL10"] >=100 :
            return "위험"
        elif obj["RAINFALL10"]>=50:
            return "경고"
        elif obj["RAINFALL10"]>=20:
            return "주의"
        else:
            return "안전"