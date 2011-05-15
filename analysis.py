import os
import subprocess

def parse_includes(input):
	includes = []

	if type(input) == type(list()):
		for filename in input: includes += parse_includes(filename)
		return includes

	assert type(input) == type('')


	# Let's see if this is a C[++] file which #includes header files.
	depfilename = input + '.clangdep'

	try:
		# Ask Clang to process include files.
		output = subprocess.check_output(
			[ 'clang', '-MD', '-MF', depfilename, '-c', input ],
			stderr = subprocess.STDOUT)

		# Were there any headers?
		if len(output) > 0: raise subprocess.CalledProcessError(0, 'No #includes')
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
		pass

	finally:
		# Clean up temporary file.
		try: os.remove(depfilename)
		except OSError, e: pass # It's ok if the file wasn't generated.

	return includes

