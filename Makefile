SRCDIR = ./src
MAINFILE = ${SRCDIR}/main.py

all: build_default

deps:
	pip install -r deps.list

check: 
	mypy --strict ${SRCDIR}

run:
	python ${MAINFILE}

clean: 
	rm -rf ./build/

