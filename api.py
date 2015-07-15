import stratus

from config import config

class service(stratus.stratus):
    """
    The api service for micropython
    """

    def api(self, request):
        output = json.dumps(request['variables'])
        headers = self.create_header()
        headers["Content-Type"] = "application/json"
        return self.end_response(headers, output)
