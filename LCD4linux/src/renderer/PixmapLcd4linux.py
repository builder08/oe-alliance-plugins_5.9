from Renderer import Renderer
from enigma import ePixmap
import os

class PixmapLcd4linux(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		self.mTime = 0
		self.swap = False

	GUI_WIDGET = ePixmap

	def postWidgetCreate(self, instance):
		self.changed((self.CHANGED_DEFAULT,))

	def changed(self, what):
		if os.path.isfile("/tmp/l4ldisplay.png"):
			try:
				mtime = os.stat("/tmp/l4ldisplay.png").st_mtime
				if self.mTime != mtime:
					if self.instance:
						if self.swap:
							if not os.path.isfile("/tmp/l4ldisplaycp.png"):
								os.symlink("/tmp/l4ldisplay.png","/tmp/l4ldisplaycp.png")
							self.instance.setPixmapFromFile("/tmp/l4ldisplaycp.png")
						else:
							self.instance.setPixmapFromFile("/tmp/l4ldisplay.png")
						self.mTime = mtime
						self.swap = not self.swap
					else:
						self.mTime = 0
			except:
				pass