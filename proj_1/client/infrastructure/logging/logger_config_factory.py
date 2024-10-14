from client.infrastructure.settings.settings import Settings
from structured_logging.configuration.logger_config import LoggerConfig
from structured_logging.logger_creation.logger_config_builder import LoggerConfigBuilder
from structured_logging.processors.null_processor import NullProcessor
from structured_logging.processors.timestamp_processor import TimestampProcessor

class LoggerConfigFactory:
    
    def create_logger_config(settings: Settings, builder: LoggerConfigBuilder) -> LoggerConfig:
        if settings.environment == 'production':
            builder.with_file_sink()  # Set the sink to console in production
            builder.add_processor(TimestampProcessor())  # Add timestamp processing in production
        elif settings.environment == 'development':
            builder.with_console_sink()  # Console sink in development
            builder.add_processor(NullProcessor())  # No special processing in development

        # Handle async settingss if required
        if settings.is_async:
            builder.as_async(settings.async_wait_delay_in_seconds)

        return builder

