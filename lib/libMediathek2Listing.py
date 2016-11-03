# -*- coding: utf-8 -*-
import urllib
import urllib2
import socket
import sys
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import re
from datetime import datetime,timedelta
import time

from libMediathekUtils import clearString
#from libMediathek import get_params

icon = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')+'/icon.png').decode('utf-8')
fanart = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')+'/fanart.jpg').decode('utf-8')
translation = xbmcaddon.Addon(id='script.module.libMediathek').getLocalizedString
def log(msg):
	xbmc.log(msg)

def addEntry(dict):	
	for key in dict:#sigh
		if isinstance(dict[key], unicode):
			dict[key] = dict[key].encode('utf-8')
	#xbmc.log(str(dict))
	if 'type' in dict and dict['type'] == 'nextPage':
		dict['name'] = translation(31040)
	if isinstance(dict["name"], unicode):
		dict["name"] = dict["name"].encode('utf-8')
	dict["name"] = clearString(dict["name"])
	if 'type' in dict and dict['type'] == 'date' and 'time' in dict:
		dict["name"] = '(' + dict["time"] + ') ' + dict["name"]
	#dict["name"] = '(' + dict["time"] + ') ' + dict["name"]
	#dict["name"] = dict["name"].replace('&amp;','&')
	#if hideAudioDisa:
	#	if 'Hörfassung' in dict["name"] or 'Audiodeskription' in dict["name"]:
	#		return False
			
	u = _buildUri(dict)
	ilabels = {
		"Title": clearString(dict.get('name','')),
		"Plot": clearString(dict.get('plot','')),
		"Plotoutline": clearString(dict.get('plot','')),
		"Duration": dict.get('duration',''),
		"Mpaa": dict.get('mpaa','')
		}
	ok=True
	liz=xbmcgui.ListItem(clearString(dict.get('name','')), iconImage="DefaultFolder.png", thumbnailImage=dict.get('thumb',icon))
	#liz.setInfo( type="Video", infoLabels={ "Title": clearString(dict.get('name','')) , "Plot": clearString(dict.get('plot','')) , "Plotoutline": clearString(dict.get('plot','')) , "Duration": dict.get('duration','') } )
	liz.setInfo( type="Video", infoLabels=ilabels)
	liz.setProperty('fanart_image',dict.get('fanart',dict.get('thumb',fanart)))
	xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="episodes" )
	if 'type' in dict and (dict['type'] == 'video' or dict['type'] == 'date'):
		liz.setProperty('IsPlayable', 'true')
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
	elif 'type' in dict and dict['type'] == 'nextPage':
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
		
	return ok
	
