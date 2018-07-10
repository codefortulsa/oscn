import oscn.parse

fp = open("examples/case.html")

party_list = oscn.parse.parties(fp)

for party in party_list:
    print(party)
