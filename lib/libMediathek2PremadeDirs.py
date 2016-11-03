import urllib
import urllib2
import socket
import xbmc
import xbmcaddon
import xbmcvfs
import re
from datetime import date, timedelta

from libMediathekUtils import getTranslation as getTranslation
from libMediathek2Listing import addEntry as addEntry


weekdayDict = { '0': getTranslation(31013),#Sonntag
				'1': getTranslation(31014),#Montag
				'2': getTranslation(31015),#Dienstag
				'3': getTranslation(31016),#Mittwoch
				'4': getTranslation(31017),#Donnerstag
				'5': getTranslation(31018),#Freitag
				'6': getTranslation(31019),#Samstag
			  }
	
def populateDirAZ(mode,ignore=[]):
	dict = {}
	dict['mode'] = mode
	if not '#' in ignore:
		dict['name'] = "#"
		dict['type'] = 'dir'
		addEntry(dict)
	letters = [chr(i) for i in xrange(ord('a'), ord('z')+1)]
	for letter in letters:
		if not letter in ignore:
			letter = letter.upper()
			dict['name'] = letter
			addEntry(dict)
	
def populateDirDate(mode,img=False):
	dict = {}
	dict['mode'] = mode
	dict['type'] = 'dir'
	dict['name'] = getTranslation(31020)
	dict['datum']  = '0'
	if img: dict['thumb']  = img[7]
	addEntry(dict)
	dict['name'] = getTranslation(31021)
	dict['datum']  = '1'
	if img: dict['thumb']  = img[8]
	addEntry(dict)
	i = 2
	while i <= 6:
		day = date.today() - timedelta(i)
		dict['name'] = weekdayDict[day.strftime("%w")]
		dict['datum']  = str(i)
		if img: dict['thumb']  = img[int(day.strftime("%w"))]
		addEntry(dict)
		i += 1

def setView(viewMode):
	skin_used = xbmc.getSkinDir()
	if skin_used == 'skin.confluence':
		xbmc.executebuiltin('Container.SetViewMode(500)') # "Thumbnail" view
	elif skin_used == 'skin.aeon.nox':
		xbmc.executebuiltin('Container.SetViewMode(512)') # "Info-wall" view.
	elif skin_used == 'skin.estuary':
		if viewMode == 'video':
			return
		elif viewMode == 'shows':
			xbmc.executebuiltin('Container.SetViewMode(502)') # "Info-wall" view.