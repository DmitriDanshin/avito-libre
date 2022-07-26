from sys import platform

DRIVER_EXECUTABLE_PATH_LINUX = "web_drivers/chromedriver"
DRIVER_EXECUTABLE_PATH_WIN = "web_drivers/chromedriver.exe"


def get_driver_path():
    match platform:
        case 'linux':
            return DRIVER_EXECUTABLE_PATH_LINUX
        case 'win32':
            return DRIVER_EXECUTABLE_PATH_WIN
        case _:
            return None
