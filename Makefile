.PHONY: nothing

nothing:
	@echo ""

run:
	python3 main.py

install:
	virtualenv -p python3 ./venv
	source ./venv/bin/activate && pip3 install -r requirements.txt
