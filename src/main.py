import requests
import sys
import json

#   {
#     "itag": 251,
#     "url": "https://rr1---sn-p2a5o-jvgl.googlevideo.com/videoplayback?expire=1701201219&ei=4_BlZf2GLMDZ1sQPwJGfyA8&ip=2800%3A40%3A37%3A42b%3Aa022%3Ab1c4%3Ac9b7%3A21b0&id=o-AN5UunsMM22un0V1VEI67AAXM3mEn_youtfIe7Ll8hyI&itag=251&source=youtube&requiressl=yes&mh=Qf&mm=31%2C29&mn=sn-p2a5o-jvgl%2Csn-x1x7dn7s&ms=au%2Crdu&mv=m&mvi=1&pl=48&initcwndbps=202500&spc=UWF9f7qV20wgghjtPiS3_bkmKPFp4_H7cO_qsQsnow&vprv=1&svpuc=1&mime=audio%2Fwebm&ns=DgxpX_8c4qzbggrb0Tf5wE8P&gir=yes&clen=5772821&dur=380.041&lmt=1700883937971314&mt=1701179126&fvip=1&keepalive=yes&fexp=24007246&c=WEB&txp=5532434&n=ooa6S2sRXnZF4YQo&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&sig=ANLwegAwRQIgOd7Kc1r4M4-iZSYuucNw_2s0oyxMOMVbLQ0VBzuS_-gCIQCEubrlavwMyP-q6LkVSuoVRYC4p8h8ldAPtnrxc-jm8A%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AM8Gb2swRgIhAMYa9ue-vzRlM4XJERfhIa-1ZHyPNXG7JdxuWiq_fr8lAiEA8Tcodh00ddY0kf4f7sTjeDQ_kiANwfQsgGv6PVA4vZ8%3D",
#     "mimeType": "audio/webm; codecs=\"opus\"",
#     "bitrate": 209600,
#     "initRange": {
#       "start": "0",
#       "end": "265"
#     },
#     "indexRange": {
#       "start": "266",
#       "end": "925"
#     },
#     "lastModified": "1700883937971314",
#     "contentLength": "5772821",
#     "quality": "tiny",
#     "projectionType": "RECTANGULAR",
#     "averageBitrate": 121519,
#     "audioQuality": "AUDIO_QUALITY_MEDIUM",
#     "approxDurationMs": "380041",
#     "audioSampleRate": "48000",
#     "audioChannels": 2,
#     "loudnessDb": -3.8199997
#   }


script_name = sys.argv[0]
videoId = sys.argv[1]

def get_video_formats(videoId):
    url = f'https://www.youtube.com/youtubei/v1/player'
    data = {
        "videoId": videoId,
        "context": {
            "client": {
                "clientName": "WEB",
                "clientVersion": "2.20230810.05.00"
            }
        }
    }
    response = requests.post(url, json=data)
    formats = response.json()['streamingData']['adaptiveFormats']
    return formats

def parse_formats(formats):
    res = "{:<3} | {:<10} | {:<5}".format("TAG", "FORMAT", "QUALITY") + "\n"
    res += "{:<3}|{:<10}|{:<5}".format("----","------------","--------") + "\n"
    for format in formats:
        
        itag = str(format['itag'])
        mimeType = str(format['mimeType'])
        mediaFormat = mimeType.split(";")[0]
        
        qualityLabel = (format['qualityLabel']
                          if mediaFormat.split("/")[0] == "video" 
                          else "")
        
        audioQuality = (format['audioQuality'].removeprefix("AUDIO_QUALITY_").lower() 
                         if mediaFormat.split("/")[0] == "audio" 
                         else "")
        

        formatedLine = "{:<3} | {:<10} | {:<5}".format(itag,
                                                           mediaFormat,
                                                             qualityLabel if mediaFormat.split("/")[0] == "video" else audioQuality)
        
        res += formatedLine + '\n'
    return res

def download_video(itagv, itaga, formats):
    videoUrl = next(info['url'] for info in formats if info['itag'] == itagv)
    audioUrl = next(info['url'] for info in formats if info['itag'] == itaga)
    print(f'vidurl:{videoUrl}')
    print(f'audurl:{audioUrl}')
    pass

def main():
    formats = get_video_formats(videoId)
    res = parse_formats(formats)
    print(res)

    itagv = int(input("ingrese tag de video: "))
    itaga = int(input("ingrese tag de audio: "))
    download_video(itagv,itaga,formats)

main() 
