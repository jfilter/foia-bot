"""
build markov model from json file
"""

from markov_chains import util
from markov_chains import posified_text


def build_model(corpus_path, model_base_path, state_size=2):
    """
    create and save markov chain model
    """
    data = util.read_json(corpus_path)

    text = " ".join([d["content"] for d in data])
    text_model = posified_text.POSifiedText(text, state_size=state_size)

    util.save_json(f"{model_base_path}_{state_size}.json", text_model.to_json())
