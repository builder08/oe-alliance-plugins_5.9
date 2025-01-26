# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: /home/oe1/atv75arm/build-enviroment/builds/openatv/release/sf8008/tmp/work/sf8008-oe-linux-gnueabi/enigma2-plugin-extensions-chromium2/1.0+20240517/image/usr/lib/enigma2/python/Plugins/Extensions/Chromium/plugin.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 2042-04-15 23:52:37 UTC (2281218757)

from __future__ import absolute_import
from . import _
from Components.ActionMap import NumberActionMap, ActionMap
from Components.ConfigList import ConfigListScreen
from Components.config import config, ConfigSubList, ConfigSubsection, ConfigYesNo, getConfigListEntry, ConfigInteger, ConfigText
from Components.Harddisk import harddiskmanager
from Components.Label import Label
from Components.PluginComponent import plugins
from Components.Sources.StaticText import StaticText
from Components.Sources.Boolean import Boolean
from Components.Pixmap import Pixmap
from enigma import iServiceInformation, eTimer, eConsoleAppContainer
from Plugins.Plugin import PluginDescriptor
from Screens.Console import Console
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from .chromium import ChromiumTVWindow
import os
import time
import datetime
language = config.osd.language.value.replace('_', '-')
NUMBER_OF_PRESETS = 14
config.plugins.Chromium = ConfigSubsection()
config.plugins.Chromium.mode = ConfigText(default='Chrome')
config.plugins.Chromium.showinpluginmenu1 = ConfigYesNo(default=True)
config.plugins.Chromium.showinpluginmenu2 = ConfigYesNo(default=True)
config.plugins.Chromium.showinpluginmenu3 = ConfigYesNo(default=True)
config.plugins.Chromium.showinpluginmenu4 = ConfigYesNo(default=True)
config.plugins.Chromium.showinpluginmenu5 = ConfigYesNo(default=True)
config.plugins.Chromium.showinmenu0 = ConfigYesNo(default=False)
config.plugins.Chromium.showinmenu1 = ConfigYesNo(default=False)
config.plugins.Chromium.showinmenu2 = ConfigYesNo(default=True)
config.plugins.Chromium.showinmenu3 = ConfigYesNo(default=False)
config.plugins.Chromium.showinmenu4 = ConfigYesNo(default=False)
config.plugins.Chromium.showinmenu5 = ConfigYesNo(default=False)
config.plugins.Chromium.autostart = ConfigYesNo(default=False)
config.plugins.Chromium.egl = ConfigYesNo(default=True)
config.plugins.Chromium.preset = ConfigInteger(default=0)
config.plugins.Chromium.presets = ConfigSubList()
for x in range(NUMBER_OF_PRESETS):
    preset = ConfigSubsection()
    preset.portal = ConfigText(default='https://')
    config.plugins.Chromium.presets.append(preset)
config.plugins.Chromium.presets[0].portal.value = 'https://www.opena.tv'
config.plugins.Chromium.presets[1].portal.value = 'https://www.netflix.com/{}/login'.format(language.replace('en-', '').replace('zh-', '').split('-')[0])
config.plugins.Chromium.presets[2].portal.value = 'https://www.youtube.com/tv'
config.plugins.Chromium.presets[3].portal.value = 'https://www.disneyplus.com/{}/'.format(language.lower())
config.plugins.Chromium.presets[4].portal.value = 'https://www.dazn.com/{}/signin'.format(language)
config.plugins.Chromium.presets[5].portal.value = 'https://www.primevideo.com/offers/nonprimehomepage/ref=atv_nb_lcl_{}'.format(language.replace('-', '_'))
config.plugins.Chromium.presets[6].portal.value = 'https://www.joyn.de/'
config.plugins.Chromium.presets[7].portal.value = 'https://www.beinsports.com'
config.plugins.Chromium.presets[8].portal.value = 'https://www.blutv.com/int'
config.plugins.Chromium.presets[9].portal.value = 'https://www.canalplus.com/'
config.plugins.Chromium.presets[10].portal.value = 'https://www.digiturkplay.com/'
config.plugins.Chromium.presets[11].portal.value = 'https://www.dsmartgo.com.tr/anasayfa'
config.plugins.Chromium.presets[12].portal.value = 'https://connect.bein.com/'

