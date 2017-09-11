import time
from LaunchAppium import LaunchAppium

appium = LaunchAppium()


def start_appium():
    appium.start_appium_as_thread()
    time.sleep(10)


def get_appium_run_status():
    print appium.check_appium_service_http()


def stop_appium():
    appium.stop_appium_service()


if __name__ == '__main__':
    start_appium()
    get_appium_run_status()
    stop_appium()

