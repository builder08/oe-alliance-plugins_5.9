# -*- coding: utf-8 -*-
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
import os, gettext

PluginLanguageDomain = "TerrestrialScan"
PluginLanguagePath = "SystemPlugins/TerrestrialScan/locale"

def localeInit():
	gettext.bindtextdomain(PluginLanguageDomain, resolveFilename(SCOPE_PLUGINS, PluginLanguagePath))

def _(txt): # for normal messages
	if gettext.dgettext(PluginLanguageDomain, txt):
		return gettext.dgettext(PluginLanguageDomain, txt)
	else:
		print "[" + PluginLanguageDomain + "] fallback to default translation for " + txt
		return gettext.gettext(txt)

def __(txt_singular, txt_plural, number): # for singular/plural messages
	if gettext.dngettext(PluginLanguageDomain, txt_singular, txt_plural, number):
		return gettext.dngettext(PluginLanguageDomain, txt_singular, txt_plural, number)
	else:
		print "[" + PluginLanguageDomain + "] fallback to default translation for " + txt_singular
		return gettext.gettext(txt_singular)


language.addCallback(localeInit())
