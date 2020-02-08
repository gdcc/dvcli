from setuptools import setup, find_packages

setup(
    name='dvcli',
    version='0.0.1',
    py_modules=find_packages(),
    install_requires=[
        'Click==7.0',
        'pyDataverse==0.2.1',
        'confuse==1.0.0'
    ],
    entry_points='''
        [console_scripts]
        dvcli=dvcli.cli:main
    ''',
)
