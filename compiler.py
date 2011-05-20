import os
import subprocess

subprocess.devnull = open(os.devnull, 'w')

from tool import Tool


class Compiler(Tool):
	""" A tool that converts source files into object files. """

	def __init__(self, binary):
		Tool.__init__(self, 'Compile', binary)

	def execute(self, inputs, outputs, paths, flags):
		if len(outputs) != 1:
			raise Exception, 'Compiler generates one file at a time, not %d' % (
					len(outputs)
				)

		print "Binary:   ", self.binhash, "(but what about deps?)"
		print "Flags:    ", self.hashstore.hash_string(' '.join(flags))
		print "Paths:    ", [ self.hashstore.hash_string(p) for p in paths ]

		print 'Input files:'
		for i in inputs:
			print '%33s: %s' % (i, self.hashstore.hash_file(i))

			includes = self.parse_includes(i)
			if len(includes) > 0:
				for j in includes:
					print "%33s: %s" % (j, self.hashstore.hash_file(j))
				print

		include_dirs = [ '-I %s' % p for p in paths ]
		argv = [ 'clang' ] + flags + include_dirs + [ '-o' ] + outputs + inputs

		print "Executing: '%s'" % (' '.join(argv))
		output = subprocess.check_call(argv)


	def parse_includes(self, filename):
		assert type(filename) == str
		includes = []

		# Let's see if this is a C[++] file which #includes header files.
		depfilename = filename + '.clangdep'

		try:
			# Ask Clang to process include files.
			output = subprocess.check_call(
					[ 'clang', '-MD', '-MF', depfilename, '-E', filename, ],
					stdout = subprocess.devnull,
					stderr = subprocess.STDOUT,
				)

			# Were there any headers?
			for line in open(depfilename).readlines():
				tokens = [
					t.replace('\n', '')
						for t in line.split(' ')
						if len(t.strip()) > 0 and t != '\\\n'
				]

				# Ignore the beginning of the first line ('target.o: target.c').
				if len(includes) == 0: tokens = tokens[2:]

				# Everything else is an #include header file.
				includes += tokens
		
		except subprocess.CalledProcessError, e:
			# The file does not have any #includes (it may be e.g. an object file).
			raise e
			pass

		finally:
			# Clean up temporary file.
			try: os.remove(depfilename)
			except OSError, e: pass # It's ok if the file wasn't generated.

		return includes

