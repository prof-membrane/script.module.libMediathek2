# -*- coding: utf-8 -*-

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import sys
"""
import urllib
import json
import time
import socket

from datetime import date, timedelta
"""
from libMediathekUtils import *
from libMediathek2Listing import *
from libMediathekTtml2Srt import *
from libMediathek2PremadeDirs import *
	
def play(d):
	listitem = xbmcgui.ListItem(path=d['media'][0]['url'])
	subs = []
	if 'subtitle' in d:
		for subtitle in d['subtitle']:
			if subtitle['type'] == 'srt':
				subs.append(subtitle['url'])
	listitem.setSubtitles(subs)
	pluginhandle = int(sys.argv[1])
	xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

def listM():#TODO: rename
	
	global params
	params = get_params()
	global pluginhandle
	pluginhandle = int(sys.argv[1])
	
	if not params.has_key('mode'):
		fallbackMode()
	else:
		modes.get(params['mode'],fallbackMode)()
		#libMediathek.setView(views.get(params['mode'],'default'))
	xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=True)	