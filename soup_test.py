import re
from bs4 import BeautifulSoup

fp = open("examples/multi_count.html")
soup = BeautifulSoup(fp, 'html.parser')

count_details = re.compile(r'Count as Filed:[.\n\s]*([A-Z]+)\,.(.+)\,[\n\s\w\:\D]*Date of Offense\:.([\d\/]*)',re.M)

counts = soup.find_all('td', 'CountDescription')

for count in counts:
    count.a.extract()
    details = count_details.search(count.text)
    import ipdb; ipdb.set_trace()
    print(details.group(1))
    print(count.text)
