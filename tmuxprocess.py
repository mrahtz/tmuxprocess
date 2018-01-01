import os
import sys
import tempfile
from multiprocessing import Process


class TmuxProcess(Process):
    tmux_sess = None

    def __init__(self, mode='outonly', *args, **kwargs):
        tmpdir = tempfile.mkdtemp()

        out_fname = os.path.join(tmpdir, 'stdout')
        os.mkfifo(out_fname)
        
        if mode == 'outonly':
            cmd = 'cat {}'.format(out_fname)
        elif mode == 'inout':
            in_fname = os.path.join(tmpdir, 'stdin')
            os.mkfifo(in_fname)
            cmd = 'cat {} & cat > {}'.format(out_fname, in_fname)
        else:
            raise ValueError("invalid mode '%s'" % mode)
        self.mode = mode

        Process.__init__(self, *args, **kwargs)

        if TmuxProcess.tmux_sess is None:
            TmuxProcess.tmux_sess = str(os.getpid())
            # self.name refers to Process.name (e.g. "TmuxProcess-1")
            # -d: start detached
            os.system("tmux new-sess -s {} -n {} -d '{}'".
                      format(TmuxProcess.tmux_sess, self.name, cmd))
        else:
            # There doesn't seem to be an easy way to create a new window
            # in a specific sesssion - only to create one in the current tmux_sess.
            # So we just have to hope the user doesn't interact with tmux
            # before the creation of the last process.
            # -d: don't make the new window current (so that when the user
            #     attaches the first process is shown)
            os.system("tmux new-window -d -n {} '{}'".format(self.name, cmd))
        self.tmux_sess = TmuxProcess.tmux_sess

        # buffering=1 gives line buffering
        self.out_fifo = open(out_fname, 'w', buffering=1)
        if mode != 'outonly':
            self.in_fifo = open(in_fname, 'r', buffering=1)


    def run(self):
        sys._stdout = sys.stdout
        sys.stdout = self.out_fifo
        if self.mode == 'inout':
            sys._stdin = sys.stdin
            sys.stdin = self.in_fifo
        Process.run(self)
