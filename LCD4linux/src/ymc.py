# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import
try:
	import simplejson
except:
	import json as simplejson

from six.moves.urllib.request import urlopen
from .plugin import L4logE

class YMC:
	def __init__(self, ip):
		self.IP = ip

	def Urlget(self, url):
		f = urlopen(url, timeout=1)
		fr = f.read()
		fc = f.code
		f.close()
		return (fr, fc)

	def getPlayInfo(self):
		try:
			content, resp = self.Urlget("http://%s/YamahaExtendedControl/v1/netusb/getPlayInfo" % self.IP)
			if resp == 200:
				r = simplejson.loads(content)
				return r
			else:
				return {}
		except:
			L4logE("YMC Error")
			return {}

	def getStatus(self):
		try:
			content, resp = self.Urlget("http://%s/YamahaExtendedControl/v1/main/getStatus" % self.IP)
			if resp == 200:
				r = simplejson.loads(content)
				return r
			else:
				return {}
		except:
			L4logE("YMC Error")
			return {}
