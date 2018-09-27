import os
import sys
import tempfile
from multiprocessing import Process


class TmuxProcess(Process):
    tmux_sess = None

    def __init__(self, mode='outonly', *args, **kwargs):
        tmpdir = tempfile.mkdtemp()
        if mode not in ['outonly', 'inout']:
            raise ValueError("Invalid mode '{}'".format(mode))
        self.mode = mode

        self.out_fifos = {}
        out_fnames = {}
        for name in ['stdout', 'stderr']:
            out_fnames[name] = os.path.join(tmpdir, name)
            os.mkfifo(out_fnames[name])
        if mode == 'inout':
            in_fname = os.path.join(tmpdir, 'stdin')
            os.mkfifo(in_fname)

        cmd = 'cat {} & cat {}'.format(out_fnames['stdout'], out_fnames['stderr'])
        if mode == 'inout':
            cmd += ' & cat > {}'.format(in_fname)

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

        # Done /after/ attaching to the pipes, so that open doesn't block
        # buffering=1 gives line buffering
        for name in ['stdout', 'stderr']:
            self.out_fifos[name] = open(out_fnames[name], 'w', buffering=1)
        if mode == 'inout':
            self.in_fifo = open(in_fname, 'r', buffering=1)

    def run(self):
        sys._stdout = sys.stdout
        sys._stderr = sys.stderr
        sys.stdout = self.out_fifos['stdout']
        sys.stderr = self.out_fifos['stderr']
        if self.mode == 'inout':
            sys._stdin = sys.stdin
            sys.stdin = self.in_fifo
        Process.run(self)
