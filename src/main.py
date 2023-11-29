import requests
import sys
import json
from tqdm import tqdm
import time
import os
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import execjs
from extractor import Extractor

script_name = sys.argv[0]
videoId = sys.argv[1]




def download_file(url, filename):
    for tries in range(1,4):
        try:
            fileExists = os.path.exists(filename)
            
            downloadedRange = os.path.getsize(filename) if fileExists else 0

            rangeHeader = {'Range': f'bytes={downloadedRange}-'} if fileExists else {}

            with requests.get(url, headers=rangeHeader, stream=True) as response:
                response.raise_for_status()

                total_size = int(response.headers.get('content-length', 0))
                
                with open(filename, 'wb') as local_file, tqdm(
                    desc= f'Downloading {filename}',
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    initial=downloadedRange
                ) as progressbar:
                    
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            local_file.write(chunk)
                            progressbar.update(len(chunk))
                
                print(f'Download completed: {filename}')
                break
        except requests.exceptions.RequestException as e:
            
            print(f"Error during download: {e}")
            if tries < 3:
                print(f"Retrying in 3 seconds...")
                time.sleep(3)




def download_video(video_url, audio_url):
    download_file(video_url, "video_out")
    download_file(audio_url, "audio_out")
    # todo: merge audio and video

def main():
    ext = Extractor(videoId)
    
    res = ext.parse_formats()
    print(res)

    tag_video = int(input("ingrese tag de video: "))
    tag_audio = int(input("ingrese tag de audio: "))
    
    video_url = ext.get_format_url(tag_video)
    audio_url = ext.get_format_url(tag_audio)
    
    download_video(ext.solve_challenge(video_url), ext.solve_challenge(audio_url))

main()
