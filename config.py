import os
import configparser

from PyQt5 import QtSql, QtWidgets

basedir = os.path.abspath(os.path.dirname(__file__))

def default_connection():
    config = check_config()
    connection = QtSql.QSqlDatabase.addDatabase('QMYSQL')
    connection.setHostName(config['DEFAULT']['hostname'])
    connection.setPort(int(config['DEFAULT']['port']))
    connection.setDatabaseName(config['DEFAULT']['dbname'])
    connection.setUserName(config['DEFAULT']['username'])
    connection.setPassword(config['DEFAULT']['password'])
    return connection


def sqlite_connection():
    connection = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    connection.setDatabaseName(os.path.join(basedir, 'sqlite.db'))
    return connection

def desktop_size():
    desktop = QtWidgets.QApplication.desktop()
    return desktop.availableGeometry()


def check_config():
    if not os.path.exists(os.path.join(basedir, 'config.ini')):
        set_default_config()
    return get_config()


def set_default_config():
    config = configparser.ConfigParser()
    config['DEFAULT'] = {}
    config['DEFAULT']['hostname'] = 'localhost'
    config['DEFAULT']['port'] = '3306'
    config['DEFAULT']['dbname'] = ''
    config['DEFAULT']['username'] = ''
    config['DEFAULT']['password'] = ''
    write_ini_file(config)


def write_ini_file(config):
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def add_in_config(**kwargs):
    config = get_config()
    for key, value in kwargs.items():
        config['DEFAULT'][key] = value
    write_ini_file(config)
