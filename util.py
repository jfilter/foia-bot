"""utility functions"""
import json


def save_json(filename, data):
    """save json file"""
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def read_json(filename):
    """open json file"""
    data = None
    with open(filename, 'r') as infile:
        data = json.load(infile)
    return data
