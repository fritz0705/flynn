Flynn from Breaking Bad
#######################

Flynn (his real name is Walter Junior), is a protagonist in Breaking Bad and the son of
Walter White (a. k. a. Heisenberg).

Flynn is also a Python library providing CBOR [RFC7049] encoding and decoding with a
traditional buffered and a streaming interface.

Usage
=====

Flynn provides the high-level API provided by the flynn module and the low-level
encoding and decoding APIs which are provided by flynn.encoder and flynn.decoder.

	>>> flynn.dumps([1, [2, 3]])
	b'\x82\x01\x82\x02\x03'
	>>> flynn.dumph([1, [2, 3]])
	'8201820203'
	>>> flynn.loads(b'\x82\x01\x82\x02\x03')
	[1, [2, 3]]
	>>> flynn.loadh('8201820203')
	[1, [2, 3]]

Copyright / License
===================

© 2013 Fritz Conrad Grimpen

The code is licensed under a BSD-style license. The full license text is available at http://grimpen.org/license.txt

