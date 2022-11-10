from django.test import TestCase, Client


class RainFallPipeAPiTest(TestCase):
    def test_success_rainfallpipe_get(self):
        client = Client()
        response = client.get("/api/01", content_type='application/json') 
        self.assertEqual(response.status_code, 200)

    def test_fail_incorrect_gubn_code_error_get(self):
        client = Client()
        response = client.get("/api/27", content_type='application/json') 
        self.assertEqual(response.json(), {'msg': 'The GUBN CODE is not Invaild ex)1,2->01,02, 10->10'})
        self.assertEqual(response.status_code, 404)