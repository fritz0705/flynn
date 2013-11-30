# coding: utf-8

import io

class EncoderError(Exception):
	pass

def encode_str(obj):
	buf = io.BytesIO()
	encode(buf, obj)
	return buf.getvalue()

def encode(io, obj):
	if isinstance(obj, list):
		encode_list(io, obj)
	elif isinstance(obj, dict):
		encode_dict(io, obj)
	elif isinstance(obj, str):
		encode_textstring(io, obj)
	elif isinstance(obj, bytes):
		encode_bytestring(io, obj)
	elif isinstance(obj, int):
		encode_integer(io, obj)
	elif isinstance(obj, tuple):
		encode_tagging(io, obj)
	elif obj is True:
		encode_true(io)
	elif obj is False:
		encode_false(io)
	elif obj is None:
		encode_null(io)
	else:
		raise EncoderError("{} has no defined mapping".format(type(obj)))

def _encode_ibyte(major, length):
	if length < 24:
		return ((major << 5) | length).to_bytes(1, "little")
	elif length < 256:
		return ((major << 5) | 24).to_bytes(1, "little") + length.to_bytes(1, "little")
	elif length < 65536:
		return ((major << 5) | 25).to_bytes(1, "little") + length.to_bytes(2, "little")
	elif length < 4294967296:
		return ((major << 5) | 26).to_bytes(1, "little") + length.to_bytes(4, "little")
	elif length < 18446744073709551616:
		return ((major << 5) | 27).to_bytes(1, "little") + length.to_bytes(8, "little")

def encode_integer(io, integer):
	if integer < 0:
		integer = -integer - 1
		io.write(_encode_ibyte(1, integer))
	else:
		io.write(_encode_ibyte(0, integer))

def encode_textstring(io, string):
	string = string.encode("utf-8")
	io.write(_encode_ibyte(3, len(string)))
	io.write(string)

def encode_bytestring(io, string):
	io.write(_encode_ibyte(2, len(string)))
	io.write(string)

def encode_list(io, array):
	io.write(_encode_ibyte(4, len(array)))
	for elem in array:
		encode(io, elem)

def encode_dict(io, d):
	io.write(_encode_ibyte(5, len(d)))
	for key, value in d.items():
		encode(io, key)
		encode(io, value)

def encode_true(io):
	io.write(_encode_ibyte(7, 21))

def encode_false(io):
	io.write(_encode_ibyte(7, 20))

def encode_null(io):
	io.write(_encode_ibyte(7, 22))

def encode_tagging(io, tagging):
	io.write(_encode_ibyte(6, tagging[0]))
	encode(io, tagging[1])

def encode_array_generator(io, iterable):
	io.write(b"\x9f")
	for elem in iterable:
		encode(io, elem)
	io.write(b"\xff")

def encode_dict_generator(io, iterable):
	io.write(b"\xbf")
	for key, value in iterable:
		encode(io, key)
		encode(io, value)
	io.write(b"\xff")

