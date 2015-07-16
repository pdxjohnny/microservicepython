config = {
    "version": 0.1,
    "description": "Example of microservice application in python",
    # Options for services
    "service": {
        # Time between checking min_requests and max_requests
        "time_between": 10,
        # If a service falls below this many requests it should kill itself
        "min_requests": 5,
        # If a service goes above this many requests it should request a new
        # instance of itself should be started to help balence load
        "max_requests": 10,
    },
    # Proxy webserver options
    "proxy": {
        "port": 9000,
    },
    # Website options
    "website": {
        "static": "static",
        "index": "index.html",
    },
    # Swarm options
    "swarm": {
        "launch_wait": 0.05,
    },
    # Command line argument defaults
    "arg_defaults": {
        "daemon": True,
    },
}
