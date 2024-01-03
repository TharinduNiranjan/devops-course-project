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

if __name__ == '__main__':
    unittest.main()