from nose.plugins import Plugin
import traceback
import os
import re


class TerseOutPlugin(Plugin):
    name = 'terseout'

    def __init__(self):
        self.stream = None
        self.basepath = os.getcwd()
        super(TerseOutPlugin, self).__init__()

    def options(self, parser, env):
        super(TerseOutPlugin, self).options(parser, env)
        parser.add_option("--terse-stack", action="store_true",
                          default=False, help="Print stacktrace for errors")
        parser.add_option("--terse-ignore", action="append", default=None,
                          help="Paths to ignore when finding stack frame to "
                          "use as location for error.")
        parser.add_option("--terse-outside-local", action="store_true",
                          default=False, help="Consider stack frames for "
                          "files outside of the current direcory for error "
                          "location.")

    def configure(self, options, conf):
        self.terse_stack = options.terse_stack
        self.terse_ignore = options.terse_ignore or ['python', 'venv']
        self.terse_outside_local = options.terse_outside_local
        super(TerseOutPlugin, self).configure(options, conf)

    def addError(self, test, err):
        self._report('error', test, err)

    def addFailure(self, test, err):
        self._report('failure', test, err)

    def _report(self, err_or_failure, test, err):
        error_type, error, tb = err
        file_, line, *_ = self._first_local_stackframe(tb)

        message = self._strip_newlines(error)
        self.stream.writeln('{}:{}: {}'.format(file_, line, message))

        if self.terse_stack:
            self.stream.writeln(self._format_tb(tb))

    def _strip_newlines(self, error):
        message = str(error) or repr(error)
        return re.sub(r'[\r\n]+', ' ', message)

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
            so_far = path.startswith(self.basepath) or self.terse_outside_local
            return so_far and not any(
                [re.search(pat, path, flags=re.IGNORECASE)
                 for pat in self.terse_ignore]
            )

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