class ChromiumEd(Screen, ConfigListScreen):
    skin = '\n\t\t<screen name="ChromiumEd" position="center,center" size="710,550" title="Chromium Setup">\n\t\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />\n\t\t\t<widget source="key_red" render="Label" position="0,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="150,0" size="140,40" alphatest="on" />\n\t\t\t<widget source="key_green" render="Label" position="150,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t\t<widget name="config" position="5,50" size="700,500" zPosition="1" scrollbarMode="showOnDemand" />\n\t\t</screen>'

    def __init__(self, session):
        self.session = session
        Screen.__init__(self, self.session)
        Screen.setTitle(self, _('Chromium Setup'))
        self.list = []
        ConfigListScreen.__init__(self, self.list, session=self.session)
        self.loadPortals()
        self['key_red'] = StaticText(_('Cancel'))
        self['key_green'] = StaticText(_('Save'))
        self.configfound = False
        self['actions'] = NumberActionMap(['SetupActions', 'ColorActions', 'VirtualKeyboardActions'], {'ok': self.ok, 'back': self.close, 'cancel': self.close, 'red': self.close, 'green': self.save, 'showVirtualKeyboard': self.KeyText}, -2)
        self.setupTimer = eTimer()
        self.setupTimer.callback.append(self.setupCallback)
        self.setupTimer.start(1)
        if self.selectionChanged not in self['config'].onSelectionChanged:
            self['config'].onSelectionChanged.append(self.selectionChanged)
        self.selectionChanged()
        self.onLayoutFinish.append(self.setWindowTitle)

    def setupCallback(self):
        return

    def VirtualKeyBoardCallback(self, callback=None):
        if callback is not None and len(callback):
            self['config'].getCurrent()[1].setValue(callback)
            self['config'].invalidate(self['config'].getCurrent())

    def KeyText(self):
        if self['config'].getCurrentIndex() < NUMBER_OF_PRESETS:
            self.session.openWithCallback(self.VirtualKeyBoardCallback, VirtualKeyBoard, title=self['config'].getCurrent()[0], text=self['config'].getCurrent()[1].value)

    def confirmationConfig(self, result):
        if result:
            data = open(self.path, 'r').read()
            if len(data):
                data = data.split('\n')
                for x in data:
                    y = x.split(' ')
                    if len(y) == 3 and y[0] == 'portal':
                        config.plugins.Chromium.presets[int(y[1])].portal.value = y[2]
                        config.plugins.Chromium.presets[int(y[1])].save()
                config.plugins.Chromium.save()
                self.loadPortals()

    def selectionChanged(self):
        if self['config'].getCurrent() and isinstance(self['config'].getCurrent()[1], ConfigText) and ('HelpWindow' in self) and self['config'].getCurrent()[1].help_window and (self['config'].getCurrent()[1].help_window.instance is not None):
            helpwindowpos = self['HelpWindow'].getPosition()
            from enigma import ePoint
            self['config'].getCurrent()[1].help_window.instance.move(ePoint(helpwindowpos[0], helpwindowpos[1]))

    def loadPortals(self):
        self.list = []
        self.name = []
        for x in range(NUMBER_OF_PRESETS):
            self.name.append(ConfigText(default=config.plugins.Chromium.presets[x].portal.value, fixed_size=False))
            if config.plugins.Chromium.preset.value == x:
                self.list.append(getConfigListEntry('>> ' + _('WEB URL') + ' %d' % (x + 1), self.name[x]))
            else:
                self.list.append(getConfigListEntry(_('WEB URL') + ' %d' % (x + 1), self.name[x]))
        self.list.append(getConfigListEntry(_('Show Chromium in Mainmenu'), config.plugins.Chromium.showinmenu0))
        self.list.append(getConfigListEntry(_('Show Netflix in Mainmenu'), config.plugins.Chromium.showinmenu1))
        self.list.append(getConfigListEntry(_('Show YouTubeTV in Mainmenu'), config.plugins.Chromium.showinmenu2))
        self.list.append(getConfigListEntry(_('Show Disney + in Mainmenu'), config.plugins.Chromium.showinmenu3))
        self.list.append(getConfigListEntry(_('Show Dazn in Mainmenu'), config.plugins.Chromium.showinmenu4))
        self.list.append(getConfigListEntry(_('Show Prime Video in Mainmenu'), config.plugins.Chromium.showinmenu5))
        self.list.append(getConfigListEntry(_('Show Netflix in Plugin Browser'), config.plugins.Chromium.showinpluginmenu1))
        self.list.append(getConfigListEntry(_('Show YoutubeTV in Plugin Browser'), config.plugins.Chromium.showinpluginmenu2))
        self.list.append(getConfigListEntry(_('Show Disney + in Plugin Browser'), config.plugins.Chromium.showinpluginmenu3))
        self.list.append(getConfigListEntry(_('Show Dazn in Mainmenu'), config.plugins.Chromium.showinpluginmenu4))
        self.list.append(getConfigListEntry(_('Show Prime Video in Mainmenu'), config.plugins.Chromium.showinpluginmenu5))
        self.list.append(getConfigListEntry(_('Start Chromium with enigma2 (Autostart)'), config.plugins.Chromium.autostart))
        self.list.append(getConfigListEntry(_('Use EGL Hardware acceleration'), config.plugins.Chromium.egl))
        self['config'].list = self.list
        self['config'].l.setList(self.list)

    def setWindowTitle(self):
        file_name = '/usr/share/netflix/html/netflix_plugin.js'
        if os.path.isfile(file_name):
            time_ob = time.localtime(os.path.getmtime(file_name))
            version = '{}.{}.{}'.format(time_ob.tm_year, time_ob.tm_mon, time_ob.tm_mday)
            self.setTitle(_('Chromium Setup (Version: %s)' % version))

    def ok(self):
        if self['config'].getCurrentIndex() < NUMBER_OF_PRESETS:
            config.plugins.Chromium.preset.value = self['config'].getCurrentIndex()
            for x in range(NUMBER_OF_PRESETS):
                config.plugins.Chromium.presets[x].portal.value = self.name[x].value
                config.plugins.Chromium.presets[x].save()
            config.plugins.Chromium.save()
            self.loadPortals()

    def confirmationResult(self, result):
        if result:
            config.plugins.Chromium.preset.value = self['config'].getCurrentIndex()
            for x in range(NUMBER_OF_PRESETS):
                config.plugins.Chromium.presets[x].portal.value = self.name[x].value
                config.plugins.Chromium.presets[x].save()
            config.plugins.Chromium.save()
            self.loadPortals()

    def save(self):
        for x in range(NUMBER_OF_PRESETS):
            config.plugins.Chromium.presets[x].portal.value = self.name[x].value
            config.plugins.Chromium.presets[x].save()
        config.plugins.Chromium.save()
        self.close()

