import sys
import uuid
import copy
import stratus

from config import config
import proxy
import web
import api
import db

class service(stratus.stratus):
    """
    The launcher service for micropython
    """
    def __init__(self):
        super(service, self).__init__()
        self.service_name = "swarm"

    def launch(self, *args, **kwargs):
        print "Starting service..."
        launch(*args, **kwargs)
        return True

def launch(service_name):
    # Get the module the service is in
    if service_name == "swarm":
        module = sys.modules[__name__]
    else:
        module = getattr(sys.modules[__name__], service_name)
    # Get the service
    to_launch = getattr(module, "service")
    # Set the options
    options = copy.deepcopy(config)
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

def main():
    launch("swarm")
    client = stratus.client()
    client.connect(name="proxy_starter")
    # print client.connected()
    result = client.call("swarm", "launch", "proxy")
    print result()
    while True:
        pass
    return

if __name__ == '__main__':
    main()
