"""addings POS to the text class"""
import re

import markovify
import spacy


nlp = spacy.load("de_core_news_sm")

pattern = []

# https://github.com/jfilter/german-abbreviations
# respect cases here
with open("/Users/filter/code/german-abbreviations/german_abbreviations.txt") as f:
    list_of_abbr = f.readlines()

for a in list_of_abbr:
    a = a.strip()
    pattern.append(a)

    # only do it abbr. that are short to not fuck it up with e.g. 'berlin.'
    if len(a) < 6:
        a_up = a[0].upper() + a[1:]
        pattern.append(a_up)
    # for abbr. with a space, remove it also add it
    if " " in a:
        pattern.append(a.replace(" ", ""))

        a = a.replace(" ", "")
        a_up = a[0].upper() + a[1:]
        pattern.append(a_up)

# add new ones that were not coverd
new = ["o.a.", "Ref.", "Nrn.", "no.", "I.",
       "II.", "III.", "i.v.m.", "u.g.", "Rn.", "z.K.", "iSd.", "SVerf."]

remove = ["an."]

pattern.extend(new)

pattern.remove("an.")

pattern = [p.replace('*', '\\*') for p in pattern]

abbr_patter = re.compile("^(" + "|".join(pattern) + ")$")


def is_abbreviation(word):
    if word[0] == '(':
        word = word[1:]
    return abbr_patter.match(word)


def is_ordinal(word):
    return re.match("^(\.?\d+)*.$", word)


def is_sentence_ender(word):
    if word[-1] in ["?", "!"]:
        return True
    if is_ordinal(word):
        return False
    # ignore words with only one char
    if len(word) < 3:
        return False
    return word[-1] == "." and not is_abbreviation(word)


def find_greeting(sentence):
    match = re.search(
        '(Sehr geehrte.*,)|(Sehr geehrtAntragsteller/in)|Guten Tag Herr Antragsteller/in', sentence, re.IGNORECASE)
    if match:
        g = match.groups()
        return match.start(), match.end()
    return None, None


def remove_greetings(s):
    start_index, end_index = find_greeting(s)
    if start_index is None:
        return [s]
    else:
        first = s[:start_index].strip()
        second = s[end_index:].strip()
        second = second[0].upper() + second[1:]
        return [*remove_greetings(first), *remove_greetings(second)]


def split_into_sentences(text):
    text = text.replace('„', '"').replace('“', '"').replace('"', '')
    text = text.replace(' . ', '. ')

    text = re.sub('\s+', ' ', text)  # subsitute multi whitespaces into 1

    text = re.sub("(Mit freundlichen Grüßen|Mit freundlichem Gruß|Freundlicher Gruß|Freundliche Grüße|Viele Grüße|Mit freundlichen Grüssen),?",
                  "", text, count=0, flags=re.IGNORECASE)

    potential_end_pat = re.compile(r"".join([
        r"([\w\.'’&\]\)]+[\.\?!])",  # A word that ends with punctuation
        r"([‘’“”'\"\)\]]*)",  # Followed by optional quote/parens/etc
        # followed by whitespace
        r"(\s+)",
    ]), re.U)
    dot_iter = re.finditer(potential_end_pat, text)
    end_indices = [(x.start() + len(x.group(1)) + len(x.group(2)))
                   for x in dot_iter
                   if is_sentence_ender(x.group(1))]
    spans = zip([None] + end_indices, end_indices + [None])
    sentences = [text[start:end].strip() for start, end in spans]

    sentences = [s for s in sentences if 'Ursprüngliche Nachricht' not in s]

    final_sentences = []

    for s in sentences:
        final_sentences.extend(remove_greetings(s))

    return final_sentences


class POSifiedText(markovify.Text):
    # def word_split(self, sentence):
    #     return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    # def word_join(self, words):
    #     sentence = " ".join(word.split("::")[0] for word in words)
    #     return sentence

    def test_sentence_input(self, sentence):
        return len(sentence) > 10

    def sentence_split(self, text):
        """
        Splits full-text string into a list of sentences.
        """

        # results = [sent.string.strip() for sent in nlp(text).sents]
        results = split_into_sentences(text)

        with open('sentences.txt', 'w') as file_handler:
            for item in results:
                file_handler.write("{}\n".format(item))

        return results
