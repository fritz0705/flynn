#!/usr/bin/env python

import setuptools

long_description = """Flynn is a simple decoder and encoder for the CBOR binary
object format described in RFC7049. It features a full CBOR base support and
also a simple streaming interface for networking applications."""

setuptools.setup(
	name="flynn",
	version="1.0.0b2",
	packages=[
		"flynn",
	],
	author="Fritz Grimpen",
	author_email="fritz@grimpen.net",
	url="https://github.com/fritz0705/flynn.git",
	license="http://opensource.org/licenses/MIT",
	description="Simple decoder and encoder for CBOR",
	classifiers=[
		"Development Status :: 4 - Beta",
		"Environment :: Web Environment",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"Topic :: System :: Networking",
	],
	long_description=__doc__
)
