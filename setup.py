#!/usr/bin/env python

import os
import setuptools

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(
    name = "MakoCPP",
    version = "0.1",
    author = "Zhou Ming",
    author_email = "chow.ming.beijing@gmail.com",
    description = (""),
    license = "LGPL",
    keywords = "C/C++ template using mako",
    packages = setuptools.find_packages(),
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Development",
        "License :: Lesser GPL",
    ],
)
