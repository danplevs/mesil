# GLOBALS                                                                       

PROJECT_NAME = mesil
POETRY = poetry run

# COMMANDS                                                                      
.PHONY: install 
install: ## Install and activate poetry env
	poetry install


.PHONY: data
data: install ## Make dataset
	$(POETRY) python $(PROJECT_NAME)/data/make_dataset.py data/raw data/processed


.PHONY: lint_blue isort prospector
lint_blue: # Lint using blue (format)
	$(POETRY) blue --check $(PROJECT_NAME)

lint_isort: # Lint using isort (sort imports)
	$(POETRY) isort --check $(PROJECT_NAME)

prospector: # Lint using prospector (static analysis)
	$(POETRY) prospector $(PROJECT_NAME)

analyze: lint_blue lint_isort prospector ## Code analysis with blue, isort and prospector


.PHONY: blue isort format
blue: # Format using blue
	$(POETRY) blue $(PROJECT_NAME)

isort: # Sort imports
	$(POETRY) isort $(PROJECT_NAME)

format: blue isort ## Format using blue and isort


.PHONY: help
help:
	@egrep -h "\s##\s" $(MAKEFILE_LIST) | sort | awk -f script.awk
