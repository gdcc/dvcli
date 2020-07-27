from setuptools import setup, find_packages

setup(
    name='dvcli',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'click==7.1.2',
        'click-plugins==1.1.1',
        'click-log==0.3.2',
        'pyDataverse@git+https://github.com/AUSSDA/pyDataverse#3b040ff',
        'confuse==1.0.0'
    ],
    entry_points='''
        [console_scripts]
        dvcli=dvcli.cli:main
    ''',
    include_package_data=True,
)
