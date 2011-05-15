all: foo

.PHONY: clean

clean:
	rm -f foo *.o

foo: foo.o bar.o
	@./dclang --tool='/usr/bin/clang' --inputs=foo.o,bar.o --output=foo --flags='-fno-builtin'

foo.o: foo.c
	@./dclang --tool='/usr/bin/clang' --inputs=foo.c --output=foo.o --flags='-c -Wall -Werror'

bar.o: bar.c
	@./dclang --tool='/usr/bin/clang' --inputs=bar.c --output=bar.o --flags='-c -Wall -Werror'
