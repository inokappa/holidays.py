import os
import unittest
import json
import mock
from moto import mock_s3
import requests
import boto3
import holidays


class HolidaysPyTest(unittest.TestCase):
    @classmethod
    def setUp(self):
        os.environ["BUCKET_NAME"] = "holiday-py"

    @mock.patch('requests.get')
    def test_get_holiday_csv(self, mock_get):
        res = requests.Response()
        res.status_code = 200
        res._content = ''
        mock_get.return_value = res
        self.assertEqual(holidays.getHolidayCsv(), '')

    def test_decode_content(self):
        self.assertEqual(holidays.decodeContent(b'\x82\xa0'), 'あ')

    def test_convert_dict(self):
        contents = '''国民の祝日・休日月日,国民の祝日・休日名称
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
        self.assertEqual(holidays.convertDict(contents), data)

    def test_get_years(self):
        contents = {'2017-01-01': '元日',
                    '2017-01-02': '振替休日',
                    '2017-01-09': '成人の日',
                    '2018-12-24': '振替休日',
                    '2019-01-01': '元日',
                    '2019-01-14': '成人の日'}
        data = ['2017', '2018', '2019']
        self.assertListEqual(sorted(holidays.getYears(contents)), data)

    @mock_s3
    def test_save_years_data(self):
        s3 = boto3.resource('s3', region_name='ap-northeast-1')
        s3.create_bucket(Bucket=os.getenv('BUCKET_NAME'))

        contents = {'2017-01-01': '元日',
                    '2018-12-24': '振替休日',
                    '2019-01-14': '成人の日'}
        holidays.saveYearsData(contents)

        data = '{"2017-01-01": "元日"}'
        body = s3.Object('holiday-py', '2017/data.json').get()['Body'].read().decode("utf-8")
        self.assertEqual(body, data)

        data = '{"2018-12-24": "振替休日"}'
        body = s3.Object('holiday-py', '2018/data.json').get()['Body'].read().decode("utf-8")
        self.assertEqual(body, data)

        data = '{"2019-01-14": "成人の日"}'
        body = s3.Object('holiday-py', '2019/data.json').get()['Body'].read().decode("utf-8")
        self.assertEqual(body, data)

    @mock_s3
    def test_save_all_data(self):
        s3 = boto3.resource('s3', region_name='ap-northeast-1')
        s3.create_bucket(Bucket=os.getenv('BUCKET_NAME'))

        contents = {'2017-01-01': '元日',
                    '2018-12-24': '振替休日',
                    '2019-01-14': '成人の日'}
        holidays.saveAllData(contents)

        data = '{"2017-01-01": "元日", "2018-12-24": "振替休日", "2019-01-14": "成人の日"}'
        body = s3.Object('holiday-py', 'data.json').get()['Body'].read().decode("utf-8")
        sorted_body = {}
        for k, v in sorted(json.loads(body).items(), key=lambda x: x[0]):
            sorted_body[k] = v

        self.assertDictEqual(sorted_body, json.loads(data))

    @mock_s3
    def test_put_object(self):
        s3 = boto3.resource('s3', region_name='ap-northeast-1')
        s3.create_bucket(Bucket=os.getenv('BUCKET_NAME'))

        contents = {'2017-01-01': '元日',
                    '2018-12-24': '振替休日',
                    '2019-01-14': '成人の日'}
        holidays.putObject(json.dumps(contents), 'data.json')

        data = '{"2017-01-01": "元日", "2018-12-24": "振替休日", "2019-01-14": "成人の日"}'
        body = s3.Object('holiday-py', 'data.json').get()['Body'].read().decode("utf-8")
        sorted_body = {}
        for k, v in sorted(json.loads(body).items(), key=lambda x: x[0]):
            sorted_body[k] = v

        self.assertDictEqual(sorted_body, json.loads(data))
