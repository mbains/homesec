# To change this template, choose Tools | Templates
# and open the template in the editor.

from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
import random

import cgi

class HttpCmdiface(Resource, object):
    def __init__(self, getcb = None, postcb = None):
        self.getcb = getcb
        self.postcb = postcb
        super(HttpCmdiface, self).__init__()


    def render_GET(self, request):
        response = ''
        if self.getcb is not None:
            response = self.getcb(request)
            
        return response
        
    def render_POST(self, request):
        response = ''
        if self.postcb is not None:
            response = self.postcb(request)

        return response
    
if __name__ == '__main__':
    root = Resource()
    root.putChild("/on", HttpCmdiface())
    root.putChild("/off", HttpCmdiface())
    factory = Site(root)
    reactor.listenTCP(8880, factory)
    reactor.run()