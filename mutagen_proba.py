import requests
import os
import yt_dlp
from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC, ID3NoHeaderError

def find_info_music(question):
    url = f"https://itunes.apple.com/search?term={question}&limit=1&entity=song"
    odgovor = requests.get(url).json()
    
    if odgovor['resultCount'] > 0:
        res = odgovor['results'][0]
        #print(res)
        pic_url = res['artworkUrl100'].replace('100x100bb', '600x600bb')
        picture_bits = requests.get(pic_url).content
    
        return {
            'artist': res['artistName'],
            'title': res['trackName'],
            'album': res['collectionName'],
            'cover_data': picture_bits
        }
    
    return None

def add_covers_and_tags(mp3_path, info):
    try:
        tags = ID3(mp3_path)
    except ID3NoHeaderError:
        tags = ID3()

    tags.add(TIT2(encoding=3, text=info['title']))
    tags.add(TPE1(encoding=3, text=info['artist']))
    tags.add(TALB(encoding=3, text=info['album']))
    tags.add(
    APIC(
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc='Cover',
            data=info['cover_data']
        )
    )
    tags.save(mp3_path)
    print("Info is ready")


def proces_song(query):
    info = find_info_music(query)

    if info:
        file_name = f"{info['artist']} - {info['title']}"
    else:
        file_name = query

            #URLS = ['https://www.youtube.com/watch?v=YE7VzlLtp-4']

    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch1',
        'outtmpl': f'music/{file_name}.%(ext)s', #dodacemo sve pesme u music folder
        'postprocessors': [{  
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
        }],
        'quiet': True #da smanjim ispis na terminalu
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch1:{query}"])

    mp3_path = f"music/{file_name}.mp3"

    if info and os.path.exists(mp3_path):
        add_covers_and_tags(mp3_path, info)
        print(f" Downloaded with tags: {file_name}")
    else:
        print(f" Downloaded without tags: {file_name}")

    return mp3_path

    

#search = "Big Buck Bunny"
#path_to_file = "music/Big Buck Bunny.mp3" 
#info = find_info_music(search)

#if info:
#    print(f"Found: {info['artist']} - {info['title']} ({info['album']})")
 #   add_covers_and_tags(path_to_file, info)
#else:
#    print("No info")