from django.apps import AppConfig


class Api2Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api2"
    
    def ready(self):
        print("Starting Scheduler.....")
        from api2.data_schedule import open_api_schedule
        open_api_schedule.start()