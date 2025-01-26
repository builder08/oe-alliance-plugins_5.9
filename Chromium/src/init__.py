# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: /home/oe1/atv75arm/build-enviroment/builds/openatv/release/sf8008/tmp/work/sf8008-oe-linux-gnueabi/enigma2-plugin-extensions-chromium2/1.0+20240517/image/usr/lib/enigma2/python/Plugins/Extensions/Chromium/__init__.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 2021-10-01 03:45:53 UTC (1633059953)

from __future__ import print_function
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
import os
import gettext
PluginLanguageDomain = 'chromium'
PluginLanguagePath = 'Extensions/Chromium/locale'

def localeInit():
    gettext.bindtextdomain(PluginLanguageDomain, resolveFilename(SCOPE_PLUGINS, PluginLanguagePath))

def _(txt):
    if gettext.dgettext(PluginLanguageDomain, txt):
        return gettext.dgettext(PluginLanguageDomain, txt)
    print('[' + PluginLanguageDomain + '] fallback to default translation for ' + txt)
    return gettext.gettext(txt)
localeInit()
language.addCallback(localeInit)