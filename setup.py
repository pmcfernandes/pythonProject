from setuptools import setup, find_packages

setup(
    name='python_utilities',
    version='1.0.1',
    packages=(find_packages()),
    install_requires=['pymssql', 'pandas', ],
    url='https://github.com/pmcfernandes/pythonProject',
    license='',
    author='Pedro Fernandes',
    author_email='pmcfernandes@gmail.com',
    description="A set of simple utility APIs for higher-level python functions.",
    script_name='setup.py',
    python_requires='>=3.5',
)
