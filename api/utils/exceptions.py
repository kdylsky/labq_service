from rest_framework import status
from exceptions import CustomBaseExecption

class OpenAPIError(CustomBaseExecption):
    def __init__(self, msg):
        self.msg = msg
        self.status = status.HTTP_400_BAD_REQUEST