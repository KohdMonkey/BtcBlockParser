import os
import sys
import struct
import logging

BTC_SINGLE_HEADER_SIZE = (
	4      # version
	 + 32  # previous block hash
	 + 32  # merkle root hash
	 + 4   # timestamp
	 + 4   # difficulty
	 + 4   # nonce
)

class BtcHeader:

	def __init__(self,
		ver: int,
		prevHash: bytearray,
		mRootHash: bytearray,
		timeStp: int,
		diff: int,
		blkNonce: int
	):

		self.version = ver
		self.prevHash = prevHash
		self.mRootHash = mRootHash
		self.timestamp = timeStp
		self.difficulty = diff
		self.nonce = blkNonce

	def __str__(self):

		return str({
			'version'         : self.version,
			'previous_hash'   : '0x' + self.prevHash.hex(),
			'merkle_root_hash': '0x' + self.mRootHash.hex(),
			'timestamp'       : self.timestamp,
			'difficulty'      : self.difficulty,
			'nonce'           : self.nonce
		})

	@classmethod
	def FromBytes(cls, bt):
		(ver, prevHash, rootHash, timeStp, diff, blkNonce) = struct.unpack('<I32s32sIII', bt)
		prevHash = bytearray(prevHash)
		rootHash = bytearray(rootHash)
		prevHash.reverse()
		rootHash.reverse()
		return cls(ver, prevHash, rootHash, timeStp, diff, blkNonce)

class BtcHeaderItr:

	def __init__(self, headerDB, blkIdx: int = 0):

		self.headerDB = headerDB
		self.blkIdx = blkIdx

	def __next__(self):

		if self.blkIdx < self.headerDB.blkCount:
			h = self.headerDB[self.blkIdx]

			self.blkIdx += 1

			return h
		else:
			raise StopIteration

class BtcHeaderDB:

	def __init__(self, filename: str):

		self.logger = logging.getLogger('BtcHeaderDB')

		if not os.path.isfile(filename):
			errMsg = 'The given path, {}, to the BTC header database file doesn\'t exist.'.format(filename)
			self.logger.error(errMsg)
			raise FileNotFoundError(errMsg)

		self.filename = filename

		self.fileSize = os.stat(filename).st_size
		if self.fileSize % BTC_SINGLE_HEADER_SIZE != 0:
			errMsg = 'The given file, {}, size doesn\'t match the header size.'.format(filename)
			self.logger.error(errMsg)
			raise Exception(errMsg)

		self.blkCount = int(self.fileSize / BTC_SINGLE_HEADER_SIZE)

		self.file = None

	def __enter__(self):

		if self.file is None:
			self.file = open(self.filename, 'rb')
			self.logger.debug('Opened {} file.'.format(self.filename))

		return self

	def __exit__(self, excpType, excpValue, excpTraceback):

		if self.file is not None:
			self.file.close()
			self.file = None

	def __getitem__(self, key: int):

		if self.file is None:
			self.open()

		if key >= self.blkCount:
			errMsg = 'The BTC header database does not have block with index of {}'.format(key)
			self.logger(errMsg)
			raise KeyError(errMsg)

		self.file.seek(key * BTC_SINGLE_HEADER_SIZE)

		return BtcHeader.FromBytes(self.file.read(BTC_SINGLE_HEADER_SIZE))

	def __iter__(self):
		return BtcHeaderItr(self, 0)

	def open(self):

		if self.file is None:
			self.file = open(self.filename, 'rb')
			self.logger.debug('Opened {} file.'.format(self.filename))

	def close(self):

		if self.file is not None:
			self.file.close()
			self.file = None
