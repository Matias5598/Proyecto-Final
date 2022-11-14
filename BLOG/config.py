class Config:
    SECRET_KEY = '3075293597833f5a764239540298ceffc4e1d07cbce93a213d13527db8913c9a'

class DevelopmentConfig(Config):
    DEBUG=True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'proyecto_final'

config = {
    'development': DevelopmentConfig
}