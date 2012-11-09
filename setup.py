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
    description = ("C/C++ template using mako"),
    license = "LGPL",
    keywords = "C/C++ template mako",
    packages = setuptools.find_packages(
        exclude=["tests"],
        ),
    package_data = {'makocpp': ['CPP/*.mako',],},
    long_description=read('README'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Development",
        "License :: Lesser GPL",
    ],
)
