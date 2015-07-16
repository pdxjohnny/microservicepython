import thread
from twisted.internet import reactor
from twisted.web import proxy, server

import node
from config import config

class service(node.service):
    """
    The proxy service for micropython
    """

    def log(self, message):
        del message

    def __init__(self):
        super(service, self).__init__()
        # Never kill this process even if it gets no requests
        self.monitor = False
        thread.start_new_thread(self.start_reverse_proxy, ())

    def start_reverse_proxy(self):
        root = reverse_proxy(self)
        site = server.Site(root)
        reactor.listenTCP(config["proxy"]["port"], site)
        reactor.run(installSignalHandlers=0)

class reverse_proxy(proxy.ReverseProxyResource):
    def __init__(self, stratus_client):
        proxy.ReverseProxyResource.__init__(self, "", 0, "")
        self.stratus_client = stratus_client

    def getChild(self, path, request):
        # Send request to api
        if request.uri.startswith("/api"):
            result = self.stratus_client.call("api", node.HOST_AND_PORT).result()
        # Send request to web
        else:
            result = self.stratus_client.call("web", node.HOST_AND_PORT).result()
        host = result["host"]
        port = result["port"]
        result = proxy.ReverseProxyResource(host, port, "")
        return result.getChild(path, request)
