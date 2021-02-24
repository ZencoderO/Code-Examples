# -*- coding: utf-8 -*-

"""
preprocess-twitter.py

python preprocess-twitter.py "Some random text with #hashtags, @mentions and http://t.co/kdjfkdjf (links). :)"

Script for preprocessing tweets by Romain Paulus
with small modifications by Jeffrey Pennington
with translation to Python by Motoki Wu

Translation of Ruby script to create features for GloVe vectors for Twitter data.
http://nlp.stanford.edu/projects/glove/preprocess-twitter.rb
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import sys
import regex as re

FLAGS = re.MULTILINE | re.DOTALL

mapemoji = dict()
listOfSmileFace = ["\U0001f4af","\U0001f525", "\U0001f64c", "\u263a","\u263b","\U0001f603","\U0001f604","\U0001f605","\U0001f60a","\U0001f60e","\U0001f607","\U0001f608","\U0001f60b","\U0001f60f","\U0001f60c","\U0001f601","\U0001f600"]
listOFNeutral = ["\U0001f606","\U0001f643","\U0001f610","\U0001f611","\U0001f914","\U0001f644","\U0001f62e","\U0001f614","\U0001f616","\U0001f615"]
listOfSadFace = ["\u2639","\U0001f626","\U0001f622","\U0001f62d","\U0001f912","\U0001f915"]
lol = ["\U0001f602","\U0001f923","\U0001f920","\U0001f921","\U0001f911"]
heart = ["\U0001f618","\U0001f60d", "\U0001f60d"]

def hashtag(text):
    text = text.group()
    hashtag_body = text[1:]
    if hashtag_body.isupper():
        result = "<hashtag> {} <allcaps>".format(hashtag_body)
    else:
        result = " ".join(["<hashtag>"] + re.split(r"(?=[A-Z])", hashtag_body, flags=FLAGS))
    return result

def allcaps(text):
    text = text.group()
    return text.lower() + " <allcaps>"

def replace_all(text):
    for i in listOfSmileFace:
        text = text.replace(i, "<smile>")
    for i in listOFNeutral:
        text = text.replace(i, "<neutralface>")
    for i in listOfSadFace:
        text = text.replace(i, "<sadface>")
    for i in lol:
        text = text.replace(i, "<lolface>")
    for i in heart:
        text = text.replace(i, "<heart>")
    return text

def preprocess(text):
    # Different regex parts for smiley faces
    eyes = r"[8:=;]"
    nose = r"['`\-]?"

    def re_sub(pattern, repl):
        return re.sub(pattern, repl, text, flags=FLAGS)

    text = text.encode('unicode-escape')
    # Seperating the Emojis
    text = " \U".join(text.split("\U"))
    text = re_sub(r"{}{}p+".format(eyes, nose), "<lolface>")
    text = re_sub(r"{}{}\(+|\)+{}{}".format(eyes, nose, nose, eyes), "<sadface>")
    text = re_sub(r"{}{}[\/|l*]".format(eyes, nose), "<neutralface>")
    text = replace_all(text)
    text = text.decode('unicode-escape')

    # Remove fancy emoticons
    text = "".join(text.split('“'))
    text = "".join(text.split('”'))
    text = text.lower()
    text = text.split()
    df2 = []
    # Removing the User from the list
    for data in text:
        if not data[0] == "@":
            df2.append(data)
    text = " ".join(df2)
    # Remove special character
    # function so code less repetitive

    text = re_sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", "<url>")
    text = re_sub(r"/", "/")
    text = re_sub(r"@\w+", "<user>")
    text = re_sub(r"#\S+", hashtag)
    text = re_sub(r"[-+]?[.\d]*[\d]+[:,.\d]*", "<number>")
    text = re_sub(r"([!?.]){2,}", r"\1 <repeat>")
    text = re_sub(r"\b(\S*?)(.)\2{2,}\b", r"\1\2 <elong>")
    text = re_sub(r"\'ve", " \'ve")

    ## -- I just don't understand why the Ruby script adds <allcaps> to everything so I limited the selection.
    # text = re_sub(r"([^a-z0-9()<>'`\-]){2,}", allcaps)
    text = re_sub(r"([A-Z]){2,}", allcaps)

    return text.lower()