def setup(session, **kwargs):
    session.open(ChromiumEd)

def autostart(session, **kwargs):
    global g_timerinstance
    global g_session
    g_session = session
    g_timerinstance = eTimer()
    g_timerinstance.callback.append(timerCallback)
    g_timerinstance.start(1000)

def timerCallback():
    g_timerinstance.stop()
    left = open('/proc/stb/fb/dst_left', 'r').read()
    width = open('/proc/stb/fb/dst_width', 'r').read()
    top = open('/proc/stb/fb/dst_top', 'r').read()
    height = open('/proc/stb/fb/dst_height', 'r').read()
    config.plugins.Chromium.mode.value = 'Chrome'
    g_session.open(ChromiumTVWindow, left, top, width, height)

def main(session, **kwargs):
    left = open('/proc/stb/fb/dst_left', 'r').read()
    width = open('/proc/stb/fb/dst_width', 'r').read()
    top = open('/proc/stb/fb/dst_top', 'r').read()
    height = open('/proc/stb/fb/dst_height', 'r').read()
    config.plugins.Chromium.mode.value = 'Chrome'
    session.open(ChromiumTVWindow, left, top, width, height)

def vod1(session, **kwargs):
    left = open('/proc/stb/fb/dst_left', 'r').read()
    width = open('/proc/stb/fb/dst_width', 'r').read()
    top = open('/proc/stb/fb/dst_top', 'r').read()
    height = open('/proc/stb/fb/dst_height', 'r').read()
    config.plugins.Chromium.mode.value = 'Netflix'
    session.open(ChromiumTVWindow, left, top, width, height)

