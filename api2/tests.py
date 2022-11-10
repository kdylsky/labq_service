from django.test import TestCase, Client
from api2.models import DrainPipe, DetailDrainPipe, RainFall, DetailRainFall

class LabqAPITest(TestCase):
    def setUp(self) -> None:
        DrainPipe.objects.create(id=1, gubn=1, gubn_nam="종로")
        DetailDrainPipe.objects.create(id=1, gubn=DrainPipe.objects.get(id=1), idn="01-0001", mea_ymd="2022-11-10 13:24:05.0", mea_wal=0.5, sig_sta="통신양호", remark="종로구 병원 앞")
        DetailDrainPipe.objects.create(id=2, gubn=DrainPipe.objects.get(id=1), idn="01-0002", mea_ymd="2022-11-10 13:24:05.0", mea_wal=0.3, sig_sta="통신양호", remark="종로구 학교 앞")
        RainFall.objects.create(id=1, gu_code=110, gu_name="종로구")
        DetailRainFall.objects.create(id=1, gu_code=RainFall.objects.get(id=1),raingauge_code=1001, raingauge_name="부암동", rainfall10=200, receive_time="2022-11-10 13:19")
        DetailRainFall.objects.create(id=2, gu_code=RainFall.objects.get(id=1),raingauge_code=1002, raingauge_name="종로구청", rainfall10=100, receive_time="2022-11-10 13:19")

    def tearDown(self) -> None:
        DrainPipe.objects.all().delete()
        DetailDrainPipe.objects.all().delete()
        RainFall.objects.all().delete()
        DetailRainFall.objects.all().delete()

    def test_success_labqapi_get(self):
        """API 성공"""
        client = Client()
        response = client.get("/api2/01", content_type='application/json') 
        data = {
                "하수관": [
                    {
                        "id": 1,
                        "gubn": 1,
                        "gubn_nam": "종로"
                    },
                    [
                        {
                            "id": 1,
                            "idn": "01-0001",
                            "mea_ymd": "2022-11-10 13:24:05.0",
                            "mea_wal": 0.5,
                            "sig_sta": "통신양호",
                            "remark": "종로구 병원 앞",
                            "gubn": 1
                        },
                        {
                            "id": 2,
                            "idn": "01-0002",
                            "mea_ymd": "2022-11-10 13:24:05.0",
                            "mea_wal": 0.3,
                            "sig_sta": "통신양호",
                            "remark": "종로구 학교 앞",
                            "gubn": 1
                        }
                    ]
                ],
                "강우량": [
                    {
                        "id": 1,
                        "gu_code": 110,
                        "gu_name": "종로구"
                    },
                    [
                        {
                            "id": 1,
                            "raingauge_code": 1001,
                            "raingauge_name": "부암동",
                            "rainfall10": 200,
                            "receive_time": "2022-11-10 13:19",
                            "gu_code": 1
                        },
                        {
                            "id": 2,
                            "raingauge_code": 1002,
                            "raingauge_name": "종로구청",
                            "rainfall10": 100,
                            "receive_time": "2022-11-10 13:19",
                            "gu_code": 1
                        }
                    ]
                ]
            }
        
        self.assertEqual(response.json(), data)
        self.assertEqual(response.status_code, 200)
    
    def test_fail_gubn_code_not_invalid_get(self):
        """API 실패 잘못된 구분코드 요청"""
        client = Client()
        response = client.get("/api2/50", content_type='application/json') 
        self.assertEqual(response.json(), {'msg': 'The GUBN CODE is not Invaild ex)1,2->01,02, 10->10'})
        self.assertEqual(response.status_code, 404)

    