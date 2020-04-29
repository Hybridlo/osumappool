import json
from .misc.Mods import Mods
from .misc.ApiCalls import get_beatmap

class CustomizableTextContainer():
    '''Mappool, modpool and a map has customizable settings
       the lower the object is in the relationship, the higher
       the priority of the settings: if modpool has setting for
       text color, and a map in a modpool has another text color
       then on that map text will have the color specified
       for that map. All other maps, if they don't override it too,
       will have the color specified in modpool settings'''
    def __init__(self):
        self.settings = {}

    def set_setting(self, setting_name, setting_value):
        self.setting[setting_name] = setting_value

class Map(CustomizableTextContainer):
    def __init__(self, map_data):
        CustomizableTextContainer.__init__(self)
        self.map_id = int(map_data["beatmap_id"])
        self.star_rating = round(float(map_data["difficultyrating"]), 2)
        self.full_name = map_data["artist"] + " - " + map_data["title"] + " [" + map_data["version"] + "]"
        self.mapper = map_data["creator"]
        self.map_length = int(map_data["total_length"])
        self.bpm = int(map_data["bpm"])

    @staticmethod
    def get_from_id(key, id):
        return Map(get_beatmap(key, id))

class Modpool(CustomizableTextContainer):
    def __init__(self, mods):
        CustomizableTextContainer.__init__(self)
        self.mods = mods
        self.maps = []

class Mappool(CustomizableTextContainer):
    def __init__(self):
        CustomizableTextContainer.__init__(self)
        self.modpools = []
    
    def add_map(self, mods, map):
        for modpool in self.modpools:
            if modpool.mods == mods:
                modpool.add_map(map)    #if found the modpool with needed mods, add map to it
                return
        
        new_modpool = Modpool(mods)     #create a new one otherwise
        new_modpool.add_map(map)

        self.modpools.append(new_modpool)