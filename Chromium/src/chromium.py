# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: /home/oe1/atv75arm/build-enviroment/builds/openatv/release/sf8008/tmp/work/sf8008-oe-linux-gnueabi/enigma2-plugin-extensions-chromium2/1.0+20240517/image/usr/lib/enigma2/python/Plugins/Extensions/Chromium/chromium.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 2085-03-11 01:14:56 UTC (3635111696)

from __future__ import absolute_import
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.ServiceEventTracker import ServiceEventTracker
from enigma import fbClass, eRCInput, gMainDC, getDesktop, eSize, eServiceReference, eTimer, iPlayableService, eDVBVolumecontrol
from .browser import Browser
from Components.config import config
global g_session
global browserinstance
import struct
import traceback
import os

def OnclearMem():
    os.system('sync')
    os.system('echo 3 > /proc/sys/vm/drop_caches')
browserinstance = None
g_session = None

class ChromiumTVWindow(Screen):
    skin = '\n\t\t<screen name="ChromiumTVWindow" position="0,0" size="1280,720" backgroundColor="transparent" flags="wfNoBorder" title="Chromium Plugin">\n\t\t</screen>\n\t\t'

    def __init__(self, session, left=0, top=0, width=0, height=0):
        global browserinstance
        global g_session
        Screen.__init__(self, session)
        g_session = session
        self.closetimer = eTimer()
        self.closetimer.callback.append(self.stop_chromium_application)
        self.starttimer = eTimer()
        self.starttimer.callback.append(self.start_chromium_application)
        self.starttimer.start(100)
        self.mediatimer = eTimer()
        self.mediatimer.callback.append(self.mediatimercb)
        self.mediatimer.start(1000)
        self.count = 0
        self.ppos = 0
        self.llen = 0
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.lastservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.session.nav.stopService()
        self.mediastate = 0
        self.sendstart = 0
        self.sendstarttimer = 0
        fbClass.getInstance().lock()
        eRCInput.getInstance().lock()
        self.xres, self.yres = (getDesktop(0).size().width(), getDesktop(0).size().height())
        gMainDC.getInstance().setResolution(1280, 720)
        getDesktop(0).resize(eSize(1280, 720))
        if not browserinstance:
            browserinstance = Browser()
        browserinstance.start()

    def start_chromium_application(self):
        if browserinstance.connectedClients() == 0:
            self.count += 1
            if self.count > 50:
                self.doExit()
            return None
        self.starttimer.stop()
        browserinstance.onMediaUrlChanged.append(self.onMediaUrlChanged)
        browserinstance.onStopPlaying.append(self.onStopPlaying)
        browserinstance.onExit.append(self.onExit)
        browserinstance.onPausePlaying.append(self.onPausePlaying)
        browserinstance.onResumePlaying.append(self.onResumePlaying)
        browserinstance.onSkip.append(self.onSkip)
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evStart: self.serviceStarted, iPlayableService.evStopped: self.serviceStopped, iPlayableService.evEOF: self.serviceEOF, iPlayableService.evGstreamerPlayStarted: self.serviceStarted, iPlayableService.evVideoProgressiveChanged: self.serviceProgressiveChanged})

    def serviceProgressiveChanged(self):
        browserinstance.sendCommand(1003)

    def serviceStarted(self):
        self.mediastate = 1
        self.sendstart = 1
        self.sendstarttimer = 5

    def serviceEOF(self):
        self.serviceStopped()
        if config.plugins.Chromium.boxkey.value == False:
            return

    def serviceStopped(self):
        if self.mediastate == 1:
            browserinstance.StopMediaPlayback()
            self.mediastate = 0

    def stop_chromium_application(self):
        self.closetimer.stop()
        self.closetimer = None
        self.doExit()

    def doExit(self):
        for line in traceback.format_stack():
            open('/tmp/netflix.log', 'a+').write(line.strip())
        self.volctrl = eDVBVolumecontrol.getInstance()
        vol = self.volctrl.getVolume()
        self.volctrl.setVolume(vol, vol)
        fbClass.getInstance().unlock()
        eRCInput.getInstance().unlock()
        gMainDC.getInstance().setResolution(self.xres, self.yres)
        getDesktop(0).resize(eSize(self.xres, self.yres))
        open('/proc/stb/fb/dst_left', 'w').write(self.left)
        open('/proc/stb/fb/dst_width', 'w').write(self.width)
        open('/proc/stb/fb/dst_top', 'w').write(self.top)
        open('/proc/stb/fb/dst_height', 'w').write(self.height)
        g_session.nav.playService(self.lastservice)
        OnclearMem()
        self.close()

    def onExit(self):
        browserinstance.onMediaUrlChanged.remove(self.onMediaUrlChanged)
        browserinstance.onStopPlaying.remove(self.onStopPlaying)
        browserinstance.onExit.remove(self.onExit)
        browserinstance.onPausePlaying.remove(self.onPausePlaying)
        browserinstance.onResumePlaying.remove(self.onResumePlaying)
        browserinstance.onSkip.remove(self.onSkip)
        self.mediatimer.stop()
        self.doExit()

    def onMediaUrlChanged(self, url):
        myreference = eServiceReference(4097, 0, url)
        OnclearMem()
        g_session.nav.playService(myreference)
        self.mediastate = 0

    def onStopPlaying(self):
        g_session.nav.stopService()

    def onPausePlaying(self):
        service = g_session.nav.getCurrentService()
        if service is None:
            return False
        pauseable = service.pause()
        if pauseable is not None:
            pauseable.pause()

    def onResumePlaying(self):
        service = g_session.nav.getCurrentService()
        if service is None:
            return False
        pauseable = service.pause()
        if pauseable is not None:
            pauseable.unpause()

    def onSkip(self, val):
        if val is None:
            return
        self.doSeek(val[0] * 90)

    def mediatimercb(self):
        self.llen = 0
        self.ppos = 0
        if self.getCurrentLength() is not None:
            self.llen = self.getCurrentLength()
        if self.getCurrentPosition() is not None:
            self.ppos = self.getCurrentPosition()
        if self.ppos == 0 and self.llen == 0:
            if self.sendstart and self.sendstarttimer > 0:
                self.sendstarttimer -= 1
                if self.sendstarttimer == 0:
                    browserinstance.sendCommand(1001)
                    self.sendstart = 0
            return None
        browserinstance.sendCommand(1005, struct.pack('!II', self.pts_to_msec(self.llen), self.pts_to_msec(self.ppos)))
        if self.sendstart:
            browserinstance.sendCommand(1001)
            self.sendstart = 0

    def pts_to_msec(self, pts):
        return int(pts / 90)

    def getCurrentPosition(self):
        seek = self.getSeek()
        if seek is None:
            return
        r = seek.getPlayPosition()
        if r[0]:
            return
        return long(r[1])

    def getCurrentLength(self):
        seek = self.getSeek()
        if seek is None:
            return
        r = seek.getLength()
        if r[0]:
            return
        return long(r[1])

    def getSeek(self):
        service = g_session.nav.getCurrentService()
        if service is None:
            return
        seek = service.seek()
        if seek is None or not seek.isCurrentlySeekable():
            return None
        return seek

    def doSeek(self, pts):
        seekable = self.getSeek()
        if seekable is None:
            return
        seekable.seekTo(pts)