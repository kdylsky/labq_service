from api.utils.utils import UrlSetter
from api.utils.data_enums import DataTpye

data = DataTpye()

class UpdateData:
    def __init__(self):
        # self.urlsetter = UrlSetter(i for i in data.data.keys())
        self.urlsetter = UrlSetter("01")
   
    def _get_drainpipe(self):
        return self.urlsetter.get_drainfall_list("DrainpipeMonitoringInfo")
    
    def _get_rainall(self):
        return self.urlsetter.get_rainfall_list("ListRainfallService")

    def update(self):
        pipe = self._get_drainpipe()
        rain = self._get_rainall()