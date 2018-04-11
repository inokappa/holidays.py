# holidays.py

## これなに

内閣府が提供する祝日・休日情報の csv を JSON フォーマットで生成して Amazon S3 のバケットに保存する Python スクリプトです.

## 使い方

1. S3 バケットを作成する
2. 各種モジュールをインストール
2. コマンドを実行する

```sh
pip install -r requirements.txt
BUCKET_NAME=holiday-jp python holidays.py
```

[moto](https://github.com/spulec/moto) を利用することで, moto\_server で S3 のモックサーバーを起動して,
 以下のように実行することで, モックサーバーに対してデータを送信することができます.

```sh
ENVIRONMENT=debug BUCKET_NAME=holiday-jp python holidays.py
```
