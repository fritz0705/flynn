# coding: utf-8

import collections

Tagging = collections.namedtuple("Tagging", ["tag", "object"])

class _Undefined(object):
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not isinstance(cls._instance, cls):
			cls._instance = object.__new__(cls, *args, **kwargs)
		return cls._instance

	def __str__(self):
		return "Undefined"

	def __repr__(self):
		return "Undefined"

Undefined = _Undefined()
