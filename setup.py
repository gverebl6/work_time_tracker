from setuptools import setup

setup(
    name = 'tracker',
    version ='0.1',
    py_modules=['tracker'],
    install_requires=[
        'Click',
        'tabulate',
    ],
    entry_points='''
        [console_scripts]
        tracker=tracker:cli
    ''',
)