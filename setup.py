# Сборщик программы в исполняемый файл
from cx_Freeze import Executable, setup

executables = [Executable('main.py', base='Win32GUI', target_name='CIM', icon='gui/icon.ico')]

# Библиотеки и т.д., которые не надо ставить (тут, скорее всего, не все неиспользуемые ресурсы)
excludes = ['html', 'multiprocessing', 'unittest',
            'argparse', 'webbrowser',
            'decimal', 'audioop', 'csv', 'xml', 'html',
            'fractions', 'cmath', 'statistics', 'zlib', 'gzip',
            'tarfile', 'pydoc_data', 'multipoccessing',
            'lib2to3', 'concurrent']

# Библиотеки, которые надо в архив
zip_include_packages = ['collections', 'encodings', 'importlib', 'socket', 'threading', 'tkinter', 'PyQt5']

# Включаемые другие файлы
include_files = ['gui', 'readme.md', 'requirements.txt',
                 'plugins/assetimporters', 'plugins/audio',  # Здесь начинаются плагины PyQt
                 'plugins/bearer', 'plugins/generic',
                 'plugins/geometryloaders', 'plugins/geoservices', 'plugins/iconengines', 'plugins/imageformats',
                 'plugins/mediaservice', 'plugins/platforms', 'plugins/platformthemes',
                 'plugins/playlistformats', 'plugins/position', 'plugins/printsupport', 'plugins/renderers',
                 'plugins/sceneparsers', 'plugins/sensorgestures', 'plugins/sensors', 'plugins/sqldrivers',
                 'plugins/styles', 'plugins/texttospeech', 'plugins/webview']

# Настройки
options = {
    'build_exe': {
        'include_msvcr': True,  # Добавление файлов Microsoft Visual C++ Redistributable
        'excludes': excludes,  # Пакеты, которые НЕ нужно брать в сборку
        'zip_include_packages': zip_include_packages,  # Пакеты, которые нужно архивировать
        'include_files': include_files,  # Файлы, которые надо включать дополнительно
        'build_exe': 'build_windows'  # Папка для сборки
    }
}

setup(name='CIM',
      version='1.0.0',
      description='Bro, did you really think there is something here?',  # hehehe
      executables=executables,
      options=options)
