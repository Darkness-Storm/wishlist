from PyQt5 import QtWidgets, QtSql, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox

import config


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.con = config.default_connection()
        self.con.open()
        if self.con.isOpenError():
            QMessageBox.critical(self, 'Ошибка', 'Не удалось поключиться к базе данных!!! ' +
                                 self.con.lastError().text())
        else:
            self.check_table()
        self.set_default_pref()
        self.setCentralWidget(MainWidget(parent=self))
        self.add_menu()
        self.init_signals()

    def set_default_pref(self):
        self.setWindowTitle("Simple Wishlist")
        self.move(10, 10)
        rect = config.desktop_size()
        self.resize(rect.width()/2, rect.height()/2)

    def add_menu(self):
        self.about = QtWidgets.QAction('О программе', self)
        self.aboutQt = QtWidgets.QAction('О Qt', self)
        self.menu_reg = QtWidgets.QMenu('Справка')
        self.menu_reg.addAction(self.about)
        self.menu_reg.addAction(self.aboutQt)
        self.menuBar().addMenu(self.menu_reg)

    def init_signals(self):
        self.about.triggered.connect(self.view_about)
        self.aboutQt.triggered.connect(self.view_aboutQt)

    def view_about(self):
        str_about = '''Данная программа выполнена как тестовое задание
        для компании ООО "Виста"'''
        QMessageBox.about(self, 'О программе', str_about)

    def view_aboutQt(self):
        QMessageBox.aboutQt(self, 'About Qt')

    def check_table(self):
        if 'wishlist' not in self.con.tables():
            self.create_table()

    def create_table(self):
        user_select = QMessageBox.question(
            self,
            'Первоначальная настройка',
            "Отсутствуют необходимые для работы таблицы. Произвести первоначальную настройку? " +
            "(В случае отказа приложение не сможет нормально работать)",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        if user_select == QMessageBox.Yes:
            str_query = "CREATE TABLE wishlist (" \
                        "id int(10) unsigned NOT NULL auto_increment, " \
                        "name varchar(200), " \
                        "price DOUBLE, " \
                        "url TEXT, " \
                        "descr TEXT, " \
                        "PRIMARY KEY (id), " \
                        "FULLTEXT KEY ft1 (name,url,descr)" \
                        ") ENGINE=MyISAM DEFAULT CHARSET=utf8;"
            query = QtSql.QSqlQuery()
            result = query.exec(str_query)
            if result:
                QMessageBox.information(self, '', 'Настройка выполнена')
            else:
                print(query.lastError().text())
                print(query.lastQuery())
                QMessageBox.critical(self, 'Ошибка', 'Не удалось выполнить настройку!!! ' +
                                     query.lastError().text())


class MainWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.initUI()
        self.init_signals()
        self.set_param_tv()

    def initUI(self):
        self.main_lay = QtWidgets.QVBoxLayout(self)
        # search panel layout
        self.search_lay = QtWidgets.QHBoxLayout()
        self.str_search = QtWidgets.QLineEdit(self)
        self.btn_search = QtWidgets.QPushButton('поиск', self)
        self.btn_x = QtWidgets.QPushButton('X', self)
        self.search_lay.addWidget(self.str_search)
        self.search_lay.addWidget(self.btn_search)
        self.search_lay.addWidget(self.btn_x)
        # command panel layout
        self.cp_lay = QtWidgets.QHBoxLayout()
        self.btn_add = QtWidgets.QPushButton('Новая запись', parent=self)
        self.btn_del = QtWidgets.QPushButton('Удалить запись', parent=self)
        self.btn_url = QtWidgets.QPushButton('Открыть адрес', parent=self)
        self.spacer_cp = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.cp_lay.addWidget(self.btn_add)
        self.cp_lay.addWidget(self.btn_del)
        self.cp_lay.addWidget(self.btn_url)
        self.cp_lay.addSpacerItem(self.spacer_cp)

        self.tbl_lay = QtWidgets.QHBoxLayout()
        self.tv = QtWidgets.QTableView(self)
        self.tbl_lay.addWidget(self.tv)

        self.bot_lay = QtWidgets.QHBoxLayout()
        self.btn_close = QtWidgets.QPushButton('Выход', parent=self)
        self.btn_submit = QtWidgets.QPushButton('Записать', parent=self)
        spacer_bot = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.bot_lay.addSpacerItem(spacer_bot)
        self.bot_lay.addWidget(self.btn_submit)
        self.bot_lay.addWidget(self.btn_close)

        self.main_lay.addLayout(self.search_lay)
        self.main_lay.addLayout(self.cp_lay)
        self.main_lay.addLayout(self.tbl_lay)
        self.main_lay.addLayout(self.bot_lay)
        self.setLayout(self.main_lay)

    def init_signals(self):
        self.btn_add.clicked.connect(self.new_rec)
        self.btn_del.clicked.connect(self.del_rec)
        self.btn_close.clicked.connect(self.close)
        self.btn_search.clicked.connect(self.search)
        self.btn_url.clicked.connect(self.open_url)
        self.btn_submit.clicked.connect(self.save)
        self.btn_x.clicked.connect(self.del_filter)

    def search(self):
        if self.tv.model().isDirty():
            user_select = QMessageBox.question(
                self,
                'Сохранение записей',
                "Имеются не сохраненные записи. Хотите сохранить? " +
                "(Save-сохранить, Discard-без сохранения)",
                QMessageBox.Save | QMessageBox.Discard ,
                QMessageBox.Save
            )
            if user_select == QMessageBox.Save:
                self.tv.model().submitAll()
        self.tv.model().full_search(self.str_search.text())

    def del_filter(self):
        self.str_search.setText('')
        self.tv.model().full_search(self.str_search.text())

    def open_url(self):
        index = self.tv.currentIndex()
        url_in_db = self.tv.model().get_url(index)
        url = QtCore.QUrl(url_in_db)
        QtGui.QDesktopServices.openUrl(url)

    def save(self):
        self.tv.model().submitAll()
        self.tv.model().select()

    def new_rec(self):
        last_index = self.tv.model().rowCount()
        self.tv.model().insertRow(last_index)

    def del_rec(self):
        user_select = QMessageBox.question(
            self,
            'Удаление записи',
            "Вы действительно хотите удалить запись?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if user_select == QMessageBox.Yes:
            index = self.tv.currentIndex()
            self.tv.model().removeRow(index.row())
            self.save()

    def set_param_tv(self):
        self.tv.setModel(TableWishListModel(parent=self))
        self.tv.setSelectionMode(1)
        self.tv.setSelectionBehavior(1)
        self.tv.hideColumn(0)
        self.tv.verticalHeader().hide()
        width = self.parent().size().width()
        self.tv.setColumnWidth(1, width*0.2)
        self.tv.setColumnWidth(2, width*0.1)
        self.tv.setColumnWidth(3, width*0.35)
        self.tv.setColumnWidth(4, width*0.33)

    def closeEvent(self, event):
        if self.tv.model().isDirty():
            user_select = QMessageBox.question(
                self,
                'Выход',
                "Хотите сохранить запись? " +
                "(Save-сохранить, Discard-без сохранения, cancel-не закрывать)",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Cancel
            )
            if user_select == QMessageBox.Save:
                self.save()
                event.accept()
                self.parent().close()
            if user_select == QMessageBox.Discard:
                event.accept()
                self.parent().close()
            if user_select == QMessageBox.Cancel:
                event.ignore()
        else:
            event.accept()
            self.parent().close()


class TableWishListModel(QtSql.QSqlTableModel):

    def __init__(self, *args, **kwargs):
        QtSql.QSqlTableModel.__init__(self, *args, **kwargs)
        self.setTable('wishlist')
        self.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.setHeaderData(1, QtCore.Qt.Horizontal, 'Наименование')
        self.setHeaderData(2, QtCore.Qt.Horizontal, 'Цена')
        self.setHeaderData(3, QtCore.Qt.Horizontal, 'URL-адрес')
        self.setHeaderData(4, QtCore.Qt.Horizontal, 'Описание')
        self.select()

    def full_search(self, str_search):
        if str_search:
            self.setFilter("MATCH (name, url, descr) AGAINST ('" + str(str_search) + "' IN BOOLEAN MODE);")
        else:
            self.setFilter('')

        self.select()

    def get_id_record(self, index):
        return self.record(index.row()).value('id')

    def get_url(self, index):
        return self.record(index.row()).value('url')

