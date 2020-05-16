from setuptools import setup, find_packages

setup(
    name='MathModeling',
    version='1.10',
    packages=find_packages(),
    url='https://github.com/whitecheeks33/MathModeling.git',
    license='',
    author='Nathan Moore',
    author_email='nlm105@francis.edu',
    description='Interactive plotting program with GUI for covid-19',
    install_requires=['requests', 'pandas', 'numpy', 'matplotlib']
)
