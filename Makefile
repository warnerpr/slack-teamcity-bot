env:
	@virtualenv VENV
	@VENV/bin/pip install -r requirements.txt

test:
	@find tcslackbot -name "*.py" | xargs VENV/bin/flake8

clean:
	@rm -rf build
	@rm -rf dist
	@rm -rf VENV
	@rm -rf tcslackbot.egg-info
