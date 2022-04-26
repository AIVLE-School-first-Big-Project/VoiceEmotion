python:
	isort . && oitnb --exclude=migrations . && flake8 --ignore=E501 --exclude=migrations

html:
	prettier --bracket-same-line --write --print-width 240 .

initsub:
	git submodule init &&	git submodule update

updatesub:
	git submodule foreach git pull origin master
