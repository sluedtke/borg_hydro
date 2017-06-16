test_with_doctest:
	python3 -m pytest --doctest-modules --ignore=setup.py -v ./borg_hydro/
	python2 -m pytest --doctest-modules --ignore=setup.py -v ./borg_hydro/

test_no_doctest:
	python3 -m pytest  -v --ignore=setup.py ./borg_hydro/
	python2 -m pytest  -v --ignore=setup.py ./borg_hydro/

clean:
	find . -type d -name '__pycache__' | xargs rm -r
	find . -type d -name '.cache' | xargs rm -r

.PHONY : test_no_doctest test_with_doctest clean
