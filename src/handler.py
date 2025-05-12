from routes import app, logger


@logger.inject_lambda_context
def lambda_handler(event, context):
    return app.resolve(event, context)
