# working script. given a youtube channel, download all of the videos and thumbnails to a directory
from pytube import YouTube
from pytube import Channel
import urllib.request
import time,os
from pathlib import Path
c = Channel('https://www.youtube.com/c/killtony/videos') # replace this url with the channel you want videos from
video_count = len(c.videos)
#print(f"There are {video_count} episodes for this channel")
my_failed_vids = open("failed_to_download.txt","a+")
replacements = {"\\":"","\/":"","(":"",")":"","KILL TONY #":"KILL TONY "}

for video in c.videos:
    title = video.title
    for k,v in replacements.items():
        title = title.replace(k,v)
    video_number = title.split(' ')[2]
    file_to_check_for = (f"/home/media/podcasts/killtony/{title}.mp4")
    try:
        file_to_check_for = (f"/home/media/podcasts/killtony/{title}.mp4")
        already_downloaded = os.path.isfile(file_to_check_for)
        urllib.request.urlretrieve(video.thumbnail_url, f"/home/media/podcasts/killtony/{title}.jpg")
    except:
        try:
            title = str(title).replace("\\","")
            title = str(title).replace("/","")
            file_to_check_for = (f"/home/media/podcasts/killtony/{title}.mp4")
            already_downloaded = os.path.isfile(file_to_check_for)
            urllib.request.urlretrieve(video.thumbnail_url, f"/home/media/podcasts/killtony/{title}.jpg")
        except:
            pass
    if already_downloaded:
        print("eww, I already have this, Im not going to download it again\n")
        print(file_to_check_for)
        pass
    else:
        try:
            print(f"OHHHHH I FOUND ONE, IMMA GET IT!\n{title}\n")
            myyt_video = video.streams.get_highest_resolution()
            myyt_video.download("/home/media/podcasts/killtony/")
            print("Done, on to the next one")
        except:
            failed_to_download = f"{title} {video_number}\n"
            my_failed_vids.write(failed_to_download)
            print("\nbollocks\n")
print("done")
my_failed_vids.close()
