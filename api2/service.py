from api2.repository import LabqRepo

class LabqService:
    def __init__(self):
        self.repo = LabqRepo()
    
    def get_list(self, gubn):
        pipe = self.repo.get_drainpipe(gubn)
        rain = self.repo.get_rainfall(gubn)
        return {"하수관": pipe, "강우량":rain}  