"""
build markov model from json file
"""

import util
import posified_text

CORPUS_PATH = "/Users/filter/code/fds-util/data/suc_msg.json"
MODEL_BASE_PATH = "models/model"


def build_model(state_size=2):
    """
    create and save markov chain model
    """
    data = util.read_json(CORPUS_PATH)

    text = " ".join([d["content"] for d in data])
    text_model = posified_text.POSifiedText(text, state_size=state_size)

    util.save_json(f"{MODEL_BASE_PATH}_{state_size}.json", text_model.to_json())


def main():
    build_model()


if __name__ == "__main__":
    main()
