.PHONY: render watch install clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  make render    - Render templates once"
	@echo "  make watch     - Watch for changes and auto-render"
	@echo "  make install   - Install dependencies"
	@echo "  make clean     - Remove rendered files"
	@echo "  make help      - Show this help"

# Install dependencies
install:
	pip install -r requirements.txt

# Render templates once
render:
	python render.py

# Watch for changes and auto-render
watch:
	python render.py --watch

# Clean rendered files
clean:
	rm -rf prompts/rendered/*.md

# Development mode (watch with verbose logging)
dev:
	python render.py --watch --verbose 