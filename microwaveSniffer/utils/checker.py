import sys
import http.client as httplib
import wmi
from PyQt6.QtCore import QThread, pyqtSignal

class CheckerInit(QThread):
    internet_finished = pyqtSignal(bool)
    hardware_finished = pyqtSignal(bool)
    _is_running = True

    def __init__(self):
        super().__init__()
        self.internet_checker = InternetChecker()
        self.hardware_checker = HardwareChecker()
        self.internet_checker.finished.connect(self.internet_finished.emit)
        self.hardware_checker.finished.connect(self.hardware_finished.emit)

    def run(self):
        self.hardware_checker.start()
        while self._is_running:
            if not self.internet_checker.isRunning():
                self.internet_checker.start()
            self.sleep(5) 

    def stop(self):
        self._is_running = False
        if self.hardware_checker.isRunning():
            self.hardware_checker.terminate()  # hi??? Work Please
            self.hardware_checker.wait()
        if self.internet_checker.isRunning():
            self.internet_checker.terminate()  # PSTOP THREAD SOTP SOTPS TROPS STOP STOP
            self.internet_checker.wait()
        self.quit()

class HardwareChecker(QThread):
    finished = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.connected_devices = 0

    def run(self):
        self.c = wmi.WMI()
        initial_devices = self.c.Win32_USBControllerDevice()
        if initial_devices:
            self.connected_devices = len(initial_devices)
            self.finished.emit(True)

        
            try:
                hardware_creation = self.c.Win32_DeviceChangeEvent.watch_for(notification_type="Creation")
                if hardware_creation:
                    print("Creation detected")
                    self.connected_devices += 1
                    self.finished.emit(True)
            except wmi.x_wmi_timed_out:
                pass
            try:
                hardware_deletion = self.c.Win32_DeviceChangeEvent.watch_for(notification_type="Deletion")
                if hardware_deletion:
                    print(self.connected_devices)
                    self.connected_devices = max(0, self.connected_devices - 1)
                    self.finished.emit(self.connected_devices > 0)
            except wmi.x_wmi_timed_out:
                pass  # Handle timeout if necessary


class InternetChecker(QThread):
    finished = pyqtSignal(bool)

    def run(self):
        try:
            conn = httplib.HTTPSConnection("www.google.com", timeout=5)
            conn.request("HEAD", "/")
            response = conn.getresponse()
            conn.close()
            self.finished.emit(response.status == 200)
        except:
            self.finished.emit(False)
