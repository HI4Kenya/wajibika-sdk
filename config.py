# Configuration objects here
# Used to serve respective environments


class Config(object):
    """ Used as default environment """
    DEBUG=False
    # SQLALCHEMY_ECHO=False

class DevelopmentConfig(Config):
    """ Used as development environment """
    DEBUG=True
    EXPLAIN_TEMPLATE_LOADING=True
    # SQLALCHEMY_ECHO=True
    # Add more here
    # ...

class ProductionConfig(Config):
    """ Used as production environment """
    # Add more here
    # ...

class TestingConfig(Config):
    """ Used as environment for testing """
    DEBUG=True
    # Add more here
    # ...

app_config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig
}
