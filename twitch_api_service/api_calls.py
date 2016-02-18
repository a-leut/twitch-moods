import requests

# TODO: cache results (longer timeout for emoticons)

def _get_channels_json():
    r = requests.get('https://api.twitch.tv/kraken/streams')
    return r.json()['streams']

def _get_emoticons_json():
    r = requests.get('https://api.twitch.tv/kraken/chat/emoticons')
    return r.json()

def get_top_channel_names(limit=100):
    channels_json = _get_channels_json()
    return [c['channel']['name'] for c in channels_json[:limit]]

def get_emoticons_list():
    emoticons_json = _get_emoticons_json()
    emoticons = {}
    for e in emoticons_json['emoticons']:
        emoticons[e['regex']] = e['images'][0]['url']
    return emoticons
