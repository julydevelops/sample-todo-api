import json

from pydantic import ValidationError
from botocore.exceptions import ClientError
from aws_lambda_powertools.event_handler.api_gateway import Response


class NotFoundError(Exception):
    """Raise when a requested Todo item doesn't exist."""
    pass


def handle_not_found_error(exc: NotFoundError) -> Response:
    print("Custom NotFoundError handler called:", str(exc))
    return Response(
        status_code=404,
        content_type='application/json',
        body=json.dumps({'statusCode': 404, 'message': str(exc)})
    )


def handle_validation_error(exc: ValidationError) -> Response:
    return Response(
        status_code=422,
        content_type='application/json',
        body=json.dumps({'errors': exc.errors()})
    )


def handle_dynamodb_error(exc: ClientError) -> Response:
    return Response(
        status_code=503,
        content_type='application/json',
        body=json.dumps({'message': 'Upstream service unavailable'})
    )
