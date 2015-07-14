import sys
import uuid
import stratus

from config import config
import proxy
import web
import api
import db

def launch(service):
    # Get the service
    module = getattr(sys.modules[__name__], service)
    to_launch = getattr(module, "service")
    # Set the options
    options = {
        # Random name so all services dont connect with same hostname
        "name": str(uuid.uuid4()),
        # Specify the service
        "service": service
    }
    # Create the service
    to_launch = to_launch()
    # Start the service
    to_launch.start(**options)

def main():
    launch("proxy")
    while True:
        pass
    return

if __name__ == '__main__':
    main()
