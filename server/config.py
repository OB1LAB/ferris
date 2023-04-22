class Config(object):
    JWT_CSRF_METHODS = ["POST", "PUT", "PATCH", "DELETE"]
    CORS_ORIGINS = '*'
    PROPAGATE_EXCEPTIONS = True
