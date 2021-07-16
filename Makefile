install:
	@pip3 install --no-cache-dir -r requirements.txt

test: install
	@python3 -m unittest -v

clean:
	@rm -rf __pycache__

lint:
	@pip3 install --no-cache-dir -r requirements_lint.txt
	@black --check --diff . 2>&1

.PHONY: install test clean lint