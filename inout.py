#!/usr/bin/env python

from __future__ import print_function
from six.moves import input
from tmuxprocess import TmuxProcess

def f(name):
    print("{} running".format(name))
    while True:
        s = input()
        print("{} read:".format(name), s)

p1 = TmuxProcess(target=f, mode='inout', args=("f1", ))
print("Run")
print("  tmux attach -t {}".format(p1.tmux_sess))
print("to interact with each process.")
p1.start()
p2 = TmuxProcess(target=f, mode='inout', args=("f2", ))
p2.start()
