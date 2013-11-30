# coding: utf-8

import flynn.decoder
import flynn.encoder

def dump(obj, fp):
	return flynn.encoder.encode(fp, obj)

def dumps(obj):
	return flynn.encoder.encode_str(obj)

def load(s):
	return flynn.decoder.decode(s)

def loads(s):
	return flynn.decoder.decode(s)

