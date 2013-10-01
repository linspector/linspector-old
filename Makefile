all:

clean:
	rm -rf log
	find . -type f -name "*.pyc" -exec rm -f {} \;

docs:
	epydoc -n "Linspector - API Documentation" --html -o docs .
	
docs-pdf:
	epydoc -n "Linspector - API Documentation" --pdf -o docs .

docs-clean:
	rm -rf docs
