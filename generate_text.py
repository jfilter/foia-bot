"""generate some text"""

import random

import markovify

import util
import posified_text

model_json = util.read_json('models/model_2.json')

reconstituted_model = posified_text.POSifiedText.from_json(model_json)

random.seed(a=None, version=2)


# Print five randomly-generated sentences
for i in range(5):
    print(reconstituted_model.make_sentence())

# Print three randomly-generated sentences of no more than 140 characters


for i in range(5):
    print(reconstituted_model.make_short_sentence(140))

for i in range(5):
    print(reconstituted_model.make_sentence())

# Print three randomly-generated sentences of no more than 140 characters


for i in range(5):
    print(reconstituted_model.make_short_sentence(140))

for i in range(5):
    print(reconstituted_model.make_short_sentence(270))
