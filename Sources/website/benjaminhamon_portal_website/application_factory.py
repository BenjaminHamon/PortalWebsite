import logging
from typing import Callable, List

import flask
import jinja2
import werkzeug.exceptions

import benjaminhamon_portal_website
from benjaminhamon_portal_website.application import Application


main_logger = logging.getLogger("Website")
request_logger = logging.getLogger("Request")


def create_application() -> Application:
    title = "Benjamin Hamon's portal website"

    flask_application = flask.Flask("benjaminhamon_portal_website")
    application = Application(flask_application)

    configure(flask_application, title)
    register_handlers(flask_application, application)
    register_routes(flask_application, application)

    return application


def configure(application: flask.Flask, title: str) -> None:
    application.config["WEBSITE_TITLE"] = title
    application.config["WEBSITE_COPYRIGHT"] = benjaminhamon_portal_website.__copyright__
    application.config["WEBSITE_VERSION"] = benjaminhamon_portal_website.__version__
    application.config["WEBSITE_DATE"] = benjaminhamon_portal_website.__date__

    application.jinja_env.undefined = jinja2.StrictUndefined
    application.jinja_env.trim_blocks = True
    application.jinja_env.lstrip_blocks = True

    application.context_processor(lambda: { "url_for": versioned_url_for })


def register_handlers(flask_application: flask.Flask, application: Application) -> None:
    flask_application.log_exception = lambda exc_info: None
    flask_application.before_request(application.log_request)
    for exception in werkzeug.exceptions.default_exceptions.values():
        flask_application.register_error_handler(exception, application.handle_error)


def register_routes(flask_application: flask.Flask, application: Application) -> None:
    add_url_rule(flask_application, "/", [ "GET" ], application.home)


def add_url_rule(application: flask.Flask, path: str, methods: List[str], handler: Callable, **kwargs) -> None:
    endpoint = ".".join(handler.__module__.split(".")[1:]) + "." + handler.__name__
    application.add_url_rule(path, methods = methods, endpoint = endpoint, view_func = handler, **kwargs)


def versioned_url_for(endpoint: str, **values) -> str:
    if endpoint == "static":
        values["version"] = flask.current_app.config["WEBSITE_VERSION"]
    return flask.url_for(endpoint, **values)
