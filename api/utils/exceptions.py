from rest_framework import status
from exceptions import CustomBaseExecption

class OpenAPIError(CustomBaseExecption):
    def __init__(self, msg):
        self.msg = msg
        self.status = status.HTTP_400_BAD_REQUEST


class IncorrectGUBNError(CustomBaseExecption):
    def __init__(self):
        self.msg = "The GUBN CODE is not Invaild ex)1,2->01,02, 10->10"
        self.status = status.HTTP_404_NOT_FOUND