def addEntries(l,page=False):#TODO remove page
	lists = []
	ok = False
	i = 0
	xbmc.log(str(l))
	for dict in l:
		u = _buildUri(dict)
		#xbmc.log(str(dict))
		newdict = {}
		for key in dict:#sigh
			if key.startswith('_'):
				if isinstance(dict[key], unicode):
					dict[key] = dict[key].encode('utf-8', 'ignore')
				newdict[key[1:]] = dict[key]
				newdict[key[1:]] = dict[key]
			elif isinstance(dict[key], unicode):
				newdict[key] = dict[key].encode('utf-8', 'ignore')
			else:
				newdict[key] = dict[key]
		dict = newdict
		xbmc.log(str(dict))
		if 'type' in dict and dict['type'] == 'nextPage':
			dict['name'] = translation(31040)
			if not 'mode' in dict:
				dict['mode'] = get_params()['mode']
		if isinstance(dict["name"], unicode):
			dict["name"] = dict["name"].encode('utf-8')
		dict["name"] = clearString(dict["name"])
		if 'airedISO8601' in dict or 'airedISO8601A' in dict:
			dict['aired'],dict['airedtime'] = _airedISO8601(dict)
		if 'airedISO8601B' in dict:
			dict['aired'],dict['airedtime'] = _airedISO8601B(dict)
			
		if 'type' in dict and dict['type'] == 'date' and 'airedtime' in dict:
			dict["name"] = '(' + str(dict["airedtime"]) + ') ' + dict["name"]
		elif 'type' in dict and dict['type'] == 'date' and 'time' in dict:
			dict["name"] = '(' + str(dict["date"]) + ') ' + dict["name"]
		#dict["name"] = dict["name"].replace('&amp;','&')
		#if hideAudioDisa:
		#	if 'Hörfassung' in dict["name"] or 'Audiodeskription' in dict["name"]:
		#		return False
				
		ilabels = {
			"Title": clearString(dict.get('name','')),
			"Plot": clearString(dict.get('plot','')),
			"Plotoutline": clearString(dict.get('plot','')),
			"Duration": dict.get('duration',''),
			"Mpaa": dict.get('mpaa',''),
			"Aired": dict.get('aired',''),
			"Studio": dict.get('channel',''),
			}
		if 'episode' in dict: 
			ilabels['Episode'] = dict['episode']
		if 'Season' in dict: 
			ilabels['Season'] = dict['season']
		if 'tvshowtitle' in dict: 
			ilabels['tvshowtitle'] = dict['tvshowtitle']
			ilabels['tagline'] = dict['tvshowtitle']
			ilabels['album'] = dict['tvshowtitle']
		if 'rating' in dict:
			ilabels['rating'] = dict['rating']
		ok=True
		#liz=xbmcgui.ListItem(clearString(dict.get('name','')), iconImage="DefaultFolder.png", thumbnailImage=dict.get('thumb',icon))
		liz=xbmcgui.ListItem(clearString(dict.get('name','')))
			
		#liz.setInfo( type="Video", infoLabels={ "Title": clearString(dict.get('name','')) , "Plot": clearString(dict.get('plot','')) , "Plotoutline": clearString(dict.get('plot','')) , "Duration": dict.get('duration','') } )
		liz.setInfo( type="Video", infoLabels=ilabels)
		#if 'hasSubtitle' in dict:
		liz.addStreamInfo('subtitle', {'language': 'deu'})
		#if True:
			#liz.addStreamInfo('subtitle',{'language':'de'})
		#liz.setProperty('fanart_image',dict.get('fanart',dict.get('thumb',fanart)))
		#try:
		art = {}
		art['thumb'] = dict.get('thumb')
		art['landscape'] = dict.get('thumb')
		#art['poster'] = dict.get('poster')
		art['poster'] = dict.get('thumb')
		art['fanart'] = dict.get('fanart',dict.get('thumb',fanart))
		art['icon'] = dict.get('channelLogo','')
		#art.append({'landscape': dict.get('thumb')})
		#art.append({'fanart': dict.get('fanart',dict.get('thumb',fanart))})
		#xbmc.log(str(art))
		liz.setArt(art)
		#except: pass
		if 'type' in dict:
			if dict['type'] == 'clip':
				xbmc.log('ignoring clip')
			elif dict.get('type',None) == 'video' or dict.get('type',None) == 'live' or dict.get('type',None) == 'date':
				xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="episodes" )
				liz.setProperty('IsPlayable', 'true')
				lists.append([u,liz,False])
			elif 'type' in dict and dict['type'] == 'nextPage':
				#lists.append([u,liz,True])
				lists.append([u,liz,True])
			elif dict['type'] == 'shows':
				#xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="episodes" )
				xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="tvshows" )
				lists.append([u,liz,True])
			else:
				xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="files" )
				lists.append([u,liz,True])
		else:
			#xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="files" )
			lists.append([u,liz,True])
			
		i+=1
		xbmc.log('added ' + str(i) + ' entries')
		xbmc.log(str(dict))
	xbmcplugin.addDirectoryItems(int(sys.argv[1]), lists)
	#xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_PROGRAM_COUNT)
	#xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="episodes" )		
	return ok

