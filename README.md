# postSlackMyWeight

FitbitのAPIを使用してAWS lambdaを使ってSlackに通知を送れます（一日一回を想定）

# 動作環境

## 必要なもの

- AWS Lambda(このコードのデプロイ先です)
- Cloud Watch(Lambda functionを定期実行するために使います)
- Fitbit API
- AWS DynamoDB(アクセストークン、リフレッシュトークンを登録・更新するのに使います)

## ENV

CLIENT_ID・・・FitbitのClient ID
CLIENT_SECRET・・・FitbitのClient Sectet
SLACK_URL・・・POST先のSlackのURL

## DynamoDB

以下のテーブルと項目を使います。Fitbitの設定画面に書いてあるそれぞれの項目でレコードを作成してください。

テーブル名・・・fitbit_table
プライマリキー・・・client_id(String)

項目
- access_token(String)
- refresh_token(String)
