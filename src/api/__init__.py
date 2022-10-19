import json

import azure.functions as func
import logging
from src.api import app as application

__version__ = "0.0.1"
logger = logging.getLogger(__name__)


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logger.info("Receiving request for main handler.")
    try:
        http_response = func.WsgiMiddleware(application.wsgi_app).handle(req, context)
        http_response.headers["x-function-invocationId"] = context.invocation_id
        http_response.headers["x-function-version"] = __version__
        return http_response
    except Exception as error:
        logger.exception(str(error))
        return func.HttpResponse(
            json.dumps({"message": str(error)}),
            mimetype="application/json",
            status_code=504
        )