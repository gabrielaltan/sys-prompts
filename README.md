# System Prompt Renderer

This repository renders modular system prompts using reusable instruction blocks.

## 📂 Structure

- `blocks/`: Reusable instructions (e.g., tone, roles, formats)
- `templates/`: Templates using `${block-id}` placeholders
- `rendered/`: Auto-generated, final prompt outputs
- `render.py`: Script to generate `rendered/` prompts

## ▶️ How to Use

1. Edit or add your instruction blocks in `blocks/`
2. Create templates in `templates/` using `${block-name}` syntax
3. Run:
```bash
python render.py
```
4. The rendered prompts will appear in `rendered/`

## 🧩 Format 

### Blocks
```md
<!block-tag>
...
<!/block-tag>
```

### Block Reference in Templates
```md
${block-tag}
```