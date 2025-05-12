import json
# from types import SimpleNamespace
from botocore.exceptions import ClientError

import handler
import routes


def test_create_todo_success(mocker, put_event, dummy_context):
    # Spy on table.put_item to ensure it's called correctly
    spy = mocker.spy(routes.table, 'put_item')

    event = put_event({'title': 'Write tests'})
    response = handler.lambda_handler(event, dummy_context)

    # Validate HTTP response
    assert response['statusCode'] == 201
    body = json.loads(response['body'])
    assert body['id'] == 'fixed-uuid'
    assert body['title'] == 'Write tests'
    assert body['done'] is False
    assert 'created_at' in body

    # Validate DynamoDB interaction
    assert spy.called
    args, kwargs = spy.call_args
    assert kwargs['Item']['id'] == 'fixed-uuid'
    assert kwargs['Item']['title'] == 'Write tests'


def test_create_todo_validation_error(put_event, dummy_context):
    # Missing 'title' should trigger the Pydantic ValidationError → 422
    event = put_event({})
    response = handler.lambda_handler(event, dummy_context)

    assert response['statusCode'] == 422
    body = json.loads(response['body'])
    # Ensure Pydantic reported a missing 'title' field
    assert any(err['loc'] == ['title'] for err in body['errors'])


def test_create_todo_dynamodb_failure(mocker, put_event, dummy_context):
    # Arrange: patch put_item to raise a ClientError
    error_response = {
        'Error': {
            'Code': 'ProvisionedThroughputExceededException',
            'Message': 'Throughput exceeded'
        }
    }
    mocker.patch(
        'routes.table.put_item',
        side_effect=ClientError(error_response, 'PutItem')
    )

    event = put_event({'title': 'Write tests'})
    response = handler.lambda_handler(event, dummy_context)

    # Should be translated by your global ClientError handler → 503
    assert response['statusCode'] == 503
    body = json.loads(response['body'])
    assert 'Upstream service unavailable' in body['message']


# def test_get_todo_by_id(mocker, dummy_context):
#     event = {
#         "resource":           "/todos/{todo_id}",
#         "path":               "/todos/1234-uuid",
#         "httpMethod":         "GET",
#         "pathParameters":     {"todo_id": "1234-uuid"},
#         "body":               None,
#         "isBase64Encoded":    False,
#         "requestContext": {
#             "requestId":      "test-request-id",
#             "resourcePath":   "/todos/{todo_id}",
#             "httpMethod":     "GET",
#         },
#     }
#     expected_item = {
#         "id": "1234-uuid",
#         "title": "Test read",
#         "done": False,
#         "created_at": "2025-05-01T12:00:00Z",
#     }

#     mocker.patch(
#         "routes.table.get_item",
#         return_value={"Item": expected_item}
#     )

#     response = handler.lambda_handler(event, dummy_context)
#     print(response)

#     assert response['statusCode'] == 200


# def test_get_todo_not_found(mocker, dummy_context):
#     event = {
#         "resource":           "/todos/{todo_id}",
#         "path":               "/todos/1234-uuid",
#         "httpMethod":         "GET",
#         "pathParameters":     {"todo_id": "1234-uuid"},
#         "body":               None,
#         "isBase64Encoded":    False,
#         "requestContext": {
#             "requestId":      "test-request-id",
#             "resourcePath":   "/todos/{todo_id}",
#             "httpMethod":     "GET",
#         },
#     }

#     mocker.patch(
#         "routes.table.get_item",
#         return_value={}
#     )

#     response = handler.lambda_handler(event, dummy_context)

#     print(response)

#     assert response['statusCode'] == 404
#     body = json.loads(response['body'])
#     assert body['message'] == "Todo not found"
