"""
split text into sentences

part is c & p from the orignal implementation
"""

import re


def setup_pattern():
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

    return re.compile("^(" + "|".join(pattern) + ")$")


def is_abbreviation(word, pattern):
    """
    checks if the words it an abbr
    """
    if word[0] == '(':
        word = word[1:]
    return pattern.match(word)


def is_ordinal(word):
    """
    checks if the word is an ordinal
    """
    return re.match(r"^(\.?\d+)*.$", word)


def is_sentence_ender(word, abbr_pattern):
    """
    checks if the words ends the sentence
    """
    if word[-1] in ["?", "!"]:
        return True
    if is_ordinal(word):
        return False
    # ignore words with only one char
    if len(word) < 3:
        return False
    return word[-1] == "." and not is_abbreviation(word, abbr_pattern)


def find_greeting(sentence):
    """
    returns the start and end position of the greetings, if found. Otherwise, returns None.
    """
    match = re.search(
        r'(Sehr geehrte.*,)|(Sehr geehrtAntragsteller/in)|Guten Tag Herr Antragsteller/in',
        sentence, re.IGNORECASE)
    if match:
        g = match.groups()
        return match.start(), match.end()
    return None, None


def remove_greetings(sentence):
    """
    removes greetings from the sentence and splits the sentence into two, if found
    """
    start_index, end_index = find_greeting(sentence)
    if start_index is None:
        return [sentence]
    else:
        first = sentence[:start_index].strip()
        second = sentence[end_index:].strip()
        second = second[0].upper() + second[1:] # Ensures the senteces starts with an uppercase char
        return [*remove_greetings(first), *remove_greetings(second)]


def clean_input(text):
    """
    returnes cleaned text
    """
    text = text.replace('„', '"').replace('“', '"').replace('"', '')
    text = text.replace(' . ', '. ')

    text = re.sub(r'\s+', ' ', text)  # subsitute multi whitespaces into 1

    # remove valediction
    text = re.sub(r"((Mit )?freundliche(n|m|r)?|Viele) Gr(ü(ß|ss)en?|uß),?",
                  "", text, count=0, flags=re.IGNORECASE)
    return text


def clean_senteces(sentences):
    """
    returns cleaned sentences
    """
    sentences = [s for s in sentences if 'Ursprüngliche Nachricht' not in s]
    final_sentences = []

    for sent in sentences:
        final_sentences.extend(remove_greetings(sent))

    return final_sentences


def split_into_sentences(text):
    """
    splits text and returns a list of sentences
    """
    text = clean_input(text)

    abbr_pattern = setup_pattern()

    potential_end_pat = re.compile(r"".join([
        r"([\w\.'’&\]\)]+[\.\?!])",  # A word that ends with punctuation
        r"([‘’“”'\"\)\]]*)",  # Followed by optional quote/parens/etc
        r"(\s+)",  # Followed by whitespace
        # MODIFIED BY JFILTER, ALSO MATCHES WHEN THE NEXT SENT STARTS WITH LOWER CASE
    ]), re.U)
    dot_iter = re.finditer(potential_end_pat, text)
    end_indices = [(x.start() + len(x.group(1)) + len(x.group(2)))
                   for x in dot_iter
                   if is_sentence_ender(x.group(1), abbr_pattern)]
    spans = zip([None] + end_indices, end_indices + [None])
    sentences = [text[start:end].strip() for start, end in spans]
    sentences = clean_senteces(sentences)
    return sentences
