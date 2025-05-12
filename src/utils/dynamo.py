import boto3

dynamo = boto3.resource('dynamodb')


class DynamoClient():
    """
    Dynamo wrapper
    """
    def __init__(self):
        self.table = dynamo.Table('todo-items')
