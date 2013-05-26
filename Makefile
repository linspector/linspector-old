all:

clean:
	rm -rf log
	find . -type f -name "*.pyc" -exec rm -f {} \;

docs:
	epydoc --html -o docs ./lib
	
docs-pdf:
	epydoc --pdf -o docs ./lib

docs-clean:
	rm -rf docs
