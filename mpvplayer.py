import os
import os.path
import json
import psutil

from settings import readsettings
from settings import writesettings

def ismpvplayerplaying():
    for pid in psutil.pids():
        p=psutil.Process(pid)
        if 'mpv'in p.name():
            mpvactive=True
            break
        else:
            mpvactive=False
    return mpvactive

#Function to manage mpv start volume
def mpvplayergetvolume():
    mpvvolume=readsettings('mpvplayer','volume')
    return mpvvolume

def mpvplayeradjustvolume(mpvvolumelevel):
    if ismpvplayerplaying():
       if mpvvolumelevel < mpvplayergetvolume():
          os.system('echo \'{ "command": ["set_property", "volume", "'+ mpvvolumelevel +'"] }\' | socat - /tmp/mpvsocket')

def mpvplayerrestorevolume(mpvvolumelevel):
    if ismpvplayerplaying():
       os.system('echo \'{ "command": ["set_property", "volume", "'+ mpvvolumelevel +'"] }\' | socat - /tmp/mpvsocket')

def mpvplayersetvolume(mpvvolumelevel):
    if ismpvplayerplaying():
       os.system('echo \'{ "command": ["set_property", "volume", "'+ mpvvolumelevel +'"] }\' | socat - /tmp/mpvsocket')
    writesettings('mpvplayer','volume',mpvvolumelevel)

def mpvplayermute():
    mpvplayersetvolume("0")

def mpvplayerunmute():
    mpvplayersetvolume("70")

def mpvplayer(mpvvolume,mediaurl):
    mediaurl=("'"+mediaurl+"'")
    os.system('mpv --really-quiet --volume='+str(mpvvolume)+' '+ mediaurl)

def mpvplayerstop():
    if ismpvplayerplaying():
       os.system('echo \'{"command": ["quit"]}\' | socat - /tmp/mpvsocket')

def mpvplayercycle():
    if ismpvplayerplaying():
       os.system('echo \'{"command": ["cycle", "pause"]}\' | socat - /tmp/mpvsocket')
