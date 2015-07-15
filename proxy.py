import stratus

from config import config

class service(stratus.stratus):
    """
    The proxy service for micropython
    """
    def __init__(self):
        super(service, self).__init__()
        self.start_webserver()

    def start_webserver(self):
        print "Starting webserver..."
        return True
