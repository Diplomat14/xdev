from setuptools import setup, find_packages
import os

def readme():
    with open(os.path.dirname(os.path.abspath(__file__)) + '/README.rst') as f:
        return f.read()

setup(
    name='xdev',
    version='0.1',
    description='Cross-platform development framework.',
    long_description=readme(),
    url='TBD',
    author='Aleksey Denysyuk',
    author_email='diplomt@gmail.com',
    license='MIT', #TBD
    packages=find_packages(),
    install_requires=[],
    #dependency_links=['http://server/user/repo/tarball/master#egg=package-1.0'],
    entry_points = {
        'console_scripts':['xdev-main=xdev.console.command_line:main']
    },
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False
)