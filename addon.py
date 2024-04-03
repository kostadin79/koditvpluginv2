# -*- coding: utf-8 -*-
import urllib.request as urllib
import os
from re import compile as Compile
from xbmc import log
from xbmcgui import Dialog
from xbmcswift2 import Plugin
from xbmcaddon import Addon
from xbmcvfs import translatePath
from settings import *

ADDON_PATH=ADDON_PATH = translatePath(Addon().getAddonInfo('path'))
TV_THUMBNAIL_DIR = os.path.join(ADDON_PATH, 'resources', 'media')

plugin=Plugin()

opener=urllib.build_opener(urllib.HTTPHandler,urllib.HTTPRedirectHandler())
urllib.install_opener(opener)

@plugin.route('/')
def index():
    items=[]
    for tv in TV_LIST:
        try:
            source=openUrl(tv['url'])
        except:
            source=None
        if source:
            iframe_url = DOMAIN + Compile('<iframe src="(.+?)"').findall(source)[0]
            thumbnail=os.path.join(TV_THUMBNAIL_DIR, tv['thumbnail'])
            items.append({'label':tv['title'],'thumbnail': thumbnail,'path': plugin.url_for('index_source',url=iframe_url,name=tv['title'],icon=thumbnail,referer_url=tv['url'])})
        else:
         log('No source!!!!')
    return plugin.finish(items)
 
@plugin.route('/stream/<url>/<name>/<icon>/<referer_url>')
def index_source(url,name,icon,referer_url):
    source=openUrl(url,referer_url)
    stream_url=Compile('file:"(.+?)"').findall(source)
    item={'label':name,'path':stream_url[0]}
    plugin.play_video(item)
    Dialog().notification(name,'',icon,8000,sound=False)
    return plugin.finish(None,succeeded=False)

def openUrl(url,add_referer_url=''):
    req=create_request(url)
    if add_referer_url:
        req.add_header('Referer', add_referer_url)
    response=urllib.urlopen(req)
    source=response.read().decode('utf-8')
    response.close()
    return source


def create_request(url):
    req=urllib.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
    req.add_header('Accept-Language','en-US,en;q=0.9')
    req.add_header('Cache-Control','no-cache')
    req.add_header('Pragma','no-cache')
    return req


if __name__ == '__main__':
    plugin.run()