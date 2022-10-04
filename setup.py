#!/usr/bin/env python

__all__ = [
    'VERSION'
]

import setuptools

MAJOR      = 0
MINOR      = 1
MICRO      = 0
TEST_VER   = 'a'
ISRELEASED = True
VERSION    = '%d.%d.%d%s' % (MAJOR, MINOR, MICRO, TEST_VER)

setuptools.setup(
    name="AlzKB",
    version=VERSION,
    author="Joseph D. Romano, Van Truong, Yun Hao, Li Shen, and Jason H. Moore",
    description="A graph knowledge base for Alzheimer disease",
    url="https://github.com/EpistasisLab/AlzKB.git",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    include_package_data=True,
    install_requires=[
        'ista @ git+https://github.com/JDRomano2/ista@c036c1074e0b59df704a0aeb097862108b012b45'
    ],
    entry_points={
        'console_scripts': [
            'alzkb=alzkb.build:main'
        ]
    }
)
