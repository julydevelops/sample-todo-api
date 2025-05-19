import boto3
import errors
import os
import uuid

from botocore.exceptions import ClientError
from datetime import datetime, timezone
from pydantic import ValidationError
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.api_gateway import (
    ApiGatewayResolver,
    Response,
)

from models import EventBody, Todo

app = ApiGatewayResolver()
logger = Logger(service='todo-api')

table_name = os.environ.get('TABLE_NAME', 'todo-items')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)


# Register exception handlers:
app.exception_handler(ValidationError)(errors.handle_validation_error)
app.exception_handler(ClientError)(errors.handle_dynamodb_error)
app.exception_handler(
    errors.NotFoundError
)(errors.handle_not_found_error)


@app.post('/todo')
def create_todo():
    body = EventBody(**app.current_event.json_body)

    logger.info("Event Received", 
                extra={"event_body": app.current_event.json_body})

    item = {
        'id': str(uuid.uuid4()),
        'title': body.title,
        'done': False,
        'created_at': datetime.now(timezone.utc).isoformat(),
    }

    table.put_item(Item=item)
    logger.info('Todo created', extra={'todo_id': item['id']})

    return Response(
        status_code=201,
        content_type='application/json',
        body=Todo(**item).model_dump_json()
    )


@app.get('/todo/{todo_id}')
def get_todo(todo_id):
    # todo_id = app.current_event.path_parameter['todo_id']

    response = table.get_item(Key={'id': todo_id})

    logger.info("Fetching todo", extra={"todo_id": todo_id})

    if not response.get('Item'):
        raise errors.NotFoundError("Todo not found")

    return Response(
        status_code=200,
        content_type='application/json',
        body=Todo(**response['Item']).model_dump_json()
    )
