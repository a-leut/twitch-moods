import requests

# TODO: cache api results in redis (longer timeout for emoticons)

def _get_channels_json():
    r = requests.get('https://api.twitch.tv/kraken/streams')
    return r.json()['streams']

def _get_emoji_json():
    r = requests.get('https://api.twitch.tv/kraken/chat/emoticons')
    return r.json()

def get_top_channel_names(limit=100):
    channels_json = _get_channels_json()
    return ['#' + c['channel']['name'] for c in channels_json[:limit]]

def get_emoji_names_urls():
    emoticons_json = _get_emoji_json()
    names, urls = [], []
    for e in emoticons_json['emoticons']:
        names.append(e['regex'])
        urls.append(e['images'][0]['url'])
    return names, urls
