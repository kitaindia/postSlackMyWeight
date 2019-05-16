import json
import os
import boto3
import fitbit
import requests

class FitbitClient:
    def __init__(self):
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('fitbit_table')
        response = table.get_item(Key={'client_id': self.client_id})

        self.access_token = response['Item']['access_token']
        self.refresh_token = response['Item']['refresh_token']

        def refresh_call_back(token):

            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('fitbit_table')
            response = table.put_item(
                Item={
                    'client_id': self.client_id,
                    'access_token': token['access_token'],
                    'refresh_token': token['refresh_token'],
                }
            )

        self.client = fitbit.Fitbit(
            self.client_id,
            self.client_secret,
            access_token=self.access_token,
            refresh_token=self.refresh_token,
            refresh_cb=refresh_call_back,
            system='ja_JP'
        )

    def get_bodyweight(self):
      return self.client.get_bodyweight(period='7d')

def lambda_handler(event, context):
    response = FitbitClient().get_bodyweight()

    weight = response.get('weight')

    if weight:
        latest = weight[-1]
        msg = "{}の体重 {}kg".format(latest['date'], latest['weight'])

        if len(weight) > 1:
            before = weight[-2]
            diff = "({:+.1f}kg)".format(latest['weight'] - before['weight'])
            msg += diff


        payload = {
            "text": msg,
        }

        data = json.dumps(payload)

        print(payload)
        requests.post(os.getenv('SLACK_URL'), data)

    return {
        'statusCode': 200,
    }

