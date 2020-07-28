from setuptools import setup, find_packages
from dvcli.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='dvcli',
    version=VERSION,
    description='Dataverse Command Line Interface. Use and manage a Dataverse installation from your terminal.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Oliver Bertuch',
    author_email='oliver@bertuch.eu',
    url='https://github.com/GlobalDataverseCommunityConsortium/dvcli',
    license='Apache License 2.0',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'dvcli': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        dvcli = dvcli.main:main
    """,
    install_requires=[
        'cement==3.0.4',
        'jinja2',
        'pyyaml',
        'colorlog',
        'pyDataverse@git+https://github.com/AUSSDA/pyDataverse#3b040ff',
    ],
)
