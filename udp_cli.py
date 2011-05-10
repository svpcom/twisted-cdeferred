#!env/bin/python

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, task

class Helloer(DatagramProtocol):

    def startProtocol(self):
        self.host = "10.3.2.174"
        self.port = 1234

        self.n = 0

        # self.transport.connect(host, port)
        print "sending to host %s port %d" % (self.host, self.port)
        self.transport.write("hello", (self.host, self.port))
        task.LoopingCall(self.pinger).start(1)

    def pinger(self):
        self.n += 1
        self.transport.write("%d\n" % self.n, (self.host, self.port))
        print "sent %d, transport %r" % (self.n, self.transport)

    def datagramReceived(self, data, (host, port)):
        print "received %r from %s:%d, transport %r" % (data, host, port, self.transport)

    # Possibly invoked if there is no server listening on the
    # address to which we are sending.
    def connectionRefused(self):
        print "No one listening, transport %r" % self.transport

# 0 means any port, we don't care in this case
reactor.listenUDP(0, Helloer())
reactor.run()

