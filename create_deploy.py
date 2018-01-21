"""
pip install markovify -t $(pwd)
pip install python-twitter -t $(pwd)
"""

from os import walk
import shutil

files = ["source/tweet.py", "source/config.py"]
dir = "source/markov_chains"
models = ["models/no_2.json", "models/yes_2.json"]

def change_imports(text):
    text = text.replace("from markov_chains ", "")
    for m in models:
        text = text.replace(m, change_path(m))
    return text


def change_path(path):
    new_start_index = path.rfind('/')
    new_path = path[new_start_index + 1:]
    return new_path

for m in models:
    shutil.copyfile(m, 'dist/' + change_path(m))


for (dirpath, dirnames, filenames) in walk(dir):
    files.extend([ dir + '/' + fn for fn in filenames])
    break

print(files)

for f in files:
    text = None
    with open(f, 'r') as infile:
        text = infile.read()
    text = change_imports(text)

    new_path = 'dist/' + change_path(f)

    with open(new_path, 'w') as outfile:
        outfile.write(text)

