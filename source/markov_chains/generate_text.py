"""
generate some text from a markov model
"""

import random

import util
import posified_text

# MODEL_PATH = "models/model_2.json"
MODEL_PATH = "models/model_failed_msg_2.json"
# MODEL_PATH = "models/model_failed_msg_pos_2.json"


def generat_text():
    model_json = util.read_json(MODEL_PATH)

    model = posified_text.POSifiedText.from_json(model_json)

    # generate seed so the randomnes changes every time the script gets executed
    random.seed(a=None, version=2)

    for _ in range(20):
        print(model.make_short_sentence(200))

def main():
    generat_text()

if __name__ == "__main__":
    main()
