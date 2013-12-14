# coding: utf-8

import sys
import argparse

import flynn
import json

def main(args=sys.argv[1:]):
	formats = {"json", "cbor", "cbori", "cborh", "cborhi"}
	argparser = argparse.ArgumentParser()
	argparser.add_argument("-i", "--input-format", choices=formats, default="cbor")
	argparser.add_argument("-o", "--output-format", choices=formats, default="cbor")
	args = argparser.parse_args(args)
	if args.input_format in {"cbor", "cbori"}:
		input_format = "cbor"
	else:
		input_format = args.input_format
	output_format = args.output_format

	intermediate = None
	if input_format in {"cbor", "cbori"}:
		intermediate = flynn.load(sys.stdin.buffer.raw)
	elif input_format in {"cborh", "cborhi"}:
		intermediate = flynn.loadh(sys.stdin.read())
	elif input_format == "json":
		intermediate = json.load(sys.stdin)

	if output_format == "cbor":
		flynn.dump(intermediate, sys.stdout.buffer.raw)
	elif output_format == "cbori":
		flynn.dump(intermediate, sys.stdout.buffer.raw, cls=flynn.encoder.InfiniteEncoder)
	elif output_format == "cborh":
		sys.stdout.write(flynn.dumph(intermediate))
		sys.stdout.write("\n")
	elif output_format == "cborhi":
		sys.stdout.write(flynn.dumph(intermediate, cls=flynn.encoder.InfiniteEncoder))
		sys.stdout.write("\n")
	elif output_format == "json":
		json.dump(intermediate, sys.stdout)
		sys.stdout.write("\n")

if __name__ == "__main__":
	main()

