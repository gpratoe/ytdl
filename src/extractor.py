import re
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import execjs
import json

class Extractor:
    def __init__(self, videoId):
        self.videoId = videoId
        self.video_json = self._get_video_json(videoId)
        self.formats = self._get_video_formats(videoId)
        self.playerUrl = self._get_player_url(videoId)
        self.challenge = self._get_challenge(videoId)
    def _get_video_json(self,videoId):
        url = f'https://www.youtube.com/youtubei/v1/player'
        data = {
            "videoId": videoId,
            "context": {
                "client": {
                    "clientName": "MWEB",
                    "clientVersion": "2.20231129.01.00"
                }
            }
        }
        response = requests.post(url, json=data)
        
        return response.json()
    
    def _get_video_formats(self, videoId):
        formats = self.video_json['streamingData']['adaptiveFormats']
        return formats

    def _get_player_url(self, videoId):
        response = requests.get(f'https://www.youtube.com/embed/{videoId}')

        pattern = r'\/s\/player\/(\w+)\/player_ias.vflset\/\w+\/base.js'
        match = re.search(pattern, response.text)
        player_hash = match.group(1)
        return f'https://www.youtube.com/s/player/{player_hash}/player_ias.vflset/en_US/base.js'

    def _get_challenge(self, videoId):
        playerUrl = self._get_player_url(videoId)

        response_txt = requests.get(playerUrl).text

        challenge_name = re.search(r'\.get\("n"\)\)&&\(b=([a-zA-Z0-9$]+)(?:\[(\d+)\])?\([a-zA-Z0-9]\)', response_txt).group(1)
        challenge_name = re.search(r'var {}\s*=\s*\[(.+?)\]\s*[,;]'.format(challenge_name), response_txt).group(1)

        challenge_pattern = r'{}\s*=\s*function\s*\(([\w$]+)\)\s*{{(.+?)\s*return\s*[\w$]+\.join\(""\)}};'.format(challenge_name)
        challenge = re.search(challenge_pattern, response_txt, re.DOTALL).group(0)

        challenge = re.sub(r'^\w+\s*=\s*', '', challenge)
        challenge = re.sub(r';$', '', challenge)

        return challenge
    def parse_formats(self):
        res = "{:<3} | {:<10} | {:<5}".format("TAG", "FORMAT", "QUALITY") + "\n"
        res += "{:<3}|{:<10}|{:<5}".format("----","------------","--------") + "\n"
        for format in self.formats:
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
    
    def _get_format_info(self, tag):
        return next(info for info in self.formats if info['itag'] == tag)

    def get_format_url(self, tag):
        formatInfo = self._get_format_info(tag)
        url = formatInfo['url']
        return url
    
    def solve_challenge(self, formatUrl):
        
        parsed_url = urlparse(formatUrl)

        query_params = parse_qs(parsed_url.query)

        n = query_params['n'][0]

        n_transformed = execjs.eval(f"(({self.challenge})(String('{n}')).split)('{{ return a; }}')")[0]

        
        query_params['n'][0] = n_transformed

        encoded_query_params = urlencode(query_params, doseq=True)
        updated_url = urlunparse(parsed_url._replace(query=encoded_query_params))    

        return updated_url
    
    def get_video_length(self):
        return int(self.video_json['videoDetails']['lengthSeconds'])