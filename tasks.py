from invoke import run, task

@task
def readme(context):
    try:
        run("gh-md-toc --insert README.md && rm -f README.md.*.*")
    except Exception:
        pass


@task
def test(context):
    try:
        run("python -m unittest tests.test_holidays -v")
    except Exception:
        pass
