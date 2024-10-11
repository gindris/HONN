from structured_logging.configuration.environment import Environment
from structured_logging.processors.abstract_processor import AbstractProcessor

class EnvironmentProcessor(AbstractProcessor):
    def __init__(self, environment: Environment):
        super().__init__()
        self.environment = environment

    def process(self, data: dict) -> dict:
        # Add the environment key to the log data
        data['environment'] = self.environment.value
        return data
