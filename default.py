#!  /usr/bin/python
#   Title: samsungremote.py
#   Author: Asif Iqbal
#   Date: 05APR2012
#   Info: To send remote control commands to the Samsung tv over LAN
#   TODO:
 
import socket
import base64
import time, datetime
import xbmc
import xbmcaddon
import xbmcgui
import os
import simplejson
import socket

__addon__ = xbmcaddon.Addon()
__cwd__ = __addon__.getAddonInfo('path')
__scriptname__ = __addon__.getAddonInfo('name')
__version__ = __addon__.getAddonInfo('version')
__icon__ = __addon__.getAddonInfo('icon')
__ID__ = __addon__.getAddonInfo('id')
__language__ = __addon__.getLocalizedString


tvip = "192.168.1.250"
#IP Address of TV
myip = "192.168.1.50"
#Used for the access control/validation, but not after that AFAIK
mymac = "00-01-80-65-BE-A3"
#What the iPhone app reports
appstring = "iphone..iapp.samsung"
#Might need changing to match your TV type
tvappstring = "iphone.UE50ES5500.iapp.samsung"
#What gets reported when it asks for permission
remotename = "XBMC Samsung Remote by xtoxico"
 


global g_jumpBackSecs
g_jumpBackSecs = 0

# Function to send keys
def sendKey(skey, dataSock, appstring):
  messagepart3 = chr(0x00) + chr(0x00) + chr(0x00) + chr(len(base64.b64encode(skey))) + chr(0x00) + base64.b64encode(skey);
  part3 = chr(0x00) + chr(len(appstring)) + chr(0x00) + appstring + chr(len(messagepart3)) + chr(0x00) + messagepart3 dataSock.send(part3);

def log(msg):
  xbmc.log("### [%s] - %s" % (__scriptname__,msg,),level=xbmc.LOGDEBUG )

def getSetting(setting):
  return __addon__.getSetting(setting).strip()

#log( "[%s] - Version: %s Started" % (__scriptname__,__version__))

class MyPlayer( xbmc.Player ):
  def __init__( self, *args, **kwargs ):
    xbmc.Player.__init__( self )
    #log('MyPlayer - init')
  
  def onPlayBackStarted( self ):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((tvip, 55000))
    ipencoded = base64.b64encode(myip)
    macencoded = base64.b64encode(mymac)
    messagepart1 = chr(0x64) + chr(0x00) + chr(len(ipencoded)) + chr(0x00) + ipencoded + chr(len(macencoded)) + chr(0x00) + macencoded + chr(len(base64.b64encode(remotename))) + chr(0x00) + base64.b64encode(remotename)
    part1 = chr(0x00) + chr(len(appstring)) + chr(0x00) + appstring + chr(len(messagepart1)) + chr(0x00) + messagepart1
    sock.send(part1)
    messagepart2 = chr(0xc8) + chr(0x00)
    part2 = chr(0x00) + chr(len(appstring)) + chr(0x00) + appstring + chr(len(messagepart2)) + chr(0x00) + messagepart2
    sock.send(part2)
    sendKey("KEY_HDMI1",sock,tvappstring)
    time.sleep(1)
    sock.close()

player_monitor = MyPlayer()

while not xbmc.abortRequested:
      xbmc.sleep(100)







 



