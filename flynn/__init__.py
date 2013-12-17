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

load = flynn.decoder.load
loads = flynn.decoder.loads

def dumph(*args, **kwargs):
	return base64.b16encode(dumps(*args, **kwargs)).decode("utf-8")

def loadh(data, *args, **kwargs):
	return loads(base64.b16decode(data), *args, **kwargs)

