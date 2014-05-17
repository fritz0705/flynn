# coding: utf-8

import sys

if sys.version_info[0] == 2:
	import struct

	def _build_fmt(length, endianess, signed):
		format_ = ""
		if endianess == "big":
			format_ += ">"
		elif endianess == "little":
			format_ += "<"
		if length == 1:
			format_ += "b" if signed else "B"
		elif length == 2:
			format_ += "h" if signed else "H"
		elif length == 4:
			format_ += "i" if signed else "I"
		elif length == 8:
			format_ += "q" if signed else "Q"
		return format_

	def to_bytes(val, length, endianess, signed=False):
		return struct.pack(_build_fmt(length, endianess, signed), val)

	def from_bytes(val, length, endianess, signed=False):
		return struct.unpack(_build_fmt(length, endianess, signed), val)[0]
else:
	def from_bytes(val, length, endianess, signed=False):
		return int.from_bytes(val, endianess, signed=signed)
	
	def to_bytes(val, length, endianess, signed=False):
		return val.to_bytes(length, endianess, signed=signed)

