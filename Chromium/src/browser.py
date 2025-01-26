# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: /home/oe1/atv75arm/build-enviroment/builds/openatv/release/sf8008/tmp/work/sf8008-oe-linux-gnueabi/enigma2-plugin-extensions-chromium2/1.0+20240517/image/usr/lib/enigma2/python/Plugins/Extensions/Chromium/browser.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 2028-03-24 01:13:44 UTC (1837473224)

from __future__ import absolute_import
import os
import struct
from enigma import eConsoleAppContainer, getDesktop
from Components.VolumeControl import VolumeControl
from Components.config import config
from . import datasocket

class Browser:

    def __init__(self):
        self.onUrlChanged = []
        self.onUrlInfoChanged = []
        self.onMediaUrlChanged = []
        self.onExit = []
        self.onStopPlaying = []
        self.onPausePlaying = []
        self.onResumePlaying = []
        self.onSkip = []
        self.commandserver = None

    def connectedClients(self):
        return self.commandserver.connectedClients()

    def start(self):
        if not self.commandserver:
            size_w = getDesktop(0).size().width()
            size_h = getDesktop(0).size().height()
            self.commandserver = datasocket.CommandServer()
            datasocket.onCommandReceived.append(self.onCommandReceived)
            datasocket.onBrowserClosed.append(self.onBrowserClosed)
            container = eConsoleAppContainer()
            url = config.plugins.Chromium.presets[config.plugins.Chromium.preset.value].portal.value
            useragent = "--user-agent='Mozilla/5.0 (X11;CrOS armv7i 13982.88.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'"
            if config.plugins.Chromium.mode.value == 'Netflix':
                url = config.plugins.Chromium.presets[1].portal.value
            if config.plugins.Chromium.mode.value == 'YouTubeTV':
                url = config.plugins.Chromium.presets[2].portal.value
                useragent = "--user-agent='Mozilla/5.0 (SMART-TV; Linux; Tizen 4.0.0.2) AppleWebkit/605.1.15 (KHTML, like Gecko) SamsungBrowser/9.2 TV Safari/605.1.15'"
            if config.plugins.Chromium.mode.value == 'Disney':
                url = config.plugins.Chromium.presets[3].portal.value
            if config.plugins.Chromium.mode.value == 'Dazn':
                url = config.plugins.Chromium.presets[4].portal.value
            if config.plugins.Chromium.mode.value == 'PrimeVideo':
                url = config.plugins.Chromium.presets[5].portal.value
            if config.plugins.Chromium.egl.value == True:
                container.execute(f'/usr/share/netflix/prepare.sh;export LD_LIBRARY_PATH=/usr/share/netflix/lib/nss:/usr/share/netflix/;/usr/share/netflix/bin --no-sandbox --no-zygote --ozone-platform=egl --enable-spatial-navigation {useragent} {url}')
            else:
                container.execute(f'/usr/share/netflix/prepare.sh;export LD_LIBRARY_PATH=/usr/share/netflix/lib/nss:/usr/share/netflix/;/usr/share/netflix/bin --no-sandbox --no-zygote --disable-gpu --enable-spatial-navigation {useragent} {url}')

    def stop(self):
        if self.commandserver:
            self.commandserver = None

    def onCommandReceived(self, cmd, data):
        if cmd == 1000:
            for x in self.onMediaUrlChanged:
                x(data)
        elif cmd == 1001:
            for x in self.onStopPlaying:
                x()
        elif cmd == 1002:
            for x in self.onPausePlaying:
                x()
        elif cmd == 1003:
            for x in self.onResumePlaying:
                x()
        elif cmd == 1005:
            for x in self.onSkip:
                x(struct.unpack('!I', data))
        elif cmd == 1100:
            VolumeControl.instance and VolumeControl.instance.volUp()
        elif cmd == 1101:
            VolumeControl.instance and VolumeControl.instance.volDown()
        elif cmd == 1102:
            VolumeControl.instance and VolumeControl.instance.volMute()
        elif cmd == 1999:
            for x in self.onExit:
                x()

    def onBrowserClosed(self):
        self.commandserver = None
        for x in self.onExit:
            x()

    def sendCommand(self, cmd, data=''):
        if self.commandserver is not None:
            self.commandserver.sendCommand(cmd, data)

    def sendUrl(self, url):
        return

    def StopMediaPlayback(self):
        if config.plugins.Stalker.boxkey.value == True:
            self.sendCommand(1002)
        else:
            self.sendCommand(5)