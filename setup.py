#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
        name='lighty-thumbnailer',
        version='0.1.7',
        description='sorl.thumbnail inspired image thumbnailer',
        long_description=open('README').read(),
        author='Andrey Grygoryev',
        author_email='undeadgrandse@gmail.com',
        license='BSD',
        url='https://github.com/GrAndSE/lighty-thumbnailer',
        packages=find_packages(),
        platforms="any",
        zip_safe=False,
        classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Multimedia :: Graphics',
        ],
)
