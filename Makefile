.PHONY: help install test lint format clean docs \
        collector-init collector-status collector-watch collector-run collector-resume \
        collector-retry collector-clear collector-update \
        cdk-init cdk-synth cdk-deploy cdk-destroy cdk-diff cdk-bootstrap cdk-set-token

# Python command (use python3 on macOS)
PYTHON := python3

# Colors for terminal output
CYAN := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
MAGENTA := \033[35m
RESET := \033[0m
BOLD := \033[1m

help:
	@echo ""
	@echo "$(BOLD)$(CYAN)📚 Categories of the Commons - Development Commands$(RESET)"
	@echo ""
	@echo "$(BOLD)$(GREEN)Setup:$(RESET)"
	@echo "  $(CYAN)make install$(RESET)        Install dependencies and setup environment"
	@echo "  $(CYAN)make install-dev$(RESET)    Install with development dependencies"
	@echo ""
	@echo "$(BOLD)$(GREEN)Development:$(RESET)"
	@echo "  $(CYAN)make test$(RESET)           Run tests with pytest"
	@echo "  $(CYAN)make lint$(RESET)           Run linting (flake8, mypy)"
	@echo "  $(CYAN)make format$(RESET)         Format code with black"
	@echo "  $(CYAN)make check$(RESET)          Run all checks (lint + test)"
	@echo ""
	@echo "$(BOLD)$(GREEN)🤖 Local Collection (Phase 1):$(RESET)"
	@echo "  $(CYAN)make collector-init CATEGORY=stadium$(RESET)    Initialize queue for category"
	@echo "  $(CYAN)make collector-status$(RESET)                   Show collection status"
	@echo "  $(CYAN)make collector-watch$(RESET)                    Live status dashboard (updates every 5s)"
	@echo "  $(CYAN)make collector-run LIMIT=10$(RESET)             Collect N projects (stops at rate limit)"
	@echo "  $(CYAN)make collector-run-wait LIMIT=10$(RESET)        Collect N, wait for rate limit reset"
	@echo "  $(CYAN)make collector-resume$(RESET)                   Resume collection from last state"
	@echo "  $(CYAN)make collector-retry$(RESET)                    Retry failed projects"
	@echo "  $(CYAN)make collector-update$(RESET)                   Update existing data with delta"
	@echo "  $(CYAN)make collector-update CATEGORY=federation$(RESET) Update specific category"
	@echo "  $(CYAN)make collector-clear$(RESET)                    Clear collection state"
	@echo ""
	@echo "$(BOLD)$(GREEN)☁️  AWS Deployment (Phase 2 - CDK):$(RESET)"
	@echo "  $(CYAN)make cdk-bootstrap$(RESET)  Bootstrap CDK in your AWS account (first time)"
	@echo "  $(CYAN)make cdk-synth$(RESET)      Synthesize CloudFormation template"
	@echo "  $(CYAN)make cdk-diff$(RESET)       Show changes vs deployed stack"
	@echo "  $(CYAN)make cdk-deploy$(RESET)     Deploy to AWS"
	@echo "  $(CYAN)make cdk-destroy$(RESET)    Destroy AWS resources"
	@echo "  $(CYAN)make cdk-set-token$(RESET)  Store GitHub token in SSM Parameter"
	@echo ""
	@echo "$(BOLD)$(GREEN)📊 Data:$(RESET)"
	@echo "  $(CYAN)make collect$(RESET)        Run single project collection"
	@echo "  $(CYAN)make analyze$(RESET)        Run analysis pipeline"
	@echo ""
	@echo "$(BOLD)$(GREEN)📖 Documentation:$(RESET)"
	@echo "  $(CYAN)make docs$(RESET)           Build documentation"
	@echo "  $(CYAN)make notebooks$(RESET)      Start Jupyter Lab"
	@echo ""
	@echo "$(BOLD)$(GREEN)🧹 Cleanup:$(RESET)"
	@echo "  $(CYAN)make clean$(RESET)          Remove temporary files and caches"
	@echo ""

install:
	@echo "$(CYAN)📦 Installing dependencies...$(RESET)"
	pip install -r requirements.txt
	pip install -e .
	@echo "$(GREEN)✅ Installation complete!$(RESET)"

install-dev:
	@echo "$(CYAN)📦 Installing development dependencies...$(RESET)"
	pip install -r requirements.txt
	pip install -e ".[dev,docs,notebooks]"
	@echo "$(GREEN)✅ Development installation complete!$(RESET)"

test:
	@echo "$(CYAN)🧪 Running tests...$(RESET)"
	pytest -v --cov=src tests/

lint:
	@echo "$(CYAN)🔍 Running linters...$(RESET)"
	flake8 src/ tests/
	mypy src/

format:
	@echo "$(CYAN)✨ Formatting code...$(RESET)"
	black src/ tests/
	isort src/ tests/
	@echo "$(GREEN)✅ Code formatted!$(RESET)"

check: lint test

collect:
	@echo "$(CYAN)📥 Running data collection...$(RESET)"
	$(PYTHON) src/collection/github_collector.py

analyze:
	@echo "$(CYAN)📊 Running analysis pipeline...$(RESET)"
	$(PYTHON) src/analysis/entropy_calculation.py

docs:
	@echo "$(CYAN)📖 Building documentation...$(RESET)"
	cd docs && sphinx-build -b html . _build/

notebooks:
	@echo "$(CYAN)🚀 Starting Jupyter Lab...$(RESET)"
	jupyter lab

clean:
	@echo "$(YELLOW)🧹 Cleaning up...$(RESET)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.log" -delete 2>/dev/null || true
	rm -rf build/ dist/ htmlcov/ .coverage 2>/dev/null || true
	@echo "$(GREEN)✅ Cleaned up temporary files$(RESET)"

# =============================================================================
# Local Collection Commands (Phase 1)
# =============================================================================

CATEGORY ?= stadium
LIMIT ?= 10

collector-init:
	@echo "$(CYAN)🚀 Initializing collection queue for category: $(BOLD)$(CATEGORY)$(RESET)"
	$(PYTHON) -m src.collection.collector_daemon init --category $(CATEGORY)

collector-status:
	@echo "$(CYAN)📊 Collection Status$(RESET)"
	$(PYTHON) -m src.collection.collector_daemon status

# Watch interval in seconds (default 5)
WATCH_INTERVAL ?= 5

collector-watch:
	@echo "$(CYAN)👀 Live Status Dashboard (Ctrl+C to exit)$(RESET)"
	@while true; do \
		clear; \
		echo "$(BOLD)$(CYAN)📊 Collection Status Dashboard$(RESET)  $(YELLOW)[Updates every $(WATCH_INTERVAL)s - Ctrl+C to exit]$(RESET)"; \
		echo ""; \
		$(PYTHON) -m src.collection.collector_daemon status 2>/dev/null || echo "$(RED)No collection in progress$(RESET)"; \
		sleep $(WATCH_INTERVAL); \
	done

collector-run:
	@echo "$(CYAN)📥 Collecting up to $(BOLD)$(LIMIT)$(RESET)$(CYAN) projects...$(RESET)"
	$(PYTHON) -m src.collection.collector_daemon collect --limit $(LIMIT)

collector-run-wait:
	@echo "$(CYAN)📥 Collecting up to $(BOLD)$(LIMIT)$(RESET)$(CYAN) projects (will wait for rate limit)...$(RESET)"
	$(PYTHON) -m src.collection.collector_daemon collect --limit $(LIMIT) --wait

collector-resume:
	@echo "$(CYAN)▶️  Resuming collection...$(RESET)"
	$(PYTHON) -m src.collection.collector_daemon resume

collector-retry:
	@echo "$(YELLOW)🔄 Retrying failed projects...$(RESET)"
	$(PYTHON) -m src.collection.collector_daemon retry

collector-clear:
	@echo "$(RED)🗑️  Clearing collection state...$(RESET)"
	$(PYTHON) -m src.collection.collector_daemon clear --force

collector-update:
	@echo "$(MAGENTA)🔄 Updating existing data with delta...$(RESET)"
ifdef CATEGORY
	$(PYTHON) -m src.collection.collector_daemon update --category $(CATEGORY) $(if $(DAYS),--days $(DAYS)) $(if $(LIMIT),--limit $(LIMIT))
else ifdef DAYS
	$(PYTHON) -m src.collection.collector_daemon update --days $(DAYS) $(if $(LIMIT),--limit $(LIMIT))
else
	$(PYTHON) -m src.collection.collector_daemon update $(if $(LIMIT),--limit $(LIMIT))
endif

# =============================================================================
# AWS CDK Commands (Phase 2)
# =============================================================================

CDK_DIR = infra

cdk-bootstrap:
	@echo "$(CYAN)☁️  Bootstrapping CDK in your AWS account...$(RESET)"
	cd $(CDK_DIR) && npx cdk bootstrap

cdk-synth:
	@echo "$(CYAN)📝 Synthesizing CloudFormation template...$(RESET)"
	cd $(CDK_DIR) && npx cdk synth

cdk-diff:
	@echo "$(CYAN)🔍 Showing infrastructure changes...$(RESET)"
	cd $(CDK_DIR) && npx cdk diff

cdk-deploy:
	@echo "$(GREEN)🚀 Deploying to AWS...$(RESET)"
	cd $(CDK_DIR) && npx cdk deploy --require-approval never
	@echo "$(GREEN)✅ Deployment complete!$(RESET)"

cdk-destroy:
	@echo "$(RED)⚠️  This will destroy all AWS resources!$(RESET)"
	@read -p "Are you sure? [y/N] " confirm && \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		cd $(CDK_DIR) && npx cdk destroy --force; \
		echo "$(GREEN)✅ Resources destroyed$(RESET)"; \
	else \
		echo "$(YELLOW)Cancelled.$(RESET)"; \
	fi

cdk-set-token:
	@if [ -z "$(GITHUB_TOKEN)" ]; then \
		echo "$(RED)❌ Error: GITHUB_TOKEN environment variable not set$(RESET)"; \
		echo "$(YELLOW)Usage: GITHUB_TOKEN=ghp_xxx make cdk-set-token$(RESET)"; \
		exit 1; \
	fi
	@echo "$(CYAN)🔐 Storing GitHub token in SSM Parameter Store...$(RESET)"
	aws ssm put-parameter \
		--name "/github-collector/token" \
		--value "$(GITHUB_TOKEN)" \
		--type SecureString \
		--overwrite
	@echo "$(GREEN)✅ GitHub token stored in SSM Parameter Store$(RESET)"
