import sys
import uuid
import copy
import time
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

    def launch(self, *args, **kwargs):
        print "Starting service...", args[0]
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
    services = ["proxy", "db", "api", "web"]
    for name in services:
        result = client("swarm", "launch", name)()
        if result:
            print "Launched", name
        else:
            print "Failed to launch", name
    while True:
        time.sleep(300)
    return

if __name__ == '__main__':
    main()
