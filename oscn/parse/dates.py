import re

def filed(oscn_html):
    pattern = r'Filed:\s*([\w\s\,]*)'
    find = re.compile(pattern, re.M)
    search = find.search(oscn_html)
    if search.group:
        return search.group(1)
    else:
        return None

setattr(filed,'target',['OSCNrequest'])


def closed(oscn_html):
    pattern = r'Closed:\s*([\w\s\,]*)'
    find = re.compile(pattern, re.M)
    search = find.search(oscn_html)
    try:
        if search.group:
            return search.group(1)

    except AttributeError:
        return None

setattr(closed,'target',['OSCNrequest'])
