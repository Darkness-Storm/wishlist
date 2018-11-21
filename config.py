import os
from PyQt5 import QtSql, QtWidgets


basedir = os.path.abspath(os.path.dirname(__file__))

def default_connection():
    connection = QtSql.QSqlDatabase.addDatabase('QMYSQL')
    connection.setHostName('localhost')
    connection.setDatabaseName('db_wishlist')
    connection.setUserName('user')
    connection.setPassword('wishlist!23')
    return connection


def sqlite_connection():
    connection = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    connection.setDatabaseName(os.path.join(basedir, 'sqlite.db'))
    return connection

def desktop_size():
    desktop = QtWidgets.QApplication.desktop()
    return desktop.availableGeometry()
