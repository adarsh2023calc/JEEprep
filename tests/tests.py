from django.test import TestCase
from django.urls import reverse


class ApiViewsTest(TestCase):
    def test_sql_run_endpoint_returns_json(self):
        response = self.client.post(reverse('run_sql'), data={"query": "SELECT 1"}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), 'success')

    def test_generate_quiz_endpoint_exists(self):
        response = self.client.post(reverse('generate_quiz'), data={"number": 1}, content_type='application/json')
        self.assertIn(response.status_code, [200, 500])

    def test_save_assessment_returns_bad_request_without_payload(self):
        response = self.client.post('/api/save_details/', data={}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
