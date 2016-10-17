.PHONY : run_all_tests
run__all_tests:
	python3 -m pytest --doctest-modules -v ./

.PHONY : run_all_tests
run_tests:
	python3 -m pytest  -v ./
