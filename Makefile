all: test
	
test:
	mkdir tests
	cd tests
	pytest --cov-report html --cov=../src test.py && open ./htmlcov/index.html
	rmdir project-configuration
	mv .coverage, ./htmlcov tests


clear:
	rmdir tests
	rmdir htmlcov
	rmdir .coverage
	rmdir debug.log
	rmdir project-configuration

