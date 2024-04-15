# -*- coding: utf-8 -*-
from setuptools import setup; setup()

[metadata]
name = UCMPhoenix
version = 0.4
author = NegarRahmatollahi, ZhihuaWang, TingSun
author_email = nrahmato@asu.edu
license = MIT
classifiers =
	Development Status :: 3 - Alpha
	License :: OSI Approved :: MIT License
	Natural Language :: English
	Operating System :: OS Independent
	Programming Language :: Python
	Programming Language :: Python :: 3
	Programming Language :: Python :: 3 :: Only
	Programming Language :: Python :: 3.8
	Programming Language :: Python :: 3.9
	Programming Language :: Python :: 3.10
	Programming Language :: Python :: 3.11
	Intended Audience :: Developers
	Intended Audience :: Science/Research
	Intended Audience :: Information Technology
	Topic :: Education
	Topic :: Software Development
	Topic :: Software Development :: Libraries


install_requires =
	requests>=2.27.1
python_requires = >=3.8
package_dir = =src
packages = find:

where = src

console_scripts =
	UCMPhoenix = UCMPhoenix.main:main