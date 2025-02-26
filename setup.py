# -*- coding: utf-8 -*-

# Package and distribution management

# Learn more: {github_repo}

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()
    
with open('LICENSE') as f:
    license = f.read()
    
setup(
    name='demo_braille',
    version='0.1.1',
    description='Text to English Braille translation module using python. The method of Braille translation can be varied to correspond to various chapters in the Standard English Braille pdf in the docs to allow users of different stages of Braille learning progress to create translations at their level. This module is a demo subproject of an engineering system that is used to convert text to English Braille as a 3D object and then prepare it and print it on a 3D printer farm.',
    long_description=readme,
    author='Edward Middleton-Smith',
    author_email='edward.middletonsmith@gmail.com',
    url='https://github.com/Teddy-1024/demo_braille',
    license=license,
    packages=find_packages(exclude = ('tests', 'docs'))
)