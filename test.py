# coding: utf-8

import flynn
import collections

# Abbrevations
T = flynn.data.Tagging
Undef = flynn.data.Undefined
# OrderedDict is required due to non-deterministic hashing salt
O = collections.OrderedDict

expectations = [
	(0,                     "00", None),
	(1,                     "01", None),
	(10,                    "0A", None),
	(23,                    "17", None),
	(24,                    "1818", None),
	(25,                    "1819", None),
	(100,                   "1864", None),
	(1000,                  "1903E8", None),
	(1000000,               "1A000F4240", None),
	(1000000000000,         "1B000000E8D4A51000", None),
	(18446744073709551615,  "1BFFFFFFFFFFFFFFFF", None),
	# FIXME Will fail due to missing Bignum support
	#(18446744073709551616,  "C249010000000000000000"),
	(-18446744073709551616, "3BFFFFFFFFFFFFFFFF", None),
	# FIXME Will fail due to missing Bignum support
	#(-18446744073709551617, "C349010000000000000000"),
	(-1,                    "20", None),
	(-10,                   "29", None),
	(-100,                  "3863", None),
	(-1000,                 "3903E7", None),
	(False,                 "F4", None),
	(True,                  "F5", None),
	(None,                  "F6", None),
	(flynn.data.Undefined,  "F7", None),
	(T(0, "2013-03-21T20:04:00Z"), "C074323031332D30332D32315432303A30343A30305A",
		None),
	(T(1, 1363896240),      "C11A514B67B0", None),
	(b"",                   "40", None),
	(b"\x01\x02\x03\x04",   "4401020304", None),
	("",                    "60", None),
	("a",                   "6161", None),
	("IETF",                "6449455446", None),
	("\"\\",                "62225C", None),
	("\u00fc",              "62C3BC", None),
	("\u6c34",              "63E6B0B4", None),
	# FIXME This test will fail due to invalid unicode codepoints
	#("\ud800\udd51",        "64F0908591"),
	([],                    "80", None),
	([1, 2, 3],             "83010203", None),
	([1, [2, 3], [4, 5]],   "8301820203820405", None),
	({},                    "A0", None),
	(O([(1, 2), (3, 4)]),   "A201020304", None),
	(O([("a", 1), ("b", [2, 3])]), "A26161016162820203", None),
	(["a", {"b": "c"}],     "826161A161626163", None),
	(range(6),              "9F000102030405FF", [0, 1, 2, 3, 4, 5]),
	(("A", "B", "C"),       "9F614161426143FF", ["A", "B", "C"]),
]

def test_encode():
	for raw, encoded, decoded in expectations:
		print((raw, encoded))
		assert flynn.dumph(raw) == encoded

def test_decode():
	for raw, encoded, decoded in expectations:
		if decoded is None:
			decoded = raw
		elif decoded is False:
			continue
		print((raw, encoded))
		assert flynn.loadh(encoded) == decoded

