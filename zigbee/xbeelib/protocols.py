# To change this template, choose Tools | Templates
# and open the template in the editor.
from httpCmdiface           import HttpCmdiface
from twisted.web.resource   import Resource
from twisted.web.server     import Site

from scapy.fields import ShortField, XByteField, ByteField, XLongField, XShortField, LEShortField, StrFixedLenField, ByteEnumField, ConditionalField
from scapy.packet import bind_layers

from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.python.util import println
from twisted.internet.serialport import  SerialPort
import sys
from twisted.python import log
from array import array
from scapy.all import Packet, Raw
from emailer import Emailer


FRAME_TYPES = {
    'XBeeIOFrame':          0x92,
    'ATCommand':            0x08,
    'ATCommandResponse':    0x88,
    'RemoteATCommand':      0x17,
    'ZigbeeRxPacket':       0x90,
    'ZigbeeTxPacket':       0x10
}

def checksum8(load):
    sum = 0
    for bite in load:
        sum += ord(bite)

    return chr(0xff - (sum&0xff))

def flatten(*lists_in):
    flat_list = []
    for list_item in lists_in:
        flat_list.extend(list_item)

    return flat_list

long_short_address = [  XLongField("long_source", 0xFFFF),
                        XShortField("short_source", 0xFFFE)]

class XBeeOuter(Packet):
    name = "XBeeOuter"
    fields_desc = [ XByteField("start_delimit", 0x7E),
                    ShortField("length", 0),
                    XByteField("frame_type", 0)
                    ]

    def build(self):
        self.length = len(self.payload) + 1 #length of payload + 1 byte for frame_type
        return super(XBeeOuter, self).build()

    def post_build(self, pkt, pay):
        innerLoad = pkt[3:] + pay
        self.setfieldval('length', len(innerLoad))
        #print "length = ", self.length
        ck = checksum8(innerLoad)
        #print "checksum = ", hex(ord(ck))
        return pkt+pay+ck

    def xbee_checksum(self):
        return self.build()[-1]

class XBeeIOFrame(Packet):
    name = "XBeeIOFrame",
    fields_desc = flatten(
                    long_short_address,
                    [
                        ByteField("recv_options", 0),
                        ByteField("num_samples", 1),
                        ShortField("digital_mask", 0),
                        ByteField("analog_mask", 0),
                        ShortField("digital_sample", 0),
                        ShortField("analog_sample", 0)
                    ]
                )

class ATCommand(Packet):
    name = "ATCommand"
    fields_desc = [ ByteField("frame_id", 0),
                    StrFixedLenField("AT_command", "NJ", 2),
                   ]


class ATCommandResponse(Packet):
    name = "ATCommandResponse"
    fields_desc = [ ByteField("frame_id", 0),
                    StrFixedLenField("AT_command", "NJ", 2),
                    ByteEnumField("command_status", 0, {0: "OK", 1: "ERROR", 2: "Invalid Command", 3: "Invalid parameter", 4: "Tx Failure"}),
                    #ByteField("CommandData", 0) #this param is optional. not returned on SET
                    ]

class ZigbeeRxPacket(Packet):
    name = "ZigbeeReceivePacket"
    fields_desc = flatten(  
                            long_short_address,
                            [
                                XByteField("recv_options", 1),
                                #ByteField("received_data", 0) #data from device, payload
                            ]

                    )

class ZigbeeTxPacket(Packet):
    name = "ZigbeeReceivePacket"
    fields_desc = flatten(
                            [ByteField("frame_id", 0)],
                            long_short_address,
                            [
                                XByteField("broadcast_radius", 0),
                                XByteField("options", 0),
                                #ByteField("TXData", 0) #data from device, payload
                            ]

                    )


class RemoteATCommand(Packet):
    name = "RemoteATCommand"
    fields_desc = flatten( [ByteField("frame_id", 0)],
                            long_short_address,
                            [
                                XByteField("remote_cmd_options", 0),
                                StrFixedLenField("AT_command", "NJ", 2),
                                #ConditionalField(XByteField("command_parameter", 0), None)
                            ]
                            )


class RemoteATCommandResponse(Packet):
    name = "RemoteATCommandResponse"
    fields_desc = flatten( [ByteField("frame_id", 0)],
                           long_short_address,
                           [
                               StrFixedLenField("AT_command", "NJ", 2),
                               ByteEnumField("command_status", 0, {0: "OK", 1: "ERROR", 2: "Invalid Command", 3: "Invalid parameter", 4: "Tx Failure"}),
                           ])




bind_layers(XBeeOuter, XBeeIOFrame,         {'frame_type': FRAME_TYPES['XBeeIOFrame']})
bind_layers(XBeeOuter, ATCommand,           {'frame_type': FRAME_TYPES['ATCommand']})
bind_layers(XBeeOuter, ATCommandResponse,   {'frame_type': FRAME_TYPES['ATCommandResponse']})
bind_layers(XBeeOuter, RemoteATCommand,     {'frame_type': FRAME_TYPES['RemoteATCommand']})
bind_layers(XBeeOuter, ZigbeeRxPacket,      {'frame_type': FRAME_TYPES['ZigbeeRxPacket']})
bind_layers(XBeeOuter, ZigbeeTxPacket,      {'frame_type': FRAME_TYPES['ZigbeeTxPacket']})

