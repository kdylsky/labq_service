from apscheduler.schedulers.background import BackgroundScheduler
from api2.utils.utils import UpdateData

def start():
    scheduler = BackgroundScheduler()
    data_save = Real_call()
    scheduler.add_job(data_save.call_test,"interval", minutes=60, id="data_001", replace_existing=True)
    scheduler.start()

class Real_call:
    def call_test(self):
        # for i in data.data.keys():
        for i in ["01", "02"]:
            update = UpdateData(i)
            update.update_drainpipe()
            update.update_rainfall()