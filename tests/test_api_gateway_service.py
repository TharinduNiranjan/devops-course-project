import unittest
from unittest.mock import patch
from api_gateway_service.api_gateway_service import app

class TESTSAPIGatewayService(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    @patch('requests.get')  # Mock the requests.get function
    def test_get_messages(self, mock_get):
        # Mock the response from the requests.get call
        mock_get.return_value.status_code = 200

        response = self.app.get('/messages')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/plain')

    @patch('requests.put')  # Mock the requests.put function
    def test_set_init_state(self, mock_put):
        # Mock the response from the requests.put call
        mock_put.return_value.content = b"State updated to INIT"
        mock_put.return_value.status_code = 200

        response = self.app.put('/state', data='INIT')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"State updated to INIT")
        self.assertEqual(response.content_type, 'text/plain')
        mock_put.assert_called_once_with('http://service1:8001/state', data='INIT')

    @patch('requests.put')  # Mock the requests.put function
    def test_set_running_state(self, mock_put):

        mock_put.return_value.content = b"State updated to RUNNING"
        mock_put.return_value.status_code = 200

        response = self.app.put('/state', data='RUNNING')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"State updated to RUNNING")
        self.assertEqual(response.content_type, 'text/plain')
        mock_put.assert_called_once_with('http://service1:8001/state', data='RUNNING')

    @patch('requests.put')  # Mock the requests.put function
    def test_set_pause_state(self, mock_put):
        mock_put.return_value.content = b"State updated to PAUSE"
        mock_put.return_value.status_code = 200

        response = self.app.put('/state', data='PAUSE')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"State updated to PAUSE")
        self.assertEqual(response.content_type, 'text/plain')
        mock_put.assert_called_once_with('http://service1:8001/state', data='PAUSE')

    @patch('requests.put')  # Mock the requests.put function
    def test_set_shutdown_state(self, mock_put):
        mock_put.return_value.content = b"services stopped.."
        mock_put.return_value.status_code = 200

        response = self.app.put('/state', data='SHUTDOWN')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"services stopped..")
        self.assertEqual(response.content_type, 'text/plain')
        mock_put.assert_c


        called_once_with('http://service1:8001/state', data='SHUTDOWN')

    @patch('requests.put')  # Mock the requests.put function
    def test_set_fake_state(self, mock_put):
        mock_put.return_value.content = b"FAKE not found"
        mock_put.return_value.status_code = 200

        response = self.app.put('/state', data='FAKE')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"FAKE not found")
        self.assertEqual(response.content_type, 'text/plain')
        mock_put.assert_called_once_with('http://service1:8001/state', data='FAKE')

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
        mock_get.return_value.status_code = 200

        response = self.app.get('/run-log')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/plain')
        mock_get.assert_called_once_with('http://monitoring_service:8087/run-logs')
    @patch('requests.get')
    def test_get_mq_statistics(self, mock_get_rabbitmq_statistics):


        response = self.app.get('/mqstatistic')
        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()