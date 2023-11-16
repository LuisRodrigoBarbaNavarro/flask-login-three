# Class: DevelopmentConfig
class DevelopmentConfig():
    DEBUG = True
    SECRET_KEY = "qhrf$edjYTJ)*21nsThdK"
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "RodrigoBarba0608."
    MYSQL_DB = "store"

# Export
config = {"development": DevelopmentConfig}