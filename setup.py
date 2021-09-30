from setuptools import setup, find_packages

setup(
    name='dvcli',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        'click==8.0.1',
        'click-plugins==1.1.1',
        'click-log==0.3.2',
        'pyDataverse==0.3.1',
        'confuse==1.6.0'
    ],
    entry_points='''
        [console_scripts]
        dvcli=dvcli.cli:main
    ''',
    include_package_data=True,
)
