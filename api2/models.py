from django.db import models

class DrainPipe(models.Model):
    gubn = models.IntegerField()
    gubn_nam = models.CharField(max_length=10)

    class Meta:
        db_table = "drainpipes"
        managed = True
        abstract = False


class DetailDrainPipe(models.Model):
    gubn = models.ForeignKey(
        DrainPipe,
        db_column = "gubn_id",
        on_delete = models.CASCADE)
    idn = models.CharField(max_length=15)
    mea_ymd = models.DateTimeField()
    mea_wal = models.FloatField()
    sig_sta = models.CharField(max_length=20)
    remark = models.TextField()

    class Meta:
        db_table = "detaildrainpipes"
        managed = True
        abstract = False


class RainFall(models.Model):
    gu_code = models.IntegerField()
    gu_name = models.CharField(max_length=10)

    class Meta:
        db_table = "rainfalls"
        managed = True
        abstract = False


class DetailRainFall(models.Model):
    gu_code = models.ForeignKey(
        RainFall,
        db_column = "gu_code_id",
        on_delete = models.CASCADE
    )
    raingauge_code = models.IntegerField()
    raingauge_name = models.CharField(max_length=10)
    rainfall10 = models.IntegerField()
    receive_time = models.DateTimeField()

    class Meta:
        db_table = "detailrainfall"
        managed = True
        abstract = False