def text_values(ResultSet):
    text_list =[]
    for el in ResultSet:
        text_list.append(el.text.strip())
    return text_list

def add_properties(obj, names, values):
    for idx, value in enumerate(values):
        setattr(obj, names[idx], value)
