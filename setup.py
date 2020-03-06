#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="my2h_transform",
    version="0.0.1",
    author="celestian",
    author_email="petr.celestian@gmail.com",
    description="MyJOP To hJOP Transform Utility ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kmzbrnoI/my2h_transform",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'pronto = my2h_transform.__main__:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
