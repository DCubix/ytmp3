import os, sys
from pytube import YouTube
from moviepy.editor import VideoFileClip

from pytube.innertube import _default_clients

_default_clients["ANDROID"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["ANDROID_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_MUSIC"]["context"]["client"]["clientVersion"] = "6.41"
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

outDir = "temp"

def downloadYouTube(videourl):
    yt = YouTube(videourl)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    yt.download(outDir)
    print("Downloaded: ", yt.default_filename)
    return yt.default_filename

def convertToMP3(filename, trimStartHMS, trimEndHMS):
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    mp4 = VideoFileClip(os.path.join(outDir, filename))

    if trimStartHMS and trimEndHMS:
        trimStartHMS = tuple([int(x) for x in trimStartHMS.split(':')])
        trimEndHMS = tuple([int(x) for x in trimEndHMS.split(':')])
        mp4 = mp4.subclip(trimStartHMS, trimEndHMS)

    filenameMp3 = filename.replace(".mp4", ".mp3")
    mp4.audio.write_audiofile(os.path.join(outDir, filenameMp3))

    mp4.close()

    print("Converted: ", filenameMp3)
    return filenameMp3

if len(sys.argv) < 2:
    print("Usage:\n\tpython ytmp3.py <youtube-url> [start-time] [end-time]\n\tpython ytmp3.py videos.txt")
    sys.exit(1)

def processCommand(cmd: str):
    spl = cmd.strip().split()
    while len(spl) < 3:
        spl.append(None)
    url, trimStartHMS, trimEndHMS = spl

    fileName = downloadYouTube(url)
    convertToMP3(fileName, trimStartHMS, trimEndHMS)

    # delete video
    os.remove(os.path.join(outDir, fileName))

command = ' '.join(sys.argv[1:]).strip()

if command.endswith(".txt"):
    with open(command, 'r') as f:
        for line in f:
            if line.strip() == "" or line.strip().startswith("#"):
                continue
            processCommand(line)
else:
    processCommand(' '.join(sys.argv[1:]))
