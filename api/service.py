from api.utils.utils import UrlSetter
from api.repository import LabqUrlRepo

class LabqService:        
    def __init__(self)->None:
        self.DrainpipeMonitoringInfo = "DrainpipeMonitoringInfo"
        self.ListRainfallService = "ListRainfallService"
        self.repo = LabqUrlRepo() 
    
    def get_list(self, drainpipe_param: str)-> dict:        
        url = UrlSetter(drainpipe_param)
        drainpipe_data = url.get_drainfall_list(self.DrainpipeMonitoringInfo)
        rainfall_data = url.get_rainfall_list(self.ListRainfallService)        
        drainpipe = self.repo.set_drainpipe(drainpipe_data)
        rainfall = self.repo.set_rainfall(rainfall_data)
        return {"DrainPipi":drainpipe, "Rainfall":rainfall}