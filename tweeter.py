import twitter
import yaml
import urllib
import urllib2

# load twitter account info
f = open('accounts.yml')
t_lines = yaml.load(f)

def connect_line(color):
    un = t_lines[color]['account']
    pw = t_lines[color]['password']
    api = twitter.Api(username=un, password=pw)
    status = api.PostUpdate('Howl')

def statusnet(color, text):
    un = 
    url = 'https://identi.ca/api/statuses/update.xml'
    status = 'status=' + urllib.urlencode(text)

curl -u sethish:mingstad -d "status=playing with cURL" https://identi.ca/api/statuses/update.xml


connect_line('blue')
connect_line('green')