class XBEEProtocol(Protocol, object):
    """ Twisted Protocol class for handling telnet data as client"""
    STATE_DELIMIT   = 0
    STATE_LENGTH    = 1
    STATE_FINISHED  = 2

    def __init__(self, name, incomingMethod=None, *args, **kwargs):
        self.name = name
        self.state = self.STATE_FINISHED
        self.incoming = incomingMethod
        log.msg("New Protocol: " + name)
        self.data_sofar = None
        self.pkt_len = None
        super(XBEEProtocol, self).__init__(*args, **kwargs)

    def connectionMade(self):
        log.msg("LoggerProtocol Connected!")

        self.count = 1

        self.loopcount = 0

        def schedule():
            reactor.callLater(1, sendMore)
        #pkt = XBeeOuter()/ATCommand(frame_id=1, AT_command="ID")

        def sendMore():
            #relay_binary = bin( (16-self.count) % 16)[2:].zfill(4)
            relay_binary = ';1111'
            print "message = %s Log = " % (relay_binary), ["on" if x == '0'  else "off" for x in relay_binary]
            pkt = XBeeOuter()/ZigbeeTxPacket(frame_id=self.count, long_source=0x13a20040625962)/Raw(relay_binary)
            self.send(pkt.build())
            if (self.loopcount % 5) == 0:
                self.count+=1
            self.loopcount += 1
            #schedule()

        schedule()
        #reactor.callLater(3, sendMore)

    def lightsOn(self, request):
        self.zigbeeTx(';'+'0'*4, 0x13a20040625962)
        return 'Lights On'

    def lightsOff(self, request):
        self.zigbeeTx(';' + '1'*4, 0x13a20040625962)
        return 'Lights off'

    def zigbeeTx(self, data, long_src):
        self.count += 1
        pkt = XBeeOuter()/ZigbeeTxPacket(frame_id=self.count, long_source=long_src)/Raw(data)
        self.send(pkt.build())

    def connectionLost(self, reason):
        print "LoggerProtocol Disconnected: ", reason

    def dataReceived(self, data):
        """
        Send data received to registered handler
        """

        for byte in data:

            if (self.state == self.STATE_FINISHED) and (ord(byte) == 0x7e):
                self.state = self.STATE_DELIMIT
                if self.data_sofar is not None:
                    #print "starting next command, len of previous data = ", len(self.data_sofar)
                    pass
                    #if there is already data in the queue, emit it
                    #self.incoming(self, self.data_sofar)

                self.data_sofar = array('c')
                self.data_sofar.append(byte)
            
            elif self.state != self.STATE_FINISHED:
                self.data_sofar.append(byte)
                if len(self.data_sofar) == 3: #parse outer to get length
                    pkt = XBeeOuter(self.data_sofar.tostring())
                    self.pkt_len = pkt.length + 4 # 3 for preamble  and 1 for checksum
                    self.state = self.STATE_LENGTH
                    #print "expected pkt len = ", self.pkt_len

                if (self.state == self.STATE_LENGTH) and (len(self.data_sofar) == self.pkt_len):
                    self.state = self.STATE_FINISHED

                    csum = self.data_sofar[-1]
                    pkt_sans_csum = self.data_sofar[:-1].tostring()
                    pkt = XBeeOuter(pkt_sans_csum)
                    if pkt.xbee_checksum() == csum:
                        self.incoming(self, pkt_sans_csum)
                    else:
                        print "Check sum failed"
                        pkt.show()



        
        #print "Client (%s) got data (%r):" % (self.name, (data))

    def setIncoming(self, method):
        self.incoming = method

    def send(self, data):
        return self.transport.write(data)




if __name__ == "__main__":
    """ protocols.py 2, send email """
    """ protocols.py 1, show frame """
    """ protocols.py, print analog message """
    from time import strftime
    from datetime import datetime
    from pkt_processor import Pkt_Processor



    if sys.argv[-1] == '2':
        emailer = Emailer()
    else:
        emailer = None

    sensors = {}
    sensors[0x13A20040625934] = Pkt_Processor("garage", emailer)
    sensors[0x13a20040625962] = Pkt_Processor("outside", emailer)
    def m(proto, data):
        try:
            frame = XBeeOuter(data)
            if sys.argv[-1] == '1':
                frame.show()
            
            the_long_source = getattr(frame, 'long_source', None)
            if the_long_source is not None:
                thesensor = sensors.get(frame.long_source)

            if the_long_source is not None and thesensor is not None:
                thesensor.handle_message(frame)
            else:
                for sensor in sensors:
                    sensors[sensor].handle_error(frame)

#            else:
#                lumiPercent = ((1024.-frame.analog_sample)/1024)*100
#                print '%s: %s' % (strftime('%X'), lumiPercent)
        except Exception, e:
            print Exception, e
            from array import array
            a = array('B')
            a.fromstring(data)
            
            print "Exception: %s" % Exception, "data = ", [hex(x) for x in a]
            

    serialProtocol = XBEEProtocol(name="%s" % sys.argv[1], incomingMethod=m)
    port = SerialPort(serialProtocol, sys.argv[1], reactor, baudrate=9600)

    root = Resource()
    root.putChild("on", HttpCmdiface(serialProtocol.lightsOn))
    root.putChild("off", HttpCmdiface(serialProtocol.lightsOff))
    reactor.listenTCP(8880, Site(root))
    reactor.run()
