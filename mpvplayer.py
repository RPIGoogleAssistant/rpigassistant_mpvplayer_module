import os
import os.path
import json
import psutil

from settings import readsettings
from settings import writesettings

#Global variable used for track skipping
global skipamount 
skipamount = 0

#Check if mpv player is playing
def ismpvplayerplaying():
    for pid in psutil.pids():
        p=psutil.Process(pid)
        if 'mpv' in p.name():
            mpvactive=True
            break
        else:
            mpvactive=False
    return mpvactive

#Function get mpv player volume from mpvplayer.json
def mpvplayergetvolume():
    mpvvolume=readsettings('mpvplayer','volume')
    return mpvvolume

#Adjust mpv player volume temporarily (not saved to mpvplayer.json)
#restore to previous value using mpvplayerrestorevolume
def mpvplayeradjustvolume(mpvvolumelevel):
    if ismpvplayerplaying():
       if int(mpvvolumelevel) < int(mpvplayergetvolume()):
          os.system('echo \'{ "command": ["set_property", "volume", "'+ mpvvolumelevel +'"] }\' | socat - /tmp/mpvsocket')

#Restore to volume set in mpvplayer.json
def mpvplayerrestorevolume(mpvvolumelevel):
    if ismpvplayerplaying():
       os.system('echo \'{ "command": ["set_property", "volume", "'+ mpvvolumelevel +'"] }\' | socat - /tmp/mpvsocket')

#Permanenlty set volume to mpvplayer.json
def mpvplayersetvolume(mpvvolumelevel):
    if ismpvplayerplaying():
       os.system('echo \'{ "command": ["set_property", "volume", "'+ mpvvolumelevel +'"] }\' | socat - /tmp/mpvsocket')
    writesettings('mpvplayer','volume',mpvvolumelevel)

#Mute
def mpvplayermute():
    mpvplayersetvolume("0")

#Unmute
def mpvplayerunmute():
    mpvplayersetvolume("70")

#Play from url with volume level mpvvolume
def mpvplayer(mpvvolume,mediaurl):
    mediaurl=("'"+mediaurl+"'")
    os.system('mpv --really-quiet --volume='+str(mpvvolume)+' '+ mediaurl)

#Stop mpv player
def mpvplayerstop():
    if ismpvplayerplaying():
       os.system('echo \'{"command": ["quit"]}\' | socat - /tmp/mpvsocket')

#Pause/Unpause
def mpvplayercycle():
    if ismpvplayerplaying():
       os.system('echo \'{"command": ["cycle", "pause"]}\' | socat - /tmp/mpvsocket')

#Stop mpvplayer and set Global variable skipamount
def mpvplayerskip(skipby):
    mpvplayersetskip(skipby)
    mpvplayerstop()

#Get how many tracks to skip
def mpvplayergetskip():
    return int(skipamount)

#Set how many tracks to skip
def mpvplayersetskip(skipby):
    global skipamount
    skipamount = int(skipby)
