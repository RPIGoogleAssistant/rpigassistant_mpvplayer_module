import os
import os.path
import json

from settings import readsettings
from settings import writesettings

#Function to manage mpv start volume
def mpvplayergetvolume():
    mpvvolume=readsettings('mpvplayer','volume')
    return mpvvolume

def mpvplayersetvolume(mpvvolumelevel):
    os.system('echo \'{ "command": ["set_property", "volume", "'+ mpvvolumelevel +'"] }\' | socat - /tmp/mpvsocket')
    writesettings('mpvplayer','volume',mpvvolumelevel)

def mpvplayermutevolume(mpvvolumelevel):
    os.system('echo \'{ "command": ["set_property", "volume", "0"] }\' | socat - /tmp/mpvsocket')

def mpvplayer(mpvvolume,mediaurl):
    mediaurl=("'"+mediaurl+"'")
    os.system('mpv --really-quiet --volume='+str(mpvvolume)+' '+ mediaurl)

def mpvplayerstop():
    os.system('echo \'{"command": ["quit"]}\' | socat - /tmp/mpvsocket')

def mpvplayerpause():
    os.system('echo \'{"command": ["cycle", "pause"]}\' | socat - /tmp/mpvsocket')
