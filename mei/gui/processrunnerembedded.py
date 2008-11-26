import os
import processrunner

class ProcessRunnerEmbedded(processrunner.ProcessRunner):
    def draw(self, screen):
        if not self._pid:
            self._start()

        os.waitpid(self._pid, 0)
        self._quit()

    def _start(self):
        self._pid = os.fork()
        if self._pid == 0:
            os.chdir(self._path)
            os.execvp(self._cmd[0], self._cmd)
            sys.exit(0)

    def _quit(self):
        if self._pid:
            os.kill(self._pid, signal.SIGKILL)

        self._app.windows.pop()
