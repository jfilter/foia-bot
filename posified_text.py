"""addings POS to the text class"""
import re

import markovify
import spacy

ascii_lowercase = "abcdefghijklmnopqrstuvwxyz"
ascii_uppercase = ascii_lowercase.upper()

nlp = spacy.load("de_core_news_sm")


pattern = []

# https://github.com/jfilter/german-abbreviations
# respect cases here
with open("/Users/filter/code/german-abbreviations/german_abbreviations.txt") as f:
    list_of_abbr = f.readlines()

for a in list_of_abbr:
    a = a.strip()
    pattern.append(a)
    # for abbr. with a space, remove it also add it
    if " " in a:
        pattern.append(a.replace(" ", ""))

# add new ones that were not coverd
new = ["o.a.", "Ref.", "Nrn.", "no.", "I.", "II.", "III."]

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
    return re.match("^(\d)+.$", word)

def is_sentence_ender(word):
    if word[-1] in ["?", "!"]:
        return True
    if is_ordinal(word):
        return False
    # ignore words with only one char
    if len(word) < 3:
        return False
    return word[-1] == "." and not is_abbreviation(word)

# print(is_sentence_ender('erfragen.'))

def split_into_sentences(text):
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
    return sentences


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

    def test_sentence_input(self, sentence):
        return len(sentence) > 10

    def sentence_split(self, text):
        """
        Splits full-text string into a list of sentences.
        """
        text = text.replace('„', '"').replace('“', '"').replace('"', '')
        text = text.replace(' . ', '. ')

        text = re.sub('\s+', ' ', text) # subsitute multi whitespaces into 1

        # results = [sent.string.strip() for sent in nlp(text).sents]
        results = split_into_sentences(text)
        print('\n'.join(results))
        return results


# print(split_into_sentences("""Seit dem Jahr 2009 wird das zunächst europäische Projekt URA aus dem Jahr 2006 als national finanziertes Bund - Länder - Rückkehrprojekt URA 2 fortgesetzt.
#             Im Rahmen dieses Projektes können freiwillige Rückkehrer und Rückgeführte aus den beteiligten Bundesländern Baden - Württemberg, Niedersachsen, Nordrhein - Westfalen und Sachsen - Anhalt sowie zueinem geringen Teil auch Einheimische eine Unterstützung erhalten.
#             Weitere Informationen zu dem Projekt sowie der Flyer für das Projektjahr 2011 sind auf der Internetseite des Bundesamtes (www.bamf.de < http: // www.bamf.de > ) zu finden. zu d) Für die Zurückschiebung und die Durchführung der Abschiebung sind gemäß § 71 Abs. 4 und Abs. 5 Aufenthaltsgesetz die Ausländerbehörden, die mit der polizeilichen Kontrolle des grenzüberschreitenden Verkehrs beauftragten Behörden und, soweit erforderlich, die Polizei der Länder zuständig.
#       Nähere Auskünfte sind bei den angegebenen Stellen zu erfragen. zu e) Im Rahmen der vom Bundesamt durchgeführten Reintegrationsmaßnahmen werden für Rückkehrer keine Häuser erworben oder gebaut."""))
