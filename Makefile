all: foo

.PHONY: clean

CC=./dbuild --tool=compiler --bin=/usr/bin/clang
JUST_CFLAGS=-c -Wall -Werror
INCPATHS=/usr/local/include,/some/custom/include
CFLAGS=--flags="${JUST_CFLAGS}" --paths=${INCPATHS}

LD=./dbuild --tool=linker --bin=/usr/bin/clang
LIBS=m,bz2
LDPATHS=/usr/local/lib,/some/custom/libdir
LDFLAGS=--flags="${JUST_LDFLAGS}" --paths=${LDPATHS} --libs=${LIBS}

clean:
	rm -f foo *.pyc *.o

foo: foo.o bar.o
	${LD} ${LDFLAGS} --inputs=foo.o,bar.o --output=foo

foo.o: foo.c
	${CC} ${CFLAGS} --inputs=foo.c --output=foo.o

bar.o: bar.c
	${CC} ${CFLAGS} --inputs=bar.c --output=bar.o

