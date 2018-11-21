from PyQt5 import QtWidgets

import config


class NetworkSetting(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super(NetworkSetting, self).__init__(*args, **kwargs)
        self.config = config.get_config()
        self.initUI()
        self.init_signals()

    def initUI(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.db_lay = QtWidgets.QHBoxLayout()
        self.db_lab = QtWidgets.QLabel('database name', parent=self)
        self.dbname = QtWidgets.QLineEdit(parent=self)
        self.dbname.setText(self.config['DEFAULT']['dbname'])
        self.db_lay.addWidget(self.db_lab)
        self.db_lay.addWidget(self.dbname)

        self.host_lay = QtWidgets.QHBoxLayout()
        self.host_lab = QtWidgets.QLabel('hostname', parent=self)
        self.hostname = QtWidgets.QLineEdit(parent=self)
        self.hostname.setText(self.config['DEFAULT']['hostname'])
        self.host_lay.addWidget(self.host_lab)
        self.host_lay.addWidget(self.hostname)

        self.port_lay = QtWidgets.QHBoxLayout()
        self.port_lab = QtWidgets.QLabel('port', parent=self)
        self.port = QtWidgets.QLineEdit(parent=self)
        self.port.setText(self.config['DEFAULT']['port'])
        self.port_lay.addWidget(self.port_lab)
        self.port_lay.addWidget(self.port)

        self.user_lay = QtWidgets.QHBoxLayout()
        self.user_lab = QtWidgets.QLabel('username', parent=self)
        self.username = QtWidgets.QLineEdit(parent=self)
        self.username.setText(self.config['DEFAULT']['username'])
        self.user_lay.addWidget(self.user_lab)
        self.user_lay.addWidget(self.username)

        self.pass_lay = QtWidgets.QHBoxLayout()
        self.pass_lab = QtWidgets.QLabel('password', parent=self)
        self.password = QtWidgets.QLineEdit(parent=self)
        self.password.setText(self.config['DEFAULT']['password'])
        self.pass_lay.addWidget(self.pass_lab)
        self.pass_lay.addWidget(self.password)

        self.btn_save = QtWidgets.QPushButton('Сохранить', parent=self)
        self.btn_close = QtWidgets.QPushButton('Закрыть', parent=self)
        self.spacer_bot = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.bottom_lay = QtWidgets.QHBoxLayout()
        self.bottom_lay.addSpacerItem(self.spacer_bot)
        self.bottom_lay.addWidget(self.btn_save)
        self.bottom_lay.addWidget(self.btn_close)

        self.main_layout.addLayout(self.host_lay)
        self.main_layout.addLayout(self.port_lay)
        self.main_layout.addLayout(self.db_lay)
        self.main_layout.addLayout(self.user_lay)
        self.main_layout.addLayout(self.pass_lay)
        self.main_layout.addLayout(self.bottom_lay)

    def init_signals(self):
        self.btn_save.clicked.connect(self.save)
        self.btn_close.clicked.connect(self.close)

    def save(self):
        hostname = self.hostname.text()
        port = self.port.text()
        dbname = self.dbname.text()
        username = self.username.text()
        password = self.password.text()
        config.add_in_config(hostname=hostname, port=port, dbname=dbname, username=username, password=password)
        QtWidgets.QMessageBox.information(self, 'Предупреждение', 'Необходим перезапуск программы')
        self.close()
