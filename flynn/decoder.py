# coding: utf-8

import io

import flynn.data

class _Break(Exception):
	pass

class InvalidCborError(Exception):
	pass

def decode(obj):
	if isinstance(obj, bytes):
		obj = iter(obj)
	elif isinstance(obj, str):
		obj = iter(bytes.fromhex(obj))
	elif isinstance(obj, io.IOBase):
		def byte_gen(obj):
			while True:
				yield obj.read(1)[0]
		obj = byte_gen(obj)
	try:
		return _decode_iter(obj)
	except _Break:
		raise InvalidCborError(obj, "Invalid break item found")

def _decode_iter(stream, jump_table=None):
	if jump_table is None: jump_table = _jump_table
	mtype, ainfo = _decode_ibyte(stream)

	try:
		decoder = _jump_table[mtype]
	except KeyError:
		raise InvalidCborError(bytestream, "Invalid major type {}".format(major_type))
	
	return decoder(mtype, ainfo, stream)

def _decode_length(mtype, ainfo, stream):
	if ainfo < 24:
		return ainfo
	elif ainfo == 24:
		return int.from_bytes(_consume(stream, 1), "big")
	elif ainfo == 25:
		return int.from_bytes(_consume(stream, 2), "big")
	elif ainfo == 26:
		return int.from_bytes(_consume(stream, 4), "big")
	elif ainfo == 27:
		return int.from_bytes(_consume(stream, 8), "big")
	elif ainfo == 31:
		return None
	
	raise InvalidCborError(stream, "Invalid additional information {}".format(ainfo))

def _decode_ibyte(stream):
	ibyte = _consume(stream, 1)[0]
	if isinstance(ibyte, str):
		ibyte = ord(ibyte)
	return (ibyte & 0b11100000) >> 5, ibyte & 0b00011111

def _consume(stream, length):
	res = bytearray(length)
	for n in range(length):
		res[n] = next(stream)
	return bytes(res)

def decode_integer(mtype, ainfo, stream, sign):
	res = _decode_length(mtype, ainfo, stream)
	if res is None:
		raise InvalidCborError(stream, "Invalid additional information {} for integer".format(ainfo))
	if sign is True:
		return -1 - res
	else:
		return res

def decode_bytestring(mtype, ainfo, stream):
	length = _decode_length(mtype, ainfo, stream)
	if length is None:
		res = bytearray()
		while True:
			mtype_, ainfo_ = _decode_ibyte(stream)
			if (mtype_, ainfo_) == (7, 31):
				break
			if mtype_ != 2:
				raise InvalidCborError(stream, "Indefinite byte strings can only contain definite byte strings")
			res.extend(decode_bytestring(mtype_, ainfo_, stream))
		return bytes(res)
	else:
		return _consume(stream, length)

def decode_textstring(mtype, ainfo, stream):
	length = _decode_length(mtype, ainfo, stream)
	if length is None:
		res = bytearray()
		while True:
			mtype_, ainfo_ = _decode_ibyte(stream)
			if (mtype_, ainfo_) == (7, 31):
				break
			if mtype_ != 3:
				raise InvalidCborError(stream, "Indefinite text strings can only contain definite text strings")
			res.extend(decode_bytestring(mtype_, ainfo_, stream))
		return res.decode("utf-8")
	else:
		return _consume(stream, length).decode("utf-8")

def decode_array(mtype, ainfo, stream):
	length = _decode_length(mtype, ainfo, stream)
	if length is None:
		res = []
		while True:
			try:
				res.append(_decode_iter(stream))
			except _Break:
				break
		return res
	else:
		res = [None for _ in range(length)]
		for n in range(length):
			res[n] = _decode_iter(stream)
		return res

def decode_map(mtype, ainfo, stream):
	length = _decode_length(mtype, ainfo, stream)
	if length is None:
		res = {}
		try:
			while True:
				key = _decode_iter(stream)
				value = _decode_iter(stream)
				res[key] = value
		except _Break:
			pass
		return res
	else:
		res = {}
		for n in range(length):
			key, value = _decode_iter(stream), _decode_iter(stream)
			res[key] = value
		return res

def decode_tagging(mtype, ainfo, stream):
	length = _decode_length(mtype, ainfo, stream)
	return flynn.data.Tagging(length, _decode_iter(stream))

def decode_other(mtype, ainfo, stream):
	if ainfo == 20:
		return False
	elif ainfo == 21:
		return True
	elif ainfo == 22:
		return None
	elif ainfo == 23:
		return flynn.data.Undefined
	elif ainfo == 31:
		raise _Break()

_jump_table = [
	lambda *args: decode_integer(*args, sign=False),
	lambda *args: decode_integer(*args, sign=True),
	decode_bytestring,
	decode_textstring,
	decode_array,
	decode_map,
	decode_tagging,
	decode_other,
]
