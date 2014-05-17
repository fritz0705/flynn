import flynn

def obisCode(msg):
	if not isinstance(msg, bytes) or len(msg) != 6:
		raise

	return "%i-%i.%i.%i.%i*%i" % tuple(msg)

def openResponse(msg):
	if not isinstance(msg, list) or len(msg) != 6:
		raise

	print("  SML_PublicOpen.Res")
	print("    reqFileId: %r" % msg[2])
	print("    serverId: %r" % msg[3])

def getListResponse(msg):
	if not isinstance(msg, list) or len(msg) != 7:
		raise

	print("  SML_GetList.Res")
	print("    serverId: %r" % msg[1])

	for val in msg[4]:
		print("    SML_ListEntry")
		print("      objName: %s" % obisCode(val[0]))

		if isinstance(val[5], int):
			unit = val[3]
			if unit == flynn.Empty:
				unit = ""
			elif unit == 27:
				unit = " W"
			elif unit == 30:
				unit = " Wh"
			else:
				unit = " (unknown %i)" % unit

			scaler = val[4]
			if scaler == flynn.Empty:
				scaler = 0

			value = float(val[5]) * 10**scaler
			print("      interpreted value: %f%s" % (value, unit))
		else:
			print("      unit: %r" % val[3])
			print("      scaler: %r" % val[4])
			print("      value: %r" % val[5])


def rotz(msg):
	if not isinstance(msg, list) or len(msg) != 6:
		return

	body = msg[3]

	if not isinstance(body, list) or len(body) != 2:
		return

	print("SML Message")

	if   body[0] == 0x101:
		openResponse(body[1])
	#elif body[0] == 0x201:
	#	closeResponse(body[1])
	elif body[0] == 0x701:
		getListResponse(body[1])
	else:
		print("Unimplemented type: %x" % body[0])

	print()

