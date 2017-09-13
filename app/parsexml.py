from bs4 import BeautifulSoup

soup = BeautifulSoup(open('example_ttml.xml'), 'html.parser')
result = [(p['begin'], p['end'], p.text) for p in soup.find_all('p')]

for x in result:
    link = 'https://youtu.be/linktovideo?t='
    link = link + x[0][0:2] + 'h' + x[0][3:5] + 'm' + x[0][6:8] + 's'
    print(link, x[0], x[1], x[2])
