# coding: utf-8

import base64

import flynn.decoder
import flynn.encoder
import flynn.data

__all__ = [
	"decoder",
	"encoder",
	"dump",
	"dumps",
	"dumph",
	"load",
	"loads",
	"loadh",
	"Tagging",
	"Undefined"
]

dump = flynn.encoder.dump
dumps = flynn.encoder.dumps

load = flynn.decoder.load
loads = flynn.decoder.loads

Tagging = flynn.data.Tagging
Undefined = flynn.data.Undefined

def dumph(*args, **kwargs):
	return base64.b16encode(dumps(*args, **kwargs)).decode("utf-8")

def loadh(data, *args, **kwargs):
	return loads(base64.b16decode(data), *args, **kwargs)

