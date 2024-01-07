import threading
import time

class Periodic:
    def __init__(self, interval: float, func):
        self.interval = interval
        self.func = func

    def run(self):
        def exec():
            while True:
                self.func()
                time.sleep(self.interval)
    
        thread = threading.Thread(target=exec)
        thread.daemon = True
        thread.start()
    