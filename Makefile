.PHONY: install test clean lint run

PACKAGE ?= src
VENV := .venv
VENV_BIN := $(VENV)/bin

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
	@echo "$(GREEN)Clean complete.$(NC)"

run:
	@echo "$(BLUE)Running command: $(CMD) $(ARGS)$(NC)"
	@$(VENV_BIN)/python -m src/ai_cli.main.py $(CMD) $(ARGS)