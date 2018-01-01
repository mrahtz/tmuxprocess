TmuxProcess
===========

If you're prototyping with multiple processes all trying to send debug prints to
the same terminal, things can get very confusing.

``TmuxProcess`` is an extension of the ``multiprocessing`` ``Process`` class which
automatically sets up a tmux session with a separate tmux window for each
process created. With standard output for each process linked to a separate window,
it's much easier to keep track of what each individual process is doing.
(Standard input can also be tied to each separate window, so you can also send
different commands to different processes.)

Requirements
------------

tmux, and that's it!

Installation
------------

::

  pip install tmuxprocess

Usage
-----

If you only care about standard output being redirected::

    from tmuxprocess import TmuxProcess
    import time

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

Input and output from the main process will remain on the launching terminal.
When the first process is created, a new tmux session will be launched in the
background, a new tmux window created in that session, and standard output
redirected to that window. When the second process is created, a second tmux
window will be created in the same session, and its standard output similarly
redirected.

If you also want standard input redirection, initialise with ``mode='inout'``::

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

However, with this mode, because of the way that standard input redirection
is implemented, note that you will have to manually kill the session
once done.
