# coding: utf-8

import sys

if sys.version_info[0] == 2:
	import struct

	def _build_fmt(length, endianess):
		format_ = ""
		if endianess == "big":
			format_ += ">"
		elif endianess == "little":
			format_ += "<"
		if length == 1:
			format_ += "B"
		elif length == 2:
			format_ += "H"
		elif length == 4:
			format_ += "I"
		elif length == 8:
			format_ += "Q"
		return format_

	def to_bytes(val, length, endianess):
		fmt = _build_fmt(length, endianess)
		return struct.pack(_build_fmt(length, endianess), val)

	def from_bytes(val, length, endianess):
		return struct.unpack(_build_fmt(length, endianess), val)[0]
else:
	def from_bytes(val, length, endianess):
		return int.from_bytes(val, length, endianess)
	
	def to_bytes(val, length, endianess):
		return val.to_bytes(length, endianess)

