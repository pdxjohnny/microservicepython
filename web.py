import os
import thread
import threading
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SimpleHTTPServer import SimpleHTTPRequestHandler

import node
from config import config

class service(node.service):
    """
    The web service for micropython
    """

    def __init__(self):
        super(service, self).__init__()
        self.webserver = False
        self.start_webserver()

    def start_webserver(self):
        if not self.webserver:
            self.webserver = ThreadedHTTPServer(("", 0), Handler)
            thread.start_new_thread(self.webserver.serve_forever, ())
        return True


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

class Handler(SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        self.path = config["website"]["static"] + self.path
        SimpleHTTPRequestHandler.do_GET(self)
