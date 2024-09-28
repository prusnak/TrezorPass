import struct

from PySide6 import QtCore

def q2s(s):
	"""Convert QString to UTF-8 string object"""
	return str(s.toUtf8())

def s2q(s):
	"""Convert UTF-8 encoded string to QString"""
	return QtCore.QString.fromUtf8(s)

class Magic:
	"""
	Few magic constant definitions so that we know which nodes to search
	for keys.
	"""
	u = lambda fmt, s: struct.unpack(fmt, s)[0]
	headerStr = b"TZPW"
	hdr = u("!I", headerStr)
	
	unlockNode = [hdr, u("!I", b"ULCK")] # for unlocking wrapped AES-CBC key
	groupNode  = [hdr, u("!I", b"GRUP")] # for generating keys for individual password groups
	#the unlock and backup key is written in this weird way to fit display nicely
	unlockKey = "Decrypt master  key?" # string to derive wrapping key from
	
	backupNode = [hdr, u("!I", b"BKUP")] # for unlocking wrapped backup private RSA key
	backupKey = "Decrypt backup  key?" # string to derive backup wrapping key from
	
class Padding:
	"""
	PKCS#7 Padding for block cipher having 16-byte blocks
	"""
	
	def __init__(self, blocksize):
		self.blocksize = blocksize
	
	def pad(self, s):
		BS = self.blocksize
		return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
	
	def unpad(self, s):
		return s[0:-ord(s[-1])]
	