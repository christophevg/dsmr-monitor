all: serve

serve:
	gunicorn -k eventlet -w 1 --bind 0.0.0.0:8000 monitor.web:app

.python-version:
	@pyenv virtualenv 3.7.7 $$(basename ${CURDIR}) > /dev/null 2>&1 || true
	@pyenv local $$(basename ${CURDIR})
	@pyenv version

SERVICE=dsmr-monitor

pi-install:
	@sudo cp ${SERVICE}.service /lib/systemd/system/
	@sudo systemctl enable ${SERVICE}
	@sudo systemctl restart ${SERVICE}

pi-start:
	@sudo systemctl start ${SERVICE}.service

pi-restart:
	@sudo systemctl restart ${SERVICE}.service

pi-status:
	@sudo systemctl status ${SERVICE}.service

pi-stop:
	@sudo systemctl stop ${SERVICE}.service

