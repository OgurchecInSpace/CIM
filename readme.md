Это приложение - небольшой учебный проект для менеджмента фотографий котов, которые берутся с сайта cataas.com. Для начала нужно создать или выбрать существующую базу данных (программа сама подготовит БД к шерстянным испытаниям). Вы можете задавать изображениям кошек текст и/или специфичный тег, и изображение с заданными параметрами скачается и будет зафиксированно в БД. Вы можете просматривать вашу коллекцию с помощью изображения и удалять те, что не понравились.

При создании БД программа создаст папку cats в папке БД. То же самое верно и для существующей БД.


Написана под windows, корректно работает на 10 версии, другие проверены не были

Используется версия питона 3.11, т.к. cx_Freeze не дружит пока с версиями старше

Файлы и папки:
* gui - папка с gui-штуками
* * ui.py - дизайн приложения (виджеты и их настройка).
* * styles.qss - стили для приложения. К сожалению, они убирают анимации нажатия кнопок, а в ручную делать их лень
* plugins - папка, с которой связан небольшой неприятный нюанс: по какой-то причине PyQt не видит свои же плагины (корень питона\Lib\site-packages\PyQt5\Qt5\plugins), хранящиеся в виртуальной среде. Поэтому, для него нужно их (содержимое этой самой папки plugins) переложить в корень питона, от которого наследуется виртуальная среда. Для exe сборки ничего делать не надо, она автоматически всё собирает.
* constants.py - константы для программы, хранение которых в главном файле является неуместными
* main.py - основной файл, в котором всё и работает
* readme.md - вы его сейчас читаете
* requirements.txt - зависимости
* setup.py - файл, собирающий приложение в exe с помощью cx_Freeze (команда - python setup.py build)


Ссылка на сборку для windows: https://disk.yandex.ru/d/Xv-x39BW-NmSpA
