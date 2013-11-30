Flynn from Breaking Bad
#######################

Flynn (his real name is Walter Junior), is a protagonist in Breaking Bad and the son of
Walter White (a. k. a. Heisenberg).

Flynn is also a Python library providing CBOR [RFC7049] encoding and decoding with a
traditional buffered and a streaming interface.

Usage
=====

	>>> import flynn
	>>> flynn.dumps({"foo": ["bar", 5]})
	b'\xa1cfoo\x82cbar\x05'
	>>> flynn.loads(b'\xa1cfoo\x82cbar\x05')
	{'foo': ['bar', 5]}

Copyright / License
===================

© 2013 Fritz Conrad Grimpen

The code is licensed under a BSD-style license. The full license text is available at http://grimpen.org/license.txt

