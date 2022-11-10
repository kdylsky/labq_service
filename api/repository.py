from api.serializers import DrainPipeSchema, RainFallSchema

class LabqUrlRepo:
    def set_drainpipe(self, drainpipe_data: dict)-> dict:
        serializer = DrainPipeSchema(data=drainpipe_data, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.data

    def set_rainfall(self, rainfall_data: dict)-> dict:
        serializer = RainFallSchema(data=rainfall_data, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.data