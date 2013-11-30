# coding: utf-8

import io
import collections.abc

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
	elif isinstance(obj, int) and not isinstance(obj, bool):
		encode_integer(io, obj)
	elif isinstance(obj, tuple):
		if isinstance(obj[0], int):
			encode_tagging(io, obj)
		elif isinstance(obj[0], collections.abc.Iterator):
			iterator, type_ = obj
			encode_generator(io, iterator, type_)
	elif obj is True:
		encode_true(io)
	elif obj is False:
		encode_false(io)
	elif obj is None:
		encode_null(io)
	elif callable(obj):
		obj = obj()
		if isinstance(obj, collections.abc.Iterator):
			type_ = next(obj)
			encode_generator(io, obj, type_)
		else:
			encode(io, obj)
	elif isinstance(obj, collections.abc.Iterable):
		encode_array_generator(io, iter(obj))
	else:
		raise EncoderError("{} has no defined mapping".format(type(obj)))

def _encode_ibyte(major, length):
	if length < 24:
		return ((major << 5) | length).to_bytes(1, "big")
	elif length < 256:
		return ((major << 5) | 24).to_bytes(1, "big") + length.to_bytes(1, "big")
	elif length < 65536:
		return ((major << 5) | 25).to_bytes(1, "big") + length.to_bytes(2, "big")
	elif length < 4294967296:
		return ((major << 5) | 26).to_bytes(1, "big") + length.to_bytes(4, "big")
	elif length < 18446744073709551616:
		return ((major << 5) | 27).to_bytes(1, "big") + length.to_bytes(8, "big")

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

def encode_generator(io, iterable, type_):
	if type_ == "array":
		encode_array_generator(io, iterable)
	elif type_ == "map":
		encode_dict_generator(io, iterable)
	elif type_ == "text":
		encode_textstring_generator(io, iterable)
	elif type_ == "bytes":
		encode_bytestring_generator(io, iterable)
	else:
		raise EncoderError("Unknown generator type {}".format(type_))

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

def encode_bytestring_generator(io, iterable):
	io.write(b"\x5f")
	for elem in iterable:
		if not isinstance(elem, bytes):
			raise EncoderError("Bytestring generators can only yield bytes")
		encode(io, elem)
	io.write(b"\xff")

def encode_textstring_generator(io, iterable):
	io.write(b"\x7f")
	for elem in iterable:
		if not isinstance(elem, str):
			raise EncoderError("Textstring generators can only yield strings")
		encode(io, elem)
	io.write(b"\xff")

