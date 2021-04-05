all: run

run:
	gunicorn -k eventlet -w 1 monitor.web:app

.python-version:
	@pyenv virtualenv 3.7.7 $$(basename ${CURDIR}) > /dev/null 2>&1 || true
	@pyenv local $$(basename ${CURDIR})
	@pyenv version
