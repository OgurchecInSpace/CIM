from PyQt5 import QtCore, QtWidgets


# В какой-то момент я понял, что нужно изменить интерфейс, но оказалось, что я уже удалил файл .ui.
# Так что пришлось дописывать всё руками
class Ui_Cim(object):
    def setupUi(self, Cim):
        Cim.setObjectName("Cim")
        Cim.resize(811, 593)
        self.centralwidget = QtWidgets.QWidget(Cim)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.left_part = QtWidgets.QVBoxLayout()
        self.left_part.setObjectName("left_part")

        # Верхняя часть левой половины интерфейса (дополнительный интерфейс взаимодействия с БД)
        self.db_additional_interface = QtWidgets.QHBoxLayout()
        self.db_additional_interface.setObjectName("db_additional_btns")

        # Кнопка очистки БД
        self.clear_db_btn = QtWidgets.QPushButton(self.centralwidget)
        self.clear_db_btn.setObjectName('clear_db_btn')
        self.db_additional_interface.addWidget(self.clear_db_btn)

        # Лейбл с информацией о статусе подключения базы данных
        self.db_status = QtWidgets.QLabel(self.centralwidget)
        self.db_status.setObjectName('db_status')
        self.db_additional_interface.addWidget(self.db_status)

        self.left_part.addLayout(self.db_additional_interface)

        self.cat_table = QtWidgets.QTableWidget(self.centralwidget)
        self.cat_table.setObjectName("cat_table")
        self.cat_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.left_part.addWidget(self.cat_table)

        self.db_btns = QtWidgets.QHBoxLayout()
        self.db_btns.setObjectName("db_btns")
        self.new_db_btn = QtWidgets.QPushButton(self.centralwidget)
        self.new_db_btn.setObjectName("new_db_btn")
        self.db_btns.addWidget(self.new_db_btn)
        self.exists_db_btn = QtWidgets.QPushButton(self.centralwidget)
        self.exists_db_btn.setObjectName("exists_db_btn")
        self.db_btns.addWidget(self.exists_db_btn)
        self.left_part.addLayout(self.db_btns)
        self.horizontalLayout.addLayout(self.left_part)
        self.right_part = QtWidgets.QVBoxLayout()
        self.right_part.setSpacing(7)
        self.right_part.setObjectName("right_part")

        self.cat_image = QtWidgets.QLabel(self.centralwidget)
        self.cat_image.setObjectName("cat_image")
        self.right_part.addWidget(self.cat_image)
        self.settings = QtWidgets.QHBoxLayout()
        self.settings.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.settings.setSpacing(11)
        self.settings.setObjectName("settings")
        self.tags = QtWidgets.QComboBox(self.centralwidget)
        self.tags.setObjectName("tags")
        self.settings.addWidget(self.tags)
        self.text = QtWidgets.QLineEdit(self.centralwidget)
        self.text.setObjectName("text")
        self.settings.addWidget(self.text)
        self.right_part.addLayout(self.settings)
        self.get_cat_btn = QtWidgets.QPushButton(self.centralwidget)
        self.get_cat_btn.setObjectName("get_cat_btn")
        self.right_part.addWidget(self.get_cat_btn)
        self.horizontalLayout.addLayout(self.right_part)
        Cim.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Cim)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 811, 26))
        self.menubar.setObjectName("menubar")
        Cim.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Cim)
        self.statusbar.setObjectName("statusbar")
        Cim.setStatusBar(self.statusbar)

        self.retranslateUi(Cim)
        QtCore.QMetaObject.connectSlotsByName(Cim)

        self.horizontalLayout.setStretchFactor(self.left_part, 1)
        self.horizontalLayout.setStretchFactor(self.right_part, 1)

    def retranslateUi(self, Cim):
        _translate = QtCore.QCoreApplication.translate
        Cim.setWindowTitle(_translate("Cim", "Cim"))
        self.new_db_btn.setText(_translate("Cim", "Новая БД"))
        self.exists_db_btn.setText(_translate("Cim", "Существующая БД"))
        self.cat_image.setText(_translate("Cim", "Кот"))
        self.text.setPlaceholderText(_translate("Cim", "Текст для кота"))
        self.get_cat_btn.setText(_translate("Cim", "Новый кот"))
        self.clear_db_btn.setText(_translate('Cim', 'Очистить БД'))
