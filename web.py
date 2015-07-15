import stratus

from config import config

class service(stratus.stratus):
    """
    The web service for micropython
    """

    def page(self, request):
        output = request["username"] + request["password"]
        return output
        # return res
