test:
	find tcslackbot -name "*.py" | xargs flake8

clean:
	@rm -rf build
	@rm -rf dist
	@rm -rf VENV
	@rm -rf tcslackbot.egg-info
