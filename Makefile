format:
	@echo "--[isort]------------------------------------------------------------------"
	isort  --settings-file=pyproject.toml .
	@echo "--[black]------------------------------------------------------------------"
	black  --config=pyproject.toml        .

lint:
	@echo "--[isort]------------------------------------------------------------------"
	isort  --settings-file=pyproject.toml --check-only    .
	@echo "--[black]------------------------------------------------------------------"
	black  --config=pyproject.toml        --check         .
	@echo "--[flake8]-----------------------------------------------------------------"
	flake8 --config=.flake8                               .
	@echo "--[mypy]-------------------------------------------------------------------"
	mypy --explicit-package-bases --config-file=.mypy.ini .

test:
	pytest tests

.PHONY: lint format
