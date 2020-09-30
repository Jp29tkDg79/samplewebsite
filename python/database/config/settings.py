import configparser
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

class mysqlenv(object):

    def __init__(self):
        # import mysql.env
        dotenv_path = os.path.join(os.path.dirname(__file__), 'mysql.env')
        load_dotenv(dotenv_path)

        # settings
        self.__databasename = os.environ.get('MYSQL_DATABASE')
        self.__user = os.environ.get('MYSQL_USER')
        self.__password = os.environ.get('MYSQL_PASSWORD')

    @property
    def databasename(self):
        return self.__databasename

    @property
    def user(self):
        return self.__user

    @property
    def password(self):
        return self.__password

class configini(object):

    def __init__(self):

        # import config ini file
        config_ini = configparser.ConfigParser()
        config_ini.read(os.path.join(os.path.dirname(__file__), 'config.ini'), encoding='utf-8')
        # setting salt
        self.__salt = config_ini['PASSWORD']['salt']

    @property
    def Salt(self):
        return self.__salt
