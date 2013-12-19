# coding: utf-8

import io
import sys
import struct

if sys.version_info[0] == 2:
	import collections as abc
	_integer_types = (int, long)
else:
	import collections.abc as abc
	_integer_types = (int, )

_str_type = type(u"")
_bytes_type = type(b"")

import flynn.data
from flynn.utils import to_bytes

class EncoderError(Exception):
	pass

class Encoder(object):
	def __init__(self, output):
		self.output = output

	def encode(self, object):
		if isinstance(object, list):
			self.encode_list(object)
		elif isinstance(object, dict):
			self.encode_dict(object)
		elif isinstance(object, _bytes_type):
			self.encode_bytestring(object)
		elif isinstance(object, _str_type):
			self.encode_textstring(object)
		elif isinstance(object, float):
			self.encode_float(object)
		elif isinstance(object, bool):
			self.encode_boolean(object)
		elif isinstance(object, _integer_types):
			self.encode_integer(object)
		elif isinstance(object, flynn.data.Tagging):
			self.encode_tagging(object)
		elif object is flynn.data.Undefined:
			self.encode_undefined()
		elif object is None:
			self.encode_null()
		elif isinstance(object, abc.Iterable):
			self.encode_infinite_list(object)
		else:
			raise EncoderError("Object of type {} is not serializable".format(type(object)))

	def encode_list(self, list):
		self._write(_encode_ibyte(4, len(list)))
		for elem in list:
			self.encode(elem)

	def encode_dict(self, dict):
		self._write(_encode_ibyte(5, len(dict)))
		for key, value in dict.items():
			self.encode(key)
			self.encode(value)

	def encode_bytestring(self, bytestring):
		self._write(_encode_ibyte(2, len(bytestring)))
		self._write(bytestring)

	def encode_textstring(self, textstring):
		string_ = textstring.encode("utf-8")
		self._write(_encode_ibyte(3, len(string_)))
		self._write(string_)

	def encode_float(self, float):
		self._write(b"\xfb")
		self._write(struct.pack(">d", float))

	def encode_integer(self, integer):
		if integer < 0:
			integer = -integer - 1
			try:
				self._write(_encode_ibyte(1, integer))
			except TypeError:
				raise EncoderError("Encoding integers lower than -18446744073709551616 is not supported")
		else:
			try:
				self._write(_encode_ibyte(0, integer))
			except TypeError:
				raise EncoderError("Encoding integers larger than 18446744073709551615 is not supported")

	def encode_tagging(self, tagging):
		try:
			self._write(_encode_ibyte(6, tagging[0]))
		except TypeError:
			raise EncoderError("Encoding tag larger than 18446744073709551615 is not supported")
		self.encode(tagging[1])

	def encode_boolean(self, boolean):
		if boolean is True:
			self._write(_encode_ibyte(7, 21))
		elif boolean is False:
			self._write(_encode_ibyte(7, 20))
	
	def encode_null(self):
		self._write(_encode_ibyte(7, 22))

	def encode_undefined(self):
		self._write(b"\xf7")

	def encode_infinite_textstring(self, iterable):
		self._write(b"\x7f")
		for elem in iterable:
			if not isinstance(elem, _str_type):
				raise EncoderError("Object of type {} is not valid in infinite textstring".format(type(elem)))
			self.encode(elem)
		self._write(b"\xff")

	def encode_infinite_bytestring(self, iterable):
		self._write(b"\x5f")
		for elem in iterable:
			if not isinstance(elem, _bytes_type):
				raise EncoderError("Object of type {} is not valid in infinite bytestring".format(type(elem)))
			self.encode(elem)
		self._write(b"\xff")

	def encode_infinite_list(self, iterable):
		self._write(b"\x9f")
		for elem in iterable:
			self.encode(elem)
		self._write(b"\xff")

	def encode_infinite_dict(self, iterable):
		self._write(b"\xbf")
		for key, value in iterable:
			self.encode(key)
			self.encode(value)
		self._write(b"\xff")

	def _write(self, val):
		self.output.write(val)

class InfiniteEncoder(Encoder):
	chunksize = 8

	def __init__(self, output, chunksize=None):
		Encoder.__init__(self, output)
		if chunksize is not None:
			self.chunksize = chunksize

	def encode_list(self, object):
		self.encode_infinite_list(object)
	
	def encode_dict(self, object):
		self.encode_infinite_dict(object.items())
	
	def encode_textstring(self, object):
		if len(object) <= self.chunksize:
			Encoder.encode_textstring(self, object)
		else:
			chunks = int((len(object) - 1) / self.chunksize) + 1
			generator = (object[n*self.chunksize:(n+1)*self.chunksize] for n in range(chunks))
			self.encode_infinite_textstring(generator)

	def encode_bytestring(self, object):
		if len(object) <= self.chunksize:
			Encoder.encode_bytestring(self, object)
		else:
			chunks = int((len(object) - 1) / self.chunksize) + 1
			generator = (object[n*self.chunksize:(n+1)*self.chunksize] for n in range(chunks))
			self.encode_infinite_bytestring(generator)

def dump(obj, io, cls=Encoder, *args, **kwargs):
	cls(io, *args, **kwargs).encode(obj)

def dumps(obj, *args, **kwargs):
	buf = io.BytesIO()
	dump(obj, buf, *args, **kwargs)
	return buf.getvalue()

def _encode_ibyte(major, length):
	if length < 24:
		return to_bytes((major << 5) | length, 1, "big")
	elif length < 256:
		return to_bytes((major << 5) | 24, 1, "big") + to_bytes(length, 1, "big")
	elif length < 65536:
		return to_bytes((major << 5) | 25, 1, "big") + to_bytes(length, 2, "big")
	elif length < 4294967296:
		return to_bytes((major << 5) | 26, 1, "big") + to_bytes(length, 4, "big")
	elif length < 18446744073709551616:
		return to_bytes((major << 5) | 27, 1, "big") + to_bytes(length, 8, "big")
	else:
		return None

__all__ = ["Encoder", "InfiniteEncoder", "EncoderError", "dump", "dumps"]

