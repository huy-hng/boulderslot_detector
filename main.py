# %%
# from bs4 import BeautifulSoup
from requests_html import HTMLSession

# %%
# r = requests.get('https://darmstadt.studiobloc.de/bloc-slots/')
session = HTMLSession()

# r = session.get('https://darmstadt.studiobloc.de/bloc-slots/')
# text = r.html.render()

r = session.get('http://python-requests.org')
r.html.render()
r.html.search('Python 2 will retire in only {months} months!')['months']

# soup = BeautifulSoup(text, 'lxml')
# with open('test.html', 'w') as f:
# 	f.write(r.text)
# match = soup.find('div', class_='drp-calendar-weeks')
# print(match)