# coding: utf-8

import base64

import flynn.decoder
import flynn.encoder

__all__ = [
	"decoder",
	"encoder",
	"dump",
	"dumps",
	"dumph",
	"load",
	"loads",
	"loadh"
]

def dump(obj, fp):
	return flynn.encoder.encode(fp, obj)

def dumps(obj):
	return flynn.encoder.encode_str(obj)

def dumph(obj):
	return base64.b16encode(dumps(obj)).decode("utf-8")

def load(s):
	return flynn.decoder.decode(s)

def loads(s):
	return flynn.decoder.decode(s)

def loadh(s):
	return flynn.decoder.decode(s)

