import sys
from invoke import run, task

@task
def readme(context):
    try:
        run("gh-md-toc --insert README.md && rm -f README.md.*.*")
    except Exception:
        sys.exit(1)


@task
def test(context):
    try:
        run("python -m unittest tests.test_holidays -v")
    except Exception:
        sys.exit(1)

@task
def t(context):
    try:
        run("exit 1")
    except Exception:
        sys.exit(1)
