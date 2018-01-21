"""build markov model from json file"""
import re

import markovify
import spacy

import util
import posified_text

data = util.read_json('/Users/filter/code/fds-util/data/suc_msg.json')

text = " ".join([d["content"] for d in data])

# Build the model.

state_size = 2

text_model = posified_text.POSifiedText(text, state_size=state_size)

util.save_json(f'models/model_{state_size}.json', text_model.to_json())
