import re


def judge(oscn_html):
    judge_re = r'Judge:\s*([\w\s\,]*)'
    find_judge = re.compile(judge_re, re.M)
    judge_search = find_judge.search(oscn_html)
    if judge_search.group:
        return judge_search.group(1)
    else:
        return None

setattr(judge,'target',['OSCNrequest'])
