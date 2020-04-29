import urllib.request
import simplejson

def get_beatmap(key, id):
    url = f"https://osu.ppy.sh/api/get_beatmaps?k={key}&b={id}"
    response = urllib.request.urlopen(url)
    map_data = simplejson.load(response)
    return map_data[0]