import compiler, linker
import hashstore


store = hashstore.HashStore()

tools = {
	'compiler': compiler.Compiler,
	'linker': linker.Linker,
}

def create(name, binary, paths = [], flags = [], libs = []):
	if not tools.has_key(name):
		raise Exception, "Unknown tool '%s'" % name

	tool = tools[name](binary)
	tool.flags = flags
	tool.hashstore = store
	tool.libs = libs
	tool.paths = paths

	return tool

