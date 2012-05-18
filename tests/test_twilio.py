import unittest
from mock import patch
from mock import Mock
import requests

from .context import app


class TwiMLTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def assertTwiML(self, response):
        self.assertTrue("<Response>" in response.data, "Did not find " \
                "<Response>: %s" % response.data)
        self.assertTrue("</Response>" in response.data, "Did not find " \
                "</Response>: %s" % response.data)
        self.assertEqual("200 OK", response.status)

    def sms(self, body, path='/sms', number='+15555555555'):
        params = {
            'SmsSid': 'SMtesting',
            'AccountSid': 'ACtesting',
            'From': number,
            'To': '+16666666666',
            'Body': body,
            'ApiVersion': '2010-04-01',
            'Direction': 'inbound'}
        return self.app.post(path, data=params)

    def call(self, path='/voice', number='+15555555555', digits=None):
        params = {
            'CallSid': 'CAtesting',
            'AccountSid': 'ACtesting',
            'From': number,
            'To': '+16666666666',
            'CallStatus': 'ringing',
            'ApiVersion': '2010-04-01',
            'Direction': 'inbound'}
        if digits:
            params['Digits'] = digits
        return self.app.post(path, data=params)


class ExampleTests(TwiMLTest):
    @patch.object(requests, 'get')
    def test_sms(self, mock_get):
        test_file = file('./tests/test_assets/good_quote.json')
        mock_response = Mock()
        mock_response.text = test_file.read()
        mock_response.status = 200
        mock_get.return_value = mock_response
        response = self.sms("Test")
        self.assertTwiML(response)
        self.assertTrue("<Sms" in response.data, "Did not receive Sms " \
                "verb, instead: %s" % response.data)
        self.assertTrue("Last Price" in response.data, "Did not receive " \
                "stock quote, instead: %s" % response.data)

    @patch.object(requests, 'get')
    def test_smsBad(self, mock_get):
        test_file = file('./tests/test_assets/bad_quote.json')
        mock_response = Mock()
        mock_response.text = test_file.read()
        mock_response.status = 200
        mock_get.return_value = mock_response
        response = self.sms("Test")
        self.assertTwiML(response)
        self.assertTrue("<Sms" in response.data, "Did not receive Sms " \
                "verb, instead: %s" % response.data)
        self.assertTrue("Try again shortly" in response.data, "Did not " \
                "receive error message, instead: %s" % response.data)

    @patch.object(requests, 'get')
    def test_call(self, mock_get):
        test_file = file('./tests/test_assets/good_quote.json')
        mock_response = Mock()
        mock_response.text = test_file.read()
        mock_response.status = 200
        mock_get.return_value = mock_response
        response = self.call()
        self.assertTwiML(response)
        self.assertTrue("<Say" in response.data, "Did not receive Say " \
                "verb, instead: %s" % response.data)
        self.assertTrue("Last Price" in response.data, "Did not receive " \
                "stock quote, instead: %s" % response.data)

    @patch.object(requests, 'get')
    def test_callBad(self, mock_get):
        test_file = file('./tests/test_assets/bad_quote.json')
        mock_response = Mock()
        mock_response.text = test_file.read()
        mock_response.status = 200
        mock_get.return_value = mock_response
        response = self.call()
        self.assertTwiML(response)
        self.assertTrue("<Say" in response.data, "Did not receive Say " \
                "verb, instead: %s" % response.data)
        self.assertTrue("Try again shortly" in response.data, "Did not " \
                "receive error message, instead: %s" % response.data)
