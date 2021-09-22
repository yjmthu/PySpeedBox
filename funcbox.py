import os

def get_data_path() -> str:
    path = os.path.join(os.environ['APPDATA'], 'PySpeedBox')
    if not os.path.exists(path):
        os.mkdir(path)
    return path

def get_ini_path() -> str:
    return os.path.join(get_data_path(), "PySpeedBox.ini")
