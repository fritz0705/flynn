# coding: utf-8

class _Empty(object):
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not isinstance(cls._instance, cls):
			cls._instance = object.__new__(cls, *args, **kwargs)
		return cls._instance

	def __str__(self):
		return "Empty"

	def __repr__(self):
		return "Empty"

Empty = _Empty()

class _EndOfMessage(object):
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not isinstance(cls._instance, cls):
			cls._instance = object.__new__(cls, *args, **kwargs)
		return cls._instance
	
	def __str__(self):
		return "EndOfMessage"

	def __repr__(self):
		return "EndOfMessage"

EndOfMessage = _EndOfMessage()
