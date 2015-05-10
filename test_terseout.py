from __future__ import unicode_literals
import unittest
import os

try:
    from io import StringIO
except ImportError:
    import StringIO

from terseout import TerseOutPlugin


class FakeStream(object):
    def __init__(self):
        self.stream = StringIO()

    def writeln(self, data):
        self.stream.writelines(data)

    def read(self):
        return self.stream.getvalue()


class TestReporting(unittest.TestCase):

    def setUp(self):
        self.plug = TerseOutPlugin(basepath='/my/test/dir')
        self.stream = FakeStream()
        self.plug.setOutputStream(self.stream)

    def test_reports_stackframe_as_single_line(self):
        frame = ('/my/test/dir/test_file.py', 123, 'funcname', 'text')
        message = 'error message'
        self.plug._print_stack_frame(frame, message)
        self.assert_stream('/my/test/dir/test_file.py:123: error message')

    def test_selects_stackframe_with_same_basepath(self):
        frames = [
            ('/my/test/dir/test_file.py', 123, 'funcname', 'text'),
            ('/somewhere/else/internal.py', 432, 'funcname', 'text')
        ]
        frame = self.plug._first_local_stackframe(frames)
        self.assertEqual(frame[0], '/my/test/dir/test_file.py')

    def test_selects_non_local_stackframe_if_allowed(self):
        frames = [
            ('/my/test/dir/test_file.py', 123, 'funcname', 'text'),
            ('/somewhere/else/internal.py', 432, 'funcname', 'text')
        ]
        self.plug.terse_outside_local = True

        frame = self.plug._first_local_stackframe(frames)
        self.assertEqual(frame[0], '/somewhere/else/internal.py')

    def test_creates_a_compact_version_of_a_stacktrace(self):
        frames = [
            ('/my/test/dir/test_file.py', 123, 'funcname', 'text'),
            ('/somewhere/else/internal.py', 432, 'funcname', 'text')
        ]
        formatted = self.plug._format_frames(frames)
        self.assertEqual(
            formatted,
            '    /my/test/dir/test_file.py:123: funcname text' + os.linesep +
            '    /somewhere/else/internal.py:432: funcname text'
        )

    def test_syntax_errors_are_reported_directly(self):
        err = SyntaxError('invalid syntax')
        err.filename = '/offending/file.py'
        err.lineno = 441

        self.plug._report(SyntaxError, err, 'traceback here')

        self.assert_stream('/offending/file.py:441: invalid syntax')

    def assert_stream(self, expected):
        self.assertEqual(self.stream.read(), expected)
