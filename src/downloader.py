import requests
import os
import time
from tqdm import tqdm

class Downloader:
    def __init__(self):
        pass
    def download_file(self, url, filename):
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

    def download_video(self, video_url, audio_url):
        self.download_file(video_url, "video_out")
        self.download_file(audio_url, "audio_out")
        # todo: merge audio and video