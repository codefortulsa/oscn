import re
import json
from unicodedata import normalize


def clean_string(some_string):
    # Normalize unicode characters
    normal_str = normalize("NFKD", some_string)
    # Remove all types of whitespace by splitting and rejoining
    condensed = ' '.join(normal_str.split())
    return condensed


def add_properties(obj, names, values):
    for idx, value in enumerate(values):
        setattr(obj, names[idx], value)


def lists2dict(keys, values):
    return dict(zip(keys, values))


# class to allow adding metadata to returned lists
class MetaList(list):
    saved_text = ""

    @property
    def text(self):
        return self.saved_text

    @text.setter
    def text(self, new_text):
        self.saved_text = clean_string(new_text)

    def add_text(self, more_text):
        self.text += clean_string(more_text)
