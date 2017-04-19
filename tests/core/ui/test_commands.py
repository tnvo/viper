# -*- coding: utf-8 -*-
# This file is part of Viper - https://github.com/viper-framework/viper
# See the file 'LICENSE' for copying permission.

from viper.core.session import __sessions__
from viper.core.ui import commands
from viper.core.database import Database
from tests.conftest import FIXTURE_DIR
import pytest
import re
import os
import sys

try:
    from unittest import mock
except ImportError:
    # Python2
    import mock


class TestCommands:

    def teardown_method(self):
        __sessions__.close()

    def test_init(self):
        instance = commands.Commands()
        assert isinstance(instance, commands.Commands)

    def test_help(self, capsys):
        instance = commands.Commands()
        instance.cmd_help()
        instance.cmd_clear()
        instance.cmd_close()
        out, err = capsys.readouterr()
        assert re.search(r".* Commands.*", out)
        assert re.search(r".* Modules.*", out)

    def test_open(self, capsys):
        instance = commands.Commands()
        instance.cmd_open('-h')
        instance.cmd_open('-u', 'https://github.com/viper-framework/viper-test-files/raw/master/test_files/cmd.exe')
        out, err = capsys.readouterr()
        assert re.search("usage: open \[-h\] .*", out)
        assert re.search(".*Session opened on /tmp/.*", out)

    def test_notes(self, capsys):
        instance = commands.Commands()
        instance.cmd_notes('-h')
        instance.cmd_notes('-l')
        out, err = capsys.readouterr()
        assert re.search("usage: notes \[-h\] .*", out)
        assert re.search(".*No open session.*", out)

    @pytest.mark.parametrize("filename", ["chromeinstall-8u31.exe"])
    def test_notes_existing(self, capsys, filename):
        __sessions__.new(os.path.join(FIXTURE_DIR, filename))
        Database().add_note(__sessions__.current.file.sha256, 'Note test', 'This is the content')
        instance = commands.Commands()
        instance.cmd_notes('-l')
        instance.cmd_notes('-v', '1')
        instance.cmd_notes('-d', '1')
        out, err = capsys.readouterr()
        assert re.search(".*1  | Note test.*", out)
        assert re.search(".*This is the content.*", out)

    @pytest.mark.parametrize("filename", ["chromeinstall-8u31.exe"])
    def test_analysis(self, capsys, filename):
        __sessions__.new(os.path.join(FIXTURE_DIR, filename))
        instance = commands.Commands()
        instance.cmd_analysis('-h')
        instance.cmd_analysis('-l')
        instance.cmd_analysis('-v', '1')
        out, err = capsys.readouterr()
        assert re.search("usage: analysis \[-h\] .*", out)
        assert re.search(".*Saved On.*", out)
        assert re.search(".*Cmd Line.*", out)

    def test_store(self, capsys):
        instance = commands.Commands()
        instance.cmd_store('-h')
        out, err = capsys.readouterr()
        assert re.search("usage: store \[-h\] .*", out)

    def test_delete(self, capsys):
        instance = commands.Commands()
        instance.cmd_delete('-h')
        out, err = capsys.readouterr()
        assert re.search("usage: delete \[-h\] .*", out)

    def test_find(self, capsys):
        instance = commands.Commands()
        instance.cmd_find('-h')
        out, err = capsys.readouterr()
        assert re.search("usage: find \[-h\] .*", out)

    def test_tags(self, capsys):
        instance = commands.Commands()
        instance.cmd_tags('-h')
        out, err = capsys.readouterr()
        assert re.search("usage: tags \[-h\] .*", out)

    def test_sessions(self, capsys):
        instance = commands.Commands()
        instance.cmd_sessions('-h')
        out, err = capsys.readouterr()
        assert re.search("usage: sessions \[-h\] .*", out)

    def test_projects(self, capsys):
        instance = commands.Commands()
        instance.cmd_projects('-h')
        instance.cmd_projects('-l')
        out, err = capsys.readouterr()
        assert re.search("usage: projects \[-h\] .*", out)

    def test_export(self, capsys):
        instance = commands.Commands()
        instance.cmd_export('-h')
        out, err = capsys.readouterr()
        assert re.search("usage: export \[-h\] .*", out)

    def test_stats(self, capsys):
        instance = commands.Commands()
        instance.cmd_stats('-h')
        out, err = capsys.readouterr()
        assert re.search("usage: stats \[-h\] .*", out)

    def test_parent(self, capsys):
        instance = commands.Commands()
        instance.cmd_parent('-h')
        out, err = capsys.readouterr()
        assert re.search("usage: parent \[-h\] .*", out)

    @pytest.mark.parametrize("filename", ["chromeinstall-8u31.exe"])
    def test_rename(self, capsys, filename):
        __sessions__.new(os.path.join(FIXTURE_DIR, filename))
        instance = commands.Commands()
        if sys.version_info <= (3, 0):
            in_fct = 'viper.core.ui.commands.input'
        else:
            in_fct = 'builtins.input'
        with mock.patch(in_fct, return_value='chromeinstall-8u31.exe.new'):
            instance.cmd_rename()
        out, err = capsys.readouterr()
        lines = out.split('\n')
        assert re.search(r".*Current name is.*1mchromeinstall-8u31.exe.*", lines[1])
        assert re.search(r".*Refreshing session to update attributes.*", lines[2])
