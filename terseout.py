from nose.plugins import Plugin
import traceback
import os
import re


class TerseOutPlugin(Plugin):
    name = 'terseout'

    def __init__(self):
        self.stream = None
        self.basepath = os.getcwd()
        super().__init__()

    def options(self, parser, env):
        super().options(parser, env)
        parser.add_option("--print-stack", action="store_true",
                          default=False, help="Print stacktrace for errors")

    def configure(self, options, conf):
        self.print_stack = options.print_stack
        super().configure(options, conf)

    def addError(self, test, err):
        self._report('error', test, err)

    def addFailure(self, test, err):
        self._report('failure', test, err)

    def _report(self, err_or_failure, test, err):
        error_type, error, tb = err
        file_, line, *_ = self._first_local_stackframe(tb)
        self.stream.writeln('{}:{}: {} {}'.format(
            file_, line, test, str(error) or repr(error)))

        if self.print_stack:
            self.stream.writeln(self._format_tb(tb))

    def _format_tb(self, tb):
        frames = traceback.extract_tb(tb)
        return os.linesep.join(
            ['    {file_}:{line}: {func} {statement}'.format(
                file_=file_, line=line, func=func, statement=statement)
             for file_, line, func, statement in frames]
        )

    def _first_local_stackframe(self, tb):
        frames = traceback.extract_tb(tb)

        def i_like_you(frame):
            path, *_ = frame
            return (path.startswith(self.basepath) and
                    not re.search(r'python|venv', path, flags=re.IGNORECASE))

        local_frames = filter(i_like_you, reversed(frames))
        return next(local_frames, frames[-1])

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
