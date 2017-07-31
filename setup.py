from setuptools import setup, find_packages

setup(
    name='tuga',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click==6.7',
        'requests==2.18.2'
    ],
    entry_points='''
        [console_scripts]
        tuga=tuga.main:cli
    ''',
)
