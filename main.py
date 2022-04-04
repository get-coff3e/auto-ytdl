from __future__ import unicode_literals
import os
import json
import yt_dlp
from urllib.parse import urlparse
from datetime import datetime
#try:
#    from rich import print
#except:
#    pass
# rich is not required, but it looks nice

INPUTFILE = 'channels.json'


def fileValidation():
    with open(INPUTFILE) as f:
        if not os.path.exists(INPUTFILE):
            print(f"{INPUTFILE} not found. Add entries in before continuing")
            f.write('{\n\t"channels": [\n\t]\n}')
            f.close()
        c_load = json.load(f)
        c = c_load['channels']

        if not len(c):
            print("No entries to download")
            exit()
        else:
            print(f"# of Channels: {len(c)}")
        return c


if __name__ == "__main__":
    c = fileValidation()
    storedHour = datetime.now().hour

    while len(c):
        currentHour = datetime.now().hour
        
        if currentHour != storedHour:
            print(f"Time changed:\tHour {currentHour}:00:00")
            storedHour = datetime.now().hour

        for entry in c:
            website = urlparse(entry).hostname

            OUTTMPL = f"Download/{website}/%(channel)s/%(playlist)s/%(title)s/%(id)s.%(ext)s"
            YDL_OPTS = {
                'format': 'bestvideo/best',
                'outtmpl': OUTTMPL,
                #'verbose': True,
                'ignoreerrors': True,
                'quiet': True,
                'writedescription': True,
                'writeinfojson': True,
                'writeannotations': True,
                'writethubmnail': True,
                'writesubtitles': True
            }

            with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
                info_dict = ydl.extract_info(entry, download=False)
                channel_name = info_dict.get("url", None)

                if not os.path.exists(f'Download/{website}/{channel_name}') or currentHour != storedHour:
                    print(f"Downloading {channel_name} from {website}")
                    try:
                        ydl.download(entry)
                    except KeyboardInterrupt:
                        pass
