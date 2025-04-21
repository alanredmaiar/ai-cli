.PHONY: install test clean lint run build bump

PACKAGE ?= src
VENV := .venv
VENV_BIN := $(VENV)/bin
BUILD_DIR := dist

# Definición de colores
GREEN := \033[0;32m
RED := \033[0;31m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m  # No Color

BUILD_PRINT = $(BLUE)Building $<$(NC)

COMPILE_cpp = $(CXX) $(CFLAGS) -o $@ -c $< $(MAKEDEP) $(INCLUDES)
COMPILE_cpp_OUT=$$($(COMPILE_cpp) 2>&1 | sed 's/error/$(RED)error$(NC)/g' 's/warning/$(YELLOW)warning$(NC)/g' 's/^/$(BLUE)/' 's/$$/$(NC)/')

%.o : %.cpp
	@echo "$(BUILD_PRINT)\n$(COMPILE_cpp)\n$(COMPILE_cpp_OUT)"
.SUFFIXES: .o .cpp


install:
	@echo "$(BLUE)Installing dependencies...$(NC)"
	@uv sync
	@uv pip uninstall ai-cli && uv pip install -e .

bump:
	@echo "$(BLUE)Bumping version...$(NC)"
	@if [ -n "$(filter --downgrade,$(MAKECMDGOALS))" ]; then \
		DOWNGRADE="--downgrade"; \
	fi; \
	RULE="version"; \
	for arg in $(MAKECMDGOALS); do \
		if [ "$$arg" != "bump" ] && [ "$$arg" != "--downgrade" ]; then \
			RULE="version $$arg"; \
			break; \
		fi; \
	done; \
	uv run scripts/transformers/version_bumper.py $$RULE $$DOWNGRADE
	@for arg in $(MAKECMDGOALS); do \
		if [ "$$arg" != "bump" ]; then \
			$(MAKE) --no-print-directory -f $(firstword $(MAKEFILE_LIST)) dummy DUMMY="$$arg" > /dev/null 2>&1 || true; \
		fi; \
	done

build:
	@echo "$(BLUE)Building application into $(BUILD_DIR) directory...$(NC)"
	@uv build

test:
	@echo "$(BLUE)Running tests...$(NC)"
	@$(VENV_BIN)/pytest -xvs test/unit/

lint:
	@echo "$(BLUE)Running linters...$(NC)"
	@echo "$(GREEN)Running Ruff on $(PACKAGE)$(NC)"
	@$(VENV_BIN)/ruff check $(PACKAGE) --fix --show-fixes
	@$(VENV_BIN)/ruff format $(PACKAGE)
	@echo "$(GREEN)Running Pyright on $(PACKAGE)$(NC)"
	@$(VENV_BIN)/pyright $(PACKAGE) || true
	@echo "$(GREEN)Done.$(NC)"

clean:
	@echo "$(BLUE)Cleaning project...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.pyd" -delete
	@find . -type f -name ".coverage" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@find . -type d -name "*.egg" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".coverage" -exec rm -rf {} +
	@find . -type d -name "htmlcov" -exec rm -rf {} +
	@find . -type f -name "*-filtered.log" -delete
	@rm -rf $(BUILD_DIR)
	@echo "$(GREEN)Clean complete.$(NC)"

run:
	@echo "$(BLUE)Running command: $(CMD) $(ARGS)$(NC)"
	@$(VENV_BIN)/python -m src/ai_cli.main.py $(CMD) $(ARGS)