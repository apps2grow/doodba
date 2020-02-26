from copier.main import copy
from plumbum import local
from plumbum.cmd import diff

from .helpers import git_temporary_tag


@git_temporary_tag()
def test_default_settings(tmpdir):
    copy(".", tmpdir, vcs_ref="test", force=True)
    diff("--context=3", "--recursive", local.cwd / "tests" / "default_settings", tmpdir)
