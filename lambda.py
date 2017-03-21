from __future__ import print_function

import boto3
import json

print('Loading function')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    '''
    Gets verification file from s3. TODO change the file once response is given
    '''
    #print("Received event: " + json.dumps(event, indent=2))
    s3 = boto3.resource('s3')
    response = s3.Bucket("archaeology-lookup").Object("newfile.txt").get()
    responsecontent = response['Body'].read().decode('utf-8')

    operations = {
        'GET': responsecontent
    }


    operation = event['httpMethod']
    if operation in operations:
        payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        return respond(None, operations[operation])
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
