import os
import csv
import json
import requests
import boto3


def getHolidayCsv():
    '''祝日 csv データ内閣府より取得する
    '''
    try:
        res = requests.get('http://www8.cao.go.jp/chosei/shukujitsu/syukujitsu_kyujitsu.csv', timeout=3)
        res.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        sys.exit(1)

    return res.content


def decodeContent(content):
    '''取得した csv データをデコードする
    '''
    decoded_content = content.decode('shift_jis')
    return decoded_content


def convertDict(decoded_content):
    '''デコードした csv データを辞書型に変更する
    '''
    reader = csv.reader(decoded_content.splitlines(), delimiter=',')
    header = next(reader)
    data = {}
    for line in reader:
        if line[1] == '休日':
            line[1] = '振替休日'
        data[line[0]] = line[1]

    return data

    
def getYears(contents):
    '''辞書データから祝日・休日の「年」だけを取り出す
    '''
    years = []
    for k in contents.keys():
        years.append(k.split('-')[0])
    return list(set(years))


def putObject(contents, key):
    '''生成した JSON データを S3 バケットに put する
    '''
    session = boto3.session.Session()
    if os.getenv('ENVIRONMENT') == 'debug':
        s3 = session.client(service_name='s3', endpoint_url='http://127.0.0.1:5001/')
    else:
        s3 = session.client(service_name='s3')

    s3.put_object(ACL='private',
                  Body=contents,
                  Bucket=os.getenv('BUCKET_NAME'),
                  Key=key)


def saveYearsData(contents):
    '''年ごとの祝日・休日データを JSON データを保存する
    '''
    years = getYears(contents)

    for year in years:
        data = {}
        for k, v in contents.items():
            if year in k:
                data[k] = v

        putObject(json.dumps(data, ensure_ascii=False), '%s/data.json' % year)


def saveAllData(contents):
    '''全ての年の祝日・休日データを保存する
    '''
    # 全体のデータを保存
    putObject(json.dumps(contents, ensure_ascii=False), 'data.json')


def main():
    '''Main
    '''
    res = getHolidayCsv()
    decoded_content = decodeContent(res)
    contents = convertDict(decoded_content)
    saveYearsData(contents)
    saveAllData(contents)


if __name__ == '__main__':
    main()
