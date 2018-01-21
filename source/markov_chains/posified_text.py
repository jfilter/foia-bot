"""
addings POS to the text class
"""

import markovify
# import spacy

from markov_chains import sentence_boundary_detection

# nlp = spacy.load("de_core_news_sm")


class POSifiedText(markovify.Text):
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
