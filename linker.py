import os
import subprocess

from tool import Tool


class Linker(Tool):
	""" A tool that links object files together into libraries or binaries. """

	def __init__(self, binary):
		Tool.__init__(self, 'Link', binary)
		print binary


	def execute(self, inputs, outputs, paths, flags):
		print "Binary:   ", self.binhash, "(but what about deps?)"
		print "Flags:    ", self.hashstore.hash_string(' '.join(flags))
		print "Paths:    ", [ self.hashstore.hash_string(p) for p in paths ]

		if len(outputs) != 1:
			raise Exception, 'Linker generates one file at a time, not %d' % (
					len(outputs)
				)

		print 'Dependencies:'
		libdeps = self.parse_libs(inputs)
		for j in libdeps:
			print "%33s: %s" % (j, self.hashstore.hash_file(j))
		print

		libdirs = [ '-I %s' % p for p in paths ]
		argv = [ 'clang' ] + flags + libdirs + [ '-o' ] + outputs + inputs

		print "Executing: '%s'" % (' '.join(argv))
		return_code = subprocess.check_call(
				argv,
				stdout = subprocess.devnull,
				stderr = subprocess.devnull,
			)


	def parse_libs(self, files):
		assert type(files) == list

		try:
			# Ask clang to trace library dependencies.
			output = subprocess.check_output(
					[ 'clang', '-dynamiclib', '-t' ] + files,
					stderr = subprocess.devnull,
				)

			libs = output.split('\n')
			return [ l.strip() for l in libs if len(l) > 0 ]


		except subprocess.CalledProcessError, e:
			print 'Error:', e
			pass   # No library dependencies

		return libs

