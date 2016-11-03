import urllib
import urllib2
import socket
import xbmc
import xbmcaddon
import xbmcvfs
import re

	
def pvrCheckStartTimeIsComparable(a,b):
	n = abs(a-b)
	if n <= 15:
		return True
	else:
		return False
def pvrCheckIfMovie(name):
	if name.startswith("Fernsehfilm Deutschland"):
		return True
	else:
		return False
def pvrCheckDurationIsComparable(a,b,maxDeviation = 10):
	deviation = abs((a * 100) / b - 100)
	if deviation <= maxDeviation:
		return True
	else:
		return False

def pvrCheckNameIsComparable(a,b):
	if a == b:
		return True
	else:
		return _wordRatio(a,b)
	
def _wordRatio(a,b,maxRatio=0.7):
	xbmc.log(a)
	xbmc.log(b)
	i = 0
	aSplit = a.split(" ")
	bSplit = b.split(" ")
	for word in aSplit:
		if word in bSplit:
			i += 1
	ratio = i / len(aSplit) 
	if ratio >= maxRatio:
		return True
	else: return False
