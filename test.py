from twisted.internet import reactor
from twisted.web import proxy, server

class LocalResource(proxy.ReverseProxyResource):
    def render(self, request):
        return "Hello World"

class LocalOrRemoteResource(proxy.ReverseProxyResource):
    def __init__(self, host, port, path):
        proxy.ReverseProxyResource.__init__(self, host, port, path)
        self.host = host
        self.port = port
        self.path = path

    def getChild(self, path, request):
        if request.uri.startswith("/api"):
            print "LocalResource"
            return LocalResource(self.host, self.port, self.path)
        else:
            result = proxy.ReverseProxyResource(self.host, self.port, self.path)
            return result.getChild(path, request)

root = LocalOrRemoteResource('raat.jf.intel.com', 80, '')
site = server.Site(root)
reactor.listenTCP(8080, site)
reactor.run()
