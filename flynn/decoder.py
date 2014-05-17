# coding: utf-8

import io
import struct
import math

import flynn.data
import flynn.utils

class InvalidSMLError(Exception):
	pass

class Decoder(object):
	def __init__(self, input):
		self.input = input

	def decode(self):
		mtype, ainfo = self._decode_ibyte()
		if mtype == 0 and ainfo == 0:
			return flynn.data.EndOfMessage
		elif mtype == 0:
			# octet string
			if ainfo == 1:
				return flynn.data.Empty
			else:
				return self._decode_octet_string(ainfo-1)
		elif mtype == 0x5:
			if ainfo == 0x2:
				return self._decode_int8()
			elif ainfo == 0x3:
				return self._decode_int16()
			elif ainfo == 0x5:
				return self._decode_int32()
			elif ainfo == 0x9:
				return self._decode_int64()
		elif mtype == 0x6:
			if ainfo == 0x2:
				return self._decode_uint8()
			elif ainfo == 0x3:
				return self._decode_uint16()
			elif ainfo == 0x5:
				return self._decode_uint32()
			elif ainfo == 0x9:
				return self._decode_uint64()
		elif mtype == 0x4 and ainfo == 0x2:
			return self._decode_boolean()
		elif mtype == 0x7:
			return self._decode_list(ainfo)
		raise InvalidSMLError("Unexpected TL field {}".format((mtype << 4) | ainfo))

	def _decode_octet_string(self, length):
		return self._read(length)

	def _decode_int8(self):
		return flynn.utils.from_bytes(self._read(1), 1, "big")
	_decode_uint8 = _decode_int8

	def _decode_int16(self):
		return flynn.utils.from_bytes(self._read(2), 2, "big")
	_decode_uint16 = _decode_int16
	
	def _decode_int32(self):
		return flynn.utils.from_bytes(self._read(4), 4, "big")
	_decode_uint32 = _decode_int32

	def _decode_int64(self):
		return flynn.utils.from_bytes(self._read(8), 8, "big")
	_decode_uint64 = _decode_int64

	def _decode_boolean(self):
		return self._read(1) != b"\x00"

	def _decode_list(self, length):
		res = []
		for n in range(length):
			res.append(self.decode())
		return res
	
	def _decode_ibyte(self):
		byte = self._read(1)[0]
		mtype, ainfo = (byte & 0b11110000) >> 4, byte & 0b1111
		while mtype == 0b1100:
			byte = self._read(1)[0]
			mtype, ainfo_new = (byte & 0b11110000) >> 4, byte & 0b1111
			ainfo = ainfo << 4 | ainfo_new
		return mtype, ainfo

	def _read(self, n):
		m = self.input.read(n)
		if len(m) != n:
			raise InvalidSMLError("Expected {} bytes, got {} bytes instead".format(n, len(m)))
		return m
	
def load(fp, cls=Decoder, *args, **kwargs):
	return cls(fp, *args, **kwargs).decode()

def loads(data, cls=Decoder, *args, **kwargs):
	return cls(io.BytesIO(data), *args, **kwargs).decode()

__all__ = ["InvalidSMLError", "Decoder", "load", "loads"]

