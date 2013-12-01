Flynn, the CBOR serializer
##########################

Flynn (his real name is Walter White Jr.), is a protagonist in Breaking Bad and the son of
Walter White (a. k. a. Heisenberg).

Flynn is also a Python library providing CBOR [RFC7049] encoding and decoding with a
traditional buffered and a streaming interface.

Usage
=====

The Flynn API is really simple and inspired by existing Python serialisation
modules like json and pickle. The flynn module has four methods called dumps,
dump, loads and load, where dumps will return the serialised input as bytes
string, while dump will write the serialised input to a file descriptor. The
same applies to loads and load.

	>>> flynn.dumps([1, [2, 3]])
	b'\x82\x01\x82\x02\x03'
	>>> flynn.loads(b'\x82\x01\x82\x02\x03')
	[1, [2, 3]]

Furthermore, Flynn supports generators and other iterables as input for
streaming support:

	>>> flynn.dumps(range(5))
	b'\x9f\x00\x01\x02\x03\x04\xff'
	>>> flynn.loads(b'\x9f\x00\x01\x02\x03\x04\xff')
	[0, 1, 2, 3, 4]

Or to generate a map using an iterable:

	>>> flynn.dumps((((a, a) for a in range(5)), "map"))
	b'\xbf\x00\x00\x01\x01\x02\x02\x03\x03\x04\x04\xff'
	>>> flynn.loads(b'\xbf\x00\x00\x01\x01\x02\x02\x03\x03\x04\x04\xff')
	{0: 0, 1: 1, 2: 2, 3: 3, 4: 4}

Copyright / License
===================

© 2013 Fritz Conrad Grimpen

The code is licensed under the MIT license, provided in the COPYING file of the
Flynn distribution.

