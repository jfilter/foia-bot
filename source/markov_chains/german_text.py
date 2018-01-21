"""
modified orginally Text class to better peform on German text
"""

import random
import markovify

from markov_chains import util
from markov_chains import sentence_boundary_detection

# MODEL_PATH = "models/model_2.json"
MODEL_PATH = "models/model_failed_msg_2.json"
# MODEL_PATH = "models/model_failed_msg_pos_2.json"

# import spacy
# nlp = spacy.load("de_core_news_sm")


class GermanText(markovify.Text):
    """
    overwrite orignal implementation which was focues on English
    """
    # def word_split(self, sentence):
    #     return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    # def word_join(self, words):
    #     sentence = " ".join(word.split("::")[0] for word in words)
    #     return sentence

    def test_sentence_input(self, sentence):
        return len(sentence) > 7

    def sentence_split(self, text):
        """
        Splits full-text string into a list of sentences.
        """

        # results = [sent.string.strip() for sent in nlp(text).sents]
        results = sentence_boundary_detection.split_into_sentences(text)

        with open('sentences/1.txt', 'w') as file_handler:
            for item in results:
                file_handler.write("{}\n".format(item))

        return results


def generat_text():
    model = setup_model(MODEL_PATH)

    for _ in range(20):
        print(model.make_short_sentence(200))


def setup_model(path):
    model_json = util.read_json(path)

    model = GermanText.from_json(model_json)

    # generate seed so the randomnes changes every time the script gets executed
    random.seed(a=None, version=2)
    return model


def build_model(corpus_path, model_base_path, state_size=2):
    """
    create and save markov chain model
    """
    data = util.read_json(corpus_path)

    text = " ".join([d["content"] for d in data])
    text_model = GermanText(text, state_size=state_size)

    util.save_json(f"{model_base_path}_{state_size}.json",
                   text_model.to_json())
