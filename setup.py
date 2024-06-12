# -*- coding: utf-8 -*-

# Package and distribution management

# Learn more: {github_repo}

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()
    
with open('LICENSE') as f:
    license = f.read()
    
setup(
    name='project/package name',
    version='0.1.0',
    description='Project/package description',
    long_description=readme,
    author='Edward Middleton-Smith',
    author_email='edward.middletonsmith@gmail.com',
    url='github_repo',
    license=license,
    packages=find_packages(exclude('tests', 'docs'))
)