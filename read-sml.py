#!/usr/bin/env python3

import pprint
import argparse
import sys

import flynn

argparser = argparse.ArgumentParser()
argparser.add_argument("file", nargs="?", default=sys.stdin.buffer.raw)

args = argparser.parse_args()

file = args.file
if isinstance(file, str):
	file = open(file, "rb")

def search(f, needle):
	buf = f.read(len(needle))
	while buf != b"\x1b\x1b\x1b\x1b\x01\x01\x01\x01":
		r = f.read(1)
		if not r:
			raise EOFError()
		buf = buf[1:] + r

while True:
	try:
		search(file, b"\x1b\x1b\x1b\x1b\x01\x01\x01\x01")
	except EOFError:
		break
	while True:
		try:
			msg = flynn.load(file)
		except flynn.InvalidSMLError:
			break
		if msg == flynn.EndOfMessage:
			break
		pprint.pprint(msg)

