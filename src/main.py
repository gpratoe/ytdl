import sys
from extractor import Extractor
from downloader import Downloader

script_name = sys.argv[0]
videoId = sys.argv[1]


def main():
    ext = Extractor(videoId)
    dwnloader = Downloader()

    res = ext.parse_formats()
    print(res)

    tag_video = int(input("ingrese tag de video: "))
    tag_audio = int(input("ingrese tag de audio: "))
    
    video_url = ext.get_format_url(tag_video)
    audio_url = ext.get_format_url(tag_audio)

    dwnloader.download_video(ext.solve_challenge(video_url), ext.solve_challenge(audio_url))

main()
