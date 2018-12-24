import json

class Artist():
    def __init__(self, json_object):
        self.id = json_object.id
        self.name  = name