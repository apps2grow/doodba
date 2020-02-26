from contextlib import contextmanager

from plumbum.cmd import git


@contextmanager
def git_temporary_tag(commit=True, tag="test"):
    # Commit local changes and tag them
    if commit:
        git("add", ".")
        git(
            "commit",
            "--author=Test<test@test>",
            "--message=test",
            "--allow-empty",
            "--no-verify",
        )
    git("tag", "--force", tag)
    try:
        yield
    finally:
        git("tag", "--delete", tag)
        git("reset", "HEAD^")
