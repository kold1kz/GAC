all: 
	
test: clear htmlcov
	rm -rf ./tests/*
	pytest -v --cov-report html --cov=. ./src/test.py
	mv ./.coverage tests
	mv htmlcov tests
	

htmlcov:
	open ./tests/htmlcov/index.html

clear:
	rm -rf project-configuration
	rm -rf ./.coverage
	rm -rf htmlcov

clear_debug:
	rm -rf debug.log

clear_test:
	rm -rf ./tests/*
	rm -rf ./tests/.coverage

compile_windows: run
	./venv/Scripts/activate
	python3 ./src/with_async.py -o gac.exe

compile_linux: run
	source ./venv/bin/activate
	python3 ./src/with_async.py -o ./src/gac.exe

run:
	./src/gac.exe
