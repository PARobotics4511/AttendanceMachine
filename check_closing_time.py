import time
import datetime
import subprocess

def check():
    if(datetime.datetime.now().time() >= datetime.time(16,00)):
        subprocess.call(["omxplayer", "-o", "local", "-l", "0057", "../../Downloads/Closing_Time.mp3"])