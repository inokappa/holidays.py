import os
import csv
import json
import requests
import boto3


def getHolidayCsv():
    res = requests.get('http://www8.cao.go.jp/chosei/shukujitsu/syukujitsu_kyujitsu.csv')
    return res.content


def decodeContent(content):
    decoded_content = content.decode('shift_jis')
    return decoded_content


def convertJson(decoded_content):
    reader = csv.reader(decoded_content.splitlines(), delimiter=',')
    header = next(reader)
    data = {}
    for line in reader:
        if line[1] == '休日':
            line[1] = '振替休日'
        data[line[0]] = line[1]

    return data
    

def putObject(contents, key):
    session = boto3.session.Session()
    if os.getenv('ENVIRONMENT') == 'debug':
        s3 = session.client(service_name='s3', endpoint_url='http://127.0.0.1:5000/')
    else:
        s3 = session.client(service_name='s3')
    s3.put_object(ACL='private', Body=contents, Bucket=os.getenv('BUCKET_NAME'), Key=key)


def saveObject(contents):
    o = json.loads(contents)
    years = []
    for k in o.keys():
        years.append(k.split('-')[0])

    for year in list(set(years)):
        data = {}
        for k, v in o.items():
            if year in k:
                data[k] = v

        putObject(json.dumps(data), '%s/data.json' % year)

    putObject(contents, 'data.json')


def main():
    res = getHolidayCsv()
    decoded_content = decodeContent(res)
    content = convertJson(decoded_content)
    saveObject(content)


if __name__ == '__main__':
    main()
