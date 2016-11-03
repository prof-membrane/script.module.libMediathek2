import urllib
import urllib2
import socket
import xbmc
import xbmcaddon
import xbmcvfs
import re
temp = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')+'temp').decode('utf-8')
dict = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')+'dict.py').decode('utf-8')

def log(msg):
	xbmc.log(msg)