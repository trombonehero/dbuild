import binascii
import hashlib
import sys


class Tool:
	""" A tool used in the compilation process. """

	binary = None
	paths = []
	flags = []

	hashstore = None


	def __init__(self, short_description, binary):
		self.short_description = short_description
		self.binary = binary

	def run(self, inputs, outputs, extra_paths = [], extra_flags = []):
		self.binhash = self.hashstore.hash_file(self.binary)
		paths = self.paths + extra_paths
		flags = self.flags + extra_flags

		self.execute(inputs, outputs, paths, flags)

	def execute(self, inputs, outputs, paths, flags):
		raise Exception, "The '%s' tool has not overridden Tool.execute()" % (
				self.short_description
			)

	def print_action(self, inputs, outputs, output_stream = sys.stdout):
		output_stream.write("%12s %s => %s\n" % (
					self.short_description + ':',
					inputs,
					outputs,
				)
			)

	def __repr__(self):
		return "Tool '%s' { flags: %s, paths: %s }" % (
				self.short_description,
				self.flags,
				self.paths,
			)

