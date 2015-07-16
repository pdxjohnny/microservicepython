import time
import thread
import stratus

from config import config

class service(stratus.stratus):
    """
    A swarm node that lets the swarm manger know
    how many requests it has processed
    """

    def __init__(self):
        super(service, self).__init__()
        self.requests_per_min = 0
        self.monitor = True
        thread.start_new_thread(self.monitor_requests, ())

    def monitor_requests(self):
        s_config = config["service"]
        self.running = True
        while self.running and self.monitor:
            time.sleep(s_config["time_between"])
            self.log("{} {} {}".format(self.name, self.service_name, self.requests_per_min))
            self.info({"requests": self.requests_per_min})
            if s_config["min_requests"] > self.requests_per_min:
                self.disconnect()
            elif s_config["max_requests"] < self.requests_per_min:
                self.call("swarm", "launch", self.service_name)
            self.requests_per_min = 0

    def call_method(self, data):
        if self.monitor:
            self.requests_per_min += 1
        return super(service, self).call_method(data)
