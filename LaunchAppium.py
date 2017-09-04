import subprocess
import threading
import sys
import os
import urllib2
import json
import shlex
import time
import argparse

from processInfo import ProcessInfo


class LaunchAppium(object):
    def __init__(self):
        """
        Utility to Launch Appium Services. Useful for QA automation
            -- To Start/Stop Appium services
            -- To get Appium services status
        """
        if sys.platform == "win32":
            self.nodejs = r'C:\\PROGRA~2\\Appium\\node.exe'
            self.appium = r"C:\\PROGRA~2\\Appium\\node_modules\\appium\\bin" \
                          r"\\Appium.js"
            self.arguments = "--address 127.0.0.1 --port 4723 --no-reset"
            self.node_service = "node.exe"
        else:
            raise ValueError("Unsupported Platform. Work Under Progress of "
                             "Darwin/Mac")

    @staticmethod
    def check_appium_service_http():
        """
        Method to check if appium service is running on machine or not.
        uses urllib2 library to open appium url and get response.
        :return: if appium service is running it returns Status and version
        of appium running, else it returns -1 and none
        """
        response = urllib2.urlopen('http://localhost:4723/wd/hub/status')
        headers = response.info()
        data = json.loads(response.read())
        build_details = data['value']
        return data['status'], str(build_details['build']['version'])

    def launch_appium_node_service(self):
        """
        Method to launch appium node service on
        windows/mac machine.
        :return: Return appium service process id
        """
        appium_required_js = [self.nodejs, self.appium]
        for bin in appium_required_js:
            if os.path.isfile(bin):
                print "System has {}  file ".format(bin)
            else:
                print "Please check appium installation"
                return False
        print "Launching Appium Service on Windows"

        cmd = """{} {} {}""".format(self.nodejs,
                                    self.appium,
                                    self.arguments)
        final_command = shlex.split(cmd)

        print final_command
        appiumservice = subprocess.Popen(final_command)

        return appiumservice

    def start_appium_as_thread(self):
        """
        Start appium service as a thread and this is the
        preferred way to start appium service.
        :return:
        """
        try:
            t = threading.Thread(
                target=self.launch_appium_node_service)

            t.start()
            # t.setDaemon(True)
            # t.join()
        except Exception as e:
            print "Unable to start Appium service: {} " \
                .format(e.message)

    def get_appium_process_id(self):
        """
        Returns the process id of the node service
        :return:
        """
        p = ProcessInfo()
        if sys.platform == "win32":
            print "windows: Got node Service : {}".format(p.get_process_id(
                self.node_service))
            return p.get_process_id(self.node_service)

    def stop_appium_service(self):
        """
        Stops the Appium i.e. node Service
        :return:
        """
        stop = ProcessInfo()
        if sys.platform == "win32":
            status = stop.stop_process_by_id(self.node_service)
            print "Appium stopped ?? :{}".format(status)


def parse_cmd_line():
    parser = argparse.ArgumentParser(description="Utility to start/stop "
                                                 "Appium for automation ")
    parser.add_argument("--option", action="store", required=True,
                        help="Options are start/stop/status. Usage: "
                             "launchAppium.py --Option start")
    user_args = parser.parse_args()
    return user_args


def main():
    arguments = parse_cmd_line()
    print arguments
    a = LaunchAppium()

    if arguments.option == 'start':
        a.start_appium_as_thread()
        time.sleep(25)
    elif arguments.option == 'stop':
        a.stop_appium_service()
    elif arguments.option == 'status':
        a.check_appium_service_http()
    else:
        raise ValueError("Invalid command line option")


if __name__ == "__main__":
    main()
