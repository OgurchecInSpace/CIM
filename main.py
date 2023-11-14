import os
import sqlite3

import constants  # Действительные теги для котиков
import threading
import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from gui.ui import Ui_Cim


# Класс для коммуникации, чтобы не путать функцию, на которую ведёт сигнал, и сам сигнал.
# Ну и просто для структурированности
class Communicate(QObject):
    # типы параметров сигнала указывают на типы параметров is_good, tag, text, cat_photo_path,
    # которые будут передаваться в дальнейшем
    process_request = pyqtSignal(bool, str, str, str)


# Ошибка, связанная с сайтом cataas.com
class CatAasError(Exception):
    pass


class Cim(QMainWindow, Ui_Cim):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        self.communicate = Communicate()
        self.communicate.process_request.connect(self.process_request)

        self.final_setupUi()
        self.cats_directory = ''
        self.db_file = ''
        self.current_cat = ''
        self.connection = None

        self.new_db_btn.clicked.connect(self.get_db_directory)
        self.exists_db_btn.clicked.connect(self.get_db_file)
        self.get_cat_btn.clicked.connect(self.get_cat)
        self.clear_db_btn.clicked.connect(self.clear_db)
        self.cat_table.clicked.connect(self.click_table)

    # Последние штрихи в создании UI, заполнении форм данными, установка иконки, стилей и т.д.
    def final_setupUi(self):
        self.db_status.setText('База данных не подключена')
        self.tags.addItems([''] + constants.real_tags)

        # какая-то штука, чтобы windows понял, что запускаемая программа - не python, и её нужно группировать отдельно
        # (выносить в другую группу иконок в панели задач снизу, а следовательно, и ставить ей другую иконку)
        import ctypes
        myappid = u'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # Иконка для приложения
        icon = QtGui.QIcon()
        icon.addFile('gui/icon.ico')
        self.setWindowIcon(icon)

        # Стили
        file = QtCore.QFile("gui/styles.qss")
        file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly | QtCore.QIODevice.OpenModeFlag.Text)
        stream = QtCore.QTextStream(file)
        self.setStyleSheet(stream.readAll())

    # Выбор уже имеющейся базы данных
    def get_db_file(self):
        file = QFileDialog.getOpenFileName(self, "Выберите базу данных", 'c:/', 'База данных (*.sqlite)')[0]
        if file.strip() == '':  # Если файл не выбран
            return

        self.prepare_open_db(file[:file.rindex('/')], file)

    # Выбор папки для новой базы данных
    def get_db_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Выберите папку для базы данных", 'c:/')
        if directory.strip() == '':  # Если директория не выбрана
            return

        full_path = f'{directory}/cats_db.sqlite'

        # Закрываем соединение, если оно было
        if self.connection is not None:
            self.connection.close()

        # Удаляем старый файл
        if os.path.exists(full_path):
            os.remove(full_path)

        # Создание пустого файла базы данных
        with open(full_path, 'xb'):
            pass

        self.prepare_open_db(directory, full_path, new_db=True)

    # Метод, подготавливающий работу с новой БД
    def prepare_open_db(self, directory, full_path, new_db=False):
        if not new_db:
            # Закрываем соединение, если оно было
            if self.connection is not None:
                self.connection.close()
        self.draw_cat('')  # Убираем рисунок кота

        self.db_file = full_path  # Назначаем новую базу данных

        new_directory = f'{directory}/cats'

        if not os.path.exists(new_directory):  # Если папки с котами нет - создаём таковую
            os.mkdir(new_directory)
        self.cats_directory = new_directory

        self.fill_db()  # Заполняем базу данных таблицами и тегами таблицу тегов, ведь их может там не быть
        self.db_status.setText(f'Подключено к: {full_path}')

    # Заполнение базы данных базовыми данными, которые понадобятся в будущем
    def fill_db(self):
        # Заполнение базы данных таблицами для котов и тегов
        self.connection = sqlite3.connect(self.db_file)
        cur = self.connection.cursor()
        try:
            # Создание таблички с тегами
            cur.execute("""CREATE TABLE tags (
                            id  INTEGER PRIMARY KEY AUTOINCREMENT
                                UNIQUE
                                NOT NULL,
                            tag INTEGER NOT NULL);""")

        except sqlite3.OperationalError:
            # Если таблица тегов есть, то идём дальше
            pass

        try:
            # Создание таблички с котиками
            cur.execute("""CREATE TABLE cats (
                               id   INTEGER PRIMARY KEY AUTOINCREMENT
                                    UNIQUE
                                    NOT NULL,
                               path TEXT    NOT NULL,
                               tag  INTEGER REFERENCES tags (id),
                               text TEXT);""")

        except sqlite3.OperationalError:
            # Аналогично таблице тегам
            pass

        # Очищаем таблицу с тегами и заполняем заново (верными данными), потому что там могут быть неприятные вещи,
        # которые могут мешать корректной работе в дальнейшем.
        cur.execute('DELETE FROM tags')
        self.connection.commit()

        # Заполнение базы с тегами собственно тегами
        sql_request = 'INSERT INTO tags(id, tag) VALUES '
        values = ', '.join([f"({tag_id}, '{tag}')" for tag_id, tag in enumerate(constants.real_tags, start=1)])
        sql_request += values
        try:
            cur.execute(sql_request)
            self.connection.commit()
        except sqlite3.OperationalError:
            # Я не знаю, может ли тут пойти что-то не так, но лучше перестраховаться
            pass
        self.visualize_db()
        cur.close()

    def get_cat(self):
        # Если база данных не подключена, то ничего делать не будем
        if not self.db_file:
            return

        text = self.text.text()
        tag = self.tags.currentText()

        # Собираем запрос (документация сервиса: https://cataas.com/doc.html)
        request = 'https://cataas.com/cat'
        if tag:
            request += f'/{tag}'

        if text:
            request += f'/says/{text}'

        cur = self.connection.cursor()
        # id последнего кота (нужен для названия файла)
        last_id = cur.execute('SELECT id FROM cats ORDER BY id DESC LIMIT 1').fetchone()
        cur.close()
        if last_id is None:  # Если так получилось, что котов ещё никто не сохранял, то берём id как 1
            last_id = 1
        else:
            last_id = last_id[0] + 1

        cat_photo_path = f'{self.cats_directory}/cat_{last_id}.jpg'
        # Запрос картинки, её скачивание, сохранение в БД и систему и реакция на теоретическую недоступность сервиса
        threading.Thread(target=self._get_cat, args=(request, tag, text, cat_photo_path)).start()

    # Чистка БД
    def clear_db(self):
        if self.connection is None:
            return
        cur = self.connection.cursor()
        cur.execute('DELETE FROM cats')
        self.connection.commit()
        cur.close()

        self.visualize_db()
        self.draw_cat('')

    # Отрисовка базы данных с котами (а также обновление её представления для пользователя)
    def visualize_db(self):
        # Полная очистка таблицы (мне лень отслеживать, что именно удаляется/добавляется/чистится и где,
        # поэтому я сделал так)
        self.cat_table.clear()
        self.cat_table.setRowCount(0)
        self.cat_table.setColumnCount(0)

        cur = self.connection.cursor()
        cats = cur.execute('SELECT * FROM cats').fetchall()
        cur.close()
        header = ['id', 'path', 'tag', 'text']  # Заголовок
        self.cat_table.setColumnCount(len(header))
        self.cat_table.setHorizontalHeaderLabels(header)
        # Постепенно заполняем таблицу котами
        if cats:
            for row, cat in enumerate(cats):
                self.cat_table.setRowCount(self.cat_table.rowCount() + 1)
                for column, part in enumerate(cat):
                    self.cat_table.setItem(row, column, QTableWidgetItem(str(part)))

    # Отрисовка кота
    def draw_cat(self, path):
        pixmap = QtGui.QPixmap(path)
        self.cat_image.setPixmap(pixmap)
        self.cat_image.show()
        self.cat_image.setScaledContents(True)
        self.resizeEvent(None)

    # Если на таблицу нажимают, то нужно отрисовать кота из того ряда, по которому нажали
    def click_table(self, item):
        path = self.cat_table.item(item.row(), 1).text()
        self.draw_cat(path)

    # Специально вынесенная функция, работающая в отдельном потоке.
    # Это сделано для того, чтобы вся программа не зависала,
    # пока идёт ожидание ответа от cataas.com, скачивание и сохранение фото
    def _get_cat(self, request, tag, text, cat_photo_path):
        try:
            cat_photo = requests.get(request)  # Получаем фото
            # Проверяем код ответа на то, что сервер работает и отвечает, а не как всегда
            if cat_photo.status_code in [408, 419, 504, 522, 524]:
                raise CatAasError
            cat_photo = cat_photo.content
            # сохраняем картиночку
            with open(cat_photo_path, 'wb') as file:
                file.write(cat_photo)
            self.communicate.process_request.emit(True, tag, text, cat_photo_path)
        except CatAasError:  # Сервер снова лежит или что-то
            self.communicate.process_request.emit(False, tag, text, cat_photo_path)

    # Обработка ответа на запрос изображения кота
    def process_request(self, is_good, tag, text, cat_photo_path):
        # Если всё хорошо
        if is_good:
            cur = self.connection.cursor()
            # Теперь надо положить в базу данных информацию о новом котике
            if tag != '':
                db_tag = constants.real_tags.index(tag) + 1  # id тега,
                # прибавление единицы из-за того, что в sql отсчёт id начинается с 1
            else:
                db_tag = ''
            sql_request = "INSERT INTO cats('path', 'tag', 'text') VALUES (?, ?, ?)"
            cur.execute(sql_request, (cat_photo_path, db_tag, text))
            self.connection.commit()
            self.draw_cat(cat_photo_path)
            self.visualize_db()
            cur.close()
        # Если сайт не работает
        else:
            # Уведомление об ошибке со стороны сервера
            message = QMessageBox(self)
            message.setText('Сервер сервиса cataas.com не доступен в данный момент, попробуйте позднее')
            message.setWindowTitle('Упс')
            message.show()

    def keyPressEvent(self, event):
        key = event.key()
        if key in [Qt.Key_Delete, Qt.Key_Backspace]:  # Если нажатие клавиши подразумевает удаление
            row = self.cat_table.currentRow()
            if row == -1:  # Если никакой ряд не выбран, то ничего не делаем
                return

            cat_id = int(self.cat_table.item(row, 0).text())  # id кота, на которого нажали
            cur = self.connection.cursor()
            cur.execute('DELETE FROM cats WHERE id=?', (cat_id,))
            self.connection.commit()
            cur.close()
            self.visualize_db()
            self.draw_cat('')

    def closeEvent(self, a0):
        # Если подключение было таки создано, то его надо закрыть при выключении программы
        if self.connection is not None:
            self.connection.close()

    def resizeEvent(self, a0):
        # Эти действия вроде как должны приводить к тому, что левая и правая части интерфейса будут +- равны,
        # но что-то не получается
        self.horizontalLayout.setStretchFactor(self.left_part, 1)
        self.horizontalLayout.setStretchFactor(self.right_part, 1)
        self.right_part.setStretchFactor(self.cat_image, 1)
        self.right_part.setStretchFactor(self.settings, 1)
        self.right_part.setStretchFactor(self.get_cat_btn, 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Cim()
    ex.show()
    sys.exit(app.exec())
