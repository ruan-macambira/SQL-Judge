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
    session.install('-e', 'test/integration/plug-ins/sql_judge_json_adapter')
    session.run('pytest', 'test/integration', '--integration-cover')
