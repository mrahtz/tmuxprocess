import os
import sys
import tempfile
from multiprocessing import Process


class TmuxProcess(Process):
    session_name = None

    def __init__(self, *args, **kwargs):
        tmpdir = tempfile.mkdtemp()
        out_fname = os.path.join(tmpdir, 'stdout')
        in_fname = os.path.join(tmpdir, 'stdin')
        os.mkfifo(out_fname)
        os.mkfifo(in_fname)

        cmd = 'cat {} & cat > {}'.format(out_fname, in_fname)
        if 'mode' in kwargs:
            if kwargs['mode'] == 'out_only':
                cmd = 'cat {}'.format(out_fname)
            del kwargs['mode']

        Process.__init__(self, *args, **kwargs)

        if TmuxProcess.session_name is None:
            TmuxProcess.session_name = str(os.getpid())
            os.system("tmux new-session -s {} -n {} -d '{}'".
                      format(TmuxProcess.session_name, self.name, cmd))
        else:
            os.system("tmux new-window -n {} '{}'".format(self.name, cmd))
        self.session_name = TmuxProcess.session_name

        # buffering=1 gives line buffering
        self.out_fifo = open(out_fname, 'w', buffering=1)
        self.in_fifo = open(in_fname, 'r', buffering=1)

    def run(self):
        sys._stdout = sys.stdout
        sys._stdin = sys.stdin
        sys.stdout = self.out_fifo
        sys.stdin = self.in_fifo
        Process.run(self)
