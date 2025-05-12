import json
import pytest


class DummyContext:
    def __init__(self):
        self.aws_request_id = 'test-request-id'
        self.function_name = 'test_function'
        self.function_version = '$LATEST'
        self.invoked_function_arn = (
            'arn:aws:lambda:us-east-1:123456789012:function:test_function'
        )
        self.log_group_name = '/aws/lambda/test_function'
        self.log_stream_name = '2025/04/28/[$LATEST]abcdef1234567890'
        self.memory_limit_in_mb = '128'


@pytest.fixture
def put_event():
    def _event(body_dict):
        return {
            'httpMethod': 'POST',
            'path': '/todos',
            'body': json.dumps(body_dict),
        }
    return _event


@pytest.fixture(autouse=True)
def fix_uuid(mocker):
    mocker.patch('uuid.uuid4', return_value='fixed-uuid')


@pytest.fixture
def dummy_context():
    return DummyContext()
