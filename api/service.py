from api.utils.utils import UrlSetter

class LabqService:        
    def __init__(self)->None:
        self.DrainpipeMonitoringInfo = "DrainpipeMonitoringInfo"
        self.ListRainfallService = "ListRainfallService"
    
    def get_list(self, drainpipe_param: str)-> dict:        
        url = UrlSetter(drainpipe_param)
        drainpipe = url.get_drainfall_list(self.DrainpipeMonitoringInfo)
        rainfall = url.get_rainfall_list(self.ListRainfallService)        
        return {"DrainPipi":drainpipe, "Rainfall":rainfall}