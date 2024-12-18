import re
import json
from unicodedata import normalize


def clean_string(some_string):
    # Normalize unicode characters
    normal_str = normalize("NFKD", some_string)
    # Remove all types of whitespace by splitting and rejoining
    condensed = ' '.join(normal_str.split())
    return condensed

def text_values(ResultSet):
    return [clean_string(el.text) for el in ResultSet]


def column_titles(thead):
    return [hdr for hdr in map(lambda str: str.lower(), text_values(thead))]


def add_properties(obj, names, values):
    for idx, value in enumerate(values):
        setattr(obj, names[idx], value)


def lists2dict(keys, values):
    return {k: v for k, v in map(lambda k, v: (k, v), keys, values)}


def old_find_values(soup, key_names):
    key_values = []
    for key in key_names:
        key_found = soup.find(string=re.compile(f"{key}:"))
        key_value = key_found.split(":")[1] if key_found else ""
        key_values.append(clean_string(key_value))
    return lists2dict(key_names, key_values)


def find_values(soup, key_names):
    """
    Find key word in soup and return a dictionary of key value pairs
    """
    return {
        key: clean_string((match := soup.find(string=lambda text: text and f"{key}:" in text)) and match.split(":", 1)[1].strip() or "")
        for key in key_names
    }



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


def table2dict(bs4_table):
    get_text = lambda el: clean_string(el.text)
    header = bs4_table.thead.find_all("th")
    data = bs4_table.tbody.find_all("td")
    keys = map(get_text, header)
    values = map(get_text, data)
    new_dict = {k: v for k, v in zip(keys, values)}
    return new_dict
