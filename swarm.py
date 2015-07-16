import sys
import uuid
import copy
import time
import json
import thread
import random
import stratus
import datetime

from config import config
import proxy
import web
import api
import db

class service(stratus.stratus):
    """
    The launcher service for micropython
    """

    def log(self, arg):
        del arg

    def _recv(self, sock):
        data = super(service, self)._recv(sock)
        # print "RECEVED", data
        return data

    def post_call(self, request):
        recv_data = self.form_data(request['data'])
        service_name = recv_data.get("service", True)
        # print service_name
        services = [node for node in self.clients \
            if "service" in self.clients[node] \
                and self.clients[node]["service"] == service_name]
        # print services
        if len(services) < 1:
            self.launch(service_name)
            time.sleep(config["swarm"]["launch_wait"])
        return super(service, self).post_call(request)

    def launch(self, *args, **kwargs):
        return launch(*args, **kwargs)

def launch(service_name, extra_options={}):
    print "Starting {}...".format(service_name)
    # Get the module the service is in
    if service_name == "swarm":
        module = sys.modules[__name__]
    else:
        module = getattr(sys.modules[__name__], service_name)
    # Get the service
    to_launch = getattr(module, "service")
    # Set the options
    options = copy.deepcopy(config["service"])
    options.update(extra_options)
    options.update({
        # Random name so all services dont connect with same hostname
        "name": str(uuid.uuid4()),
        # Specify the service
        "service": service_name
    })
    # Create the service
    to_launch = to_launch()
    # Start the service
    to_launch.connect(**options)
    return options
