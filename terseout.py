from nose.plugins import Plugin
import traceback as t


class TerseOutPlugin(Plugin):
    name = 'terseout'

    def __init__(self):
        self.stream = None
        super().__init__()

    def addError(self, test, err):
        self._report('error', test, err)

    def addFailure(self, test, err):
        self._report('failure', test, err)

    def _report(self, err_or_failure, test, err):
        error_type, error, traceback = err
        self.stream.writeln('{location}: {message}'.format(
            location=self._location(traceback),
            message=str(error) or repr(error),
        ))

    def _location(self, traceback):
        tb = t.extract_tb(traceback)

        selected = tb[-1]

        file_, line, func, statement = selected
        return '{}:{}'.format(file_, line)

    def setOutputStream(self, stream):
        class NullStream:
            def write(self, *arg, **kwargs):
                pass

            def writeln(self, *arg, **kwargs):
                pass

            def flush(self, *arg, **kwargs):
                pass

        self.stream = stream
        return NullStream()
