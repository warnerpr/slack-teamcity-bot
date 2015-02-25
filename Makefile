BIN := "VENV/bin"

env:
	@virtualenv VENV
	@$(BIN)/pip install -r requirements.txt

test:
	@find tcslackbot -name "*.py" | xargs $(BIN)/flake8
	@$(BIN)/nosetests tcslackbot

clean:
	@rm -rf build
	@rm -rf dist
	@rm -rf VENV
	@rm -rf tcslackbot.egg-info
