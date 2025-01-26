# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: /home/oe1/atv75arm/build-enviroment/builds/openatv/release/sf8008/tmp/work/sf8008-oe-linux-gnueabi/enigma2-plugin-extensions-chromium2/1.0+20240517/image/usr/lib/enigma2/python/Plugins/Extensions/Chromium/datasocket.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 2088-08-23 15:58:29 UTC (3744115109)

global onCommandReceived
global onBrowserClosed
global browserclients
import struct
import os
from twisted.internet.protocol import ServerFactory, Protocol
browserclients = []
onCommandReceived = []
onBrowserClosed = []

class ClientConnection(Protocol):
    magic = 987654321
    data = ''
    headerformat = '!III'
    headersize = struct.calcsize(headerformat)
    datasize = 0
    cmd = 0

    def dataReceived(self, data):
        self.data += data
        while len(self.data):
            if self.datasize == 0 and len(self.data) >= self.headersize:
                magic, self.cmd, self.datasize = struct.unpack(self.headerformat, self.data[:self.headersize])
                self.data = self.data[self.headersize:]
                if magic != self.magic:
                    self.data = ''
                    self.datasize = 0
            if len(self.data) >= self.datasize:
                for x in onCommandReceived:
                    x(self.cmd, self.data[:self.datasize])
                    break
                self.data = self.data[self.datasize:]
                self.datasize = 0
            else:
                break

    def connectionMade(self):
        browserclients.append(self)

    def connectionLost(self, reason):
        browserclients.remove(self)
        if not len(browserclients):
            for x in onBrowserClosed:
                x()

class CommandServer:

    def __init__(self):
        from twisted.internet import reactor
        self.factory = ServerFactory()
        self.factory.protocol = ClientConnection
        try:
            os.remove('/tmp/.sock.netflix')
        except:
            pass
        else:
            pass
        self.port = reactor.listenUNIX('/tmp/.sock.netflix', self.factory)

    def __del__(self):
        for client in browserclients:
            client.transport.loseConnection()

    def sendCommand(self, cmd, data=''):
        for client in browserclients:
            client.transport.write(struct.pack('!III', client.magic, cmd, len(data)))
            if len(data):
                client.transport.write(data)

    def connectedClients(self):
        return len(browserclients)