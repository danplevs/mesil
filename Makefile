# GLOBALS                                                                       

PROJECT_NAME = mesil
PYTHON_INTERPRETER = python3
CONDA_EXE = C:/Users/daniel/miniconda3/Scripts/conda.exe
SOURCE_CODE = src

# COMMANDS                                                                      

## @ environment
.PHONY: lock create_env update_env delete_env
lock: environment.yml ## create lockfile from environment.yml
	conda-lock -f environment.yml

create_env: lock environment.yml ## create conda environment
	conda-lock install -n $(PROJECT_NAME)

update_env: environment.yml ## update packages in conda environment
	$(CONDA_EXE) update -f environment.yml

delete_env: ## delete conda environment
	$(CONDA_EXE) env remove -n $(PROJECT_NAME)


## @ data
.PHONY: data
data: create_env ## make dataset
	$(PYTHON_INTERPRETER) src/data/make_dataset.py data/raw data/processed

## @ files
.PHONY: clean
clean: ## delete all compiled Python files
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


## @ analysis
.PHONY: blue isort prospector
blue: ## lint using blue
	blue $(SOURCE_CODE)

isort: ## sort imports
	isort $(SOURCE_CODE)

prospector: # statically analyze source code
	prospector $(SOURCE_CODE)

analyze: blue isort prospector


# PROJECT RULES                                                                 

# Self Documenting Commands                                                     

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
