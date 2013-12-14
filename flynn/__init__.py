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

dump = flynn.encoder.dump
dumps = flynn.encoder.dumps

def dumph(*args, **kwargs):
	return base64.b16encode(dumps(*args, **kwargs)).decode("utf-8")

def load(s):
	return flynn.decoder.decode(s)

def loads(s):
	return flynn.decoder.decode(s)

def loadh(s):
	return flynn.decoder.decode(s)

