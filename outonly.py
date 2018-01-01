#!/usr/bin/env python3

from __future__ import print_function
import time
from tmuxprocess import TmuxProcess

def f(name):
    print("{} running".format(name))
    while True:
        print("{} sleeping".format(name))
        time.sleep(1)

p1 = TmuxProcess(target=f, args=("f1", ))
print("Run")
print("  tmux attach -t {}".format(p1.tmux_sess))
print("to interact with each process.")
p1.start()
p2 = TmuxProcess(target=f, args=("f2", ))
p2.start()
