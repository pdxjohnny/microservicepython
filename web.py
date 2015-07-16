import node
from config import config

class service(node.service):
    """
    The web service for micropython
    """

    def page(self, request):
        output = request["username"] + request["password"]
        return output
