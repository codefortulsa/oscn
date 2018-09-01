import re

from .. import settings

find_judge = re.compile(r'Judge:\s*([\w\s\,]*)', re.M)
find_titles = re.compile('|'.join(settings.REMOVE_TITLES))
find_name_parts = re.compile(r'(\w+\.*)', re.I)

def judge(oscn_html):
    judge_search = find_judge.search(oscn_html)
    if judge_search.group:
        found_name = judge_search.group(1).upper()
        found_name = find_titles.sub('', found_name)
        if re.search(',', found_name):
            return found_name
        else:
            name_parts = find_name_parts.findall(found_name)
            last_name = name_parts.pop()
            if name_parts == []:
                return last_name
            found_name = last_name + ', ' + ' '.join(name_parts)
            return found_name
    else:
        return None

setattr(judge, 'target', ['Case'])
