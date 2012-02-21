import logging

from rpclib.application import Application
from rpclib.decorator import srpc
from rpclib.interface.wsdl import Wsdl11
from rpclib.protocol.soap import Soap11
from rpclib.service import ServiceBase
from rpclib.model.complex import Iterable
from rpclib.model.primitive import Integer
from rpclib.model.primitive import String
from rpclib.server.wsgi import WsgiApplication

class MessageService(ServiceBase):
    @srpc(String, Integer, _returns=Iterable(String))
    def send_message(name):
        yield 'Your message: %s' % name

if __name__=='__main__':
    try:
        from wsgiref.simple_server import make_server
    except ImportError:
        print "Error: example server code requires Python >= 2.5"

    logging.basicConfig(level=logging.INFO)
    logging.getLogger('rpclib.protocol.xml').setLevel(logging.DEBUG)

    application = Application([MessageService], 'kent.temporary.soap',
                interface=Wsdl11(), in_protocol=Soap11(), out_protocol=Soap11())

    server = make_server('127.0.0.1', 7789, WsgiApplication(application))

    print "listening to http://127.0.0.1:7789"
    print "wsdl is at: http://127.0.0.1:7789/?wsdl"

    server.serve_forever()