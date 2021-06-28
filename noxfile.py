# pylint: disable=C
import nox

VERSIONS = ['3.7', '3.8']

@nox.session(python=VERSIONS, reuse_venv=True)
def unit(session):
    session.install('pytest', 'pytest-cov', 'pytest-icdiff', 'pytest-integration')
    session.install('-e', '.')
    session.run('pytest')

@nox.session(python=VERSIONS, reuse_venv=True)
def integration(session):
    session.install('pytest', 'pytest-cov', 'pytest-icdiff', 'pytest-integration')
    session.install('-e', '.')
    session.run('pytest', 'test/integration', '--integration-cover')

@nox.session(python=VERSIONS, reuse_venv=True)
def example(session):
    session.install('-e', '.')
    session.run('python', 'examples/run.py', 'examples/', env={'PYTHONPATH': 'examples:$PYTHONPATH'})
