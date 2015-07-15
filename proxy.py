import stratus
import SimpleHTTPSServer

from config import config

class service(stratus.stratus):
    """
    The proxy service for micropython
    """
    def __init__(self):
        super(service, self).__init__()
        self.webserver = False
        self.start_webserver()

    def start_webserver(self):
        print "Starting webserver..."
        if not self.webserver:
            self.webserver = webserver(self)
            self.webserver.start(**config["webserver"])
        return True

class webserver(SimpleHTTPSServer.handler):
    """
    Webserver to accept requests from the internet
    Requests are processed by self.stratus_client
    which automaticly distributes requests to services
    """
    def __init__(self, stratus_client):
        super(webserver, self).__init__()
        self.stratus_client = stratus_client
        self.actions = [
            ('post', '/api/:username', self.api, self.auth),
            ('get', '/api/:username', self.api, self.auth),
            ('get', '/:file', self.web, self.auth)
        ]

    def auth(self, request):
        del request["socket"]
        authorized, response = self.basic_auth(request)
        if not authorized:
            return response
        request["username"], request["password"] = response
        return True

    def web(self, request):
        page = self.stratus_client("web", "page", request)
        page = page.result()
        headers = self.create_header()
        return self.end_response(headers, page)

    def api(self, request):
        output = json.dumps(request['variables'])
        headers["Content-Type"] = "application/json"
        headers = self.create_header()
        return self.end_response(headers, output)