def vod2(session, **kwargs):
    left = open('/proc/stb/fb/dst_left', 'r').read()
    width = open('/proc/stb/fb/dst_width', 'r').read()
    top = open('/proc/stb/fb/dst_top', 'r').read()
    height = open('/proc/stb/fb/dst_height', 'r').read()
    config.plugins.Chromium.mode.value = 'YouTubeTV'
    session.open(ChromiumTVWindow, left, top, width, height)

def vod3(session, **kwargs):
    left = open('/proc/stb/fb/dst_left', 'r').read()
    width = open('/proc/stb/fb/dst_width', 'r').read()
    top = open('/proc/stb/fb/dst_top', 'r').read()
    height = open('/proc/stb/fb/dst_height', 'r').read()
    config.plugins.Chromium.mode.value = 'Disney'
    session.open(ChromiumTVWindow, left, top, width, height)

def vod4(session, **kwargs):
    left = open('/proc/stb/fb/dst_left', 'r').read()
    width = open('/proc/stb/fb/dst_width', 'r').read()
    top = open('/proc/stb/fb/dst_top', 'r').read()
    height = open('/proc/stb/fb/dst_height', 'r').read()
    config.plugins.Chromium.mode.value = 'Dazn'
    session.open(ChromiumTVWindow, left, top, width, height)

def vod5(session, **kwargs):
    left = open('/proc/stb/fb/dst_left', 'r').read()
    width = open('/proc/stb/fb/dst_width', 'r').read()
    top = open('/proc/stb/fb/dst_top', 'r').read()
    height = open('/proc/stb/fb/dst_height', 'r').read()
    config.plugins.Chromium.mode.value = 'PrimeVideo'
    session.open(ChromiumTVWindow, left, top, width, height)

def startMenu(menuid):
    if menuid != 'mainmenu':
        return []
    return [(_('Chromium Browser'), main, 'Chromium Plugin', 80)]

def VOD1Menu(menuid):
    if menuid != 'mainmenu':
        return []
    return [(_('Netflix'), vod1, 'Netflix Plugin', 80)]

def VOD2Menu(menuid):
    if menuid != 'mainmenu':
        return []
    return [(_('YouTubeTV'), vod2, 'youtubetv', 80)]

def VOD3Menu(menuid):
    if menuid != 'mainmenu':
        return []
    return [(_('Disney +'), vod3, 'Disney Plugin', 80)]

def VOD4Menu(menuid):
    if menuid != 'mainmenu':
        return []
    return [(_('Dazn'), vod4, 'Dazn', 80)]

def VOD5Menu(menuid):
    if menuid != 'mainmenu':
        return []
    return [(_('Prime Video'), vod5, 'PrimeVideo', 80)]

