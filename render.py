from pathlib import Path
import re
import logging
from typing import Dict
import yaml

# Directories
BASE_DIR = Path("prompts")
BLOCKS_DIR = BASE_DIR / "blocks"
TEMPLATES_DIR = BASE_DIR / "templates"
RENDERED_DIR = BASE_DIR / "rendered"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def main() -> None:
    """Entry point: load blocks and render templates."""
    blocks = loads_blocks()
    render_templates(blocks)


def loads_blocks() -> Dict[str, str]:
    """
    Load all block definitions from YAML files in the blocks directory.
    Returns:
        dict: Mapping of block names to their content.
    Raises:
        ValueError: If a block file is invalid YAML or not a dict of strings.
    """
    blocks = {}
    for file_path in BLOCKS_DIR.glob("*.yaml"):
        try:
            # Use yaml.load with SafeLoader to handle aliases properly
            content = yaml.load(file_path.read_text(), Loader=yaml.SafeLoader)
        except Exception as e:
            raise ValueError(
                f"Block file {file_path.name} could not be parsed as YAML: {e}"
            )
        if not isinstance(content, dict):
            raise ValueError(
                f"Block file {file_path.name} does not contain a dictionary at the top level."
            )
        for k, v in content.items():
            if not isinstance(k, str):
                raise ValueError(
                    f"Block file {file_path.name} contains non-string key: {k}"
                )
            if isinstance(v, str):
                blocks[k] = v
            elif isinstance(v, list):
                blocks[k] = "\n\n".join(str(item) for item in v)
            else:
                raise ValueError(
                    f"Block file {file_path.name} contains unsupported value type for key {k}: {type(v)}"
                )
    return blocks


def render_templates(blocks: Dict[str, str]) -> None:
    """
    Render all templates using the provided blocks.
    Args:
        blocks: Mapping of block names to their content.
    """
    for file_path in TEMPLATES_DIR.glob("*.md"):
        content = file_path.read_text()
        rendered = render(file_path.name, content, blocks)
        save_rendered_file(file_path.name, rendered)


def render(filename: str, content: str, blocks: Dict[str, str]) -> str:
    """
    Render a template by replacing block placeholders with their content.
    Args:
        content: The template content.
        blocks: Mapping of block names to their content.
    Returns:
        The rendered template as a string.
    Raises:
        ValueError: If a block is referenced but not found.
    """

    def replace_block(match):
        key = match.group(1)
        rendered = blocks.get(key, "")
        if not rendered:
            raise ValueError(f"Block {key} not found in blocks for {filename}.")
        return rendered

    return re.sub(r"\$\{([a-zA-Z0-9_-]+)\}", replace_block, content)


def save_rendered_file(filename: str, content: str) -> None:
    """
    Save a rendered file to the rendered directory.
    Args:
        filename: Name of the file to save.
        content: Content to write.
    """
    RENDERED_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RENDERED_DIR / filename
    output_path.write_text(content)
    logging.info(f"Rendered file {filename} saved.")


if __name__ == "__main__":
    main()