def _buildUri(dict):
	u = dict.get('pluginpath',sys.argv[0])+'?'
	i = 0
	#return u
	for key in dict.keys():
		if not key.startswith('_'):
			if i > 0:
				u += '&'
			u += key + '=' + urllib.quote_plus(dict[key].encode('utf-8'))
			i += 1
		#if key == 'plot': continue
		#if key == 'name': key = 'n'#continue
		"""
		#if key == 'plot': dict[key] = 'Kevin Bieksa fires a one-timer on net, but Aaron Dell quickly gets across for the save to keep the Sharks ahead midway through the 2nd'
		#if key == 'name': dict[key] = 'Dell denies Bieksa\'s one-timer'#continue
		if key == 'url': dict[key] = 'https://nhl.bamcontent.com/nhl/id/v1/45179303/details/web-v1.json'#continue
		if key == 'mode': dict[key] = 'play'#continue
		if key == 'duration': dict[key] = '9'#continue
		if key == 'type': dict[key] = 'video'#continue
		if key == 'thumb': dict[key] = 'https://nhl.bamcontent.com/images/photos/282520130/640x360/cut.jpeg'#continue
		#"""
		"""
		if isinstance(dict[key], basestring):
			dict[key] = dict[key]#.encode('utf8')
		else:
			dict[key] = str(dict[key])
		"""
		#u += key.encode('utf8') + '=' + urllib.quote_plus(dict[key])
	xbmc.log(u)
	#return 'plugin://plugin.video.nhlvideocenter/?plot=Kevin+Bieksa+fires+a+one-timer+on+net%2C+but+Aaron+Dell+quickly+gets+across+for+the+save+to+keep+the+Sharks+ahead+midway+through+the+2nd&name=Dell+denies+Bieksa%27s+one-timer&url=https%3A%2F%2Fnhl.bamcontent.com%2Fnhl%2Fid%2Fv1%2F45179303%2Fdetails%2Fweb-v1.json&mode=play&duration=9&type=video&thumb=https%3A%2F%2Fnhl.bamcontent.com%2Fimages%2Fphotos%2F282520130%2F640x360%2Fcut.jpeg'
	#return 'plugin://plugin.video.nhlvideocenter/?url=https%3A%2F%2Fsearch-api.svc.nhl.com%2Fsvc%2Fsearch%2Fv2%2Fnhl_global_en%2Ftopic%2F277774732%3Fpage%3D1%26sort%3Dnew%26type%3Dvideo%26hl%3Dfalse%26expand%3Dimage.cuts.640x360%252Cimage.cuts.1136x640&type=dir&mode=listVideos'
	return u
	
def _airedISO8601A(dict):
	xbmc.log(dict['airedISO8601'])
	iso = dict['airedISO8601']			
	try:
		tempdate = datetime.strptime(iso[:19], '%Y-%m-%dT%H:%M:%S')
	except TypeError:#workaround:
		tempdate = datetime(*(time.strptime(iso[:19], '%Y-%m-%dT%H:%M:%S')[0:6]))
	offset = iso[-6:]
	log(offset)
	HH,MM = offset[1:].split(':')
	delta = timedelta(hours=int(HH),minutes=int(MM))
	if offset.startswith('+'):
		tempdate += delta
	else:
		tempdate -= delta
	return tempdate.strftime('%Y-%m-%d'), tempdate.strftime('%H:%S')
	
def _airedISO8601(dict):
	iso = dict['airedISO8601']			
	try:
		tempdate = datetime.strptime(iso[:19], '%Y-%m-%dT%H:%M:%S')
	except TypeError:#workaround:
		tempdate = datetime(*(time.strptime(iso[:19], '%Y-%m-%dT%H:%M:%S')[0:6]))
	offset = iso.replace(':','')[-5:]
	log(offset)
	HH = offset[1:3]
	MM = offset[4:5]
	delta = timedelta(hours=int(HH),minutes=int(MM))
	if offset.startswith('+'):
		tempdate += delta
	else:
		tempdate -= delta
	return tempdate.strftime('%Y-%m-%d'), tempdate.strftime('%H:%S')
	
	
def get_params():
	param={}
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]= urllib.unquote_plus(splitparams[1])

	return param