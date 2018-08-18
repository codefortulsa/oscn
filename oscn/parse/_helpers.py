from unicodedata import normalize

def clean_string(some_string):
    # removes escape chars and excess spaces
    normal_str = normalize('NFKD',some_string)
    return normal_str.strip()
    
def text_values(ResultSet):
    text_list =[]
    for el in ResultSet:
        text_list.append(clean_string(el.text))
    return text_list

def add_properties(obj, names, values):
    for idx, value in enumerate(values):
        setattr(obj, names[idx], value)
