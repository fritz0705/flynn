# coding: utf-8

import base64

import flynn.decoder
import flynn.data

__all__ = [
	"decoder",
	"load",
	"loads",
	"loadh",
	"EndOfMessage",
	"Empty",
	"InvalidSMLError"
]

load = flynn.decoder.load
loads = flynn.decoder.loads

EndOfMessage = flynn.data.EndOfMessage
Empty = flynn.data.Empty

InvalidSMLError = flynn.decoder.InvalidSMLError

def dumph(*args, **kwargs):
	return base64.b16encode(dumps(*args, **kwargs)).decode("utf-8")

def loadh(data, *args, **kwargs):
	return loads(base64.b16decode(data), *args, **kwargs)

