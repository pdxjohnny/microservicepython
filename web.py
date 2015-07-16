import os

import node
from config import config

STATIC_DIR = os.path.dirname(os.path.realpath(__file__))
STATIC_DIR = os.path.join(STATIC_DIR, config["website"]["static"])
print STATIC_DIR

class service(node.service):
    """
    The web service for micropython
    """

    def page(self, request):
        if request["page"] == "/":
            page = config["website"]["index"]
        else:
            page = request["page"][1:]
        if page[-1] == "/":
            page += config["website"]["index"]
        serve_file = os.path.join(STATIC_DIR, page)
        output = "404 Not Found"
        try:
            serve_file = open(serve_file, "rb")
            output = ''.join([line.strip() for line in serve_file])
        except:
            pass
        # print output
        return output
