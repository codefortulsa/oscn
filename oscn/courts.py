import requests
import functools

from bs4 import BeautifulSoup

saved_courts = [
    'adair',
    'alfalfa',
    'appellate',
    'atoka',
    'beaver',
    'beckham',
    'blaine',
    'bryan',
    'caddo',
    'canadian',
    'carter',
    'cherokee',
    'choctaw',
    'cimarron',
    'cleveland',
    'coal',
    'comanche',
    'cotton',
    'craig',
    'creek',
    'bristow',
    'drumright',
    'custer',
    'delaware',
    'dewey',
    'ellis',
    'garfield',
    'garvin',
    'grady',
    'grant',
    'greer',
    'harmon',
    'harper',
    'haskell',
    'hughes',
    'jackson',
    'jefferson',
    'johnston',
    'kay',
    'poncacity',
    'kingfisher',
    'kiowa',
    'latimer',
    'leflore',
    'lincoln',
    'logan',
    'love',
    'major',
    'marshall',
    'mayes',
    'mcclain',
    'mccurtain',
    'mcintosh',
    'murray',
    'muskogee',
    'noble',
    'nowata',
    'okfuskee',
    'oklahoma',
    'okmulgee',
    'henryetta',
    'osage',
    'ottawa',
    'payne',
    'pawnee',
    'pittsburg',
    'pontotoc',
    'pottawatomie',
    'pushmataha',
    'rogermills',
    'rogers',
    'seminole',
    'sequoyah',
    'stephens',
    'texas',
    'tillman',
    'tulsa',
    'wagoner',
    'washington',
    'washita',
    'woods',
    'woodward']


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9'
    }

@functools.lru_cache()
def courts():
    try:
        response = requests.get('https://www.oscn.net/dockets/',headers=headers,verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form', action = 'Results.aspx')
        select = form.find('select', id='db')
        options = select.find_all('option')
        court_vals = [ option['value'] for option in options ]
        court_vals.remove('all')
        return court_vals
    except:
        return saved_courts
