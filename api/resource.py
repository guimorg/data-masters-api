"""Resources for API"""
from pathlib import Path

from api import (
    routes,
    log
)

from api.config import MACHINE_LEARNING_OPTION as model_config


_logger = log.get_logger()


# Constants
SCHEMA_PATH = Path(model_config('schemas_path'))
SCHEMA_IN = SCHEMA_PATH / model_config('schema_in')
SCHEMA_OUT = SCHEMA_PATH / model_config('schema_out')


class Resource:
    """
    Resource that actually creates handler functions
    and add all routes to the API.
    """
    def __init__(self, add_route_fun, executor):
        _logger.debug(f'Initializing Resource object {self}')
        self.add_route_fun = add_route_fun
        # Intanciate Handler Object for Machine Learning
        self.machine_learning_object = routes.MachineLearning(
            schema_in=SCHEMA_IN,
            schema_out=SCHEMA_OUT,
            executor=executor,
        )
        self.healthcheck_object = routes.HealthCheck()
        # Register Routes
        self.register(
            endpoint='/v1/healthcheck',
            handler=self.healthcheck_object
        )
        self.register(
            endpoint='/v1/predict',
            handler=self.machine_learning_object
        )

    def register(self, endpoint, handler):
        """
        Register route to Application
        """
        _logger.debug(f'Adding route {endpoint} to API...')
        self.add_route_fun('*', endpoint, handler.dispatch)
