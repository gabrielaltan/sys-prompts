```
███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗        
██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║        
███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║        
╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║        
███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║        
╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝        
██████╗ ██████╗  ██████╗ ███╗   ███╗██████╗ ████████╗███████╗
██╔══██╗██╔══██╗██╔═══██╗████╗ ████║██╔══██╗╚══██╔══╝██╔════╝
██████╔╝██████╔╝██║   ██║██╔████╔██║██████╔╝   ██║   ███████╗
██╔═══╝ ██╔══██╗██║   ██║██║╚██╔╝██║██╔═══╝    ██║   ╚════██║
██║     ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║        ██║   ███████║
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝        ╚═╝   ╚══════╝
```
# Render

This repository renders modular system prompts using reusable instruction blocks plus RAG files for Agents.

## 📂 Structure

- `prompts/blocks/`: Reusable instructions (e.g., tone, roles, formats). In YAML files.
- `prompts/templates/`: Templates using `${block-id}` placeholders
- `prompts/rendered/`: Auto-generated, final prompt outputs
- `render.py`: Script to generate `rendered/` prompts

## ▶️ Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
# or
make install
```

### Render Templates
```bash
# Single render
python render.py
# or
make render
# or
./render.sh
```

## 🚀 Practical Usage Methods

### 1. Watch Mode (Recommended for Development)
Automatically re-renders when you change blocks or templates:
```bash
python render.py --watch
# or
make watch
# or
./render.sh watch
```

### 2. VS Code Integration
Use the built-in tasks (Ctrl+Shift+P → "Tasks: Run Task"):
- **Render Templates**: Single render
- **Watch Templates**: Auto-render on changes
- **Clean Rendered**: Remove all rendered files

### 3. Shell Script
Quick commands with the `render.sh` script:
```bash
./render.sh          # Render once
./render.sh watch    # Watch mode
./render.sh dev      # Watch with verbose logging
./render.sh clean    # Clean rendered files
./render.sh help     # Show all options
```

### 4. Make Commands
```bash
make render    # Render once
make watch     # Watch mode
make dev       # Watch with verbose logging
make clean     # Clean rendered files
make help      # Show all options
```

## 🧩 Format 

### Blocks
```yaml
block-tag-one: |
    This is a reusable block of text
    that can be referenced in templates.

block-tag-two: |
    Another block with different content.
```

### Block Reference in Templates
```md
# My Template

${block-tag-one}

Some additional content here.

${block-tag-two}
```

## 🔧 Advanced Usage

### Command Line Options
```bash
python render.py --help
python render.py --watch --verbose
```

### Programmatic Usage
```python
from render import TemplateRenderer

renderer = TemplateRenderer()
renderer.render_all()  # Render all templates
```

## 📝 Development Workflow

1. **Start watch mode**: `./render.sh watch`
2. **Edit blocks** in `prompts/blocks/*.yaml`
3. **Edit templates** in `prompts/templates/*.md`
4. **View results** in `prompts/rendered/*.md`
5. **Templates auto-update** as you save changes

## 🎯 Tips

- Use watch mode during development for instant feedback
- Keep blocks focused and reusable
- Use descriptive block names for better organization
- The renderer caches blocks for better performance
- All rendered files are automatically created in `prompts/rendered/`
