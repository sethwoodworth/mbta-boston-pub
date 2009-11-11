import twitter
import yaml

# load twitter account info
f = open('accounts.yml')
t_lines = yaml.load(f)

def connect_line(color):
    un = t_lines[color]['account']
    pw = t_lines[color]['password']
    api = twitter.Api(username=un, password=pw)
    status = api.PostUpdate('Howl')

connect_line('blue')
connect_line('green')
