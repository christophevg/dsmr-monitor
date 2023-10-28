all: serve

serve:
	gunicorn -k eventlet -w 1 --bind 0.0.0.0:8000 monitor.web:app

.python-version:
	@pyenv virtualenv $$(basename ${CURDIR}) > /dev/null 2>&1 || true
	@pyenv local $$(basename ${CURDIR})
	@pyenv version

upgrade:
	@pip list --outdated | tail +3 | cut -d " " -f 1 | xargs -n1 pip install -U

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

