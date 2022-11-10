from apscheduler.schedulers.background import BackgroundScheduler
from api2.utils.utils import UpdateData
from api.utils.data_enums import DataTpye

def start():
    """한시간 간격으로 하수도&강수량 DB데이터 업데이트"""
    scheduler = BackgroundScheduler()
    data_save = ScheduleCall()
    scheduler.add_job(data_save.call_open_api,"interval", minutes=60, id="data_001", replace_existing=True)
    scheduler.start()

data = DataTpye()
class ScheduleCall:
    def call_open_api(self):
        for i in data.data.keys():
            update = UpdateData(i)
            update.update_drainpipe()
            update.update_rainfall()