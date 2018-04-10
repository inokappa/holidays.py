import unittest
import mock
import requests
import holiday

class HolidayPyTest(unittest.TestCase):
   @mock.patch('requests.get')
   def test_get_holiday_csv(self, mock_get):
       res = requests.Response()
       res._content = ''
       mock_get.return_value = res
       self.assertEqual(holiday.getHolidayCsv(), '')

   def test_decode_content(self):
       self.assertEqual(holiday.decodeContent(b'\x82\xa0'), 'あ')

   def test_convert_json(self):
       content = '''国民の祝日・休日月日,国民の祝日・休日名称
2017-01-01,元日
2017-01-02,休日
2017-01-09,成人の日
2018-12-24,休日
2019-01-01,元日
2019-01-14,成人の日
'''
       data = {'2017-01-01': '元日',
               '2017-01-02': '振替休日',
               '2017-01-09': '成人の日',
               '2018-12-24': '振替休日',
               '2019-01-01': '元日',
               '2019-01-14': '成人の日'}
       self.assertEqual(holiday.convertJson(content), data)

   def test_put_object(self):



   def test_save_object(self):

