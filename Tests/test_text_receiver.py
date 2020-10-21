import unittest
import json

import __app__.TextReceiver as tr


class TestTextReceiver(unittest.TestCase):

    def test_parse_body(self):

        sample_body = "ToCountry=US&ToState=CA&NumMedia=0&ToCity=NEWBURY+PARK&FromZip=95020&FromState=CA&SmsStatus=received&FromCity=GILROY&Body=Test%21+&FromCountry=US&To=%2B18055558984&ToZip=91360&NumSegments=1&ApiVersion=2010-04-01"
        actual = tr.parse_form_values(sample_body)

        expected = {
            'ToCountry': 'US',
            'ToState': 'CA',
            'NumMedia': '0',
            'ToCity': 'NEWBURY+PARK',
            'FromZip': '95020',
            'FromState': 'CA',
            'SmsStatus': 'received',
            'FromCity': 'GILROY',
            'Body': 'Test!+',
            'FromCountry': 'US',
            'To': '+18055558984',
            'ToZip': '91360',
            'NumSegments': '1',
            'ApiVersion': '2010-04-01'
        }
        
        self.assertEqual(expected, actual)

    def test_is_right_message(self):
        self.assertTrue(tr.is_right_message("SUBSCRIBE"))
        self.assertTrue(tr.is_right_message(" Subscribe Please!"))
        self.assertTrue(tr.is_right_message("subscribe "))
        self.assertTrue(tr.is_right_message("Subscribe+"))
        self.assertTrue(tr.is_right_message("Subscribe!"))
        self.assertFalse(tr.is_right_message("UNSUBSCRIBE!"))
        self.assertFalse(tr.is_right_message("stop"))
        self.assertFalse(tr.is_right_message("hello"))

