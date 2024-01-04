import unittest
from unittest.mock import patch
from api_gateway_service import app

class TESTSAPIGatewayService(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    @patch('requests.get')  # Mock the requests.get function
    def test_get_messages(self, mock_get):
        # Mock the response from the requests.get call
        mock_get.return_value.content = b"Mocked Content"
        mock_get.return_value.status_code = 200

        response = self.app.get('/messages')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Mocked Content")
        self.assertEqual(response.content_type, 'text/plain')

    @patch('requests.put')  # Mock the requests.put function
    def test_shutdown(self, mock_put):
        # Mock the response from the requests.put call
        mock_put.return_value.content = b"Mocked Content"
        mock_put.return_value.status_code = 200

        response = self.app.put('/state', data='SHUTDOWN')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Mocked Content")
        self.assertEqual(response.content_type, 'text/plain')
    @patch('requests.put')  # Mock the requests.put function
    def test_set_state_other_than_shutdown(self, mock_put):
        # Mock the response from the requests.put call
        mock_put.return_value.content = b"Mocked Content"
        mock_put.return_value.status_code = 200

        response = self.app.put('/state', data='INIT')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Mocked Content")
        self.assertEqual(response.content_type, 'text/plain')
        mock_put.assert_called_once_with('http://service1:8001/state', data='INIT')

    @patch('requests.get')  # Mock the requests.get function
    def test_get_state(self, mock_get):
        # Mock the response from the requests.get call
        mock_get.return_value.content = b"Mocked Content"
        mock_get.return_value.status_code = 200

        response = self.app.get('/state')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Mocked Content")
        self.assertEqual(response.content_type, 'text/plain')
        mock_get.assert_called_once_with('http://service1:8001/state')

    @patch('requests.get')  # Mock the requests.get function
    def test_get_run_log(self, mock_get):
        # Mock the response from the requests.get call
        mock_get.return_value.content = b"Mocked Content"
        mock_get.return_value.status_code = 200

        response = self.app.get('/run-log')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Mocked Content")
        self.assertEqual(response.content_type, 'text/plain')
        mock_get.assert_called_once_with('http://monitoring_service:8087/run-logs')
if __name__ == '__main__':
    unittest.main()