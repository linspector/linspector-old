all:

clean:
	rm -rf log
	find . -type f -name "*.pyc" -exec rm -f {} \;

docs:
	epydoc --html -o docs .
	
docs-pdf:
	epydoc --pdf -o docs .

docs-clean:
	rm -rf docs