def Plugins(**kwargs):
    from enigma import getDesktop
    if getDesktop(0).size().width() <= 1280:
        chromium = 'chromium_HD.png'
        netflix = 'netflix_HD.png'
        youtubetv = 'youtubetv_HD.png'
        disney = 'disney_HD.png'
        dazn = 'dazn_HD.png'
        prime = 'prime_HD.png'
    else:
        chromium = 'chromium_FHD.png'
        netflix = 'netflix_FHD.png'
        youtubetv = 'youtubetv_FHD.png'
        disney = 'disney_FHD.png'
        dazn = 'dazn_FHD.png'
        prime = 'prime_FHD.png'
    menus = []
    menus.append(PluginDescriptor(name=_('Chromium Setup'), description=_('Chromium Setup'), where=PluginDescriptor.WHERE_PLUGINMENU, icon=chromium, fnc=setup))
    menus.append(PluginDescriptor(name=_('Chromium Browser'), description=_('Chromium Browser'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main))
    menus.append(PluginDescriptor(name=_('Netflix'), description=_('Netflix'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=vod1))
    menus.append(PluginDescriptor(name=_('YouTubeTV'), description=_('YouTubeTV'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=vod2))
    menus.append(PluginDescriptor(name=_('Disney +'), description=_('Disney +'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=vod3))
    menus.append(PluginDescriptor(name=_('Dazn'), description=_('Dazn'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=vod4))
    menus.append(PluginDescriptor(name=_('PrimeVideo'), description=_('PrimeVideo'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=vod5))
    if config.plugins.Chromium.showinpluginmenu1.value:
        menus.append(PluginDescriptor(name=_('Netflix'), description=_('Netflix'), where=PluginDescriptor.WHERE_PLUGINMENU, icon=netflix, fnc=vod1))
    if config.plugins.Chromium.showinpluginmenu2.value:
        menus.append(PluginDescriptor(name=_('YoutubeTV'), description=_('YoutubeTV'), where=PluginDescriptor.WHERE_PLUGINMENU, icon=youtubetv, fnc=vod2))
    if config.plugins.Chromium.showinpluginmenu3.value:
        menus.append(PluginDescriptor(name=_('Disney +'), description=_('Disney +'), where=PluginDescriptor.WHERE_PLUGINMENU, icon=disney, fnc=vod3))
    if config.plugins.Chromium.showinpluginmenu4.value:
        menus.append(PluginDescriptor(name=_('Dazn'), description=_('Dazn'), where=PluginDescriptor.WHERE_PLUGINMENU, icon=dazn, fnc=vod4))
    if config.plugins.Chromium.showinpluginmenu5.value:
        menus.append(PluginDescriptor(name=_('PrimeVideo'), description=_('PrimeVideo'), where=PluginDescriptor.WHERE_PLUGINMENU, icon=prime, fnc=vod5))
    if config.plugins.Chromium.showinmenu0.value:
        menus.append(PluginDescriptor(name=_('Chromium Browser'), description=_('Chromium Browser'), where=PluginDescriptor.WHERE_MENU, fnc=startMenu))
    if config.plugins.Chromium.showinmenu1.value:
        menus.append(PluginDescriptor(name=_('Netflix'), description=_('Netflix'), where=PluginDescriptor.WHERE_MENU, fnc=VOD1Menu))
    if config.plugins.Chromium.showinmenu2.value:
        menus.append(PluginDescriptor(name=_('YouTubeTV'), description=_('YouTubeTV'), where=PluginDescriptor.WHERE_MENU, fnc=VOD2Menu))
    if config.plugins.Chromium.showinmenu3.value:
        menus.append(PluginDescriptor(name=_('Disney +'), description=_('Disney +'), where=PluginDescriptor.WHERE_MENU, fnc=VOD3Menu))
    if config.plugins.Chromium.showinmenu4.value:
        menus.append(PluginDescriptor(name=_('Dazn'), description=_('Dazn'), where=PluginDescriptor.WHERE_MENU, fnc=VOD4Menu))
    if config.plugins.Chromium.showinmenu5.value:
        menus.append(PluginDescriptor(name=_('Prime Video'), description=_('Prime Video'), where=PluginDescriptor.WHERE_MENU, fnc=VOD5Menu))
    if config.plugins.Chromium.autostart.value:
        menus.append(PluginDescriptor(where=PluginDescriptor.WHERE_SESSIONSTART, fnc=autostart))
    return menus