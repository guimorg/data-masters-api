"""Main file to run API - Configuration Happens Here"""
import asyncio

from aiohttp import web

from api import (
    resource,
    config,
    log,
    worker
)


_logger = log.get_logger()


async def init_app():
    """
    Initializes web application.
    Gets config file, init routes...
    """
    _app = web.Application(
        logger=_logger
    )
    _app['config'] = config.get_config()
    executor = await worker.init_workers(_app)
    init_routes(_app, executor)
    return _app


def init_routes(
    app,
    executor
):
    """
    Initializing Routes for Application.
    """
    add_route = app.router.add_route
    # Adding routes using simple Facade
    resource.Resource(add_route, executor)


def main():
    """
    Runs API.
    """
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())

    host = config.SERVER_OPTION("host")
    port = int(config.SERVER_OPTION("port"))

    # Access Log Format
    # %a: Remote IP-address
    # %r: First Line of Request
    # %s: Response status code
    # %b: Size of response in bytes, excluding HTTP headers
    # %Tf: The time taken to serve the request, in seconds
    access_log_format = "%a '%r' %s %b %Tf '%{Referrer}i' '%{User-Agent}i'"

    web.run_app(
        app,
        host=host,
        port=port,
        access_log=_logger,
        access_log_format=access_log_format
    )


if __name__ == "__main__":
    import warnings
    # Lots of warning due to Tensorflow
    # and Keras
    warnings.filterwarnings("ignore")
    main()
