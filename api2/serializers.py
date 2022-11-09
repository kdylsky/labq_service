from rest_framework import serializers

class DrainpipeSchema(serializers.Serializer):
    gubn = serializers.IntegerField()
    