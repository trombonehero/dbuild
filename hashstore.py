import binascii
import hashlib

class HashStore:
	hashes = {}
	files = {}

	def hash_string(self, s):
		assert type(s) == str
		if self.hashes.has_key(s): return self.hashes[s]

		sha = hashlib.sha256()
		sha.update(s)
		h = binascii.b2a_base64(sha.digest()).strip()

		return h

	def hash_file(self, name):
		assert type(name) == str
		if self.files.has_key(name): return self.files[name]

		content = '\n'.join(open(name).readlines())
		h = self.hash_string(content)
		self.files[name] = h

		return h

