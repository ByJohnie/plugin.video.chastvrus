# -*- coding: utf-8 -*-
#Библиотеки, които използват python и Kodi в тази приставка
import re
import sys
import os
import urllib
import urllib2
import xbmc, xbmcplugin,xbmcgui,xbmcaddon
import base64

#Място за дефиниране на константи, които ще се използват няколкократно из отделните модули
__addon_id__= 'plugin.video.chastvrus'
__Addon = xbmcaddon.Addon(__addon_id__)
MUA = 'Mozilla/5.0 (Linux; Android 5.0.2; bg-bg; SAMSUNG GT-I9195 Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Version/1.0 Chrome/18.0.1025.308 Mobile Safari/535.19' #За симулиране на заявка от мобилно устройство
UA = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0' #За симулиране на заявка от  компютърен браузър
REF = base64.b64decode("aHR0cHM6Ly9jaGFzLnR2")

#Меню с директории в приставката
def CATEGORIES():
        baseurl = REF
        req = urllib2.Request(baseurl)
        req.add_header('User-Agent', UA)
        response = urllib2.urlopen(req)
        #print 'request page url:' + url
        data=response.read()
        response.close()
        match = re.compile('<a href="(.+?)">.*\n.*src="(.+?)"').findall(data)
        for url,thumbnail in match:
         matchd = re.compile('channel/(.*)').findall(url)
         for title in matchd:
          thumbnail = REF + thumbnail
          url = REF + url
          addLink(title,url,2,thumbnail)




#Разлистване видеата на първата подадена страница
def INDEXPAGES(url):

                        ""


#Зареждане на видео
def PLAY(name,url,iconimage):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        response = urllib2.urlopen(req)
        data=response.read()
        response.close()
        br = 0 #Брояч
        match = re.compile('uid."videoplayer",file."(.+?)"').findall(data)
        for link in match:
         li = xbmcgui.ListItem(iconImage=iconimage, thumbnailImage=iconimage, path=link)
         li.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
         li.setInfo('video', { 'title': name })
         try:
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
         except:
            xbmc.executebuiltin("Notification('Грешка','Видеото липсва на сървъра!')")






#Модул за добавяне на отделно заглавие и неговите атрибути към съдържанието на показваната в Kodi директория - НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty("IsPlayable" , "true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok



#Модул за добавяне на отделна директория и нейните атрибути към съдържанието на показваната в Kodi директория - НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


#НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def get_params():
        param=[]
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
                                param[splitparams[0]]=splitparams[1]
                                
        return param







params=get_params()
url=None
name=None
iconimage=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        name=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass


#Списък на отделните подпрограми/модули в тази приставка - трябва напълно да отговаря на кода отгоре
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
    
elif mode==1:
        print ""+url
        INDEXPAGES(url)

elif mode==2:
        print ""+url
        PLAY(name,url,iconimage)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
