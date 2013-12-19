# coding: utf-8

import flynn
import collections

# Abbrevations
T = flynn.data.Tagging
Undef = flynn.data.Undefined
# OrderedDict is required due to non-deterministic hashing salt
O = collections.OrderedDict

expectations = [
	(0,                     "00"),
	(1,                     "01"),
	(10,                    "0A"),
	(23,                    "17"),
	(24,                    "1818"),
	(25,                    "1819"),
	(100,                   "1864"),
	(1000,                  "1903E8"),
	(1000000,               "1A000F4240"),
	(1000000000000,         "1B000000E8D4A51000"),
	(18446744073709551615,  "1BFFFFFFFFFFFFFFFF"),
	# FIXME Will fail due to missing Bignum support
	#(18446744073709551616,  "C249010000000000000000"),
	(-18446744073709551616, "3BFFFFFFFFFFFFFFFF"),
	# FIXME Will fail due to missing Bignum support
	#(-18446744073709551617, "C349010000000000000000"),
	(-1,                    "20"),
	(-10,                   "29"),
	(-100,                  "3863"),
	(-1000,                 "3903E7"),
	(False,                 "F4"),
	(True,                  "F5"),
	(None,                  "F6"),
	(flynn.data.Undefined,  "F7"),
	(T(0, "2013-03-21T20:04:00Z"), "C074323031332D30332D32315432303A30343A30305A"),
	(T(1, 1363896240),      "C11A514B67B0"),
	(b"",                   "40"),
	(b"\x01\x02\x03\x04",   "4401020304"),
	("",                    "60"),
	("a",                   "6161"),
	("IETF",                "6449455446"),
	("\"\\",                "62225C"),
	("\u00fc",              "62C3BC"),
	("\u6c34",              "63E6B0B4"),
	# FIXME This test will fail due to invalid unicode codepoints
	#("\ud800\udd51",        "64F0908591"),
	([],                    "80"),
	([1, 2, 3],             "83010203",),
	([1, [2, 3], [4, 5]],   "8301820203820405"),
	({},                    "A0"),
	(O([(1, 2), (3, 4)]),   "A201020304"),
	(O([("a", 1), ("b", [2, 3])]), "A26161016162820203"),
	(["a", {"b": "c"}],     "826161A161626163"),
]

def test_encode():
	for raw, encoded in expectations:
		print((raw, encoded))
		assert flynn.dumph(raw) == encoded

def test_decode():
	for raw, encoded in expectations:
		print((raw, encoded))
		assert flynn.loadh(encoded) == raw

